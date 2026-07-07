"""
JCL Parser
Parses IBM JCL (Job Control Language) files to extract:
  - Job definitions (JOB cards)
  - Job steps (EXEC cards) — which program each step runs
  - Dataset definitions (DD cards) — input/output files per step
  - Step comments — plain-text description blocks above each step
  - SORT/IDCAMS utility steps
  - Inline SYSIN data

No migration mapping — purely structural parsing of what exists.
"""

import re
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field, asdict

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console(force_terminal=True, highlight=False, legacy_windows=False)


# ─────────────────────────────────────────────
# Data Classes
# ─────────────────────────────────────────────

@dataclass
class JclDataset:
    """One DD (Data Definition) — a file/dataset used by a step."""
    dd_name: str                      # SYSOUT, STEPLIB, CUSTOUT, etc.
    dsn: str = ""                     # Dataset name
    disp: str = ""                    # SHR, NEW, MOD, OLD
    disposition_normal: str = ""      # CATLG, DELETE, KEEP, PASS
    disposition_abnormal: str = ""
    direction: str = "UNKNOWN"        # INPUT | OUTPUT | SYSTEM | INLINE
    recfm: str = ""
    lrecl: str = ""
    unit: str = ""
    space: str = ""
    is_inline: bool = False           # DD * — data in stream


@dataclass
class JclStep:
    """One EXEC step in a JCL job."""
    step_name: str
    program: str = ""                 # PGM=... value (empty for PROC steps)
    proc: str = ""                    # PROC=... value
    step_type: str = "PGM"           # PGM | PROC | SORT | IDCAMS | UTIL
    comment_lines: List[str] = field(default_factory=list)   # //* lines above step
    datasets: List[JclDataset] = field(default_factory=list)
    sysin_data: List[str] = field(default_factory=list)      # Inline SYSIN content
    cond: str = ""                    # COND= value
    line_number: int = 0


@dataclass
class JclJob:
    """A parsed JCL job (one .jcl file = one job)."""
    job_name: str
    file_name: str
    file_path: str
    file_hash: str
    job_description: str = ""        # From JOB card string param
    job_class: str = ""
    msg_class: str = ""
    comment_lines: List[str] = field(default_factory=list)   # Header comments
    steps: List[JclStep] = field(default_factory=list)
    programs_called: List[str] = field(default_factory=list)  # All PGM= values (deduped)
    input_datasets: List[str] = field(default_factory=list)   # All input DSNs
    output_datasets: List[str] = field(default_factory=list)  # All output DSNs

    def to_dict(self) -> Dict:
        return asdict(self)


# ─────────────────────────────────────────────
# Parser
# ─────────────────────────────────────────────

