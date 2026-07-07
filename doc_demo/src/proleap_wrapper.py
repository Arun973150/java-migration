"""
ProLeap COBOL Parser Wrapper
Real integration with ProLeap Java parser via JPype.
Extracts full AST, statements, control flow, and data hierarchy -- Swimm-style.
"""

import os
import re
import json
import glob
import hashlib
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field, asdict

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console(force_terminal=True, highlight=False, legacy_windows=False)

# ============================================================
# Data Classes
# ============================================================

@dataclass
class ParsedProgram:
    """Represents a fully parsed COBOL program."""
    file_name: str
    file_path: str
    file_hash: str
    program_id: str
    program_type: Optional[str] = None
    line_count: int = 0
    paragraphs: Optional[List[Dict]] = None
    data_items: Optional[List[Dict]] = None
    files: Optional[List[Dict]] = None
    statements: Optional[List[Dict]] = None
    calls: Optional[List[Dict]] = None
    performs: Optional[List[Dict]] = None
    copybooks: Optional[List[str]] = None
    exec_cics: Optional[List[Dict]] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class ParsedCopybook:
    """Represents a parsed COBOL copybook."""
    file_name: str
    file_path: str
    file_hash: str
    copybook_name: str
    data_items: Optional[List[Dict]] = None

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ParsedScreen:
    """Represents a parsed BMS screen definition."""
    file_name: str
    file_path: str
    mapset_name: str
    maps: Optional[List[Dict]] = None

    def to_dict(self) -> Dict:
        return asdict(self)


# ============================================================
# ProLeap Wrapper
# ============================================================

