"""
JSON-to-English Translator for COBOL Knowledge Base
Reads raw parsed JSON from parsed_output/ and translates it into plain English.
Also displays the raw JSON side-by-side for transparency.
"""

import json
import textwrap
from pathlib import Path
from typing import Dict, List, Any, Optional


class JsonTranslator:
    """Translates raw parsed JSON program data into plain English."""

    def __init__(self, parsed_output_dir: str = "parsed_output"):
        self.parsed_dir = Path(parsed_output_dir)
        self._programs_cache = None
        self._copybooks_cache = None
        self._screens_cache = None

    # ────────────────────────────────────────────
    # Data loading
    # ────────────────────────────────────────────

    def _load_programs(self) -> List[Dict]:
        """Load and cache programs.json."""
        if self._programs_cache is None:
            path = self.parsed_dir / "programs.json"
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self._programs_cache = json.load(f)
            else:
                self._programs_cache = []
        return self._programs_cache

    def _load_copybooks(self) -> List[Dict]:
        """Load and cache copybooks.json."""
        if self._copybooks_cache is None:
            path = self.parsed_dir / "copybooks.json"
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self._copybooks_cache = json.load(f)
            else:
                self._copybooks_cache = []
        return self._copybooks_cache

    def _load_screens(self) -> List[Dict]:
        """Load and cache screens.json."""
        if self._screens_cache is None:
            path = self.parsed_dir / "screens.json"
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self._screens_cache = json.load(f)
            else:
                self._screens_cache = []
        return self._screens_cache

    def get_program_json(self, program_id: str) -> Optional[Dict]:
        """Get the raw parsed JSON for a specific program."""
        programs = self._load_programs()
        pid = program_id.upper().strip()
        for prog in programs:
            if prog.get("program_id", "").upper() == pid:
                return prog
        return None

    def list_programs(self) -> List[str]:
        """List all program IDs in parsed data."""
        programs = self._load_programs()
        seen = set()
        result = []
        for p in programs:
            pid = p.get("program_id", "")
            if pid and pid not in seen:
                seen.add(pid)
                result.append(pid)
        return sorted(result)

    # ────────────────────────────────────────────
    # Translation Engine
    # ────────────────────────────────────────────

    def translate_program(self, program_id: str) -> Dict[str, str]:
        """
        Translate a program's parsed JSON to English.

        Returns:
            Dict with 'raw_json' (formatted JSON string) and 'english' (translation)
        """
        prog = self.get_program_json(program_id)
        if not prog:
            return {
                "raw_json": "{}",
                "english": f"Program '{program_id}' not found in parsed_output/programs.json.",
                "found": False
            }

        # Build the raw JSON (compact but readable, limited to key sections)
        json_summary = {
            "program_id": prog.get("program_id"),
            "file_name": prog.get("file_name"),
            "program_type": prog.get("program_type"),
            "line_count": prog.get("line_count"),
            "paragraphs": [
                {"name": p["name"], "line_start": p["line_start"], "line_end": p["line_end"],
                 "statement_count": p.get("statement_count", 0)}
                for p in prog.get("paragraphs", [])
            ],
            "data_items_count": len(prog.get("data_items", [])),
            "data_items_sample": [
                {"name": d.get("name"), "level": d.get("level_number"),
                 "picture": d.get("picture"), "section": d.get("section")}
                for d in prog.get("data_items", [])[:10]
            ],
            "files": prog.get("files", []),
            "calls": prog.get("calls", []),
            "performs": prog.get("performs", []),
            "copybooks": prog.get("copybooks", []),
            "exec_cics": prog.get("exec_cics", []),
        }

        raw_json = json.dumps(json_summary, indent=2)
        english = self._json_to_english(prog)

        return {
            "raw_json": raw_json,
            "english": english,
            "found": True
        }

    def _json_to_english(self, prog: Dict) -> str:
        """Convert a program's parsed JSON into a comprehensive English description."""
        pid = prog.get("program_id", "UNKNOWN")
        lines = []

        # Header
        lines.append(f"# Program: {pid}")
        lines.append("")

        # Basic info
        lines.append(f"**{pid}** is a **{prog.get('program_type', 'UNKNOWN')}** COBOL program "
                      f"located in `{prog.get('file_path', 'N/A')}`. "
                      f"It consists of **{prog.get('line_count', '?')} lines** of code.")
        lines.append("")

        # Paragraphs (control flow)
        paragraphs = prog.get("paragraphs", [])
        if paragraphs:
            lines.append(f"## Control Flow ({len(paragraphs)} paragraphs)")
            lines.append("")
            lines.append("The program is structured into the following paragraphs (sections of logic):")
            lines.append("")
            for p in paragraphs:
                name = p.get("name", "?")
                start = p.get("line_start", "?")
                end = p.get("line_end", "?")
                stmt_count = p.get("statement_count", 0)

                # Translate paragraph name to purpose
                purpose = self._translate_paragraph_name(name)
                lines.append(f"- **{name}** (lines {start}–{end}): {purpose}")

                # Show statements if any
                stmts = p.get("statements", [])
                if stmts:
                    for s in stmts[:5]:
                        lines.append(f"  - `{s.get('type', '?')}` at line {s.get('line_number', '?')}")

            lines.append("")

        # PERFORMs (internal flow)
        performs = prog.get("performs", [])
        if performs:
            lines.append(f"## Internal PERFORM Flow ({len(performs)} calls)")
            lines.append("")
            lines.append("These are internal paragraph-to-paragraph control transfers:")
            lines.append("")

            # Group by source
            by_source = {}
            for pf in performs:
                src = pf.get("source_paragraph", "?")
                by_source.setdefault(src, []).append(pf)

            for src, pf_list in by_source.items():
                lines.append(f"**From `{src}`:**")
                for pf in pf_list:
                    target = pf.get("target_paragraph", "?")
                    ptype = pf.get("perform_type", "SIMPLE")
                    line = pf.get("line_number", "?")
                    cond = pf.get("condition")

                    desc = f"  - Calls `{target}` at line {line}"
                    if ptype != "SIMPLE":
                        desc += f" ({ptype})"
                    if cond:
                        desc += f" — condition: `{cond}`"
                    lines.append(desc)
                lines.append("")

        # External CALLs
        calls = prog.get("calls", [])
        if calls:
            lines.append(f"## External Program Calls ({len(calls)} calls)")
            lines.append("")
            for c in calls:
                target = c.get("target", c.get("called_program", "?"))
                location = c.get("location", c.get("call_location", "?"))
                line = c.get("line_number", "?")
                lines.append(f"- Calls external program **{target}** from `{location}` at line {line}")
            lines.append("")

        # Data items
        data_items = prog.get("data_items", [])
        if data_items:
            lines.append(f"## Data Items ({len(data_items)} variables)")
            lines.append("")
            lines.append("Key data structures defined in this program:")
            lines.append("")
            for d in data_items[:15]:
                name = d.get("name", "?")
                level = d.get("level_number", "?")
                pic = d.get("picture", "")
                section = d.get("section", "")
                desc = f"- **{name}** — Level {level}"
                if pic:
                    desc += f", PIC `{pic}`"
                if section:
                    desc += f" (in {section})"
                lines.append(desc)
            if len(data_items) > 15:
                lines.append(f"- ... and {len(data_items) - 15} more variables")
            lines.append("")

        # Files
        files = prog.get("files", [])
        if files:
            lines.append(f"## File I/O ({len(files)} files)")
            lines.append("")
            for f in files:
                fname = f.get("file_name", f.get("name", "?"))
                ftype = f.get("file_type", "?")
                access = f.get("access_mode", "?")
                lines.append(f"- **{fname}** — Type: {ftype}, Access: {access}")
            lines.append("")

        # Copybooks
        copybooks = prog.get("copybooks", [])
        if copybooks:
            lines.append(f"## Copybook Dependencies ({len(copybooks)} copybooks)")
            lines.append("")
            lines.append("This program includes the following shared data structures:")
            lines.append("")
            for cb in copybooks:
                lines.append(f"- `{cb}`")
            lines.append("")

        # EXEC CICS
        exec_cics = prog.get("exec_cics", [])
        if exec_cics:
            lines.append(f"## CICS Commands ({len(exec_cics)} commands)")
            lines.append("")
            lines.append("This is an online (CICS) program with the following CICS interactions:")
            lines.append("")
            for ec in exec_cics:
                cmd = ec.get("command", "?")
                line = ec.get("line_number", "?")
                lines.append(f"- `EXEC CICS {cmd}` at line {line}")
            lines.append("")

        return "\n".join(lines)

    def _translate_paragraph_name(self, name: str) -> str:
        """Translate a COBOL paragraph name into a human-readable purpose."""
        name_upper = name.upper()

        # Common COBOL naming conventions
        translations = {
            "MAIN-PARA": "Main program entry point and high-level orchestration",
            "MAIN": "Main program entry point",
            "FILE-CONTROL": "File definitions and I/O configuration",
        }

        if name_upper in translations:
            return translations[name_upper]

        # Pattern-based translations
        if "INITIALIZE" in name_upper or "INIT" in name_upper:
            return "Initialization and setup logic"
        if "EXIT" in name_upper:
            return "Exit point (paragraph boundary marker)"
        if "PROCESS" in name_upper:
            return "Core processing logic"
        if "READ" in name_upper:
            return "Data reading / input operation"
        if "WRITE" in name_upper:
            return "Data writing / output operation"
        if "DELETE" in name_upper:
            return "Record deletion logic"
        if "UPDATE" in name_upper:
            return "Record update logic"
        if "VALIDATE" in name_upper or "EDIT" in name_upper:
            return "Input validation / data editing"
        if "FIND" in name_upper or "SEARCH" in name_upper or "LOOKUP" in name_upper:
            return "Record lookup / search operation"
        if "DISPLAY" in name_upper or "SHOW" in name_upper or "SCREEN" in name_upper:
            return "Screen display / user interface"
        if "ERROR" in name_upper or "ABEND" in name_upper:
            return "Error handling / abnormal termination"
        if "CHECKPOINT" in name_upper:
            return "Transaction checkpoint for recovery"
        if "OPEN" in name_upper:
            return "File / resource open operation"
        if "CLOSE" in name_upper:
            return "File / resource close and cleanup"
        if "SEND" in name_upper:
            return "Data transmission / message sending"
        if "RECEIVE" in name_upper:
            return "Data reception / message receiving"
        if "EXTRACT" in name_upper:
            return "Data extraction logic"
        if "CHECK" in name_upper:
            return "Condition checking / validation"
        if "EXPIRED" in name_upper:
            return "Expiration checking logic"
        if "AUTH" in name_upper:
            return "Authorization processing"
        if "XREF" in name_upper:
            return "Cross-reference lookup"

        return "Program logic section"