class JclParser:
    """
    Regex-based JCL parser.
    Handles continuation lines (// at col 1-2, space at col 3+).
    """

    # Utility programs — not COBOL
    UTILITY_PROGRAMS = {
        "SORT", "SYNCSORT", "DFSORT", "IDCAMS", "IEBGENER", "IEBCOPY",
        "IEFBR14", "IKJEFT01", "IRXJCL", "FTP", "ASMHCL", "ASMH",
        "IEBUPDTE", "IEHINITT", "IEBCOMPR", "IEHPROGM",
    }

    def __init__(self):
        pass

    @staticmethod
    def _file_hash(path: str) -> str:
        h = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()

    def parse_file(self, file_path: str) -> Optional[JclJob]:
        """Parse a single JCL file. Returns None if not a valid JCL."""
        path = Path(file_path)
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            console.print(f"[yellow]  Warning: Cannot read {path.name}: {e}[/yellow]")
            return None

        lines = raw.splitlines()
        # Merge continuation lines into logical records
        logical = self._merge_continuations(lines)
        if not logical:
            return None

        # First logical line must be a JOB card
        job_card = self._find_job_card(logical)
        if not job_card:
            return None  # Not a proper JCL job file

        job_name, job_desc, job_class, msg_class = job_card

        job = JclJob(
            job_name=job_name,
            file_name=path.name,
            file_path=str(path),
            file_hash=self._file_hash(file_path),
            job_description=job_desc,
            job_class=job_class,
            msg_class=msg_class,
        )

        # Parse body: comments → header comments; EXEC cards → steps; DD cards → datasets
        self._parse_body(logical, job)

        # Collect summary fields
        seen_progs = set()
        seen_in = set()
        seen_out = set()
        for step in job.steps:
            if step.program and step.program not in seen_progs:
                job.programs_called.append(step.program)
                seen_progs.add(step.program)
            for ds in step.datasets:
                if not ds.dsn or ds.is_inline:
                    continue
                if ds.direction == "INPUT" and ds.dsn not in seen_in:
                    job.input_datasets.append(ds.dsn)
                    seen_in.add(ds.dsn)
                elif ds.direction == "OUTPUT" and ds.dsn not in seen_out:
                    job.output_datasets.append(ds.dsn)
                    seen_out.add(ds.dsn)

        return job

    # ─────────────────────────────────────────
    # Continuation merging
    # ─────────────────────────────────────────

    def _merge_continuations(self, lines: List[str]) -> List[Dict]:
        """
        Merge JCL continuation lines.
        A continuation line starts with // followed by at least one space
        and has content starting at col 16+.
        Returns list of {text, line_no, type} dicts.
        """
        records = []
        buf = None
        buf_start = 0

        for i, line in enumerate(lines, 1):
            if len(line) < 2:
                if buf:
                    records.append({"text": buf, "line": buf_start, "raw_lines": [buf]})
                    buf = None
                continue

            # Comment
            if line[:3] == "//*":
                if buf:
                    records.append({"text": buf, "line": buf_start})
                    buf = None
                comment = line[3:].strip()
                records.append({"text": "//*" + comment, "line": i, "is_comment": True})
                continue

            # JCL statement
            if line[:2] == "//":
                # Continuation of previous: // followed by spaces starting before col 16
                # Real continuation: col 1-2 = //, col 3 = space, col 16+ has content
                is_continuation = (
                    buf is not None
                    and len(line) > 3
                    and line[2] == " "
                    and line.rstrip()  # not blank
                )
                if is_continuation:
                    buf = buf.rstrip() + " " + line[3:].strip()
                else:
                    if buf:
                        records.append({"text": buf, "line": buf_start})
                    buf = line
                    buf_start = i
                continue

            # Inline data (between DD * and /*)
            if buf:
                records.append({"text": buf, "line": buf_start})
                buf = None
            if line.strip() == "/*":
                records.append({"text": "/*", "line": i, "is_end_inline": True})
            else:
                records.append({"text": line, "line": i, "is_inline_data": True})

        if buf:
            records.append({"text": buf, "line": buf_start})

        return records

    # ─────────────────────────────────────────
    # JOB card
    # ─────────────────────────────────────────

    def _find_job_card(self, records: List[Dict]):
        """Find the JOB card and return (name, description, class, msgclass)."""
        for rec in records:
            text = rec.get("text", "")
            if rec.get("is_comment"):
                continue
            m = re.match(r"^//(\w+)\s+JOB\s*(.*)", text, re.IGNORECASE)
            if m:
                name = m.group(1)
                rest = m.group(2).strip()
                desc = ""
                job_class = ""
                msg_class = ""

                # Extract quoted description
                dm = re.match(r"['\"]([^'\"]*)['\"]", rest)
                if dm:
                    desc = dm.group(1)

                cm = re.search(r"CLASS=(\w+)", rest, re.IGNORECASE)
                if cm:
                    job_class = cm.group(1)
                mm = re.search(r"MSGCLASS=(\w+)", rest, re.IGNORECASE)
                if mm:
                    msg_class = mm.group(1)

                return name, desc, job_class, msg_class
        return None

    # ─────────────────────────────────────────
    # Body parsing
    # ─────────────────────────────────────────

    def _parse_body(self, records: List[Dict], job: JclJob):
        current_step: Optional[JclStep] = None
        pending_comments: List[str] = []
        in_inline = False

        for rec in records:
            text = rec.get("text", "")
            line_no = rec.get("line", 0)

            # Inline data
            if rec.get("is_end_inline"):
                in_inline = False
                continue
            if rec.get("is_inline_data") or in_inline:
                if current_step and current_step.datasets:
                    last_dd = current_step.datasets[-1]
                    if last_dd.is_inline:
                        last_dd.dd_name  # just reference it
                if current_step:
                    current_step.sysin_data.append(text)
                continue

            # Comment line
            if rec.get("is_comment"):
                comment_text = text[3:].strip()
                if comment_text:
                    pending_comments.append(comment_text)
                continue

            if not text.startswith("//"):
                continue

            # Parse the statement name and type
            stmt_m = re.match(r"^//(\S*)\s+(\w+)(.*)", text)
            if not stmt_m:
                continue

            stmt_name = stmt_m.group(1)      # may be empty for continuation
            stmt_type = stmt_m.group(2).upper()
            stmt_rest = stmt_m.group(3).strip()

            # Skip JOB card (already parsed)
            if stmt_type == "JOB":
                # Header comments before JOB card → job header comments
                job.comment_lines = pending_comments[:]
                pending_comments = []
                continue

            # EXEC — new step
            if stmt_type == "EXEC":
                if current_step:
                    job.steps.append(current_step)

                program, proc, step_type = self._parse_exec(stmt_rest)
                current_step = JclStep(
                    step_name=stmt_name or f"STEP{len(job.steps)+1}",
                    program=program,
                    proc=proc,
                    step_type=step_type,
                    comment_lines=pending_comments[:],
                    line_number=line_no,
                )
                pending_comments = []

                # COND=
                cond_m = re.search(r"COND=\(([^)]+)\)", stmt_rest, re.IGNORECASE)
                if cond_m:
                    current_step.cond = cond_m.group(1)
                continue

            # DD — dataset definition within current step
            if stmt_type == "DD" and current_step is not None:
                ds = self._parse_dd(stmt_name, stmt_rest)
                if "DD *" in text or stmt_rest.strip().startswith("*"):
                    ds.is_inline = True
                    in_inline = True
                current_step.datasets.append(ds)
                pending_comments = []
                continue

            # PROC, PEND, etc — just capture comments
            pending_comments = []

        # Don't forget the last step
        if current_step:
            job.steps.append(current_step)

    # ─────────────────────────────────────────
    # EXEC parsing
    # ─────────────────────────────────────────

    def _parse_exec(self, rest: str):
        """Parse EXEC statement. Returns (program, proc, step_type)."""
        program = ""
        proc = ""

        pgm_m = re.search(r"PGM=(\w+)", rest, re.IGNORECASE)
        if pgm_m:
            program = pgm_m.group(1).upper()
            if program in self.UTILITY_PROGRAMS:
                step_type = "UTIL"
            else:
                step_type = "PGM"
            return program, "", step_type

        proc_m = re.search(r"PROC=(\w+)", rest, re.IGNORECASE)
        if proc_m:
            proc = proc_m.group(1).upper()
            return "", proc, "PROC"

        # Could be positional PROC name: EXEC MYPROCNAME
        # (no PGM= or PROC= keyword)
        pos_m = re.match(r"^(\w+)", rest.strip())
        if pos_m:
            candidate = pos_m.group(1).upper()
            if candidate not in ("PGM", "PROC", "PEND"):
                return "", candidate, "PROC"

        return "", "", "UNKNOWN"

    # ─────────────────────────────────────────
    # DD parsing
    # ─────────────────────────────────────────

    def _parse_dd(self, dd_name: str, rest: str) -> JclDataset:
        ds = JclDataset(dd_name=dd_name)

        dsn_m = re.search(r"DSN=([^\s,]+)", rest, re.IGNORECASE)
        if dsn_m:
            ds.dsn = dsn_m.group(1).strip().rstrip(",")

        disp_m = re.search(r"DISP=(?:\(([^)]+)\)|(\w+))", rest, re.IGNORECASE)
        if disp_m:
            raw_disp = disp_m.group(1) or disp_m.group(2) or ""
            parts = [p.strip() for p in raw_disp.split(",")]
            ds.disp = parts[0] if parts else ""
            ds.disposition_normal  = parts[1] if len(parts) > 1 else ""
            ds.disposition_abnormal = parts[2] if len(parts) > 2 else ""

        dcb_m = re.search(r"DCB=\(([^)]+)\)", rest, re.IGNORECASE)
        if dcb_m:
            dcb = dcb_m.group(1)
            rf = re.search(r"RECFM=(\w+)", dcb, re.IGNORECASE)
            ll = re.search(r"LRECL=(\d+)", dcb, re.IGNORECASE)
            ds.recfm = rf.group(1) if rf else ""
            ds.lrecl = ll.group(1) if ll else ""

        unit_m = re.search(r"UNIT=(\w+)", rest, re.IGNORECASE)
        if unit_m:
            ds.unit = unit_m.group(1)

        space_m = re.search(r"SPACE=\(([^)]+)\)", rest, re.IGNORECASE)
        if space_m:
            ds.space = space_m.group(1)

        # Determine direction from DISP and DD name
        ds.direction = self._infer_direction(dd_name, ds.disp)

        return ds

    @staticmethod
    def _infer_direction(dd_name: str, disp: str) -> str:
        name_upper = dd_name.upper()
        disp_upper = disp.upper()

        # System DDs
        if name_upper in ("SYSOUT", "SYSPRINT", "SYSUDUMP", "SYSABEND",
                           "SYSTSPRT", "SYSMSGS", "SYSLOG"):
            return "SYSTEM"

        # Load library, JES output
        if name_upper in ("STEPLIB", "JOBLIB", "LINKLIB"):
            return "SYSTEM"

        # SYSIN is typically input to a utility
        if name_upper == "SYSIN":
            return "INPUT"

        # DISP-based
        if disp_upper in ("SHR", "OLD"):
            return "INPUT"
        if disp_upper in ("NEW", "MOD"):
            return "OUTPUT"
        if "CATLG" in disp_upper or "PASS" in disp_upper:
            return "OUTPUT"

        # Name hints
        if any(k in name_upper for k in ("IN", "INPUT", "SRC", "SOURCE", "SORTIN")):
            return "INPUT"
        if any(k in name_upper for k in ("OUT", "OUTPUT", "DEST", "SORTOUT")):
            return "OUTPUT"

        return "UNKNOWN"

    # ─────────────────────────────────────────
    # Repository scan
    # ─────────────────────────────────────────

    def parse_repository(self, repo_path: str) -> List[JclJob]:
        """Scan a directory tree for JCL files and parse them all."""
        root = Path(repo_path)
        # On Windows rglob is case-insensitive — dedupe by resolved path.
        _all = list(root.rglob("*.jcl")) + list(root.rglob("*.JCL"))
        _seen = set()
        jcl_files = []
        for _p in _all:
            _key = str(_p.resolve()).lower()
            if _key in _seen:
                continue
            _seen.add(_key)
            jcl_files.append(_p)

        console.print(f"[cyan]Found {len(jcl_files)} JCL files[/cyan]")
        jobs = []

        with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                      BarColumn(), console=console) as progress:
            task = progress.add_task("Parsing JCL...", total=len(jcl_files))
            for jcl_file in jcl_files:
                job = self.parse_file(str(jcl_file))
                if job:
                    jobs.append(job)
                    console.print(f"[green]  OK[/green] {jcl_file.name} "
                                  f"→ {len(job.steps)} steps, "
                                  f"programs: {', '.join(job.programs_called) or 'none'}")
                else:
                    console.print(f"[yellow]  SKIP[/yellow] {jcl_file.name} (no JOB card)")
                progress.advance(task)

        console.print(f"[green]OK - Parsed {len(jobs)} JCL jobs[/green]")
        return jobs

    def save_results(self, jobs: List[JclJob], output_dir: str):
        """Save parsed JCL to JSON."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        data = [j.to_dict() for j in jobs]
        with open(out / "jcl_jobs.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        console.print(f"[green]OK - Saved {len(jobs)} JCL jobs → {out}/jcl_jobs.json[/green]")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse JCL files from a repository")
    parser.add_argument("repo_path", help="Path to directory containing JCL files")
    parser.add_argument("--output", "-o", default="parsed_output", help="Output directory")
    args = parser.parse_args()

    p = JclParser()
    jobs = p.parse_repository(args.repo_path)
    p.save_results(jobs, args.output)
