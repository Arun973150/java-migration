"""
SQLite-backed PMODEL generator for Unisys AB Suite migration demos.

The generator intentionally reads the knowledge database instead of opening a
single COBOL source file. That keeps the path scalable for full-codebase
generation after the parser/graph pipeline has populated SQLite and Neo4j.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import xml.etree.ElementTree as etree
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


ZERO_GUID = "00000000-0000-0000-0000-000000000000"
LANGUAGE_GUID = "000003E8-0000-0000-0000-000000000000"
MODEL_GUID = "00000001-0000-0000-0000-000000000000"


@dataclass
class PModelGenerationResult:
    program_id: str
    output_path: Optional[str]
    xml_text: str
    data_object_count: int
    method_count: int
    statement_count: int


class SQLitePModelGenerator:
    """Generate a PMODEL PublicInterchangeFile from SQLite graph facts."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._id_counter = 0
        self._used_names: Dict[str, int] = {}

    def generate_program(self, program_id: str, output_path: Optional[str] = None) -> PModelGenerationResult:
        program_id = program_id.upper().strip()
        with self._connect() as conn:
            program = self._fetch_one(conn, "SELECT * FROM programs WHERE program_id = ?", (program_id,))
            if not program:
                raise ValueError(f"Program {program_id} was not found in SQLite.")

            data_items = self._fetch_all(
                conn,
                """
                SELECT * FROM data_items
                WHERE program_id = ?
                ORDER BY COALESCE(line_number, 999999), id
                """,
                (program_id,),
            )
            file_records = self._fetch_all(
                conn,
                """
                SELECT * FROM file_records
                WHERE program_id = ?
                ORDER BY COALESCE(line_number, 999999), id
                """,
                (program_id,),
            )
            paragraphs = self._fetch_all(
                conn,
                """
                SELECT * FROM paragraphs
                WHERE program_id = ?
                ORDER BY COALESCE(line_start, 999999), paragraph_name
                """,
                (program_id,),
            )
            statements = self._fetch_all(
                conn,
                """
                SELECT * FROM statements
                WHERE program_id = ?
                ORDER BY COALESCE(line_number, 999999), id
                """,
                (program_id,),
            )
            files = self._fetch_all(conn, "SELECT * FROM files WHERE program_id = ? ORDER BY file_name", (program_id,))
            copybooks = self._fetch_all(
                conn,
                "SELECT * FROM copybook_usage WHERE program_id = ? ORDER BY copybook_name",
                (program_id,),
            )
            calls = self._fetch_all(
                conn,
                "SELECT * FROM program_calls WHERE caller_program = ? ORDER BY COALESCE(line_number, 999999)",
                (program_id,),
            )

        self._id_counter = 0
        self._used_names = {}
        root = self._build_root()
        model = self._add_model(root, program)
        segment = self._add_segment(model, program, files, copybooks, calls)

        data_count = self._add_data_objects(segment, data_items, file_records)
        method_count = self._add_methods(segment, paragraphs, statements)

        xml_text = self._format_xml(root)
        self._validate_xml(xml_text)

        if output_path:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(xml_text, encoding="utf-16")

        return PModelGenerationResult(
            program_id=program_id,
            output_path=str(output_path) if output_path else None,
            xml_text=xml_text,
            data_object_count=data_count,
            method_count=method_count,
            statement_count=len(statements),
        )

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def _fetch_one(conn: sqlite3.Connection, sql: str, params: Tuple[Any, ...]) -> Optional[Dict[str, Any]]:
        row = conn.execute(sql, params).fetchone()
        return dict(row) if row else None

    @staticmethod
    def _fetch_all(conn: sqlite3.Connection, sql: str, params: Tuple[Any, ...]) -> List[Dict[str, Any]]:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]

    def _build_root(self) -> etree.Element:
        root = etree.Element("PublicInterchangeFile")
        root.set("SchemaVersion", "1.0")
        root.set("Source", "COBOL-Knowledge-SQLite")
        root.set("SourceVersion", "9.0.1020.14")
        root.set("ProductFeatures", "16")
        root.set("Creator", "COBOL-Migration-Hub")
        root.set("CreationTime", datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

        language = etree.SubElement(root, "LANGUAGE")
        language.set("Id", LANGUAGE_GUID)
        language.set("Inherits", ZERO_GUID)
        language.set("Name", "Primary")
        language.set("Description", "")
        language.set("Locale", "1033")
        return root

    def _add_model(self, root: etree.Element, program: Dict[str, Any]) -> etree.Element:
        model_name = self._clean_name(f"{program['program_id']}_MODEL")
        model = etree.SubElement(root, "MODEL")
        model.set("Id", MODEL_GUID)
        model.set("Name", model_name)
        model.set("Owner", ZERO_GUID)
        model.set("Description", program.get("business_purpose") or f"Generated PMODEL for {program['program_id']}")
        model.set("Visibility", "Public")
        model.set("Author", "COBOL-Migration-Hub")
        model.set("VersionFile", f"{model_name}.model")
        model.set("IsEnforcePersistent", "No")
        model.set("IsEnforcePresentation", "No")
        model.set("Sok", "123")
        model.set("Eok", "125")
        model.set("IsAccessControlled", "No")
        model.set("PrimaryPresentationType", "Graphical")
        return model

    def _add_segment(
        self,
        model: etree.Element,
        program: Dict[str, Any],
        files: List[Dict[str, Any]],
        copybooks: List[Dict[str, Any]],
        calls: List[Dict[str, Any]],
    ) -> etree.Element:
        segment = etree.SubElement(model, "OBJECT")
        segment_id = self._new_id()
        name = self._unique_name(self._clean_name(program["program_id"]))
        segment.set("Id", segment_id)
        segment.set("Name", name)
        segment.set("Alias", program["program_id"][:12])
        segment.set("Owner", MODEL_GUID)
        segment.set("Description", program.get("business_name") or f"Converted from COBOL program {program['program_id']}")
        segment.set("Visibility", "Public")
        segment.set("Author", "COBOL-Migration-Hub")
        segment.set("VersionFile", f"{name}.model")
        self._set_class_defaults(segment, stereotype="Segment", dimensions="0")

        doc = etree.SubElement(segment, "Documentation")
        doc.text = "\n".join(
            [
                f"Program: {program['program_id']}",
                f"Type: {program.get('program_type') or 'UNKNOWN'}",
                f"Source path captured in SQLite: {program.get('file_path') or 'not available'}",
                f"Files: {', '.join(f.get('file_name', '') for f in files) or 'None'}",
                f"Copybooks: {', '.join(c.get('copybook_name', '') for c in copybooks) or 'None'}",
                f"Calls: {', '.join(c.get('called_program', '') for c in calls) or 'None'}",
                f"Generated: {datetime.now().isoformat(timespec='seconds')}",
            ]
        )
        return segment

    def _add_data_objects(
        self,
        segment: etree.Element,
        data_items: List[Dict[str, Any]],
        file_records: List[Dict[str, Any]],
    ) -> int:
        count = 0
        object_by_key: Dict[Tuple[str, str], etree.Element] = {}

        for item in self._dedupe_fields(data_items + self._file_records_as_data_items(file_records)):
            raw_name = item.get("name") or item.get("field_name") or "FIELD"
            parent_name = item.get("parent_name")
            parent = object_by_key.get((item.get("section") or "", parent_name or "")) if parent_name else None
            owner = parent if parent is not None else segment

            obj = etree.SubElement(owner, "OBJECT")
            obj.set("Id", self._new_id())
            obj.set("Name", self._unique_name(self._clean_name(raw_name)))
            obj.set("Alias", raw_name[:32])
            obj.set("Owner", owner.get("Id", ""))
            obj.set("Sequence", str(count + 1))
            obj.set("Description", item.get("description") or "")
            obj.set("Visibility", "Public")
            obj.set("Author", "")
            obj.set("VersionFile", "")
            obj.set("IsSealed", "Yes")
            primitive, length, decimals = self._picture_to_type(item.get("picture"))
            obj.set("Primitive", primitive)
            obj.set("Length", str(max(1, length)))
            if decimals:
                obj.set("Decimals", str(decimals))
            self._set_attribute_defaults(obj)

            if item.get("value"):
                value = etree.SubElement(obj, "VALUE")
                value.set("Id", self._new_id())
                value.set("Name", LANGUAGE_GUID)
                value.set("Owner", obj.get("Id", ""))
                initial = etree.SubElement(value, "InitialValue")
                initial.text = str(item["value"]).strip("'\"")

            object_by_key[(item.get("section") or "", raw_name)] = obj
            count += 1

        return count

    def _add_methods(
        self,
        segment: etree.Element,
        paragraphs: List[Dict[str, Any]],
        statements: List[Dict[str, Any]],
    ) -> int:
        statements_by_paragraph: Dict[Optional[str], List[Dict[str, Any]]] = {}
        for statement in statements:
            statements_by_paragraph.setdefault(statement.get("paragraph_name"), []).append(statement)

        method_count = 0
        main_statements = statements_by_paragraph.get(None) or []
        if main_statements:
            self._add_method(segment, "Main", main_statements, "Top-level procedure statements")
            method_count += 1

        seen = set()
        for paragraph in paragraphs:
            para_name = paragraph.get("paragraph_name")
            if not para_name or para_name in seen:
                continue
            seen.add(para_name)
            para_statements = statements_by_paragraph.get(para_name, [])
            self._add_method(segment, para_name, para_statements, paragraph.get("purpose") or "")
            method_count += 1

        for para_name, para_statements in sorted(statements_by_paragraph.items(), key=lambda item: str(item[0])):
            if para_name is None or para_name in seen:
                continue
            self._add_method(segment, para_name, para_statements, "")
            method_count += 1

        return method_count

    def _add_method(
        self,
        segment: etree.Element,
        name: str,
        statements: List[Dict[str, Any]],
        description: str,
    ) -> etree.Element:
        method = etree.SubElement(segment, "METHOD")
        method.set("Id", self._new_id())
        method.set("Name", self._unique_name(self._clean_name(name)))
        method.set("Owner", segment.get("Id", ""))
        method.set("Description", description or "")
        method.set("Visibility", "Public")
        method.set("Author", "")
        method.set("VersionFile", "")
        method.set("IsFinal", "No")
        method.set("Language", "LDL")
        logic = etree.SubElement(method, "Logic")
        logic.text = self._statements_to_ldlplus(statements)
        return method

    def _statements_to_ldlplus(self, statements: Iterable[Dict[str, Any]]) -> str:
        statements = list(statements)
        has_structured_blocks = any(
            (statement.get("statement_type") or "").upper() in {"ELSE", "END-IF", "END-PERFORM", "END-EVALUATE"}
            for statement in statements
        )
        lines: List[str] = []
        for statement in statements:
            stype = (statement.get("statement_type") or "").upper()
            details = self._json_dict(statement.get("details_json"))
            normalized = statement.get("normalized_text") or ""
            line_no = statement.get("line_number")

            if stype == "MOVE":
                src, dst = self._move_operands(details, normalized)
                if src and dst:
                    lines.append(self._assignment_or_move(src, dst))
                else:
                    lines.append(self._todo("Review COBOL MOVE manually", normalized, line_no))
            elif stype == "DISPLAY":
                content = details.get("content") or normalized.removeprefix("DISPLAY").strip().rstrip(".")
                if content:
                    lines.append(f"Message Attention {self._display_expression_to_ldl(content)}")
                else:
                    lines.append(self._todo("Review COBOL DISPLAY manually", normalized, line_no))
            elif stype == "PERFORM":
                target = (details.get("target") or self._perform_target(normalized)).strip().rstrip(".")
                if target.upper().startswith("UNTIL "):
                    condition = target[6:].strip()
                    if has_structured_blocks:
                        lines.append(f"Loop While ({self._negated_condition_to_ldl(condition)})")
                    else:
                        lines.extend(
                            [
                                "Loop",
                                f"If {self._condition_to_ldl(condition)}",
                                "Break",
                                "End",
                                self._todo("Rebuild PERFORM UNTIL body from control-flow analysis", normalized, line_no),
                                "End",
                            ]
                        )
                elif target:
                    lines.append(f"{self._clean_name(target)}()")
                else:
                    lines.append(self._todo("Review COBOL PERFORM manually", normalized, line_no))
            elif stype == "IF":
                condition = details.get("condition") or self._if_condition(normalized)
                if condition:
                    lines.append(f"DoWhen ({self._condition_to_ldl(condition)})")
                    if not has_structured_blocks:
                        lines.append(self._todo("Rebuild IF body from control-flow analysis", normalized, line_no))
                        lines.append("End")
                else:
                    lines.append(self._todo("Review COBOL IF manually", normalized, line_no))
            elif stype == "ELSE":
                lines.append("Else")
            elif stype in {"END-IF", "END-PERFORM"}:
                lines.append("End")
            elif stype == "EVALUATE":
                subject = details.get("subject")
                lines.append(f"BeginCase {self._expression_to_ldl(subject)}" if subject else self._todo("Review COBOL EVALUATE manually", normalized, line_no))
            elif stype == "WHEN":
                condition = details.get("condition")
                if condition and condition.upper() == "OTHER":
                    lines.append("Otherwise")
                elif condition:
                    lines.append(f"Case {self._expression_to_ldl(condition)}")
                else:
                    lines.append(self._todo("Review COBOL WHEN manually", normalized, line_no))
            elif stype == "END-EVALUATE":
                lines.append("EndCase")
            elif stype == "CONTINUE":
                lines.append("Continue")
            elif stype == "INITIALIZE":
                target = details.get("target") or normalized.removeprefix("INITIALIZE").strip().rstrip(".")
                lines.append(self._todo("Map COBOL INITIALIZE to AB Suite initialization", target, line_no))
            elif stype in {"READ", "WRITE", "OPEN", "CLOSE", "REWRITE", "DELETE", "START"}:
                target = details.get("file") or ""
                lines.append(self._todo(f"Map COBOL {stype} to AB Suite data access", target or normalized, line_no))
            elif stype == "CALL":
                target = details.get("target")
                if target and target.strip("'\"").upper() != "UNKNOWN":
                    clean_target = target.strip("'\"")
                    lines.append(self._todo("Map external COBOL CALL to AB Suite integration", clean_target, line_no))
                else:
                    lines.append(self._todo("Review external COBOL CALL manually", normalized or "CALL UNKNOWN", line_no))
            elif stype == "ARITHMETIC":
                arithmetic = self._arithmetic_to_ldl(normalized)
                lines.append(arithmetic if arithmetic else self._todo("Review COBOL arithmetic manually", normalized, line_no))
            elif stype == "EXIT":
                verb = (details.get("verb") or normalized).upper()
                lines.append("Exit" if "EXIT" in verb or "GOBACK" in verb or "STOP" in verb else self._todo("Review COBOL exit manually", normalized, line_no))
            elif normalized:
                lines.append(self._todo("Review COBOL statement manually", normalized, line_no))

        return "\n".join(lines) if lines else ": No executable statements captured in SQLite"

    def _assignment_or_move(self, source: str, destination: str) -> str:
        src = self._expression_to_ldl(source)
        dst = self._expression_to_ldl(destination)
        if self._is_group_like(source) or self._is_group_like(destination):
            return f"Move {src} {dst}"
        return f"{dst} := {src}"

    @staticmethod
    def _move_operands(details: Dict[str, Any], normalized: str) -> Tuple[str, str]:
        src = details.get("source")
        dst = details.get("destination")
        if src and dst:
            return str(src), str(dst)
        match = re.match(r"^\s*MOVE\s+(.+?)\s+TO\s+(.+?)\.?\s*$", normalized, flags=re.IGNORECASE)
        if not match:
            return "", ""
        return match.group(1).strip(), match.group(2).strip()

    @staticmethod
    def _perform_target(normalized: str) -> str:
        match = re.match(r"^\s*PERFORM\s+(.+?)\.?\s*$", normalized, flags=re.IGNORECASE)
        return match.group(1).strip() if match else ""

    @staticmethod
    def _if_condition(normalized: str) -> str:
        match = re.match(r"^\s*IF\s+(.+?)\.?\s*$", normalized, flags=re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def _arithmetic_to_ldl(self, normalized: str) -> str:
        text = normalized.strip().rstrip(".")
        patterns = [
            (
                r"^ADD\s+(.+?)\s+TO\s+(.+?)\s+GIVING\s+(.+)$",
                lambda m: f"{self._expression_to_ldl(m.group(3))} := {self._expression_to_ldl(m.group(2))} + {self._expression_to_ldl(m.group(1))}",
            ),
            (
                r"^ADD\s+(.+?)\s+TO\s+(.+)$",
                lambda m: f"{self._expression_to_ldl(m.group(2))} := {self._expression_to_ldl(m.group(2))} + {self._expression_to_ldl(m.group(1))}",
            ),
            (
                r"^SUBTRACT\s+(.+?)\s+FROM\s+(.+?)\s+GIVING\s+(.+)$",
                lambda m: f"{self._expression_to_ldl(m.group(3))} := {self._expression_to_ldl(m.group(2))} - {self._expression_to_ldl(m.group(1))}",
            ),
            (
                r"^SUBTRACT\s+(.+?)\s+FROM\s+(.+)$",
                lambda m: f"{self._expression_to_ldl(m.group(2))} := {self._expression_to_ldl(m.group(2))} - {self._expression_to_ldl(m.group(1))}",
            ),
            (
                r"^MULTIPLY\s+(.+?)\s+BY\s+(.+?)\s+GIVING\s+(.+)$",
                lambda m: f"{self._expression_to_ldl(m.group(3))} := {self._expression_to_ldl(m.group(1))} * {self._expression_to_ldl(m.group(2))}",
            ),
            (
                r"^DIVIDE\s+(.+?)\s+BY\s+(.+?)\s+GIVING\s+(.+)$",
                lambda m: f"{self._expression_to_ldl(m.group(3))} := {self._expression_to_ldl(m.group(1))} / {self._expression_to_ldl(m.group(2))}",
            ),
            (
                r"^COMPUTE\s+(.+?)\s*=\s*(.+)$",
                lambda m: f"{self._expression_to_ldl(m.group(1))} := {self._expression_to_ldl(m.group(2))}",
            ),
        ]
        for pattern, renderer in patterns:
            match = re.match(pattern, text, flags=re.IGNORECASE)
            if match:
                return renderer(match)
        return ""

    @staticmethod
    def _json_dict(value: Optional[str]) -> Dict[str, Any]:
        if not value:
            return {}
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}

    def _set_class_defaults(self, elem: etree.Element, stereotype: str = "NoStereotype", dimensions: str = "1") -> None:
        elem.set("Stereotype", stereotype)
        elem.set("Primitive", "AsClass")
        elem.set("Inherits", ZERO_GUID)
        elem.set("Dimensions", dimensions)
        elem.set("IsAbstract", "No")
        elem.set("IsExternal", "No")
        elem.set("IsInner", "No")
        elem.set("IsSynchronous", "Yes")
        elem.set("RSNCapable", "No")
        elem.set("MemberPersistence", "No")
        elem.set("DateFormat", "UK")
        elem.set("MemberVisibility", "Private")
        elem.set("BaseYear", "1957")
        elem.set("CenturyStartYear", "0")
        elem.set("RefreshScreen", "Yes")
        elem.set("DateCompareSetGLBCentury", "No")
        elem.set("AllowPurge", "No")
        elem.set("PrintIfPresent", "No")
        elem.set("HasMaint", "No")
        elem.set("CurrencySign", "36")
        elem.set("PresentationType", "None")
        elem.set("DefaultDevice", "Object::LinePrinter")
        elem.set("EventSet", ZERO_GUID)
        elem.set("LockSign", "No")
        elem.set("StandardHeading", "Yes")
        elem.set("LineSpacing", "Single")
        elem.set("VideoCapable", "No")
        elem.set("ReportParameter", ZERO_GUID)
        elem.set("MaintProfile", ZERO_GUID)
        elem.set("IsCopied", "No")
        elem.set("LeftFillNumerics", "No")

    def _set_attribute_defaults(self, elem: etree.Element) -> None:
        elem.set("Inherits", ZERO_GUID)
        elem.set("Template", f"{ZERO_GUID},NONE")
        elem.set("Dimensions", "1")
        elem.set("Semantics", "EAESemantics")
        elem.set("IsConstant", "No")
        elem.set("IsPersistent", "No")
        elem.set("RSNCapable", "No")
        elem.set("DateFormat", "UK")
        elem.set("Direction", "InOut")
        elem.set("NOFOrder", "2147483647")
        elem.set("NOFType", "Minus")
        elem.set("NOFLength", "0")
        elem.set("BaseYear", "1957")
        elem.set("CenturyStartYear", "0")
        elem.set("RefreshScreen", "Yes")
        elem.set("DateCompareSetGLBCentury", "No")
        elem.set("AllowPurge", "No")
        elem.set("PrintIfPresent", "No")
        elem.set("HasMaint", "No")
        elem.set("CurrencySign", "36")
        elem.set("DefaultDevice", "Object::LinePrinter")
        elem.set("EventSet", ZERO_GUID)
        elem.set("LockSign", "No")
        elem.set("StandardHeading", "Yes")
        elem.set("LineSpacing", "Single")
        elem.set("VideoCapable", "No")
        elem.set("ReportParameter", ZERO_GUID)
        elem.set("MaintProfile", ZERO_GUID)
        elem.set("IsCopied", "No")
        elem.set("LeftFillNumerics", "No")

    def _new_id(self) -> str:
        self._id_counter += 1
        return f"ID_NewElement{self._id_counter}"

    def _unique_name(self, base: str) -> str:
        base = base or "UnnamedElement"
        count = self._used_names.get(base, 0)
        self._used_names[base] = count + 1
        if count == 0:
            return base
        return f"{base}_{count + 1}"

    @staticmethod
    def _clean_name(name: Any) -> str:
        cleaned = str(name or "UnnamedElement").strip().rstrip(".").replace("-", "_")
        cleaned = re.sub(r"[^A-Za-z0-9_]", "_", cleaned)
        cleaned = re.sub(r"_+", "_", cleaned).strip("_")
        if not cleaned:
            cleaned = "UnnamedElement"
        if cleaned[0].isdigit():
            cleaned = f"P_{cleaned}"
        return cleaned[:128]

    def _ldl_name(self, value: str) -> str:
        value = str(value).strip().rstrip(".")
        if value.startswith(("'", '"')) or value.isnumeric():
            return value
        upper = value.upper()
        if upper in {"ZERO", "ZEROS", "ZEROES"}:
            return "GLB.ZEROS"
        if upper in {"SPACE", "SPACES"}:
            return "GLB.SPACES"
        return self._clean_name(value)

    def _expression_to_ldl(self, value: str) -> str:
        expression = str(value).strip().rstrip(".")
        expression = re.sub(r"\bZEROES?\b|\bZEROS\b", "GLB.ZEROS", expression, flags=re.IGNORECASE)
        expression = re.sub(r"\bSPACES?\b", "GLB.SPACES", expression, flags=re.IGNORECASE)
        expression = re.sub(r"(?<=[A-Za-z0-9_])-(?=[A-Za-z0-9_])", "_", expression)
        expression = re.sub(r"\b([A-Za-z][A-Za-z0-9_]*)\(([^()]*)\)", r"\1[\2]", expression)
        return expression

    def _display_expression_to_ldl(self, value: str) -> str:
        expression = self._expression_to_ldl(value)
        return re.sub(
            r"((?:'[^']*'|\"[^\"]*\"))\s+([A-Za-z][A-Za-z0-9_\[\], ]*)$",
            r"\1 & \2",
            expression,
        )

    @staticmethod
    def _is_group_like(value: str) -> bool:
        text = str(value).upper()
        return any(token in text for token in ("-REC", "-RECORD", " RECORD", " GROUP"))

    def _condition_to_ldl(self, value: str) -> str:
        condition = str(value).strip().rstrip(".")
        condition = re.sub(r"\bEQUAL\s+TO\b", "=", condition, flags=re.IGNORECASE)
        condition = re.sub(r"\bNOT\s+EQUAL\s+TO\b", "<>", condition, flags=re.IGNORECASE)
        condition = re.sub(r"\bNOT\s*=", "<>", condition, flags=re.IGNORECASE)
        condition = re.sub(r"\bGREATER\s+THAN\b", ">", condition, flags=re.IGNORECASE)
        condition = re.sub(r"\bLESS\s+THAN\b", "<", condition, flags=re.IGNORECASE)
        condition = re.sub(r"\bZEROS?\b|\bZEROES\b", "GLB.ZEROS", condition, flags=re.IGNORECASE)
        condition = re.sub(r"\bSPACES?\b", "GLB.SPACES", condition, flags=re.IGNORECASE)
        condition = re.sub(r"(?<=[A-Za-z0-9_])-(?=[A-Za-z0-9_])", "_", condition)
        condition = re.sub(r"\b([A-Za-z][A-Za-z0-9_]*)\(([^()]*)\)", r"\1[\2]", condition)
        return condition

    def _negated_condition_to_ldl(self, value: str) -> str:
        condition = self._condition_to_ldl(value)
        replacements = [
            (" <> ", " = "),
            (" <= ", " > "),
            (" >= ", " < "),
            (" = ", " <> "),
            (" < ", " >= "),
            (" > ", " <= "),
        ]
        for old, new in replacements:
            if old in condition:
                return condition.replace(old, new, 1)
        return f"NOT ({condition})"

    @staticmethod
    def _comment(text: str, line_no: Optional[int]) -> str:
        prefix = f": line {line_no}: " if line_no else ": "
        return prefix + (text or "statement not captured")

    def _todo(self, action: str, detail: str, line_no: Optional[int]) -> str:
        payload = f"TODO {action}"
        if detail:
            payload += f" ({detail})"
        return self._comment(payload, line_no)

    @staticmethod
    def _dedupe_fields(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        result = []
        for row in rows:
            key = (
                row.get("section"),
                row.get("name") or row.get("field_name"),
                row.get("parent_name"),
                row.get("line_number"),
            )
            if key in seen:
                continue
            seen.add(key)
            result.append(row)
        return result

    @staticmethod
    def _file_records_as_data_items(file_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        rows = []
        for row in file_records:
            item = dict(row)
            item["name"] = row.get("field_name") or row.get("record_name")
            item["section"] = f"FILE:{row.get('file_name') or ''}"
            rows.append(item)
        return rows

    @staticmethod
    def _picture_to_type(picture: Optional[str]) -> Tuple[str, int, int]:
        if not picture:
            return "AsClass", 1, 0
        pic = picture.upper().replace(" ", "")
        primitive = "AsString" if "X" in pic or "A" in pic else "AsSignedNumber" if "S9" in pic else "AsNumber"
        numbers = [int(n) for n in re.findall(r"\((\d+)\)", pic)]
        if numbers:
            length = sum(numbers)
        else:
            length = len(re.findall(r"[9XA]", pic))
        decimals = 0
        if "V" in pic:
            after_v = pic.split("V", 1)[1]
            dec_groups = [int(n) for n in re.findall(r"\((\d+)\)", after_v)]
            decimals = sum(dec_groups) if dec_groups else len(re.findall(r"9", after_v))
        return primitive, max(1, length), decimals

    @staticmethod
    def _format_xml(root: etree.Element) -> str:
        etree.indent(root, space="  ")
        xml_body = etree.tostring(root, encoding="unicode")
        return '<?xml version="1.0" encoding="UTF-16" standalone="yes"?>\n' + xml_body

    @staticmethod
    def _validate_xml(xml_text: str) -> None:
        body = re.sub(r"^\s*<\?xml[^?]*\?>\s*", "", xml_text)
        etree.fromstring(body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AB Suite PMODEL from SQLite knowledge graph facts.")
    parser.add_argument("--db", default="data/cobol_knowledge.db")
    parser.add_argument("--program", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = SQLitePModelGenerator(args.db).generate_program(args.program, args.output)
    print(
        json.dumps(
            {
                "program_id": result.program_id,
                "output_path": result.output_path,
                "data_objects": result.data_object_count,
                "methods": result.method_count,
                "statements": result.statement_count,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