class ProLeapWrapper:
    """
    Wrapper for ProLeap COBOL Parser via JPype.
    Extracts full AST including statements, control flow, and data hierarchy.
    """

    def __init__(
        self,
        lib_dir: str = "lib",
        cobol_format: str = "FIXED",
        copybook_dirs: List[str] = None,
        copybook_extensions: List[str] = None,
    ):
        self.lib_dir = lib_dir
        self.cobol_format = cobol_format
        self.copybook_dirs = copybook_dirs or []
        self.copybook_extensions = copybook_extensions or ["cpy", "CPY"]
        self._jvm_started = False
        self._classes = {}

    # ----------------------------------------------------------
    # JVM Management
    # ----------------------------------------------------------

    def _start_jvm(self):
        """Start JVM with ProLeap JARs on the classpath."""
        if self._jvm_started:
            return

        import jpype

        if jpype.isJVMStarted():
            self._jvm_started = True
            self._load_classes()
            return

        # Locate JAVA_HOME
        java_home = os.environ.get("JAVA_HOME", "")
        if not java_home:
            # Try common Windows install paths
            for candidate in [
                r"C:\Program Files\ojdkbuild\java-17-openjdk-17.0.3.0.6-1",
                r"C:\Program Files\Eclipse Adoptium\jdk-17*",
                r"C:\Program Files\Java\jdk-17*",
            ]:
                matches = glob.glob(candidate)
                if matches:
                    java_home = matches[0]
                    break
            if java_home:
                os.environ["JAVA_HOME"] = java_home

        # Build classpath from all JARs in lib/
        jars = glob.glob(os.path.join(self.lib_dir, "*.jar"))
        if not jars:
            raise FileNotFoundError(
                f"No JAR files found in {self.lib_dir}/. "
                "Build ProLeap first: cd proleap-cobol-parser && mvn clean package -DskipTests"
            )

        classpath = os.pathsep.join(jars)
        console.print(f"[cyan]Starting JVM with {len(jars)} JARs[/cyan]")

        jpype.startJVM(classpath=[classpath])
        self._jvm_started = True
        self._load_classes()
        console.print("[green]OK - JVM started, ProLeap classes loaded[/green]")

    def _load_classes(self):
        """Load Java classes via JClass (avoids Python 'io' collision)."""
        import jpype
        self._classes = {
            "Runner": jpype.JClass("io.proleap.cobol.asg.runner.impl.CobolParserRunnerImpl"),
            "Format": jpype.JClass("io.proleap.cobol.preprocessor.CobolPreprocessor$CobolSourceFormatEnum"),
            "Params": jpype.JClass("io.proleap.cobol.asg.params.impl.CobolParserParamsImpl"),
            "File": jpype.JClass("java.io.File"),
            "ArrayList": jpype.JClass("java.util.ArrayList"),
        }

    def _build_params(self, extra_copybook_dirs: List[str] = None):
        """Build CobolParserParams with format + copybook config."""
        params = self._classes["Params"]()
        fmt = getattr(self._classes["Format"], self.cobol_format, None)
        if fmt is None:
            console.print(f"[yellow]Warning: format {self.cobol_format} unknown, defaulting to FIXED[/yellow]")
            fmt = self._classes["Format"].FIXED
        params.setFormat(fmt)

        # Copybook directories
        dirs = self._classes["ArrayList"]()
        all_dirs = self.copybook_dirs + (extra_copybook_dirs or [])
        for d in all_dirs:
            dirs.add(self._classes["File"](str(d)))
        params.setCopyBookDirectories(dirs)

        # Copybook extensions
        exts = self._classes["ArrayList"]()
        for ext in self.copybook_extensions:
            exts.add(ext)
        params.setCopyBookExtensions(exts)

        return params

    # ----------------------------------------------------------
    # Utility
    # ----------------------------------------------------------

    @staticmethod
    def _compute_file_hash(file_path: str) -> str:
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def _safe_str(java_obj) -> Optional[str]:
        """Safely convert a Java object to Python string."""
        if java_obj is None:
            return None
        return str(java_obj)

    @staticmethod
    def _get_line(ctx) -> int:
        """Get line number from an ANTLR context."""
        try:
            if ctx and ctx.getStart():
                return int(ctx.getStart().getLine())
        except:
            pass
        return 0

    @staticmethod
    def _get_line_end(ctx) -> int:
        """Get ending line number from an ANTLR context."""
        try:
            if ctx and ctx.getStop():
                return int(ctx.getStop().getLine())
        except:
            pass
        return 0

    # ----------------------------------------------------------
    # Core Parsing
    # ----------------------------------------------------------

    def parse_cobol_file(self, file_path: str, extra_copybook_dirs: List[str] = None) -> ParsedProgram:
        """Parse a single COBOL file using ProLeap."""
        self._start_jvm()
        file_path = Path(file_path)
        file_hash = self._compute_file_hash(str(file_path))

        console.print(f"[cyan]  Parsing: {file_path.name}[/cyan]")

        params = self._build_params(extra_copybook_dirs)
        runner = self._classes["Runner"]()
        java_file = self._classes["File"](str(file_path.resolve()))

        try:
            program = runner.analyzeFile(java_file, params)
        except Exception as e:
            console.print(f"[red]  Error parsing {file_path.name}: {e}[/red]")
            # Fall back to regex-based extraction
            return self._fallback_parse(file_path, file_hash)

        # Get program unit
        comp_units = list(program.getCompilationUnits())
        if not comp_units:
            return self._fallback_parse(file_path, file_hash)

        cu = comp_units[0]
        pu = cu.getProgramUnit()

        # Extract program ID
        prog_id = file_path.stem.upper()
        id_div = pu.getIdentificationDivision()
        if id_div:
            pid = id_div.getProgramIdParagraph()
            if pid:
                prog_id = self._safe_str(pid.getName()) or prog_id

        # Detect program type
        program_type = self._detect_type(pu)

        # Count source lines
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        line_count = len(content.split("\n"))

        # Extract COPY statements from raw source
        copybooks = self._extract_copybooks_from_source(content)

        # Extract all structural data from the AST
        paragraphs, statements, calls, performs, exec_cics = self._extract_procedure_division(pu)
        data_items = self._extract_data_division(pu)
        files = self._extract_file_control(pu)

        return ParsedProgram(
            file_name=file_path.name,
            file_path=str(file_path),
            file_hash=file_hash,
            program_id=prog_id,
            program_type=program_type,
            line_count=line_count,
            paragraphs=paragraphs,
            data_items=data_items,
            files=files,
            statements=statements,
            calls=calls,
            performs=performs,
            copybooks=copybooks,
            exec_cics=exec_cics,
        )

    # ----------------------------------------------------------
    # AST Extraction: Procedure Division
    # ----------------------------------------------------------

    def _extract_procedure_division(self, pu):
        """Extract paragraphs, statements, calls, performs from Procedure Division."""
        paragraphs = []
        all_statements = []
        all_calls = []
        all_performs = []
        all_exec_cics = []

        pd = pu.getProcedureDivision()
        if not pd:
            return paragraphs, all_statements, all_calls, all_performs, all_exec_cics

        for para in pd.getParagraphs():
            para_name = self._safe_str(para.getParagraphName().getName())
            ctx = para.getCtx()
            line_start = self._get_line(ctx)
            line_end = self._get_line_end(ctx)

            para_stmts = []
            para_calls = []
            para_performs = []
            para_cics = []

            # Walk every statement in this paragraph
            if hasattr(para, "getStatements"):
                for stmt in para.getStatements():
                    stmt_info = self._classify_statement(stmt, para_name)
                    if stmt_info:
                        para_stmts.append(stmt_info)
                        all_statements.append(stmt_info)

                        # Classify into calls / performs / cics
                        stype = stmt_info["type"]
                        if stype == "CALL":
                            call_info = {
                                "called_program": stmt_info.get("target", "UNKNOWN"),
                                "line_number": stmt_info["line"],
                                "call_location": para_name,
                            }
                            para_calls.append(call_info)
                            all_calls.append(call_info)

                        elif stype == "PERFORM":
                            perf_info = {
                                "source_paragraph": para_name,
                                "target_paragraph": stmt_info.get("target", "UNKNOWN"),
                                "perform_type": stmt_info.get("perform_type", "SIMPLE"),
                                "line_number": stmt_info["line"],
                                "condition": stmt_info.get("condition"),
                            }
                            para_performs.append(perf_info)
                            all_performs.append(perf_info)

                        elif stype == "EXEC_CICS":
                            cics_info = {
                                "command": stmt_info.get("cics_command", "UNKNOWN"),
                                "line_number": stmt_info["line"],
                                "paragraph": para_name,
                                "details": stmt_info.get("details", {}),
                            }
                            para_cics.append(cics_info)
                            all_exec_cics.append(cics_info)

            paragraphs.append({
                "name": para_name,
                "line_start": line_start,
                "line_end": line_end,
                "statement_count": len(para_stmts),
                "statements": para_stmts,
                "calls": para_calls,
                "performs": para_performs,
                "exec_cics": para_cics,
            })

        return paragraphs, all_statements, all_calls, all_performs, all_exec_cics

    def _classify_statement(self, stmt, para_name: str) -> Optional[Dict]:
        """Classify a ProLeap statement node into our schema."""
        class_name = str(stmt.getClass().getSimpleName())
        ctx = stmt.getCtx()
        line = self._get_line(ctx)
        line_end = self._get_line_end(ctx)

        # Get the raw text of the statement
        raw_text = ""
        try:
            if ctx:
                start = ctx.getStart()
                stop = ctx.getStop()
                if start and stop:
                    stream = start.getTokenSource().getInputStream()
                    raw_text = str(stream.getText(start.getStartIndex(), stop.getStopIndex()))
        except:
            pass

        base = {
            "paragraph": para_name,
            "line": line,
            "line_end": line_end,
            "raw_text": raw_text[:500],  # cap length
        }

        if "IfStatement" in class_name:
            condition = self._extract_condition_text(raw_text, "IF")
            return {**base, "type": "IF", "condition": condition}

        elif "EvaluateStatement" in class_name:
            subject = self._extract_evaluate_subject(raw_text)
            whens = self._extract_evaluate_whens(raw_text)
            return {**base, "type": "EVALUATE", "subject": subject, "whens": whens}

        elif "PerformStatement" in class_name:
            target, ptype, condition = self._extract_perform_details(raw_text)
            return {**base, "type": "PERFORM", "target": target, "perform_type": ptype, "condition": condition}

        elif "CallStatement" in class_name:
            target = self._extract_call_target(raw_text)
            return {**base, "type": "CALL", "target": target}

        elif "MoveStatement" in class_name:
            src, dst = self._extract_move_details(raw_text)
            return {**base, "type": "MOVE", "source": src, "destination": dst}

        elif "ReadStatement" in class_name:
            return {**base, "type": "READ", "file": self._extract_io_file(raw_text, "READ")}

        elif "WriteStatement" in class_name:
            return {**base, "type": "WRITE", "file": self._extract_io_file(raw_text, "WRITE")}

        elif "ExecCicsStatement" in class_name:
            cmd, details = self._extract_cics_details(raw_text)
            return {**base, "type": "EXEC_CICS", "cics_command": cmd, "details": details}

        elif "SetStatement" in class_name:
            return {**base, "type": "SET"}

        elif "DisplayStatement" in class_name:
            return {**base, "type": "DISPLAY"}

        elif "StopStatement" in class_name:
            return {**base, "type": "STOP"}

        elif "GoToStatement" in class_name:
            target = self._extract_goto_target(raw_text)
            return {**base, "type": "GOTO", "target": target}

        elif "GobackStatement" in class_name or "StopRunStatement" in class_name:
            return {**base, "type": "GOBACK"}

        elif "OpenStatement" in class_name:
            return {**base, "type": "OPEN", "file": self._extract_io_file(raw_text, "OPEN")}

        elif "CloseStatement" in class_name:
            return {**base, "type": "CLOSE", "file": self._extract_io_file(raw_text, "CLOSE")}

        elif "StartStatement" in class_name:
            return {**base, "type": "START"}

        elif "DeleteStatement" in class_name:
            return {**base, "type": "DELETE"}

        elif "RewriteStatement" in class_name:
            return {**base, "type": "REWRITE"}

        elif "ComputeStatement" in class_name:
            return {**base, "type": "COMPUTE"}

        elif "AddStatement" in class_name or "SubtractStatement" in class_name:
            return {**base, "type": "ARITHMETIC"}

        elif "MultiplyStatement" in class_name or "DivideStatement" in class_name:
            return {**base, "type": "ARITHMETIC"}

        elif "StringStatement" in class_name or "UnstringStatement" in class_name:
            return {**base, "type": "STRING_OP"}

        elif "ContinueStatement" in class_name:
            return None  # skip trivial

        else:
            return {**base, "type": class_name.replace("Impl", "").replace("Statement", "").upper()}

    # ----------------------------------------------------------
    # Statement Detail Extractors (from raw text)
    # ----------------------------------------------------------

    @staticmethod
    def _extract_condition_text(raw: str, keyword: str) -> str:
        """Extract condition from IF statement raw text."""
        m = re.search(rf'{keyword}\s+(.+?)(?:\s+THEN|\s*$)', raw, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()[:300]
        return raw[:200]

    @staticmethod
    def _extract_evaluate_subject(raw: str) -> str:
        m = re.search(r'EVALUATE\s+(.+?)(?:\s+ALSO|\s+WHEN)', raw, re.IGNORECASE | re.DOTALL)
        return m.group(1).strip() if m else ""

    @staticmethod
    def _extract_evaluate_whens(raw: str) -> List[str]:
        whens = re.findall(r'WHEN\s+(.+?)(?=\s+WHEN|\s+END-EVALUATE|$)', raw, re.IGNORECASE | re.DOTALL)
        return [w.strip()[:200] for w in whens][:10]

    @staticmethod
    def _extract_perform_details(raw: str):
        target = "INLINE"
        ptype = "SIMPLE"
        condition = None

        m = re.search(r'PERFORM\s+([A-Z0-9][A-Z0-9-]*)', raw, re.IGNORECASE)
        if m:
            target = m.group(1)

        if re.search(r'THRU\s|THROUGH\s', raw, re.IGNORECASE):
            ptype = "THRU"
        if re.search(r'UNTIL\s', raw, re.IGNORECASE):
            ptype = "UNTIL"
            cm = re.search(r'UNTIL\s+(.+?)(?:\s+END-PERFORM|$)', raw, re.IGNORECASE | re.DOTALL)
            if cm:
                condition = cm.group(1).strip()[:200]
        if re.search(r'VARYING\s', raw, re.IGNORECASE):
            ptype = "VARYING"
        if re.search(r'TIMES', raw, re.IGNORECASE):
            ptype = "TIMES"

        return target, ptype, condition

    @staticmethod
    def _extract_call_target(raw: str) -> str:
        m = re.search(r"CALL\s+['\"]([A-Z0-9-]+)['\"]", raw, re.IGNORECASE)
        if m:
            return m.group(1)
        m = re.search(r"CALL\s+([A-Z0-9-]+)", raw, re.IGNORECASE)
        return m.group(1) if m else "UNKNOWN"

    @staticmethod
    def _extract_move_details(raw: str):
        m = re.search(r'MOVE\s+(.+?)\s+TO\s+(.+)', raw, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()[:100], m.group(2).strip()[:200]
        return "", ""

    @staticmethod
    def _extract_io_file(raw: str, verb: str) -> str:
        m = re.search(rf'{verb}\s+([A-Z0-9][A-Z0-9-]*)', raw, re.IGNORECASE)
        return m.group(1) if m else ""

    @staticmethod
    def _extract_goto_target(raw: str) -> str:
        m = re.search(r'GO\s+TO\s+([A-Z0-9][A-Z0-9-]*)', raw, re.IGNORECASE)
        return m.group(1) if m else ""

    @staticmethod
    def _extract_cics_details(raw: str):
        """Extract EXEC CICS command and its parameters."""
        m = re.search(r'EXEC\s+CICS\s+(\w+)', raw, re.IGNORECASE)
        cmd = m.group(1).upper() if m else "UNKNOWN"
        details = {}

        # Common CICS parameters
        for param in ["MAP", "MAPSET", "PROGRAM", "DATASET", "FILE", "TRANSID",
                       "FROM", "INTO", "LENGTH", "RIDFLD", "COMMAREA", "QUEUE"]:
            pm = re.search(rf"{param}\s*\(\s*([^)]+)\s*\)", raw, re.IGNORECASE)
            if pm:
                details[param.lower()] = pm.group(1).strip().strip("'\"")

        return cmd, details

    # ----------------------------------------------------------
    # AST Extraction: Data Division
    # ----------------------------------------------------------

    def _extract_data_division(self, pu) -> List[Dict]:
        """Extract all data items with hierarchy."""
        items = []
        dd = pu.getDataDivision()
        if not dd:
            return items

        sections = [
            ("WORKING-STORAGE", dd.getWorkingStorageSection()),
            ("LINKAGE", dd.getLinkageSection()),
            ("FILE", dd.getFileSection()),
        ]

        for section_name, section in sections:
            if not section:
                continue
            try:
                entries = list(section.getDataDescriptionEntries())
            except:
                continue

            parent_stack = {}  # level -> name, for hierarchy tracking

            for entry in entries:
                try:
                    name = self._safe_str(entry.getName()) or "FILLER"
                    level = int(entry.getLevelNumber())
                    ctx = entry.getCtx()
                    line = self._get_line(ctx)

                    # PIC clause
                    pic = None
                    try:
                        pc = entry.getPictureClause()
                        if pc:
                            pic = self._safe_str(pc.getPictureString())
                    except:
                        pass

                    # USAGE clause
                    usage = None
                    try:
                        uc = entry.getUsageClause()
                        if uc:
                            usage = self._safe_str(uc.getUsage())
                    except:
                        pass

                    # VALUE clause
                    value = None
                    try:
                        vc = entry.getValueClause()
                        if vc:
                            value = self._safe_str(vc)[:100]
                    except:
                        pass

                    # Parent tracking (hierarchy)
                    parent_name = None
                    if level > 1 and level != 88:
                        # Find nearest parent with lower level
                        for plevel in sorted(parent_stack.keys(), reverse=True):
                            if plevel < level:
                                parent_name = parent_stack[plevel]
                                break
                    if level != 88:
                        parent_stack[level] = name
                        # Remove deeper levels
                        for k in list(parent_stack.keys()):
                            if k > level:
                                del parent_stack[k]
                    elif parent_stack:
                        # 88-level: parent is the last non-88 entry
                        max_level = max(k for k in parent_stack.keys())
                        parent_name = parent_stack[max_level]

                    items.append({
                        "name": name,
                        "level_number": level,
                        "picture": pic,
                        "usage": usage,
                        "value": value,
                        "section": section_name,
                        "parent_name": parent_name,
                        "line_number": line,
                    })
                except Exception as e:
                    continue

        return items

    # ----------------------------------------------------------
    # AST Extraction: File Control
    # ----------------------------------------------------------

    def _extract_file_control(self, pu) -> List[Dict]:
        """Extract file definitions from Environment Division."""
        files = []
        ed = pu.getEnvironmentDivision()
        if not ed:
            return files

        try:
            ios = ed.getInputOutputSection()
            if not ios:
                return files
            fcs = ios.getFileControlSection()
            if not fcs:
                return files

            for fce in fcs.getFileControlEntries():
                name = self._safe_str(fce.getName()) or "UNKNOWN"
                org = ""
                access = ""
                try:
                    oc = fce.getOrganizationClause()
                    if oc:
                        org = self._safe_str(oc.getOrganization()) or ""
                except:
                    pass
                try:
                    ac = fce.getAccessModeClause()
                    if ac:
                        access = self._safe_str(ac.getAccessMode()) or ""
                except:
                    pass

                files.append({
                    "file_name": name,
                    "file_type": org if org else "SEQUENTIAL",
                    "organization": org,
                    "access_mode": access,
                    "line_number": self._get_line(fce.getCtx()) if hasattr(fce, "getCtx") else 0,
                })
        except:
            pass

        return files

    # ----------------------------------------------------------
    # Program Type Detection
    # ----------------------------------------------------------

    def _detect_type(self, pu) -> str:
        """Detect if program is ONLINE (CICS), DB2, or BATCH."""
        pd = pu.getProcedureDivision()
        if not pd:
            return "BATCH"

        for para in pd.getParagraphs():
            if hasattr(para, "getStatements"):
                for stmt in para.getStatements():
                    cn = str(stmt.getClass().getSimpleName())
                    if "ExecCics" in cn:
                        return "ONLINE"
                    if "ExecSql" in cn:
                        return "DB2"
        return "BATCH"

    # ----------------------------------------------------------
    # Source-Level Extraction (supplements AST)
    # ----------------------------------------------------------

    @staticmethod
    def _extract_copybooks_from_source(content: str) -> List[str]:
        """Extract COPY statements from raw source."""
        copybooks = set()
        for line in content.split("\n"):
            if len(line) > 6 and line[6] == "*":
                continue
            m = re.search(r"COPY\s+([A-Z0-9][A-Z0-9-]*)", line, re.IGNORECASE)
            if m:
                copybooks.add(m.group(1).upper())
        return sorted(copybooks)

    # ----------------------------------------------------------
    # Fallback Parser (regex, when ProLeap fails on a file)
    # ----------------------------------------------------------

    def _fallback_parse(self, file_path: Path, file_hash: str) -> ParsedProgram:
        """Regex-based fallback for files ProLeap can't handle."""
        console.print(f"[yellow]  Using fallback parser for {file_path.name}[/yellow]")
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")

        # Strip column 1-6 sequence area + column 73-80 sequence area, then
        # search for PROGRAM-ID. The COBOL name may be on the same line OR
        # on the next non-blank, non-comment line.
        def _strip_columns(line: str) -> str:
            body = line[6:] if len(line) > 6 else line
            return body[:66] if len(body) > 66 else body

        def _is_comment(line: str) -> bool:
            return len(line) > 6 and line[6] == "*"

        # Acceptable COBOL program-id pattern (must contain at least one letter)
        valid_id_pat = re.compile(r"^[A-Z][A-Z0-9-]{0,29}$")

        def _try_extract_id(text: str) -> Optional[str]:
            """Pull the first identifier-like token; reject all-digits."""
            text = text.strip().strip(".").strip(",").strip()
            if not text:
                return None
            tok = text.split()[0].strip(".,")
            tok_upper = tok.upper()
            if valid_id_pat.match(tok_upper):
                return tok_upper
            return None

        prog_id = file_path.stem.upper()
        for idx, raw_line in enumerate(lines):
            if _is_comment(raw_line):
                continue
            body = _strip_columns(raw_line)
            if "PROGRAM-ID" not in body.upper():
                continue
            # Split on the FIRST period after PROGRAM-ID
            after = re.split(r"PROGRAM-ID\s*\.\s*", body, maxsplit=1, flags=re.IGNORECASE)
            tail = after[1] if len(after) > 1 else ""
            candidate = _try_extract_id(tail)
            # If empty / sequence-number / nothing on this line, walk forward
            # until we find a real identifier line.
            if not candidate:
                for j in range(idx + 1, min(idx + 6, len(lines))):
                    if _is_comment(lines[j]):
                        continue
                    next_body = _strip_columns(lines[j])
                    if not next_body.strip():
                        continue
                    candidate = _try_extract_id(next_body)
                    if candidate:
                        break
            if candidate:
                prog_id = candidate
            break

        ptype = "BATCH"
        if any("EXEC CICS" in l.upper() for l in lines):
            ptype = "ONLINE"
        elif any("EXEC SQL" in l.upper() for l in lines):
            ptype = "DB2"

        # Simple regex extraction
        paragraphs = []
        para_pat = re.compile(r"^       ([A-Z0-9][A-Z0-9-]*)\s*\.\s*$")
        cur_para, cur_start = None, 0
        for i, line in enumerate(lines, 1):
            if len(line) > 6 and line[6] == "*":
                continue
            m = para_pat.match(line)
            if m:
                if cur_para:
                    paragraphs.append({"name": cur_para, "line_start": cur_start, "line_end": i - 1,
                                       "statement_count": 0, "statements": [], "calls": [], "performs": [], "exec_cics": []})
                cur_para, cur_start = m.group(1), i
        if cur_para:
            paragraphs.append({"name": cur_para, "line_start": cur_start, "line_end": len(lines),
                               "statement_count": 0, "statements": [], "calls": [], "performs": [], "exec_cics": []})

        calls = []
        for i, line in enumerate(lines, 1):
            m = re.search(r"CALL\s+['\"]([A-Z0-9-]+)['\"]", line, re.IGNORECASE)
            if m:
                calls.append({"called_program": m.group(1), "line_number": i, "call_location": ""})

        performs = []
        for i, line in enumerate(lines, 1):
            m = re.search(r"PERFORM\s+([A-Z0-9][A-Z0-9-]*)", line, re.IGNORECASE)
            if m:
                performs.append({"source_paragraph": "MAIN", "target_paragraph": m.group(1),
                                 "perform_type": "SIMPLE", "line_number": i, "condition": None})

        copybooks = self._extract_copybooks_from_source(content)

        return ParsedProgram(
            file_name=file_path.name, file_path=str(file_path), file_hash=file_hash,
            program_id=prog_id, program_type=ptype, line_count=len(lines),
            paragraphs=paragraphs, data_items=[], files=[], statements=[],
            calls=calls, performs=performs, copybooks=copybooks, exec_cics=[],
        )

    # ----------------------------------------------------------
    # BMS Screen Parser
    # ----------------------------------------------------------

    def parse_bms_file(self, file_path: str) -> ParsedScreen:
        """Parse a BMS (Basic Mapping Support) screen definition."""
        file_path = Path(file_path)
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        raw_lines = content.split("\n")

        # Join continuation lines (lines ending with '-' in ~col 72 mean next line continues)
        joined_lines = []
        current = ""
        for line in raw_lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("*"):
                continue
            # Check for continuation: line has '-' at or near column 72
            # BMS continuation: non-comment line ending with '-' after column 70
            if len(line) >= 71 and line[71:72] == '-':
                # This line continues on next line - strip the '-' and leading spaces of continuation
                current += stripped.rstrip('-').rstrip() + " "
                continue
            elif current:
                # Previous line(s) had continuation, this is the final part
                # Strip leading spaces (continuation indent)
                current += stripped
                joined_lines.append(current)
                current = ""
            else:
                joined_lines.append(stripped)
        if current:
            joined_lines.append(current)

        mapset_name = file_path.stem.upper()
        maps = []
        current_map = None

        for joined_line in joined_lines:
            upper = joined_line.upper()

            # DFHMSD - Mapset definition
            m = re.search(r"(\w+)\s+DFHMSD", upper)
            if m:
                mapset_name = m.group(1)
                continue

            # DFHMDI - Map definition
            m = re.search(r"(\w+)\s+DFHMDI", upper)
            if m:
                current_map = {
                    "map_name": m.group(1),
                    "fields": [],
                    "size": self._extract_bms_param(joined_line, "SIZE"),
                    "line": self._extract_bms_param(joined_line, "LINE"),
                    "column": self._extract_bms_param(joined_line, "COLUMN"),
                }
                maps.append(current_map)
                continue

            # DFHMDF - Field definition (named field)
            m = re.search(r"(\w+)\s+DFHMDF", upper)
            if m and current_map is not None:
                field_name = m.group(1)
                pos = self._extract_bms_param(joined_line, "POS")
                length = self._extract_bms_param(joined_line, "LENGTH")
                attrb = self._extract_bms_param(joined_line, "ATTRB")
                color = self._extract_bms_param(joined_line, "COLOR")
                initial = self._extract_bms_param(joined_line, "INITIAL")

                # Determine field type from attributes
                field_type = "OUTPUT"
                if attrb:
                    attrb_upper = attrb.upper()
                    if "UNPROT" in attrb_upper:
                        field_type = "INPUT"
                    elif "PROT" in attrb_upper or "ASKIP" in attrb_upper:
                        field_type = "OUTPUT"

                row, col = 0, 0
                if pos:
                    pm = re.match(r"\(?\s*(\d+)\s*,\s*(\d+)\s*\)?", pos)
                    if pm:
                        row, col = int(pm.group(1)), int(pm.group(2))

                current_map["fields"].append({
                    "field_name": field_name,
                    "field_type": field_type,
                    "length": int(length) if length and length.isdigit() else 0,
                    "row_position": row,
                    "col_position": col,
                    "attributes": attrb or "",
                    "color": color or "",
                    "initial_value": initial or "",
                })
                continue

            # Unnamed DFHMDF (label/decoration)
            if "DFHMDF" in upper and current_map is not None:
                initial = self._extract_bms_param(joined_line, "INITIAL")
                pos = self._extract_bms_param(joined_line, "POS")
                length = self._extract_bms_param(joined_line, "LENGTH")
                if pos:
                    row, col = 0, 0
                    pm = re.match(r"\(?\s*(\d+)\s*,\s*(\d+)\s*\)?", pos)
                    if pm:
                        row, col = int(pm.group(1)), int(pm.group(2))
                    initial_text = (initial or "").strip("'\" ")
                    current_map["fields"].append({
                        "field_name": f"_LABEL_{row}_{col}",
                        "field_type": "LABEL",
                        "length": int(length) if length and length.isdigit() else len(initial_text),
                        "row_position": row,
                        "col_position": col,
                        "attributes": "ASKIP",
                        "color": self._extract_bms_param(joined_line, "COLOR") or "",
                        "initial_value": initial_text,
                    })

        return ParsedScreen(
            file_name=file_path.name,
            file_path=str(file_path),
            mapset_name=mapset_name,
            maps=maps,
        )

    @staticmethod
    def _extract_bms_param(line: str, param: str) -> Optional[str]:
        """Extract a BMS parameter value from a line (handles parenthesized values)."""
        # Handle parenthesized values like POS=(1,8), ATTRB=(ASKIP,FSET,NORM), SIZE=(24,80)
        m = re.search(rf"{param}\s*=\s*(\([^)]+\))", line, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # Handle quoted values like INITIAL='text here'
        m = re.search(rf"{param}\s*=\s*'([^']*)'", line, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # Handle simple values like LENGTH=40, COLOR=BLUE
        m = re.search(rf"{param}\s*=\s*([A-Z0-9_&][A-Z0-9_&]*)", line, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        return None

    # ----------------------------------------------------------
    # Repository-Wide Parsing
    # ----------------------------------------------------------

    def parse_repository(self, repo_path: str,
                          existing_hashes: Dict[str, str] = None) -> Dict[str, List]:
        """
        Parse all COBOL, BMS, and copybook files in a repository.
        existing_hashes: {file_path: md5_hash} from the DB — skip unchanged files.
        """
        repo_path = Path(repo_path)
        existing_hashes = existing_hashes or {}
        results = {"programs": [], "copybooks": [], "screens": [], "skipped": 0}

        # Find copybook directories
        cpy_dirs = []
        for d in repo_path.rglob("*"):
            if d.is_dir() and d.name.lower() in ["cpy", "cpy-bms", "copybooks", "copy"]:
                cpy_dirs.append(str(d))
        if not cpy_dirs:
            cpy_dirs = [str(repo_path)]
        self.copybook_dirs = cpy_dirs
        console.print(f"[cyan]Copybook dirs: {cpy_dirs}[/cyan]")

        # Find COBOL program files. On Windows, rglob is case-insensitive so
        # *.cbl and *.CBL both match the same files — dedupe by resolved path.
        def _dedupe_by_path(paths):
            seen = set()
            out = []
            for p in paths:
                key = str(p.resolve()).lower()
                if key in seen:
                    continue
                seen.add(key)
                out.append(p)
            return out

        cobol_files = []
        for ext in [".cbl", ".CBL", ".cob", ".COB"]:
            cobol_files.extend(repo_path.rglob(f"*{ext}"))
        cobol_files = _dedupe_by_path(cobol_files)

        cpy_files = []
        for ext in [".cpy", ".CPY"]:
            cpy_files.extend(repo_path.rglob(f"*{ext}"))
        cpy_files = _dedupe_by_path(cpy_files)

        bms_files = []
        for ext in [".bms", ".BMS"]:
            bms_files.extend(repo_path.rglob(f"*{ext}"))
        bms_files = _dedupe_by_path(bms_files)

        console.print(f"[cyan]Found: {len(cobol_files)} programs, {len(cpy_files)} copybooks, {len(bms_files)} BMS maps[/cyan]")

        # Parse programs (incremental: skip if file hash unchanged)
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                       BarColumn(), console=console) as progress:
            task = progress.add_task("Parsing COBOL programs...", total=len(cobol_files))
            for fpath in sorted(cobol_files):
                try:
                    fpath_str = str(fpath)
                    current_hash = self._compute_file_hash(fpath_str)
                    if existing_hashes.get(fpath_str) == current_hash:
                        results["skipped"] = results.get("skipped", 0) + 1
                        progress.advance(task)
                        continue
                    parsed = self.parse_cobol_file(fpath_str)
                    results["programs"].append(parsed.to_dict())
                except Exception as e:
                    console.print(f"[red]  Failed: {fpath.name}: {e}[/red]")
                progress.advance(task)

        # Parse copybooks (lightweight: just data items)
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                       BarColumn(), console=console) as progress:
            task = progress.add_task("Parsing copybooks...", total=len(cpy_files))
            for fpath in sorted(cpy_files):
                try:
                    fhash = self._compute_file_hash(str(fpath))
                    content = fpath.read_text(encoding="utf-8", errors="ignore")
                    data_items = self._parse_copybook_data_items(content)
                    cb = ParsedCopybook(
                        file_name=fpath.name, file_path=str(fpath), file_hash=fhash,
                        copybook_name=fpath.stem.upper(), data_items=data_items,
                    )
                    results["copybooks"].append(cb.to_dict())
                except Exception as e:
                    console.print(f"[yellow]  Warning: {fpath.name}: {e}[/yellow]")
                progress.advance(task)

        # Parse BMS screens
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                       BarColumn(), console=console) as progress:
            task = progress.add_task("Parsing BMS screens...", total=len(bms_files))
            for fpath in sorted(bms_files):
                try:
                    screen = self.parse_bms_file(str(fpath))
                    results["screens"].append(screen.to_dict())
                except Exception as e:
                    console.print(f"[yellow]  Warning: {fpath.name}: {e}[/yellow]")
                progress.advance(task)

        # Resolve dynamic CALL via variable (MOVE 'PROG' TO WS-VAR → CALL WS-VAR)
        self._resolve_dynamic_calls(results["programs"])

        console.print(f"[green]OK - Parsed {len(results['programs'])} programs, "
                       f"{len(results['copybooks'])} copybooks, {len(results['screens'])} screens[/green]")
        return results

    @staticmethod
    def _resolve_dynamic_calls(programs: List[Dict]):
        """
        Trace MOVE 'LITERAL' TO <var> statements to resolve CALL <var> = UNKNOWN.

        Algorithm per program:
          1. Walk all statements, collect MOVE source→destination pairs where
             source is a quoted string literal (potential program name).
          2. Build a map: variable_name → latest literal assigned to it.
          3. For each CALL whose target is UNKNOWN or a variable name (not a literal),
             look it up in the map and replace if found.
        """
        resolved_total = 0

        for prog in programs:
            statements = prog.get("statements") or []
            calls = prog.get("calls") or []

            # Collect: variable → string literal assignments from MOVE statements
            var_to_literal: Dict[str, str] = {}
            for stmt in statements:
                if stmt.get("type") != "MOVE":
                    continue
                src  = (stmt.get("source") or "").strip()
                dest = (stmt.get("destination") or "").strip()
                if not src or not dest:
                    continue
                # Source must be a quoted string literal
                m = re.match(r"""^['"]([A-Z0-9][A-Z0-9-]{1,8})['"]$""", src)
                if m:
                    var_to_literal[dest.upper()] = m.group(1).upper()

            if not var_to_literal:
                continue

            # Resolve UNKNOWN calls in this program
            resolved_here = 0
            for call in calls:
                target = (call.get("called_program") or "").upper()
                if target in ("UNKNOWN", "") or (
                    target and target not in _COBOL_LITERAL_RE.findall(target)
                ):
                    # Try to resolve from the map
                    # The raw call statement may reference a variable name
                    raw = (call.get("raw") or call.get("called_program") or "").upper().strip()
                    resolved = var_to_literal.get(raw) or var_to_literal.get(target)
                    if resolved:
                        call["called_program"] = resolved
                        call["resolved_from_variable"] = raw
                        resolved_here += 1

            if resolved_here:
                resolved_total += resolved_here
                prog["calls"] = calls

        if resolved_total:
            console.print(f"[green]  Resolved {resolved_total} dynamic CALL targets[/green]")

    def _parse_copybook_data_items(self, content: str) -> List[Dict]:
        """Extract data items from a copybook using regex."""
        items = []
        data_pat = re.compile(
            r"^\s+(\d{2})\s+([A-Z0-9][A-Z0-9-]*)\s+(?:PIC(?:TURE)?\s+)?([A-Z0-9()\-VSP.]+)?",
            re.IGNORECASE
        )
        parent_stack = {}
        for i, line in enumerate(content.split("\n"), 1):
            if len(line) > 6 and line[6] == "*":
                continue
            m = data_pat.search(line)
            if m:
                level = int(m.group(1))
                name = m.group(2)
                pic = m.group(3)
                parent = None
                if level > 1 and level != 88:
                    for pl in sorted(parent_stack.keys(), reverse=True):
                        if pl < level:
                            parent = parent_stack[pl]
                            break
                if level != 88:
                    parent_stack[level] = name
                    for k in list(parent_stack.keys()):
                        if k > level:
                            del parent_stack[k]
                elif parent_stack:
                    max_l = max(parent_stack.keys())
                    parent = parent_stack[max_l]

                items.append({
                    "name": name, "level_number": level, "picture": pic,
                    "parent_name": parent, "line_number": i,
                })
        return items

    # ----------------------------------------------------------
    # Save Results
    # ----------------------------------------------------------

    def save_results(self, results: Dict, output_dir: str):
        """Save parsed results to JSON files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        with open(output_path / "programs.json", "w") as f:
            json.dump(results["programs"], f, indent=2, default=str)

        with open(output_path / "copybooks.json", "w") as f:
            json.dump(results["copybooks"], f, indent=2, default=str)

        if results.get("screens"):
            with open(output_path / "screens.json", "w") as f:
                json.dump(results["screens"], f, indent=2, default=str)

        console.print(f"[green]OK - Saved results to {output_path}[/green]")


# ============================================================
# CLI Entry Point
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse COBOL repository with ProLeap")
    parser.add_argument("repo_path", help="Path to COBOL repository")
    parser.add_argument("--output", "-o", default="parsed_output", help="Output directory")
    parser.add_argument("--format", default="FIXED", help="COBOL format (TANDEM, FIXED)")
    parser.add_argument("--lib", default="lib", help="Directory containing ProLeap JARs")

    args = parser.parse_args()

    wrapper = ProLeapWrapper(lib_dir=args.lib, cobol_format=args.format)
    results = wrapper.parse_repository(args.repo_path)
    wrapper.save_results(results, args.output)
