"""
SQLite Loader - Swimm-Style Knowledge Base
Loads ProLeap-parsed COBOL data into SQLite with full statement-level detail.
Implements graph-based module detection.
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn


class SafeConsole:
    def print(self, *args, **kwargs):
        try:
            print(*[str(arg) for arg in args])
        except Exception:
            pass


console = SafeConsole()


class SQLiteLoader:
    """Loads parsed and enriched COBOL data into SQLite knowledge base."""

    def __init__(self, db_path: str, schema_path: str = None):
        self.db_path = db_path
        self.schema_path = schema_path or "schemas/cobol_knowledge.sql"
        self.conn = None

    def connect(self):
        """Connect to the database and initialize schema."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        # check_same_thread=False so the loader can be cached across Streamlit reruns
        # (Streamlit dispatches reruns on different threads).
        db_target = Path(self.db_path).resolve().as_uri() if os.name == "nt" else self.db_path
        self.conn = sqlite3.connect(db_target, check_same_thread=False, uri=os.name == "nt")
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

        if os.path.exists(self.schema_path):
            console.print(f"[cyan]Initializing database schema...[/cyan]")
            with open(self.schema_path, 'r') as f:
                schema_sql = f.read()
            self.conn.executescript(schema_sql)
            self.conn.commit()

        # Apply any schema migrations for columns added after initial release
        self._apply_migrations()

        console.print(f"[green]OK - Connected to {self.db_path}[/green]")

    def _apply_migrations(self):
        """Add new columns to existing tables — safe to run on any DB version."""
        new_columns = [
            ("programs", "migration_complexity",          "INTEGER"),
            ("programs", "complexity_reason",             "TEXT"),
            ("programs", "modern_equivalent",             "TEXT"),
            ("programs", "suggested_service",             "TEXT"),
            ("programs", "migration_approach",            "TEXT"),
            ("programs", "data_contracts",                "TEXT"),
            ("programs", "migration_risks",               "TEXT"),
            ("programs", "dependencies_to_migrate_first", "TEXT"),
            ("generated_docs", "context_metadata_json",   "TEXT"),
            ("generated_docs", "coverage_ledger_json",    "TEXT"),
            ("statements", "raw_text",                    "TEXT"),
            ("statements", "normalized_text",             "TEXT"),
        ]
        cursor = self.conn.cursor()
        for table, col, coltype in new_columns:
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {coltype}")
            except Exception:
                pass  # Column already exists — that's fine
        self.conn.commit()

        # Create generated_docs table (added for agentic doc pipeline)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generated_docs (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                mode          TEXT NOT NULL,
                subject       TEXT NOT NULL,
                document_text TEXT NOT NULL,
                context_metadata_json TEXT,
                coverage_ledger_json  TEXT,
                generated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(mode, subject)
            )
        """)

        # Create exec_cics table (EXEC CICS commands per program)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exec_cics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                command TEXT NOT NULL,
                paragraph_name TEXT,
                line_number INTEGER,
                details_json TEXT,
                FOREIGN KEY (program_id) REFERENCES programs(program_id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_exec_cics_program ON exec_cics(program_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_exec_cics_command ON exec_cics(command)")

        # Create exec_sql table (EXEC SQL DB2 statements per program)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exec_sql (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                command TEXT NOT NULL,
                table_name TEXT,
                cursor_name TEXT,
                paragraph_name TEXT,
                line_number INTEGER,
                sql_text TEXT,
                FOREIGN KEY (program_id) REFERENCES programs(program_id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_exec_sql_program ON exec_sql(program_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_exec_sql_command ON exec_sql(command)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_exec_sql_table   ON exec_sql(table_name)")

        # Create ims_calls table (IMS DL/I CALL 'CBLTDLI' statements per program)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ims_calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                function_code TEXT NOT NULL,
                function_name TEXT,
                pcb_name TEXT,
                segment_area TEXT,
                ssa_name TEXT,
                ssa_segment TEXT,
                ssa_qualifier TEXT,
                paragraph_name TEXT,
                line_number INTEGER,
                raw_text TEXT,
                FOREIGN KEY (program_id) REFERENCES programs(program_id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ims_calls_program ON ims_calls(program_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ims_calls_function ON ims_calls(function_code)")

        # copybook_fields — field-level dictionary for each copybook
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS copybook_fields (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                copybook_name TEXT NOT NULL,
                field_name TEXT NOT NULL,
                level_number INTEGER,
                picture TEXT,
                usage TEXT,
                value TEXT,
                parent_name TEXT,
                line_number INTEGER,
                occurs_count INTEGER,
                redefines_target TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_copybook_fields_name ON copybook_fields(copybook_name)")

        # file_records — FD record layouts per program
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                file_name TEXT NOT NULL,
                record_name TEXT,
                field_name TEXT,
                level_number INTEGER,
                picture TEXT,
                usage TEXT,
                parent_name TEXT,
                line_number INTEGER
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_records_program ON file_records(program_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_records_file ON file_records(file_name)")

        # data_movements — MOVE source -> destination (data lineage)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                source_field TEXT NOT NULL,
                destination_field TEXT NOT NULL,
                paragraph_name TEXT,
                line_number INTEGER,
                is_literal INTEGER DEFAULT 0
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_data_movements_program ON data_movements(program_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_data_movements_source ON data_movements(source_field)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_data_movements_dest ON data_movements(destination_field)")

        # code_anomalies — static-analysis findings (bugs, dead code, mismatches)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS code_anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                severity TEXT NOT NULL,
                category TEXT NOT NULL,
                rule_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                paragraph_name TEXT,
                line_number INTEGER,
                snippet TEXT,
                suggestion TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_code_anomalies_program ON code_anomalies(program_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_code_anomalies_severity ON code_anomalies(severity)")

        # mq_calls — IBM MQ API usage per program
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mq_calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                function_code TEXT NOT NULL,
                function_name TEXT,
                queue_name TEXT,
                queue_manager TEXT,
                object_descriptor TEXT,
                message_descriptor TEXT,
                options_area TEXT,
                paragraph_name TEXT,
                line_number INTEGER,
                raw_text TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mq_calls_program ON mq_calls(program_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mq_calls_function ON mq_calls(function_code)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mq_calls_queue ON mq_calls(queue_name)")

        # evaluate_branches — EVALUATE / WHEN decision tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluate_branches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                evaluate_id TEXT NOT NULL,
                subject TEXT,
                branch_index INTEGER,
                when_condition TEXT,
                action_summary TEXT,
                paragraph_name TEXT,
                line_number INTEGER,
                is_default INTEGER DEFAULT 0
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_evaluate_branches_program ON evaluate_branches(program_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_evaluate_branches_eval ON evaluate_branches(evaluate_id)")

        # cics_handles — EXEC CICS HANDLE CONDITION/AID/ABEND routing
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cics_handles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                handle_type TEXT NOT NULL,
                condition_name TEXT NOT NULL,
                target_paragraph TEXT,
                paragraph_name TEXT,
                line_number INTEGER
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cics_handles_program ON cics_handles(program_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cics_handles_target ON cics_handles(target_paragraph)")

        # program_parameters — PROCEDURE DIVISION USING ... (linkage-section parameters)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS program_parameters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                position INTEGER,
                parameter_name TEXT NOT NULL,
                source TEXT,                  -- "PROCEDURE DIVISION USING" or "ENTRY USING"
                line_number INTEGER
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_program_parameters_program ON program_parameters(program_id)")

        # file_operations — every OPEN/CLOSE with mode (INPUT/OUTPUT/I-O/EXTEND)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_id TEXT NOT NULL,
                file_name TEXT NOT NULL,
                operation TEXT NOT NULL,      -- OPEN | CLOSE
                mode TEXT,                    -- INPUT | OUTPUT | I-O | EXTEND  (NULL for CLOSE)
                paragraph_name TEXT,
                line_number INTEGER
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_ops_program ON file_operations(program_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_ops_file ON file_operations(file_name)")

        # Add resolved_target column to program_calls (dynamic CALL resolution)
        try:
            cursor.execute("ALTER TABLE program_calls ADD COLUMN resolved_target TEXT")
        except Exception:
            pass

        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    # ================================================================
    # Internal Helpers
    # ================================================================

    def _recreate_fts_triggers(self, cursor):
        """Re-create FTS sync triggers after bulk load."""
        triggers = [
            """CREATE TRIGGER IF NOT EXISTS programs_ai AFTER INSERT ON programs BEGIN
                INSERT INTO programs_fts(rowid, program_id, business_name, business_purpose)
                VALUES (NEW.id, NEW.program_id, NEW.business_name, NEW.business_purpose);
            END""",
            """CREATE TRIGGER IF NOT EXISTS programs_ad AFTER DELETE ON programs BEGIN
                INSERT INTO programs_fts(programs_fts, rowid, program_id, business_name, business_purpose)
                VALUES ('delete', OLD.id, OLD.program_id, OLD.business_name, OLD.business_purpose);
            END""",
            """CREATE TRIGGER IF NOT EXISTS programs_au AFTER UPDATE ON programs BEGIN
                INSERT INTO programs_fts(programs_fts, rowid, program_id, business_name, business_purpose)
                VALUES ('delete', OLD.id, OLD.program_id, OLD.business_name, OLD.business_purpose);
                INSERT INTO programs_fts(rowid, program_id, business_name, business_purpose)
                VALUES (NEW.id, NEW.program_id, NEW.business_name, NEW.business_purpose);
            END""",
            """CREATE TRIGGER IF NOT EXISTS data_items_ai AFTER INSERT ON data_items BEGIN
                INSERT INTO data_items_fts(rowid, name, business_name, description)
                VALUES (NEW.id, NEW.name, NEW.business_name, NEW.description);
            END""",
            """CREATE TRIGGER IF NOT EXISTS business_rules_ai AFTER INSERT ON business_rules BEGIN
                INSERT INTO business_rules_fts(rowid, rule_name, rule_statement, condition_text, action_text)
                VALUES (NEW.id, NEW.rule_name, NEW.rule_statement, NEW.condition_text, NEW.action_text);
            END""",
        ]
        for sql in triggers:
            try:
                cursor.execute(sql)
            except:
                pass

    # ================================================================
    # Loading Methods
    # ================================================================

    def update_business_context(self, program_id, data):
        """Specifically update business context fields for a program."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE programs SET
                business_name = ?,
                business_purpose = ?,
                user_role = ?,
                business_process = ?
            WHERE program_id = ?
        """, (
            data.get("business_name"),
            data.get("business_purpose"),
            data.get("user_role"),
            data.get("business_process"),
            program_id
        ))
        self.conn.commit()

    def update_paragraph_narratives(self, program_id, paragraphs):
        """Specifically update narrative fields for paragraphs."""
        cursor = self.conn.cursor()
        for p in paragraphs:
            cursor.execute("""
                UPDATE paragraphs SET
                    business_name = ?,
                    narrative = ?,
                    purpose = ?
                WHERE program_id = ? AND paragraph_name = ?
            """, (
                p.get("business_name"),
                p.get("narrative"),
                p.get("purpose"),
                program_id,
                p.get("name")
            ))
        self.conn.commit()

    def load_programs(self, programs: List[Dict]):
        """Load program data including statements, calls, performs, CICS."""
        cursor = self.conn.cursor()

        # Drop FTS triggers temporarily for bulk load performance
        for trig in ["programs_ai", "programs_ad", "programs_au",
                      "data_items_ai", "business_rules_ai"]:
            try:
                cursor.execute(f"DROP TRIGGER IF EXISTS {trig}")
            except:
                pass
        # Disable foreign keys during bulk load for performance
        cursor.execute("PRAGMA foreign_keys = OFF")
        self.conn.commit()

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                       BarColumn(), console=console) as progress:
            task = progress.add_task("Loading programs...", total=len(programs))

            for program in programs:
                try:
                    program_id = program.get("program_id")

                    # Serialize list/dict fields to JSON text for storage
                    def _to_str(val):
                        if val is None:
                            return None
                        if isinstance(val, (list, dict)):
                            return json.dumps(val)
                        return val
                    deps_json = json.dumps(program.get("dependencies_to_migrate_first") or [])
                    data_contracts = _to_str(program.get("data_contracts"))
                    migration_risks = _to_str(program.get("migration_risks"))
                    migration_approach = _to_str(program.get("migration_approach"))

                    # Insert/replace program
                    cursor.execute("""
                        INSERT OR REPLACE INTO programs (
                            program_id, file_path, file_hash, program_type, line_count,
                            business_name, business_purpose, user_role, business_process,
                            migration_complexity, complexity_reason, modern_equivalent,
                            suggested_service, migration_approach, data_contracts,
                            migration_risks, dependencies_to_migrate_first,
                            updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        program_id,
                        program.get("file_path"),
                        program.get("file_hash"),
                        program.get("program_type"),
                        program.get("line_count"),
                        program.get("business_name"),
                        program.get("business_purpose"),
                        program.get("user_role"),
                        program.get("business_process"),
                        program.get("migration_complexity"),
                        program.get("complexity_reason"),
                        program.get("modern_equivalent"),
                        program.get("suggested_service"),
                        migration_approach,
                        data_contracts,
                        migration_risks,
                        deps_json,
                        datetime.now().isoformat()
                    ))

                    # Clear old data for this program
                    for table in ["paragraphs", "data_items", "files", "statements",
                                  "performs", "copybook_usage", "exec_cics", "exec_sql",
                                  "ims_calls", "file_records", "data_movements",
                                  "code_anomalies", "mq_calls", "evaluate_branches",
                                  "cics_handles", "program_parameters", "file_operations"]:
                        cursor.execute(f"DELETE FROM {table} WHERE program_id = ?", (program_id,))
                    # program_calls uses caller_program, not program_id
                    cursor.execute("DELETE FROM program_calls WHERE caller_program = ?", (program_id,))

                    source_ranges = self._source_paragraph_ranges(
                        program.get("file_path"), program.get("paragraphs", [])
                    )

                    def _source_paragraph_for_line(line_num):
                        try:
                            line_num = int(line_num or 0)
                        except Exception:
                            return None
                        for pname, (start, end) in source_ranges.items():
                            if start <= line_num <= end:
                                return pname
                        return None

                    # Insert paragraphs. Always re-extract from source so line
                    # numbers match the current file (ProLeap output may be stale
                    # if the source has been edited since parsing). Fall back to
                    # ProLeap-supplied paragraphs only when source extraction
                    # returns nothing.
                    parsed_paras = program.get("paragraphs", []) or []
                    if program.get("file_path"):
                        try:
                            fresh = self._extract_paragraphs_from_source(program["file_path"])
                        except Exception:
                            fresh = []
                        if fresh:
                            # If ProLeap had paragraphs but they're stale, prefer fresh.
                            # If counts roughly match, keep ProLeap's enriched fields
                            # (business_name, narrative) by name-matching back into fresh.
                            by_name = {(p.get("name") or "").upper(): p for p in parsed_paras}
                            merged = []
                            for f in fresh:
                                old = by_name.get((f.get("name") or "").upper(), {})
                                merged.append({
                                    "name": f["name"],
                                    "line_start": f["line_start"],
                                    "line_end": f["line_end"],
                                    "business_name": old.get("business_name"),
                                    "narrative": old.get("narrative"),
                                    "purpose": old.get("purpose"),
                                })
                            parsed_paras = merged
                            program["paragraphs"] = merged

                    for para in parsed_paras:
                        para_name = para.get("name")
                        source_start, source_end = source_ranges.get(
                            (para_name or "").upper(),
                            (para.get("line_start"), para.get("line_end")),
                        )
                        cursor.execute("""
                            INSERT OR REPLACE INTO paragraphs (
                                program_id, paragraph_name, line_start, line_end,
                                business_name, narrative, purpose
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            program_id,
                            para_name,
                            source_start,
                            source_end,
                            para.get("business_name"),
                            para.get("narrative"),
                            para.get("purpose")
                        ))

                    # Insert data items
                    for item in program.get("data_items", []):
                        cursor.execute("""
                            INSERT OR REPLACE INTO data_items (
                                program_id, name, level_number, picture, usage, value,
                                section, parent_name, line_number,
                                business_name, description, data_type_description
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            program_id,
                            item.get("name"),
                            item.get("level_number"),
                            item.get("picture"),
                            item.get("usage"),
                            item.get("value"),
                            item.get("section"),
                            item.get("parent_name"),
                            item.get("line_number"),
                            item.get("business_name"),
                            item.get("description"),
                            item.get("data_type_description")
                        ))

                    # Insert files
                    for f in program.get("files", []):
                        cursor.execute("""
                            INSERT OR REPLACE INTO files (
                                program_id, file_name, file_type, organization,
                                access_mode, record_name, business_name, description
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            program_id, f.get("file_name"), f.get("file_type"),
                            f.get("organization"), f.get("access_mode"),
                            f.get("record_name"), f.get("business_name"), f.get("description")
                        ))

                    # Insert ALL statements (new: this was empty before)
                    for stmt in program.get("statements", []):
                        details = {k: v for k, v in stmt.items()
                                   if k not in (
                                       "type", "line", "line_end", "paragraph",
                                       "raw_text", "normalized_text", "source_code"
                                   )}
                        stmt_para = _source_paragraph_for_line(stmt.get("line")) or stmt.get("paragraph")
                        cursor.execute("""
                            INSERT OR REPLACE INTO statements (
                                program_id, paragraph_name, statement_type,
                                line_number, details_json, raw_text, normalized_text
                            ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            program_id,
                            stmt_para,
                            stmt.get("type"),
                            stmt.get("line"),
                            json.dumps(details) if details else None,
                            stmt.get("raw_text") or stmt.get("source_code"),
                            stmt.get("normalized_text"),
                        ))

                    # Insert calls
                    for call in program.get("calls", []):
                        cursor.execute("""
                            INSERT OR REPLACE INTO program_calls (
                                caller_program, called_program, call_location, line_number
                            ) VALUES (?, ?, ?, ?)
                        """, (
                            program_id,
                            call.get("called_program"),
                            call.get("call_location"),
                            call.get("line_number")
                        ))

                    # Insert performs
                    for perf in program.get("performs", []):
                        source_para = _source_paragraph_for_line(perf.get("line_number")) or perf.get("source_paragraph", "MAIN")
                        cursor.execute("""
                            INSERT OR REPLACE INTO performs (
                                program_id, source_paragraph, target_paragraph,
                                perform_type, line_number, condition
                            ) VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            program_id,
                            source_para,
                            perf.get("target_paragraph"),
                            perf.get("perform_type", "SIMPLE"),
                            perf.get("line_number"),
                            perf.get("condition")
                        ))

                    # Insert copybook usage
                    for cb in program.get("copybooks", []):
                        cursor.execute("INSERT OR IGNORE INTO copybooks (copybook_name) VALUES (?)", (cb,))
                        cursor.execute("""
                            INSERT OR REPLACE INTO copybook_usage (program_id, copybook_name) VALUES (?, ?)
                        """, (program_id, cb))

                    # Insert EXEC CICS commands
                    # If ProLeap gave all UNKNOWN commands, extract from source
                    cics_list = program.get("exec_cics", [])
                    all_unknown = cics_list and all(
                        c.get("command", "UNKNOWN") == "UNKNOWN" for c in cics_list
                    )
                    if all_unknown and program.get("file_path"):
                        cics_list = self._extract_cics_from_source(
                            program["file_path"], program.get("paragraphs", [])
                        )

                    for cics in cics_list:
                        details = {k: v for k, v in cics.items()
                                   if k not in ("command", "line_number", "paragraph")}
                        cursor.execute("""
                            INSERT INTO exec_cics (
                                program_id, command, paragraph_name,
                                line_number, details_json
                            ) VALUES (?, ?, ?, ?, ?)
                        """, (
                            program_id,
                            cics.get("command", "UNKNOWN"),
                            cics.get("paragraph"),
                            cics.get("line_number"),
                            json.dumps(details) if details else None
                        ))

                    # Insert EXEC SQL (DB2) commands — extracted from source
                    if program.get("file_path"):
                        sql_list = self._extract_sql_from_source(
                            program["file_path"], program.get("paragraphs", [])
                        )
                        for s in sql_list:
                            cursor.execute("""
                                INSERT INTO exec_sql (
                                    program_id, command, table_name, cursor_name,
                                    paragraph_name, line_number, sql_text
                                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (
                                program_id,
                                s.get("command", "UNKNOWN"),
                                s.get("table_name"),
                                s.get("cursor_name"),
                                s.get("paragraph"),
                                s.get("line_number"),
                                s.get("sql_text"),
                            ))

                    # Resolve dynamic CALLs by reading source. Insert resolved
                    # calls as NEW program_calls rows — we can't trust ProLeap's
                    # line numbers (parsed JSON may be stale relative to source).
                    if program.get("file_path"):
                        try:
                            resolutions = self._resolve_dynamic_calls_from_source(
                                program["file_path"], program.get("paragraphs", [])
                            )
                            for res in resolutions:
                                # Skip if a row already exists for the same caller+target
                                cursor.execute("""
                                    SELECT 1 FROM program_calls
                                    WHERE caller_program = ?
                                      AND (called_program = ? OR resolved_target = ?)
                                """, (program_id, res["resolved_target"], res["resolved_target"]))
                                if cursor.fetchone():
                                    continue
                                cursor.execute("""
                                    INSERT INTO program_calls (
                                        caller_program, called_program,
                                        call_location, line_number,
                                        resolved_target
                                    ) VALUES (?, 'UNKNOWN', ?, ?, ?)
                                """, (
                                    program_id,
                                    res.get("paragraph"),
                                    res.get("line_number"),
                                    res["resolved_target"],
                                ))
                        except Exception:
                            pass

                    # Insert IMS DL/I calls — extracted from source
                    if program.get("file_path"):
                        ims_list = self._extract_ims_from_source(
                            program["file_path"], program.get("paragraphs", []),
                            program.get("data_items", [])
                        )
                        for im in ims_list:
                            cursor.execute("""
                                INSERT INTO ims_calls (
                                    program_id, function_code, function_name,
                                    pcb_name, segment_area, ssa_name,
                                    ssa_segment, ssa_qualifier,
                                    paragraph_name, line_number, raw_text
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                program_id,
                                im.get("function_code", "UNKNOWN"),
                                im.get("function_name"),
                                im.get("pcb_name"),
                                im.get("segment_area"),
                                im.get("ssa_name"),
                                im.get("ssa_segment"),
                                im.get("ssa_qualifier"),
                                im.get("paragraph"),
                                im.get("line_number"),
                                im.get("raw_text"),
                            ))

                    # Insert SELECT/ASSIGN-derived file declarations
                    if program.get("file_path"):
                        try:
                            file_decls = self._extract_files_from_source(program["file_path"])
                            for f in file_decls:
                                cursor.execute("""
                                    INSERT INTO files (
                                        program_id, file_name, file_type,
                                        organization, access_mode, record_name
                                    ) VALUES (?, ?, ?, ?, ?, ?)
                                """, (
                                    program_id,
                                    f.get("file_name"),
                                    f.get("file_type"),
                                    f.get("organization"),
                                    f.get("access_mode"),
                                    f.get("record_key"),
                                ))
                        except Exception as _f_err:
                            console.print(f"[yellow]  files extraction failed for {program_id}: {_f_err}[/yellow]")

                    # Insert FD record layouts — extracted from source
                    if program.get("file_path"):
                        try:
                            fd_records = self._extract_file_records_from_source(program["file_path"])
                            for r in fd_records:
                                cursor.execute("""
                                    INSERT INTO file_records (
                                        program_id, file_name, record_name, field_name,
                                        level_number, picture, usage, parent_name, line_number
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    program_id,
                                    r.get("file_name"),
                                    r.get("record_name"),
                                    r.get("field_name"),
                                    r.get("level_number"),
                                    r.get("picture"),
                                    r.get("usage"),
                                    r.get("parent_name"),
                                    r.get("line_number"),
                                ))
                        except Exception as _fd_err:
                            console.print(f"[yellow]  FD extraction failed for {program_id}: {_fd_err}[/yellow]")

                    # Insert MOVE-based data lineage — extracted from source
                    if program.get("file_path"):
                        try:
                            moves = self._extract_movements_from_source(
                                program["file_path"], program.get("paragraphs", [])
                            )
                            for mv in moves:
                                cursor.execute("""
                                    INSERT INTO data_movements (
                                        program_id, source_field, destination_field,
                                        paragraph_name, line_number, is_literal
                                    ) VALUES (?, ?, ?, ?, ?, ?)
                                """, (
                                    program_id,
                                    mv.get("source_field"),
                                    mv.get("destination_field"),
                                    mv.get("paragraph"),
                                    mv.get("line_number"),
                                    mv.get("is_literal", 0),
                                ))
                        except Exception as _mv_err:
                            console.print(f"[yellow]  MOVE extraction failed for {program_id}: {_mv_err}[/yellow]")

                    # Source-side fallback for I/O statements + IF conditions.
                    # Only inserts when a row with the same line+type doesn't exist,
                    # so we never overwrite ProLeap output that's already populated.
                    if program.get("file_path"):
                        try:
                            io_stmts = self._extract_statement_sources_from_source(
                                program["file_path"], program.get("paragraphs", [])
                            )
                            for s in io_stmts:
                                details_json = json.dumps(s.get("details", {})) if s.get("details") else None

                                # Enrich an existing parser row with source text/details.
                                cursor.execute("""
                                    UPDATE statements
                                    SET raw_text = COALESCE(raw_text, ?),
                                        normalized_text = COALESCE(normalized_text, ?),
                                        paragraph_name = COALESCE(paragraph_name, ?),
                                        details_json = CASE
                                            WHEN details_json IS NULL OR details_json IN ('{}', '')
                                            THEN ?
                                            ELSE details_json
                                        END
                                    WHERE program_id = ? AND line_number = ? AND statement_type = ?
                                """, (
                                    s.get("raw_text"),
                                    s.get("normalized_text"),
                                    s.get("paragraph"),
                                    details_json,
                                    program_id,
                                    s["line_number"],
                                    s["type"],
                                ))
                                if cursor.rowcount:
                                    continue

                                cursor.execute("""
                                    INSERT INTO statements (
                                        program_id, paragraph_name, statement_type,
                                        line_number, details_json, raw_text, normalized_text
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    program_id,
                                    s.get("paragraph"),
                                    s["type"],
                                    s["line_number"],
                                    details_json,
                                    s.get("raw_text"),
                                    s.get("normalized_text"),
                                ))
                        except Exception as _io_err:
                            console.print(f"[yellow]  source statement extraction failed for {program_id}: {_io_err}[/yellow]")

                    # Static analysis: detect bugs, dead code, naming mismatches
                    if program.get("file_path"):
                        try:
                            anomalies = self._detect_code_anomalies(
                                program["file_path"], program_id, program.get("paragraphs", [])
                            )
                            for a in anomalies:
                                cursor.execute("""
                                    INSERT INTO code_anomalies (
                                        program_id, severity, category, rule_id,
                                        title, description, paragraph_name,
                                        line_number, snippet, suggestion
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    program_id,
                                    a.get("severity"),
                                    a.get("category"),
                                    a.get("rule_id"),
                                    a.get("title"),
                                    a.get("description"),
                                    a.get("paragraph_name"),
                                    a.get("line_number"),
                                    a.get("snippet"),
                                    a.get("suggestion"),
                                ))
                        except Exception as _ca_err:
                            console.print(f"[yellow]  anomaly detection failed for {program_id}: {_ca_err}[/yellow]")

                    # IBM MQ API calls
                    if program.get("file_path"):
                        try:
                            mq = self._extract_mq_calls_from_source(
                                program["file_path"], program.get("paragraphs", []),
                                program.get("data_items", []),
                            )
                            for m in mq:
                                cursor.execute("""
                                    INSERT INTO mq_calls (
                                        program_id, function_code, function_name,
                                        queue_name, queue_manager, object_descriptor,
                                        message_descriptor, options_area,
                                        paragraph_name, line_number, raw_text
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    program_id,
                                    m.get("function_code"),
                                    m.get("function_name"),
                                    m.get("queue_name"),
                                    m.get("queue_manager"),
                                    m.get("object_descriptor"),
                                    m.get("message_descriptor"),
                                    m.get("options_area"),
                                    m.get("paragraph"),
                                    m.get("line_number"),
                                    m.get("raw_text"),
                                ))
                        except Exception as _mq_err:
                            console.print(f"[yellow]  MQ extraction failed for {program_id}: {_mq_err}[/yellow]")

                    # EVALUATE / WHEN branches
                    if program.get("file_path"):
                        try:
                            evals = self._extract_evaluate_branches_from_source(
                                program["file_path"], program.get("paragraphs", []),
                            )
                            for e in evals:
                                cursor.execute("""
                                    INSERT INTO evaluate_branches (
                                        program_id, evaluate_id, subject, branch_index,
                                        when_condition, action_summary,
                                        paragraph_name, line_number, is_default
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    program_id,
                                    e.get("evaluate_id"),
                                    e.get("subject"),
                                    e.get("branch_index"),
                                    e.get("when_condition"),
                                    e.get("action_summary"),
                                    e.get("paragraph"),
                                    e.get("line_number"),
                                    e.get("is_default", 0),
                                ))
                        except Exception as _ev_err:
                            console.print(f"[yellow]  EVALUATE extraction failed for {program_id}: {_ev_err}[/yellow]")

                    # CICS HANDLE CONDITION routing
                    if program.get("file_path"):
                        try:
                            handles = self._extract_cics_handles_from_source(
                                program["file_path"], program.get("paragraphs", []),
                            )
                            for h in handles:
                                cursor.execute("""
                                    INSERT INTO cics_handles (
                                        program_id, handle_type, condition_name,
                                        target_paragraph, paragraph_name, line_number
                                    ) VALUES (?, ?, ?, ?, ?, ?)
                                """, (
                                    program_id,
                                    h.get("handle_type"),
                                    h.get("condition_name"),
                                    h.get("target_paragraph"),
                                    h.get("paragraph_name"),
                                    h.get("line_number"),
                                ))
                        except Exception as _h_err:
                            console.print(f"[yellow]  CICS HANDLE extraction failed for {program_id}: {_h_err}[/yellow]")

                    # PROCEDURE DIVISION USING / ENTRY USING parameters
                    if program.get("file_path"):
                        try:
                            params = self._extract_program_parameters_from_source(program["file_path"])
                            for pp in params:
                                cursor.execute("""
                                    INSERT INTO program_parameters (
                                        program_id, position, parameter_name,
                                        source, line_number
                                    ) VALUES (?, ?, ?, ?, ?)
                                """, (
                                    program_id,
                                    pp.get("position"),
                                    pp.get("parameter_name"),
                                    pp.get("source"),
                                    pp.get("line_number"),
                                ))
                        except Exception as _pp_err:
                            console.print(f"[yellow]  PROCEDURE USING extraction failed for {program_id}: {_pp_err}[/yellow]")

                    # OPEN/CLOSE with explicit modes
                    if program.get("file_path"):
                        try:
                            ops = self._extract_file_operations_from_source(
                                program["file_path"], program.get("paragraphs", [])
                            )
                            for op in ops:
                                cursor.execute("""
                                    INSERT INTO file_operations (
                                        program_id, file_name, operation, mode,
                                        paragraph_name, line_number
                                    ) VALUES (?, ?, ?, ?, ?, ?)
                                """, (
                                    program_id,
                                    op.get("file_name"),
                                    op.get("operation"),
                                    op.get("mode"),
                                    op.get("paragraph"),
                                    op.get("line_number"),
                                ))
                        except Exception as _op_err:
                            console.print(f"[yellow]  file-op extraction failed for {program_id}: {_op_err}[/yellow]")

                except Exception as e:
                    import traceback
                    console.print(f"[yellow]Warning: Error loading {program.get('program_id')}: {e}[/yellow]")
                    traceback.print_exc()

                progress.advance(task)

        # Re-enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        self.conn.commit()

        # Rebuild FTS indexes from content tables
        try:
            cursor.execute("INSERT INTO programs_fts(programs_fts) VALUES('rebuild')")
            cursor.execute("INSERT INTO data_items_fts(data_items_fts) VALUES('rebuild')")
            cursor.execute("INSERT INTO business_rules_fts(business_rules_fts) VALUES('rebuild')")
            self.conn.commit()
        except Exception as e:
            console.print(f"[yellow]Warning: FTS rebuild: {e}[/yellow]")

        # Re-create FTS triggers from schema
        try:
            self._recreate_fts_triggers(cursor)
            self.conn.commit()
        except Exception as e:
            console.print(f"[yellow]Warning: FTS trigger re-creation: {e}[/yellow]")

        console.print(f"[green]OK - Loaded {len(programs)} programs[/green]")

    @staticmethod
    def _source_paragraph_ranges(file_path: str, paragraphs: List[Dict]) -> Dict[str, tuple]:
        """Map paragraph names to physical source line ranges by scanning labels.

        Parser line ranges can drift after COPY expansion. Anything extracted
        directly from source should use these physical ranges for attribution.
        """
        import re
        from pathlib import Path

        src = Path(file_path or "")
        if not src.exists():
            return {}
        try:
            lines = src.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            return {}

        names = []
        for p in paragraphs or []:
            name = (p.get("name") or p.get("paragraph_name") or "").upper()
            if name:
                names.append(name)
        if not names:
            return {}

        def _body(raw_line: str) -> str:
            if len(raw_line) > 6 and raw_line[6] == "*":
                return ""
            body = raw_line[6:] if len(raw_line) > 6 else raw_line
            return body[:66] if len(body) > 66 else body

        starts = []
        for idx, raw_line in enumerate(lines, 1):
            body = _body(raw_line).strip().upper()
            for name in names:
                if re.match(rf"^{re.escape(name)}\s*\.", body):
                    starts.append((idx, name))
                    break
        starts.sort()

        ranges = {}
        for pos, (start, name) in enumerate(starts):
            end = starts[pos + 1][0] - 1 if pos + 1 < len(starts) else len(lines)
            ranges[name] = (start, end)
        return ranges

    @staticmethod
    def _resolve_dynamic_calls_from_source(file_path: str, paragraphs: List[Dict]) -> List[Dict]:
        """For each `CALL <variable>` in the source, scan backward in the same paragraph
        for the most recent `MOVE 'LITERAL' TO <variable>` and resolve the call target.
        Returns: [{line_number, paragraph, variable, resolved_target}, ...]"""
        import re
        from pathlib import Path

        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        lines = content.split("\n")

        # Strip column 1-6 sequence area + comment lines.
        # Also strip quoted string literals so we don't match "CALL" inside DISPLAY text.
        _quote_pat = re.compile(r"'[^']*'|\"[^\"]*\"")
        def _stripped(idx):
            line = lines[idx]
            if len(line) > 6 and line[6] == "*":
                return ""
            body = line[6:] if len(line) > 6 else line
            # Also strip the trailing column-73-80 sequence area if present
            if len(body) > 66:
                body = body[:66]
            # Replace any quoted literal with whitespace so it can't match keywords
            body = _quote_pat.sub(lambda m: " " * len(m.group()), body)
            return body

        source_ranges = SQLiteLoader._source_paragraph_ranges(file_path, paragraphs)

        def _find_paragraph(line_num):
            for pname, (start, end) in source_ranges.items():
                if start <= line_num <= end:
                    return {"name": pname, "line_start": start, "line_end": end}
            for p in paragraphs or []:
                start = p.get("line_start", 0)
                end = p.get("line_end", 0)
                if start and end and start <= line_num <= end:
                    return p
            return None

        # Match `CALL <bare-identifier>` (no quotes) — that's a dynamic call.
        call_var_pat = re.compile(r"\bCALL\s+([A-Z][A-Z0-9-]*)\b(?!\s*['\"])", re.IGNORECASE)
        # Match `MOVE 'literal' TO <identifier>` or `MOVE "literal" TO <identifier>`
        move_lit_pat = re.compile(
            r"\bMOVE\s+['\"]([A-Z0-9_-]+)['\"]\s+TO\s+([A-Z][A-Z0-9-]*)\b",
            re.IGNORECASE,
        )

        results = []
        for idx in range(len(lines)):
            line_num = idx + 1
            text = _stripped(idx)
            if not text or "CALL" not in text.upper():
                continue
            m = call_var_pat.search(text)
            if not m:
                continue
            var_name = m.group(1).upper()
            # Skip COBOL keywords that look like identifiers
            if var_name in ("USING", "GIVING", "RETURNING", "BY"):
                continue

            para = _find_paragraph(line_num)
            if not para:
                continue
            para_start = para.get("line_start", 1)

            # Walk backward inside the same paragraph for the latest MOVE literal TO var
            resolved = None
            for back_idx in range(idx - 1, max(para_start - 2, -1), -1):
                back_text = _stripped(back_idx)
                if not back_text:
                    continue
                for mm in move_lit_pat.finditer(back_text):
                    if mm.group(2).upper() == var_name:
                        resolved = mm.group(1).upper()
                        break
                if resolved:
                    break

            if resolved:
                results.append({
                    "line_number": line_num,
                    "paragraph": para.get("name"),
                    "variable": var_name,
                    "resolved_target": resolved,
                })

        return results

    @staticmethod
    def _extract_paragraphs_from_source(file_path: str) -> List[Dict]:
        """Fallback paragraph parser. Detects lines that look like
        `       PARAGRAPH-NAME.` (column 8+, ends with period, identifier-like)
        inside the PROCEDURE DIVISION. Returns [{name, line_start, line_end}, ...]."""
        import re
        from pathlib import Path
        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        lines = content.split("\n")

        in_proc = False
        # In COBOL, a paragraph header MUST start in Area A (columns 8-11). The
        # regex requires the name to start at column 8 (i.e. body[0] is the name's
        # first character with at most one leading space — accommodates editor tabs).
        # Names CAN start with a digit (e.g. 1400-COMPUTE-FEES).
        para_pat = re.compile(r"^\s{0,3}([A-Z0-9][A-Z0-9-]{2,30})\s*\.\s*$")
        # COBOL keywords/sections/scope-terminators that match the regex but
        # aren't paragraph names.
        skip = {
            # Section / division markers
            "PROCEDURE", "DIVISION", "SECTION", "FILE", "WORKING-STORAGE",
            "LINKAGE", "LOCAL-STORAGE", "INPUT-OUTPUT", "FILE-CONTROL",
            "I-O-CONTROL", "DATA", "ENVIRONMENT", "IDENTIFICATION",
            "CONFIGURATION", "SPECIAL-NAMES", "SOURCE-COMPUTER",
            "OBJECT-COMPUTER", "PROGRAM-ID", "AUTHOR", "DATE-WRITTEN",
            "DATE-COMPILED", "INSTALLATION", "SECURITY", "REMARKS",
            # Statement / scope terminators
            "EXIT", "STOP", "GOBACK", "CONTINUE", "END-EXEC",
            "END-IF", "END-EVALUATE", "END-PERFORM", "END-READ", "END-WRITE",
            "END-CALL", "END-SEARCH", "END-START", "END-STRING", "END-UNSTRING",
            "END-COMPUTE", "END-ADD", "END-SUBTRACT", "END-MULTIPLY", "END-DIVIDE",
            "END-RETURN", "END-RECEIVE", "END-INVOKE", "END-DELETE",
            "TRUE", "FALSE", "NULL",
        }

        paras = []
        cur_name = None
        cur_start = 0
        for i, raw in enumerate(lines):
            line_num = i + 1
            if len(raw) > 6 and raw[6] == "*":
                continue
            body = raw[6:] if len(raw) > 6 else raw
            body = body[:66] if len(body) > 66 else body
            up = body.upper()
            if "PROCEDURE DIVISION" in up:
                in_proc = True
                continue
            if not in_proc:
                continue
            m = para_pat.match(body)
            if not m:
                continue
            name = m.group(1).upper()
            if name in skip:
                continue

            # Close out previous paragraph
            if cur_name:
                paras.append({"name": cur_name, "line_start": cur_start, "line_end": line_num - 1})
            cur_name = name
            cur_start = line_num

        if cur_name:
            paras.append({"name": cur_name, "line_start": cur_start, "line_end": len(lines)})

        return paras

    @staticmethod
    def _extract_program_parameters_from_source(file_path: str) -> List[Dict]:
        """Pull `PROCEDURE DIVISION USING param1 param2 ...` and any
        `ENTRY 'name' USING ...` clauses. Each parameter becomes a row."""
        import re
        from pathlib import Path
        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        lines = content.split("\n")

        def _strip(line):
            if len(line) > 6 and line[6] == "*":
                return ""
            body = line[6:] if len(line) > 6 else line
            return body[:66] if len(body) > 66 else body

        # Collect both patterns. PROCEDURE DIVISION USING may span multiple lines.
        cleaned = [(i + 1, _strip(l)) for i, l in enumerate(lines)]
        joined_with_lines = []
        for ln, body in cleaned:
            joined_with_lines.append((ln, body))

        results = []

        # PROCEDURE DIVISION USING
        for idx, (ln, body) in enumerate(joined_with_lines):
            up = body.upper().lstrip()
            if not up.startswith("PROCEDURE DIVISION"):
                continue
            # Capture USING list — may run across lines until a period
            tail = body
            j = idx + 1
            while "." not in tail and j < len(joined_with_lines):
                tail += " " + joined_with_lines[j][1]
                j += 1
            tail = re.sub(r"\s+", " ", tail)
            m = re.search(r"USING\s+([^.]+)", tail, re.IGNORECASE)
            if m:
                names = re.findall(r"[A-Z][A-Z0-9-]*", m.group(1))
                for pos, name in enumerate(names):
                    if name.upper() in ("BY", "REFERENCE", "VALUE", "CONTENT"):
                        continue
                    results.append({
                        "position": pos,
                        "parameter_name": name.upper(),
                        "source": "PROCEDURE DIVISION USING",
                        "line_number": ln,
                    })
            break  # only one PROCEDURE DIVISION per program

        # ENTRY 'name' USING — secondary entry points (e.g. ENTRY 'DLITCBL' USING)
        for ln, body in joined_with_lines:
            m = re.search(r"\bENTRY\s+['\"][A-Z0-9-]+['\"]\s+USING\s+([^.]+)", body, re.IGNORECASE)
            if not m:
                continue
            names = re.findall(r"[A-Z][A-Z0-9-]*", m.group(1))
            for pos, name in enumerate(names):
                if name.upper() in ("BY", "REFERENCE", "VALUE", "CONTENT"):
                    continue
                results.append({
                    "position": pos,
                    "parameter_name": name.upper(),
                    "source": "ENTRY USING",
                    "line_number": ln,
                })

        return results

    @staticmethod
    def _extract_file_operations_from_source(file_path: str,
                                               paragraphs: List[Dict]) -> List[Dict]:
        """Extract OPEN/CLOSE statements with their explicit mode.
        Pattern: OPEN INPUT FILE-A FILE-B  /  OPEN OUTPUT FILE-X  /  OPEN I-O FILE-Y
                CLOSE FILE-A FILE-B"""
        import re
        from pathlib import Path
        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        lines = content.split("\n")

        def _strip(line):
            if len(line) > 6 and line[6] == "*":
                return ""
            body = line[6:] if len(line) > 6 else line
            return body[:66] if len(body) > 66 else body

        def _find_para(line_num):
            for p in paragraphs:
                start = p.get("line_start", 0)
                end = p.get("line_end", 0)
                if start and end and start <= line_num <= end:
                    return p.get("name")
            return None

        # OPEN  <mode> file [, file ...] [<mode> file ...]
        open_pat = re.compile(
            r"\bOPEN\s+(INPUT|OUTPUT|I-O|EXTEND)\s+([A-Z][A-Z0-9-]*(?:\s*,?\s*[A-Z][A-Z0-9-]*)*)",
            re.IGNORECASE,
        )
        close_pat = re.compile(r"\bCLOSE\s+([A-Z][A-Z0-9-]*(?:\s*,?\s*[A-Z][A-Z0-9-]*)*)",
                                re.IGNORECASE)

        results = []
        for i, raw in enumerate(lines):
            body = _strip(raw)
            if not body.strip():
                continue
            ln = i + 1
            # OPEN — multi-mode supported by repeated regex application
            for m in open_pat.finditer(body):
                mode = m.group(1).upper()
                files = re.split(r"[,\s]+", m.group(2).strip())
                for f in files:
                    f = f.strip(",")
                    if not f or not re.match(r"^[A-Z][A-Z0-9-]*$", f, re.IGNORECASE):
                        continue
                    # Skip COBOL keywords masquerading as filenames
                    if f.upper() in ("INPUT", "OUTPUT", "I-O", "EXTEND", "REVERSED",
                                       "WITH", "NO", "REWIND", "LOCK"):
                        continue
                    results.append({
                        "file_name": f.upper(),
                        "operation": "OPEN",
                        "mode": mode,
                        "paragraph": _find_para(ln),
                        "line_number": ln,
                    })
            # CLOSE
            for m in close_pat.finditer(body):
                files = re.split(r"[,\s]+", m.group(1).strip())
                for f in files:
                    f = f.strip(",")
                    if not f or not re.match(r"^[A-Z][A-Z0-9-]*$", f, re.IGNORECASE):
                        continue
                    if f.upper() in ("WITH", "REEL", "UNIT", "NO", "REWIND", "LOCK"):
                        continue
                    results.append({
                        "file_name": f.upper(),
                        "operation": "CLOSE",
                        "mode": None,
                        "paragraph": _find_para(ln),
                        "line_number": ln,
                    })
        return results

    @staticmethod
    def _extract_mq_calls_from_source(file_path: str, paragraphs: List[Dict],
                                       data_items: List[Dict] = None) -> List[Dict]:
        """Extract IBM MQ API calls. Pattern:
            CALL 'MQOPEN'  USING HCONN, OBJDESC, OPTIONS, HOBJ, COMPCODE, REASON
            CALL 'MQGET'   USING HCONN, HOBJ, MQMD, MQGMO, BUFLEN, BUFFER, ...
            CALL 'MQPUT'   USING HCONN, HOBJ, MQMD, MQPMO, BUFLEN, BUFFER, ...
            CALL 'MQCLOSE' USING HCONN, HOBJ, OPTIONS, COMPCODE, REASON
            CALL 'MQCONN' / 'MQDISC' / 'MQCMIT' / 'MQBACK'
        Also tries to resolve queue name by following MOVE statements that
        populate MQOD-OBJECTNAME / OBJDESC-OBJECTNAME just before the call."""
        import re
        from pathlib import Path

        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        lines = content.split("\n")

        def _strip_seq(line: str) -> str:
            if len(line) > 6 and line[6] == "*":
                return ""
            body = line[6:] if len(line) > 6 else line
            return body[:66] if len(body) > 66 else body

        def _find_paragraph(line_num):
            for p in paragraphs:
                start = p.get("line_start", 0)
                end = p.get("line_end", 0)
                if start and end and start <= line_num <= end:
                    return p.get("name")
            return None

        FUNCTIONS = {
            "MQCONN":  "Connect to queue manager",
            "MQDISC":  "Disconnect from queue manager",
            "MQOPEN":  "Open a queue or other object",
            "MQCLOSE": "Close a queue or other object",
            "MQGET":   "Read a message from a queue",
            "MQPUT":   "Write a message to a queue",
            "MQPUT1":  "Open + write + close in one call",
            "MQINQ":   "Inquire on object attributes",
            "MQSET":   "Set object attributes",
            "MQCMIT":  "Commit pending unit of work",
            "MQBACK":  "Backout pending unit of work",
            "MQSUB":   "Register a subscription",
            "MQSUBRQ": "Subscription request",
        }

        # Build call regex: CALL '<MQfunc>' USING <args>
        func_or = "|".join(FUNCTIONS.keys())
        call_pat = re.compile(
            rf"CALL\s+['\"]({func_or})['\"]\s+USING\s+([^.]+?)(?:\.|END-CALL|$)",
            re.IGNORECASE,
        )

        results = []

        # Concatenate body for multi-line CALL statements
        body_lines = []
        line_offsets = []  # cumulative chars per line -> line number
        cum = 0
        for i, raw in enumerate(lines):
            body = _strip_seq(raw)
            body_lines.append(body)
            line_offsets.append(cum)
            cum += len(body) + 1
        joined = "\n".join(body_lines)

        def _line_for_offset(off):
            # binary search would be nicer; len < 5k usually
            for ln, o in enumerate(line_offsets):
                if o > off:
                    return ln  # 1-based: ln-1 is the index, ln is the line above
            return len(line_offsets)

        for m in call_pat.finditer(joined):
            fn = m.group(1).upper()
            args_block = re.sub(r"\s+", " ", m.group(2)).strip().rstrip(",")
            args = [a.strip() for a in args_block.split(",") if a.strip()]
            line_num = _line_for_offset(m.start())
            para = _find_paragraph(line_num)

            # Argument layout: convention is HCONN, HOBJ, MQMD, MQGMO/MQPMO, ...
            # We capture the named areas we recognize.
            object_descriptor = None
            message_descriptor = None
            options_area = None
            queue_manager = None
            for a in args:
                au = a.upper()
                if "OBJDESC" in au or "MQOD" in au:
                    object_descriptor = a
                elif "MQMD" in au or "MSGDESC" in au:
                    message_descriptor = a
                elif "MQGMO" in au or "MQPMO" in au or "MQCNO" in au or au.endswith("OPTIONS"):
                    options_area = a
                elif "QMGR" in au or "QMNAME" in au or "QM-NAME" in au:
                    queue_manager = a

            # Try to resolve queue name from a recent MOVE 'QNAME' TO MQOD-OBJECTNAME
            queue_name = None
            for back in range(line_num - 1, max(0, line_num - 30), -1):
                bb = body_lines[back - 1] if back - 1 < len(body_lines) else ""
                qm = re.search(
                    r"MOVE\s+['\"]([A-Z0-9._-]+)['\"]\s+TO\s+([A-Z0-9-]*OBJECTNAME[A-Z0-9-]*|[A-Z0-9-]*Q-?NAME[A-Z0-9-]*)",
                    bb,
                    re.IGNORECASE,
                )
                if qm:
                    queue_name = qm.group(1).upper()
                    break

            results.append({
                "function_code": fn,
                "function_name": FUNCTIONS.get(fn, fn),
                "queue_name": queue_name,
                "queue_manager": queue_manager,
                "object_descriptor": object_descriptor,
                "message_descriptor": message_descriptor,
                "options_area": options_area,
                "paragraph": para,
                "line_number": line_num,
                "raw_text": m.group(0)[:300],
            })

        return results

    @staticmethod
    def _extract_evaluate_branches_from_source(file_path: str,
                                                 paragraphs: List[Dict]) -> List[Dict]:
        """Parse EVALUATE / WHEN / END-EVALUATE blocks. Each WHEN clause becomes
        one branch row. Captures the subject (what's being evaluated) and the
        condition for each branch."""
        import re
        from pathlib import Path
        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        lines = content.split("\n")

        def _strip_seq(line: str) -> str:
            if len(line) > 6 and line[6] == "*":
                return ""
            body = line[6:] if len(line) > 6 else line
            return body[:66] if len(body) > 66 else body

        def _find_paragraph(line_num):
            for p in paragraphs:
                start = p.get("line_start", 0)
                end = p.get("line_end", 0)
                if start and end and start <= line_num <= end:
                    return p.get("name")
            return None

        eval_open = re.compile(r"^\s*EVALUATE\s+(.+?)(?:\.\s*$|$)", re.IGNORECASE)
        when_pat = re.compile(r"^\s*WHEN\s+(.+?)(?:\.\s*$|$)", re.IGNORECASE)
        end_eval = re.compile(r"^\s*END-EVALUATE", re.IGNORECASE)

        results = []
        # Stack of currently-open EVALUATEs: list of dicts
        stack = []

        for i, raw in enumerate(lines):
            body = _strip_seq(raw)
            line_num = i + 1
            if not body.strip():
                continue
            up = body.strip().upper()

            m_eval = eval_open.match(body)
            if m_eval:
                subject = m_eval.group(1).strip()
                # Multi-line subject: walk forward until first WHEN
                if "WHEN" in subject.upper():
                    # split on first WHEN
                    pre, _, _ = subject.upper().partition("WHEN")
                    subject = subject[:len(pre)].strip()
                eid = f"{file_path}:{line_num}"
                stack.append({
                    "evaluate_id": eid,
                    "subject": subject,
                    "branch_index": 0,
                    "line_number": line_num,
                    "paragraph": _find_paragraph(line_num),
                    "branches": [],
                    "current_branch": None,
                })
                continue

            if not stack:
                continue

            # End of innermost EVALUATE
            if end_eval.match(body):
                evblock = stack.pop()
                # Flush current branch
                if evblock["current_branch"]:
                    evblock["branches"].append(evblock["current_branch"])
                for b in evblock["branches"]:
                    results.append({
                        "evaluate_id": evblock["evaluate_id"],
                        "subject": evblock["subject"],
                        "branch_index": b["index"],
                        "when_condition": b["condition"],
                        "action_summary": b["action"],
                        "paragraph": evblock["paragraph"],
                        "line_number": b["line_number"],
                        "is_default": 1 if b["condition"].strip().upper() in ("OTHER", "OTHER-WISE") else 0,
                    })
                continue

            current = stack[-1]
            m_when = when_pat.match(body)
            if m_when:
                # Flush previous branch
                if current["current_branch"]:
                    current["branches"].append(current["current_branch"])
                cond = m_when.group(1).strip()
                idx = current["branch_index"]
                current["branch_index"] += 1
                current["current_branch"] = {
                    "index": -1 if cond.upper().startswith("OTHER") else idx,
                    "condition": cond,
                    "action": "",
                    "line_number": line_num,
                }
                continue

            # Body inside a WHEN — capture first non-empty action line
            if current["current_branch"] and not current["current_branch"]["action"]:
                current["current_branch"]["action"] = body.strip()[:120]

        return results

    @staticmethod
    def _extract_cics_handles_from_source(file_path: str,
                                            paragraphs: List[Dict]) -> List[Dict]:
        """Extract EXEC CICS HANDLE CONDITION/AID/ABEND routing maps.
        Pattern: EXEC CICS HANDLE CONDITION ERROR(error-para) NOTFND(nf-para) END-EXEC."""
        import re
        from pathlib import Path
        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        lines = content.split("\n")

        def _strip_seq(line: str) -> str:
            if len(line) > 6 and line[6] == "*":
                return ""
            body = line[6:] if len(line) > 6 else line
            return body[:66] if len(body) > 66 else body

        def _find_paragraph(line_num):
            for p in paragraphs:
                start = p.get("line_start", 0)
                end = p.get("line_end", 0)
                if start and end and start <= line_num <= end:
                    return p.get("name")
            return None

        # Collect each EXEC CICS HANDLE block
        handle_open = re.compile(
            r"EXEC\s+CICS\s+HANDLE\s+(CONDITION|AID|ABEND)", re.IGNORECASE)

        results = []
        i = 0
        while i < len(lines):
            body = _strip_seq(lines[i])
            line_num = i + 1
            mo = handle_open.search(body)
            if not mo:
                i += 1
                continue
            handle_type = mo.group(1).upper()
            # Walk forward until END-EXEC
            block_lines = [body]
            j = i + 1
            while j < len(lines):
                bb = _strip_seq(lines[j])
                block_lines.append(bb)
                if "END-EXEC" in bb.upper():
                    break
                j += 1
            i = j + 1

            joined = re.sub(r"\s+", " ", " ".join(block_lines)).strip()
            # Strip the leading EXEC CICS HANDLE <TYPE> and trailing END-EXEC
            joined = re.sub(r"EXEC\s+CICS\s+HANDLE\s+\w+\s*", "", joined,
                             flags=re.IGNORECASE)
            joined = re.sub(r"END-EXEC\.?$", "", joined, flags=re.IGNORECASE).strip()

            # Now joined is something like: "ERROR(ERR-RTN) NOTFND(NOT-FOUND) MAPFAIL(MFAIL-RTN)"
            # Or for ABEND: "PROGRAM(my-handler)" or "LABEL(error-para)"
            cond_pat = re.compile(r"([A-Z][A-Z0-9-]*)\s*\(\s*([A-Z][A-Z0-9-]*)\s*\)",
                                   re.IGNORECASE)
            for cm in cond_pat.finditer(joined):
                results.append({
                    "handle_type": handle_type,
                    "condition_name": cm.group(1).upper(),
                    "target_paragraph": cm.group(2).upper(),
                    "paragraph_name": _find_paragraph(line_num),
                    "line_number": line_num,
                })

            # Bare conditions without parens mean SUSPEND/restore (no routing target)
            # e.g. "EXEC CICS HANDLE CONDITION ERROR END-EXEC" → routing back to default
            for word in re.findall(r"\b([A-Z][A-Z0-9-]+)\b", joined):
                if word.upper() in ("AND", "OR"): continue
                # Already captured above if inside parens
                if f"{word}(" in joined.replace(" ", ""):
                    continue
                # Skip noise
                if word in ("END", "EXEC"): continue
                results.append({
                    "handle_type": handle_type,
                    "condition_name": word.upper(),
                    "target_paragraph": None,  # cancels prior handler
                    "paragraph_name": _find_paragraph(line_num),
                    "line_number": line_num,
                })

        # Dedupe — same (program, condition, target, line)
        seen = set()
        unique = []
        for r in results:
            key = (r["handle_type"], r["condition_name"], r["target_paragraph"], r["line_number"])
            if key in seen:
                continue
            seen.add(key)
            unique.append(r)
        return unique

    @staticmethod
    def _extract_statement_sources_from_source(file_path: str, paragraphs: List[Dict]) -> List[Dict]:
        """Extract source-grounded executable statements for conversion/regeneration.

        This pass is additive to parser output. It keeps raw COBOL text and a
        normalized column-body version so downstream generators such as PMODEL
        do not need to re-open individual source files.
        """
        import re
        from pathlib import Path
        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        lines = content.split("\n")

        def _strip_seq(line: str) -> str:
            if len(line) > 6 and line[6] == "*":
                return ""
            body = line[6:] if len(line) > 6 else line
            return body[:66] if len(body) > 66 else body

        def _find_paragraph(line_num):
            for p in paragraphs:
                start = p.get("line_start", 0) or p.get("start_line", 0)
                end = p.get("line_end", 0) or p.get("end_line", 0)
                if start and end and start <= line_num <= end:
                    return p.get("name") or p.get("paragraph_name")
            return None

        # Statement patterns. Each captures the key operand when possible.
        io_patterns = [
            ("READ",     re.compile(r"^\s*READ\s+([A-Z][A-Z0-9-]*)", re.IGNORECASE)),
            ("WRITE",    re.compile(r"^\s*WRITE\s+([A-Z][A-Z0-9-]*)", re.IGNORECASE)),
            ("REWRITE",  re.compile(r"^\s*REWRITE\s+([A-Z][A-Z0-9-]*)", re.IGNORECASE)),
            ("DELETE",   re.compile(r"^\s*DELETE\s+([A-Z][A-Z0-9-]*)", re.IGNORECASE)),
            ("START",    re.compile(r"^\s*START\s+([A-Z][A-Z0-9-]*)", re.IGNORECASE)),
            ("OPEN",     re.compile(r"^\s*OPEN\s+(?:INPUT|OUTPUT|I-O|EXTEND)?\s*([A-Z][A-Z0-9-,\s]*)", re.IGNORECASE)),
            ("CLOSE",    re.compile(r"^\s*CLOSE\s+([A-Z][A-Z0-9-,\s]*)", re.IGNORECASE)),
        ]
        move_pat = re.compile(r"^\s*MOVE\s+(.+?)\s+TO\s+(.+?)(?:\.|\s*$)", re.IGNORECASE)
        display_pat = re.compile(r"^\s*DISPLAY\s+(.+?)(?:\.|\s*$)", re.IGNORECASE)
        perform_pat = re.compile(r"^\s*PERFORM\s+(.+?)(?:\.|\s*$)", re.IGNORECASE)
        call_pat = re.compile(r"^\s*CALL\s+(.+?)(?:\s+USING\s+(.+?))?(?:\.|\s*$)", re.IGNORECASE)
        eval_pat = re.compile(r"^\s*EVALUATE\s+(.+?)(?:\.|\s*$)", re.IGNORECASE)
        when_pat = re.compile(r"^\s*WHEN\s+(.+?)(?:\.|\s*$)", re.IGNORECASE)
        arithmetic_pat = re.compile(r"^\s*(ADD|SUBTRACT|MULTIPLY|DIVIDE|COMPUTE)\s+(.+?)(?:\.|\s*$)", re.IGNORECASE)
        if_pat = re.compile(r"^\s*IF\s+(.+)$", re.IGNORECASE)
        else_pat = re.compile(r"^\s*ELSE\b", re.IGNORECASE)
        end_if_pat = re.compile(r"^\s*END-IF\b", re.IGNORECASE)
        end_perform_pat = re.compile(r"^\s*END-PERFORM\b", re.IGNORECASE)
        end_evaluate_pat = re.compile(r"^\s*END-EVALUATE\b", re.IGNORECASE)
        continue_pat = re.compile(r"^\s*CONTINUE\b", re.IGNORECASE)
        initialize_pat = re.compile(r"^\s*INITIALIZE\s+(.+?)(?:\.|\s*$)", re.IGNORECASE)
        exit_pat = re.compile(r"^\s*(EXIT|STOP\s+RUN|GOBACK)\b", re.IGNORECASE)

        results = []
        in_proc = False
        for i, raw in enumerate(lines):
            body = _strip_seq(raw)
            if not body.strip():
                continue
            up = body.upper()
            if "PROCEDURE DIVISION" in up:
                in_proc = True
                continue
            if not in_proc:
                continue

            line_num = i + 1
            para = _find_paragraph(line_num)
            normalized = body.strip()

            def _row(stype: str, details: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    "type": stype,
                    "paragraph": para,
                    "line_number": line_num,
                    "details": details,
                    "raw_text": raw.rstrip("\r\n"),
                    "normalized_text": normalized,
                }

            # I/O statements
            matched = False
            for stype, pat in io_patterns:
                m = pat.match(body)
                if not m:
                    continue
                target = m.group(1).strip().split(",")[0].split()[0]
                results.append(_row(stype, {"file": target.upper()}))
                matched = True
                break
            if matched:
                continue

            mmove = move_pat.match(body)
            if mmove:
                results.append(_row("MOVE", {
                    "source": mmove.group(1).strip(),
                    "destination": mmove.group(2).strip(),
                }))
                continue

            mdisplay = display_pat.match(body)
            if mdisplay:
                results.append(_row("DISPLAY", {"content": mdisplay.group(1).strip()}))
                continue

            mperform = perform_pat.match(body)
            if mperform:
                results.append(_row("PERFORM", {"target": mperform.group(1).strip()}))
                continue

            mcall = call_pat.match(body)
            if mcall:
                details = {"target": mcall.group(1).strip()}
                if mcall.group(2):
                    details["using"] = mcall.group(2).strip()
                results.append(_row("CALL", details))
                continue

            meval = eval_pat.match(body)
            if meval:
                results.append(_row("EVALUATE", {"subject": meval.group(1).strip()}))
                continue

            mwhen = when_pat.match(body)
            if mwhen:
                results.append(_row("WHEN", {"condition": mwhen.group(1).strip()}))
                continue

            marith = arithmetic_pat.match(body)
            if marith:
                results.append(_row("ARITHMETIC", {
                    "verb": marith.group(1).upper(),
                    "expression": marith.group(2).strip(),
                }))
                continue

            mexit = exit_pat.match(body)
            if mexit:
                results.append(_row("EXIT", {"verb": mexit.group(1).upper()}))
                continue

            # IF condition (single-line capture; multi-line conditions get the first line)
            mif = if_pat.match(body)
            if mif:
                cond = mif.group(1).strip().rstrip(".")
                # Trim trailing words that look like a statement on the same line
                cond_short = cond[:160]
                results.append(_row("IF", {"condition": cond_short}))
                continue

            if else_pat.match(body):
                results.append(_row("ELSE", {}))
                continue

            if end_if_pat.match(body):
                results.append(_row("END-IF", {}))
                continue

            if end_perform_pat.match(body):
                results.append(_row("END-PERFORM", {}))
                continue

            if end_evaluate_pat.match(body):
                results.append(_row("END-EVALUATE", {}))
                continue

            if continue_pat.match(body):
                results.append(_row("CONTINUE", {}))
                continue

            minitialize = initialize_pat.match(body)
            if minitialize:
                results.append(_row("INITIALIZE", {"target": minitialize.group(1).strip()}))

        return results

    @staticmethod
    def _extract_io_statements_from_source(file_path: str, paragraphs: List[Dict]) -> List[Dict]:
        """Backward-compatible wrapper for older callers."""
        wanted = {"READ", "WRITE", "OPEN", "CLOSE", "REWRITE", "DELETE", "START", "IF"}
        return [
            row for row in SQLiteLoader._extract_statement_sources_from_source(file_path, paragraphs)
            if row.get("type") in wanted
        ]

    @staticmethod
    def _detect_code_anomalies(file_path: str, program_id: str,
                                paragraphs: List[Dict]) -> List[Dict]:
        """Static analysis pass that detects suspicious or buggy COBOL patterns.
        Returns a list of dicts ready to insert into code_anomalies."""
        import re
        from pathlib import Path
        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        lines = content.split("\n")

        def _strip_seq(line: str) -> str:
            if len(line) > 6 and line[6] == "*":
                return ""
            body = line[6:] if len(line) > 6 else line
            return body[:66] if len(body) > 66 else body

        def _find_paragraph(line_num):
            for p in paragraphs:
                start = p.get("line_start", 0)
                end = p.get("line_end", 0)
                if start and end and start <= line_num <= end:
                    return p.get("name")
            return None

        def _snippet(line_num, before=1, after=1):
            lo = max(0, line_num - 1 - before)
            hi = min(len(lines), line_num + after)
            return "\n".join(lines[lo:hi]).strip()

        anomalies = []

        # ── 1. Duplicate AND/OR condition: `X op Y AND X op Y` (likely typo) ─
        # Catches things like `IF PA-APPROVED <= 0 AND PA-APPROVED <= 0`
        cond_pat = re.compile(
            r"\b([A-Z][A-Z0-9-]*)\s*(=|<>|<=|>=|<|>|EQUAL|NOT EQUAL|GREATER|LESS)\s*"
            r"([A-Z0-9'\"-]+)\s+(AND|OR)\s+\1\s*\2\s*\3\b",
            re.IGNORECASE,
        )
        for i, raw in enumerate(lines):
            body = _strip_seq(raw)
            if not body:
                continue
            m = cond_pat.search(body)
            if m:
                anomalies.append({
                    "severity": "BUG",
                    "category": "LOGIC",
                    "rule_id": "DUPLICATE_AND_CONDITION",
                    "title": f"Duplicate condition in {m.group(4).upper()} clause",
                    "description": (
                        f"The condition `{m.group(1)} {m.group(2)} {m.group(3)}` is "
                        f"checked twice with `{m.group(4).upper()}` between them. "
                        f"This is almost certainly a typo where one side was meant to "
                        f"reference a different variable (e.g. DECLINED instead of APPROVED)."
                    ),
                    "paragraph_name": _find_paragraph(i + 1),
                    "line_number": i + 1,
                    "snippet": _snippet(i + 1),
                    "suggestion": "Verify the intended second condition with the source-of-truth spec; the most common cause is a copy-paste of the first variable.",
                })

        # ── 2. WS-PGMNAME literal that doesn't match the program's PROGRAM-ID ─
        # Flags `MOVE 'OLDNAME' TO WS-PGMNAME.` when OLDNAME != program_id
        pgm_lit_pat = re.compile(
            r"MOVE\s+['\"]([A-Z0-9-]+)['\"]\s+TO\s+WS-PGMNAME",
            re.IGNORECASE,
        )
        # Also handle  05 WS-PGMNAME PIC X(8) VALUE 'OLDNAME'.
        pgm_value_pat = re.compile(
            r"\bWS-PGMNAME\b[^.\n]*\bVALUE\s+['\"]([A-Z0-9-]+)['\"]",
            re.IGNORECASE,
        )
        for i, raw in enumerate(lines):
            body = _strip_seq(raw)
            if not body:
                continue
            for pat in (pgm_lit_pat, pgm_value_pat):
                m = pat.search(body)
                if not m:
                    continue
                literal = m.group(1).upper()
                if literal != program_id.upper():
                    anomalies.append({
                        "severity": "WARNING",
                        "category": "NAMING",
                        "rule_id": "PGMNAME_MISMATCH",
                        "title": "WS-PGMNAME literal does not match the actual PROGRAM-ID",
                        "description": (
                            f"The program identifier is `{program_id}` but the source sets "
                            f"`WS-PGMNAME` to `'{literal}'`. This is misleading for debug "
                            f"traces, runtime logs, and audit records that key off "
                            f"WS-PGMNAME."
                        ),
                        "paragraph_name": _find_paragraph(i + 1),
                        "line_number": i + 1,
                        "snippet": body.strip(),
                        "suggestion": (
                            f"Update the literal to '{program_id}' or rename the program "
                            f"to '{literal}' depending on which is canonical."
                        ),
                    })
                    break

        # ── 3. Period-inside-IF (premature termination of IF block) ──────────
        # COBOL pattern: `IF cond ... PERFORM thing.` — the period inside
        # closes the IF and the next statement runs unconditionally.
        # Heuristic: line starts with IF, contains no END-IF or ELSE before period,
        # and period appears mid-statement (not just at end).
        if_open_pat = re.compile(r"^\s*IF\b", re.IGNORECASE)
        end_if_in_block = re.compile(r"\bEND-IF\b|\bELSE\b", re.IGNORECASE)
        period_inside_pat = re.compile(r"\.\s+\w")
        for i, raw in enumerate(lines):
            body = _strip_seq(raw)
            if not body or not if_open_pat.match(body):
                continue
            # Walk forward up to 8 lines or until a period-end or END-IF
            block = body
            found_endif = False
            depth = 1
            for j in range(i + 1, min(i + 10, len(lines))):
                next_body = _strip_seq(lines[j])
                if not next_body:
                    continue
                block += " " + next_body
                if end_if_in_block.search(next_body):
                    found_endif = True
                    break
                if next_body.rstrip().endswith("."):
                    break
            if not found_endif and period_inside_pat.search(block):
                # only flag when there's a non-trivial mid-block period
                # AND no END-IF closes it
                anomalies.append({
                    "severity": "WARNING",
                    "category": "LOGIC",
                    "rule_id": "MISSING_END_IF",
                    "title": "IF block likely terminated by a period instead of END-IF",
                    "description": (
                        "An `IF` statement appears to be closed by a period mid-block "
                        "rather than an explicit `END-IF`/`ELSE`. Statements that look "
                        "nested in the IF may actually run unconditionally. This pattern "
                        "frequently masks a real conditional bug."
                    ),
                    "paragraph_name": _find_paragraph(i + 1),
                    "line_number": i + 1,
                    "snippet": _snippet(i + 1, before=0, after=4),
                    "suggestion": (
                        "Add an explicit END-IF and re-check that the statements after "
                        "the period are intentionally unconditional."
                    ),
                })

        # ── 4. Unused VAR (declared with VALUE but never referenced) ────────
        # Look for 01/05/77 declarations and check if name appears elsewhere.
        decl_pat = re.compile(
            r"^\s*(?:01|05|77)\s+([A-Z][A-Z0-9-]*)\s+PIC\b",
            re.IGNORECASE,
        )
        decls = {}  # name -> line
        for i, raw in enumerate(lines):
            body = _strip_seq(raw)
            if not body:
                continue
            m = decl_pat.match(body)
            if m:
                name = m.group(1).upper()
                if name not in ("FILLER",):
                    decls[name] = i + 1

        # Build a single concatenated body without comments to count refs
        whole = " ".join(_strip_seq(l) for l in lines).upper()
        for name, decl_line in decls.items():
            # Count case-insensitive occurrences. A real declaration counts as 1.
            count = whole.count(name)
            if count <= 1:  # only the declaration itself
                anomalies.append({
                    "severity": "NOTICE",
                    "category": "DEAD_CODE",
                    "rule_id": "UNUSED_VARIABLE",
                    "title": f"Variable `{name}` is declared but never referenced",
                    "description": (
                        f"`{name}` is declared at line {decl_line} but no other "
                        f"statement reads or writes it. Likely a leftover from prior "
                        f"refactoring or an incomplete feature."
                    ),
                    "paragraph_name": None,
                    "line_number": decl_line,
                    "snippet": lines[decl_line - 1].strip() if decl_line - 1 < len(lines) else "",
                    "suggestion": "Remove the declaration or wire it into the logic that was originally intended.",
                })

        # ── 5. STUB / UNIMPLEMENTED paragraphs ───────────────────────────────
        # Pattern: a paragraph whose body is essentially empty (only EXIT / STOP
        # / GOBACK or a "TBD"-style comment) signals an unimplemented feature.
        # Exception: COBOL convention puts an empty `<NAME>-EXIT` paragraph at
        # the end of every routine to anchor PERFORM ... THRU. Skip those.
        for p in paragraphs:
            pname = p.get("name") or ""
            ps = p.get("line_start", 0)
            pe = p.get("line_end", 0)
            if not (pname and ps and pe):
                continue
            # Skip conventional exit paragraphs — they're idiomatic, not stubs.
            up_name = pname.upper()
            if up_name.endswith("-EXIT") or up_name in ("9999-GOBACK", "GOBACK", "EXIT-PROGRAM"):
                continue
            body_lines = lines[ps:pe]   # exclusive of the header line itself
            real_lines = []
            tbd_marker = False
            for raw in body_lines:
                if len(raw) > 6 and raw[6] == "*":
                    if re.search(r"\b(TO\s+BE\s+IMPLEMENTED|TBD|TODO|NOT\s+IMPLEMENTED|STUB)\b",
                                  raw, re.IGNORECASE):
                        tbd_marker = True
                    continue
                txt = raw[6:] if len(raw) > 6 else raw
                stripped = txt.strip().rstrip(".").strip()
                if not stripped:
                    continue
                up = stripped.upper()
                if up in ("EXIT", "STOP RUN", "STOP", "GOBACK"):
                    continue
                real_lines.append(stripped)
            if not real_lines:
                anomalies.append({
                    "severity": "NOTICE",
                    "category": "INCOMPLETE",
                    "rule_id": "STUB_PARAGRAPH",
                    "title": f"Paragraph `{pname}` is a stub" + (" (TBD comment present)" if tbd_marker else ""),
                    "description": (
                        f"`{pname}` contains no executable statements other than "
                        f"EXIT/STOP/GOBACK. The migration team should treat this as "
                        f"an UNIMPLEMENTED FEATURE and surface it on the migration "
                        f"backlog."
                    ),
                    "paragraph_name": pname,
                    "line_number": ps,
                    "snippet": "\n".join(body_lines[:6]).strip(),
                    "suggestion": "Confirm whether this is intentionally empty (placeholder for future feature) or whether the implementation was lost during refactoring.",
                })

        # ── 6. MISLEADING DISPLAY message near OPEN of a different file ──────
        # Pattern: OPEN <FILE-A> ... DISPLAY 'ERROR OPENING <FILE-B>'
        # where FILE-B is an ACTUAL file declared in this program (so we know
        # the message really references the wrong file, not just descriptive
        # English text like "TRANSACTION CATEGORY BALANCE").
        open_pat = re.compile(
            r"\bOPEN\s+(?:INPUT|OUTPUT|I-O|EXTEND)\s+([A-Z][A-Z0-9-]+)",
            re.IGNORECASE,
        )
        display_pat = re.compile(r"\bDISPLAY\s+['\"]([^'\"]{3,120})['\"]", re.IGNORECASE)

        # First pass: collect every file declared in this program (from SELECT/OPEN)
        all_files_in_program = set()
        for raw in lines:
            if len(raw) > 6 and raw[6] == "*":
                continue
            body = raw[6:] if len(raw) > 6 else raw
            for mm in open_pat.finditer(body):
                all_files_in_program.add(mm.group(1).upper())
            sm = re.search(r"\bSELECT\s+([A-Z][A-Z0-9-]+)", body, re.IGNORECASE)
            if sm:
                all_files_in_program.add(sm.group(1).upper())

        for p in paragraphs:
            ps = p.get("line_start", 0)
            pe = p.get("line_end", 0)
            if not (ps and pe):
                continue
            block_lines = lines[ps - 1:pe]
            opened = None
            for raw in block_lines:
                if len(raw) > 6 and raw[6] == "*":
                    continue
                body = raw[6:] if len(raw) > 6 else raw
                mo = open_pat.search(body)
                if mo:
                    opened = mo.group(1).upper()
                md = display_pat.search(body)
                if not (md and opened):
                    continue
                msg = md.group(1).upper()

                # Look for ANOTHER file name from this program inside the message.
                # We require a real file-name match — descriptive English like
                # "TRANSACTION CATEGORY BALANCE" won't trip the warning.
                # Strategy A: message names ANOTHER file from this program
                wrong_file = None
                for fname in all_files_in_program:
                    if fname == opened:
                        continue
                    stem = re.sub(r"-?(FILE|FILES|REJECTS)$", "", fname).strip("-")
                    if not stem or len(stem) < 3:
                        continue
                    if re.search(rf"\b{re.escape(stem)}(?:[-\s]+(?:FILE|REJECTS))?\b",
                                  msg, re.IGNORECASE):
                        wrong_file = fname
                        break

                # Strategy B: "ERROR OPENING <X> FILE" pattern but the opened
                # file's stem doesn't appear anywhere in <X>. Catches cases
                # where the message names a fictional file that doesn't exist
                # in this program at all (e.g. 'DALY REJECTS FILE' inside a
                # DISCGRP-FILE opener — DALY/DAILY/REJECTS aren't related to
                # DISCGRP).
                if not wrong_file:
                    open_msg_pat = re.search(
                        r"\b(?:ERROR\s+(?:OPEN|OPENING)|UNABLE\s+TO\s+OPEN|FAILED\s+TO\s+OPEN|CANNOT\s+OPEN)\b\s*([A-Z][A-Z0-9\s-]{2,40}?)\s+FILE\b",
                        msg, re.IGNORECASE,
                    )
                    if open_msg_pat:
                        # The "X" mentioned in the message
                        named_in_msg = open_msg_pat.group(1).strip()
                        # Strip the file-name stems (and common synonyms)
                        opened_stem = re.sub(r"-?(FILE|FILES|REJECTS)$", "", opened).strip("-")
                        # Build a set of variants for the opened file
                        variants = {opened_stem}
                        # Split on dashes too: DISCGRP-FILE → DISCGRP, DISC, GRP
                        for piece in re.split(r"-", opened_stem):
                            if len(piece) >= 3:
                                variants.add(piece)
                        # Common abbreviation expansions (small dictionary —
                        # fully generic, no app-specific names).
                        synonyms = {
                            "DISC": ["DISCOUNT"], "DISCGRP": ["DISCOUNT", "DISCOUNT GROUP"],
                            "ACCT": ["ACCOUNT"], "ACCTFILE": ["ACCOUNT"],
                            "TRAN": ["TRANSACTION"], "TRANSACT": ["TRANSACTION"],
                            "XREF": ["CROSS REFERENCE", "CROSS REF", "CROSSREF"],
                            "CUST": ["CUSTOMER"], "TCAT": ["TRANSACTION CATEGORY"],
                            "TCATBAL": ["TRANSACTION CATEGORY BALANCE"],
                            "REPT": ["REPORT"], "USR": ["USER"],
                            "BAL": ["BALANCE"], "MSTR": ["MASTER"],
                        }
                        expanded = set(variants)
                        for v in list(variants):
                            for syn in synonyms.get(v, []):
                                expanded.add(syn)
                        # Check if ANY variant appears in the message text.
                        named_upper = named_in_msg.upper()
                        if not any(v.upper() in named_upper for v in expanded):
                            anomalies.append({
                                "severity": "WARNING",
                                "category": "NAMING",
                                "rule_id": "MISLEADING_ERROR_MESSAGE",
                                "title": (
                                    f"DISPLAY message in `{p.get('name')}` says "
                                    f"\"{named_in_msg}\" but the OPEN is on `{opened}`"
                                ),
                                "description": (
                                    f"The error message refers to a file name that "
                                    f"doesn't match the file being opened. Operators "
                                    f"reading the log will look for the wrong file "
                                    f"during incident triage."
                                ),
                                "paragraph_name": p.get("name"),
                                "line_number": ps,
                                "snippet": body.strip(),
                                "suggestion": f"Update the DISPLAY string to mention `{opened}`.",
                            })
                            break

                if not wrong_file:
                    continue

                anomalies.append({
                    "severity": "WARNING",
                    "category": "NAMING",
                    "rule_id": "MISLEADING_ERROR_MESSAGE",
                    "title": (
                        f"DISPLAY message in `{p.get('name')}` references "
                        f"`{wrong_file}` but the OPEN was on `{opened}`"
                    ),
                    "description": (
                        f"Copy-paste bug: the error message displayed when "
                        f"`{opened}` fails to open will mention `{wrong_file}` "
                        f"instead — both are real files in this program. "
                        f"This will mislead operators during incident triage."
                    ),
                    "paragraph_name": p.get("name"),
                    "line_number": ps,
                    "snippet": body.strip(),
                    "suggestion": f"Update the DISPLAY string to reference `{opened}` instead of `{wrong_file}`.",
                })
                break

        # ── 7. BUSINESS FORMULA — division by 12 / 100 / 360 / 365 / 1200 etc. ──
        # These literals encode real business semantics. Capture the FULL formula
        # so the doc can quote it verbatim instead of saying "not detailed".
        # Two patterns:
        #   (a) `(<expr>) / NNN`  →  full parenthesised expression on left
        #   (b) `COMPUTE X = <expr> / NNN`  → COMPUTE form
        formula_pat = re.compile(
            r"\(([^)]{3,80})\)\s*/\s*(\d{2,6})\b"
            r"|COMPUTE\s+\S+\s*=\s*([^./\n]{3,80})\s*/\s*(\d{2,6})\b",
            re.IGNORECASE,
        )
        seen_magic = set()
        for i, raw in enumerate(lines):
            if len(raw) > 6 and raw[6] == "*":
                continue
            body = raw[6:] if len(raw) > 6 else raw
            if "/" not in body:
                continue
            for m in formula_pat.finditer(body):
                expr = (m.group(1) or m.group(3) or "").strip()
                val = m.group(2) or m.group(4)
                if not val:
                    continue
                key = (i + 1, val, expr)
                if key in seen_magic:
                    continue
                seen_magic.add(key)
                para = None
                for p in paragraphs:
                    ps = p.get("line_start", 0)
                    pe = p.get("line_end", 0)
                    if ps and pe and ps <= i + 1 <= pe:
                        para = p.get("name")
                        break
                interp = {
                    "12":   "annual → monthly conversion (÷12)",
                    "100":  "percent → decimal conversion (÷100)",
                    "360":  "360-day banking year",
                    "365":  "365-day calendar year",
                    "1000": "milli/1000 conversion",
                    "1200": "annual percentage rate → monthly decimal (combines ÷100 percent-to-decimal AND ÷12 annual-to-monthly)",
                    "10000": "basis-points → decimal",
                    "360000": "annual basis-points → daily decimal (×100 × 360)",
                }.get(val)
                # Build a clear formula label for the title
                formula_str = f"({expr}) / {val}"
                anomalies.append({
                    "severity": "WARNING" if val == "1200" else "NOTICE",
                    "category": "LOGIC",
                    "rule_id": "BUSINESS_FORMULA",
                    "title": f"Business formula: `{formula_str}`" + (f" — {interp}" if interp else ""),
                    "description": (
                        f"This formula is a business-rule calculation that MUST be "
                        f"preserved in the modern implementation. Document it verbatim "
                        f"in the Business Rules section of the doc — do not say "
                        f"\"specific formula not detailed\". Verbatim source line: "
                        f"`{body.strip()}`"
                        + (f"\n\nInterpretation: {interp}." if interp else "")
                    ),
                    "paragraph_name": para,
                    "line_number": i + 1,
                    "snippet": body.strip(),
                    "suggestion": (
                        "Replace the literal with a named constant in the modern code "
                        "and add a comment explaining the conversion. Quote the formula "
                        "verbatim in the documentation's Business Rules section."
                    ),
                })

        # ── 8. ABEND / TERMINATION — paragraphs that end the program on error ──
        # When a paragraph PERFORM 9999-ABEND-PROGRAM (or STOP RUN) on a status
        # check, the program TERMINATES — it does not "reject" or "skip" the
        # record. Surface this so docs use accurate language.
        abend_pat = re.compile(
            r"\bPERFORM\s+(?:[A-Z0-9][A-Z0-9-]*ABEND[A-Z0-9-]*)\b"
            r"|\bSTOP\s+RUN\b",
            re.IGNORECASE,
        )
        for p in paragraphs:
            ps = p.get("line_start", 0)
            pe = p.get("line_end", 0)
            if not (ps and pe):
                continue
            block = " ".join(
                (l[6:] if len(l) > 6 else l)
                for l in lines[ps - 1:pe]
                if not (len(l) > 6 and l[6] == "*")
            )
            if not abend_pat.search(block):
                continue
            anomalies.append({
                "severity": "NOTICE",
                "category": "LOGIC",
                "rule_id": "ABEND_TERMINATION",
                "title": f"Paragraph `{p.get('name')}` terminates the program on error",
                "description": (
                    f"`{p.get('name')}` calls an ABEND routine (or STOP RUN) on the "
                    f"failure path. This means an error here ENDS the entire program — "
                    f"it does NOT reject, skip, or log-and-continue. Documentation "
                    f"must use \"abend\" / \"terminate\" language, not \"reject\"."
                ),
                "paragraph_name": p.get("name"),
                "line_number": ps,
                "snippet": "",
                "suggestion": "Use ‘abend’ or ‘terminates the program’ when describing the error path of this paragraph.",
            })

        # ── 9a. UNCONDITIONAL_FOLLOW — PERFORM A then PERFORM B (no IF guard) ──
        # When two PERFORMs appear back-to-back in the same paragraph WITHOUT
        # an IF guard between them, the second always runs even if the first
        # encountered an error. This is a common bug pattern in COBOL where a
        # programmer expected the first to "return early" but it doesn't.
        #
        # We flag specifically the case `PERFORM <READ-or-fetch>` followed by
        # `PERFORM <DELETE-or-update>` because that's the highest-risk variant.
        for p in paragraphs:
            ps = p.get("line_start", 0)
            pe = p.get("line_end", 0)
            if not (ps and pe):
                continue
            block_lines = lines[ps - 1:pe]
            performs_in_para = []
            for k, raw in enumerate(block_lines):
                if len(raw) > 6 and raw[6] == "*":
                    continue
                body = raw[6:] if len(raw) > 6 else raw
                m = re.match(r"\s*PERFORM\s+([A-Z0-9][A-Z0-9-]*)", body, re.IGNORECASE)
                if m:
                    performs_in_para.append((k, m.group(1).upper(), body.strip()))
            # Look for adjacent (or near-adjacent) READ/FETCH then DELETE/UPDATE/WRITE pairs
            for i_p in range(len(performs_in_para) - 1):
                k1, name1, _ = performs_in_para[i_p]
                k2, name2, _ = performs_in_para[i_p + 1]
                # Adjacency: at most 4 lines apart (skip blanks/displays)
                if k2 - k1 > 4:
                    continue
                up1, up2 = name1.upper(), name2.upper()
                is_read = ("READ" in up1) or ("FETCH" in up1) or ("GET" in up1)
                is_mutate = ("DELETE" in up2) or ("UPDATE" in up2) or ("WRITE" in up2) or ("REWRITE" in up2)
                if not (is_read and is_mutate):
                    continue
                # Check there's no IF / EVALUATE between them
                between = " ".join(
                    (l[6:] if len(l) > 6 else l) for l in block_lines[k1+1:k2]
                    if not (len(l) > 6 and l[6] == "*")
                ).upper()
                if re.search(r"\b(IF|EVALUATE|WHEN|END-IF)\b", between):
                    continue
                anomalies.append({
                    "severity": "WARNING",
                    "category": "LOGIC",
                    "rule_id": "UNCONDITIONAL_FOLLOW",
                    "title": (
                        f"`PERFORM {name2}` runs unconditionally after `PERFORM {name1}` "
                        f"in `{p.get('name')}`"
                    ),
                    "description": (
                        f"There is no IF / EVALUATE check between the read-style "
                        f"`{name1}` and the mutating `{name2}`. If `{name1}` "
                        f"encounters an error (NOTFND, IO failure, etc.) without "
                        f"setting STOP RUN or PERFORM-aborting, `{name2}` will "
                        f"execute anyway — potentially deleting/updating against "
                        f"stale or invalid state. Verify `{name1}` aborts the "
                        f"program on failure or that `{name2}` checks a status "
                        f"flag set by `{name1}`."
                    ),
                    "paragraph_name": p.get("name"),
                    "line_number": ps + k1,
                    "snippet": "\n".join(
                        l.rstrip()[:100] for l in block_lines[k1:k2 + 1]
                    ),
                    "suggestion": (
                        f"Add an `IF <status-flag> = 'OK'` guard around `PERFORM {name2}` "
                        f"or have `{name1}` set ERR-FLG-ON / call ABEND on failure."
                    ),
                })

        # ── 9b. OPEN_WITHOUT_CLOSE — file opened but never explicitly closed ──
        opens_seen = {}   # file_name -> first OPEN line
        closes_seen = set()
        op_pat = re.compile(r"\bOPEN\s+(?:INPUT|OUTPUT|I-O|EXTEND)\s+([A-Z][A-Z0-9-]+)",
                              re.IGNORECASE)
        cl_pat = re.compile(r"\bCLOSE\s+([A-Z][A-Z0-9-,\s]+)", re.IGNORECASE)
        for i, raw in enumerate(lines):
            if len(raw) > 6 and raw[6] == "*":
                continue
            body = raw[6:] if len(raw) > 6 else raw
            for mo in op_pat.finditer(body):
                fn = mo.group(1).upper()
                opens_seen.setdefault(fn, i + 1)
            for mc in cl_pat.finditer(body):
                for tok in re.split(r"[,\s]+", mc.group(1).strip()):
                    if tok and re.match(r"^[A-Z][A-Z0-9-]+$", tok, re.IGNORECASE):
                        if tok.upper() not in ("WITH", "REEL", "UNIT", "NO", "REWIND", "LOCK"):
                            closes_seen.add(tok.upper())
        for fn, ln in opens_seen.items():
            if fn in closes_seen:
                continue
            anomalies.append({
                "severity": "WARNING",
                "category": "INCOMPLETE",
                "rule_id": "OPEN_WITHOUT_CLOSE",
                "title": f"`{fn}` is OPENed but never CLOSEd",
                "description": (
                    f"File `{fn}` is opened (line {ln}) but no `CLOSE {fn}` "
                    f"statement appears anywhere in the program. The OS will "
                    f"close it on STOP RUN, but explicit CLOSE is best practice "
                    f"and the migration team must mirror this lifecycle."
                ),
                "paragraph_name": None,
                "line_number": ln,
                "snippet": "",
                "suggestion": f"Add an explicit `CLOSE {fn}` (typically in a 9xxx-CLOSE paragraph).",
            })

        # ── 9c. STATIC_CALL — CALL 'PROGRAM' to a target not in our DB ──────
        # E.g. CALL 'COBDATFT', CALL 'CEE3ABD' — these are real external
        # subroutines (LE services or sister modules) that must be documented.
        # Don't flag CALL <variable>; the dynamic CALL resolver handles those.
        static_call_pat = re.compile(r"\bCALL\s+['\"]([A-Z][A-Z0-9-]{1,20})['\"]", re.IGNORECASE)
        # Pull set of known program IDs once per call
        try:
            cursor_known = self.conn.cursor()
            cursor_known.execute("SELECT program_id FROM programs")
            known_progs = {r[0].upper() for r in cursor_known.fetchall()}
        except Exception:
            known_progs = set()
        seen_static = set()
        for i, raw in enumerate(lines):
            if len(raw) > 6 and raw[6] == "*":
                continue
            body = raw[6:] if len(raw) > 6 else raw
            for m in static_call_pat.finditer(body):
                target = m.group(1).upper()
                if target in known_progs:
                    continue   # already in program_calls
                if target == program_id.upper():
                    continue
                if target in seen_static:
                    continue
                seen_static.add(target)
                # Friendly hints for well-known IBM services
                hints = {
                    "CEE3ABD": "IBM Language Environment ABEND service (forces program termination with a user code).",
                    "CEEDAYS": "IBM Language Environment date conversion (date string → Lilian day count).",
                    "CEEDATE": "IBM LE date formatter.",
                    "CEEISEC": "IBM LE seconds since epoch.",
                    "CEELOCT": "IBM LE local time service.",
                    "CBLTDLI": "IMS DL/I database call interface.",
                    "DSNHLI":  "DB2 host language interface (used implicitly by EXEC SQL).",
                    "MVSWAIT": "Custom MVS wait subroutine.",
                }
                hint = hints.get(target, "External subroutine — verify whether it is a sister application program, a vendor utility, or an IBM-supplied service.")
                anomalies.append({
                    "severity": "NOTICE",
                    "category": "DEPENDENCY",
                    "rule_id": "STATIC_CALL_EXTERNAL",
                    "title": f"Static CALL to external `{target}` (not in this codebase)",
                    "description": (
                        f"`CALL '{target}'` appears in the source but `{target}` is "
                        f"not a program in the loaded codebase. {hint}"
                    ),
                    "paragraph_name": None,
                    "line_number": i + 1,
                    "snippet": body.strip(),
                    "suggestion": (
                        "Document this external dependency in the Migration Notes — "
                        "the modern equivalent must replicate its behaviour."
                    ),
                })

        # ── 9. CONTROL-BREAK / ACCOUNT-BREAK pattern detector ────────────────
        # Pattern: an IF compares a key field against a "WS-LAST-..." holder,
        # then PERFORMs a flush paragraph. The same flush paragraph is also
        # called from the loop's wrap-up code. This is a control-break pattern
        # that the migration team MUST understand explicitly.
        wslast_pat = re.compile(
            r"\bIF\s+([A-Z][A-Z0-9-]*)\s*(?:NOT\s*=|<>|NOT\s+EQUAL)\s*"
            r"(WS-LAST-[A-Z0-9-]+|LAST-[A-Z0-9-]+|PREV-[A-Z0-9-]+|HOLD-[A-Z0-9-]+)",
            re.IGNORECASE,
        )
        for i, raw in enumerate(lines):
            if len(raw) > 6 and raw[6] == "*":
                continue
            body = raw[6:] if len(raw) > 6 else raw
            m = wslast_pat.search(body)
            if not m:
                continue
            key_field = m.group(1).upper()
            hold_field = m.group(2).upper()
            # Find the paragraph this is in
            para = None
            for p in paragraphs:
                ps = p.get("line_start", 0)
                pe = p.get("line_end", 0)
                if ps and pe and ps <= i + 1 <= pe:
                    para = p.get("name")
                    break
            # Look ahead a few lines for the PERFORM call (the flush paragraph)
            flush_para = None
            for k in range(i, min(i + 8, len(lines))):
                if len(lines[k]) > 6 and lines[k][6] == "*":
                    continue
                bb = lines[k][6:] if len(lines[k]) > 6 else lines[k]
                pm = re.search(r"\bPERFORM\s+([A-Z0-9][A-Z0-9-]*)\b", bb, re.IGNORECASE)
                if pm and "UPDATE" in pm.group(1).upper() or (pm and "WRITE" in pm.group(1).upper()):
                    flush_para = pm.group(1).upper()
                    break
                if pm and not pm.group(1).upper().startswith(("END-", "WHEN")):
                    flush_para = pm.group(1).upper()
                    break
            anomalies.append({
                "severity": "NOTICE",
                "category": "LOGIC",
                "rule_id": "CONTROL_BREAK_PATTERN",
                "title": f"Control-break pattern on `{key_field}` (vs `{hold_field}`)",
                "description": (
                    f"Classic control-break: when `{key_field}` changes, "
                    f"`{flush_para or '<flush paragraph>'}` is invoked to flush "
                    f"the previous group's accumulated state. After the main loop "
                    f"completes the same paragraph is typically called one more "
                    f"time to flush the final group. This is the architectural "
                    f"backbone of the program — document it explicitly with the "
                    f"key field, the holder field, and the flush paragraph name."
                ),
                "paragraph_name": para,
                "line_number": i + 1,
                "snippet": body.strip(),
                "suggestion": (
                    "In the modern implementation, replace this idiom with a "
                    "GROUP BY (SQL) or a stream group operator (collect-by-key) "
                    "and ensure the final group is also flushed."
                ),
            })

        # Cap: don't drown the LLM in dozens of low-importance unused-var notices.
        # Keep ALL bugs/warnings + top 10 unused-var notices + ALL stub/magic notices.
        bugs = [a for a in anomalies if a["severity"] in ("BUG", "WARNING")]
        unused = [a for a in anomalies
                   if a["severity"] == "NOTICE" and a["rule_id"] == "UNUSED_VARIABLE"][:10]
        other_notices = [a for a in anomalies
                          if a["severity"] == "NOTICE" and a["rule_id"] != "UNUSED_VARIABLE"]
        return bugs + unused + other_notices

    @staticmethod
    def _extract_files_from_source(file_path: str) -> List[Dict]:
        """Parse the FILE-CONTROL section to extract SELECT … ASSIGN TO …
        ORGANIZATION/ACCESS clauses. Each entry maps a logical file name
        to its DDname plus organisation and access mode."""
        import re
        from pathlib import Path
        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        lines = content.split("\n")

        def _strip_seq(line: str) -> str:
            if len(line) > 6 and line[6] == "*":
                return ""
            body = line[6:] if len(line) > 6 else line
            return body[:66] if len(body) > 66 else body

        # Find FILE-CONTROL block
        in_fc = False
        block = []
        block_start = 0
        for i, raw in enumerate(lines):
            body = _strip_seq(raw)
            up = body.upper()
            if "FILE-CONTROL" in up:
                in_fc = True
                block_start = i + 1
                continue
            if in_fc and (
                "DATA DIVISION" in up or "PROCEDURE DIVISION" in up
                or "I-O-CONTROL" in up
            ):
                break
            if in_fc:
                block.append((i + 1, body))
        if not block:
            return []

        # Group by SELECT — each SELECT statement runs until period
        results = []
        select_pat = re.compile(
            r"\bSELECT\s+(?:OPTIONAL\s+)?([A-Z][A-Z0-9-]*)\s+ASSIGN\s+TO\s+([A-Z][A-Z0-9-]*)",
            re.IGNORECASE,
        )
        org_pat = re.compile(r"\bORGANIZATION\s+(?:IS\s+)?([A-Z]+)", re.IGNORECASE)
        acc_pat = re.compile(r"\bACCESS\s+(?:MODE\s+)?(?:IS\s+)?([A-Z]+)", re.IGNORECASE)
        rec_key_pat = re.compile(r"\bRECORD\s+KEY\s+(?:IS\s+)?([A-Z][A-Z0-9-]*)", re.IGNORECASE)

        # Concatenate lines and split on period
        joined = " ".join(b[1] for b in block)
        line_map = []  # cumulative line numbers per chunk
        for ln_num, b in block:
            for _ in range(len(b) + 1):
                line_map.append(ln_num)

        # Walk through SELECT statements
        for m in select_pat.finditer(joined):
            file_name = m.group(1).upper()
            ddname = m.group(2).upper()
            # Find the matching period after this SELECT
            start = m.end()
            end = joined.find(".", start)
            if end == -1:
                end = len(joined)
            stmt = joined[start:end]

            org_m = org_pat.search(stmt)
            acc_m = acc_pat.search(stmt)
            rec_m = rec_key_pat.search(stmt)

            organization = org_m.group(1).upper() if org_m else None
            access_mode = acc_m.group(1).upper() if acc_m else None
            record_key = rec_m.group(1).upper() if rec_m else None

            file_type = "VSAM" if organization == "INDEXED" else (
                "SEQUENTIAL" if organization == "SEQUENTIAL" else organization
            )

            ln = line_map[m.start()] if m.start() < len(line_map) else None
            results.append({
                "file_name": file_name,
                "ddname": ddname,
                "file_type": file_type,
                "organization": organization,
                "access_mode": access_mode,
                "record_key": record_key,
                "line_number": ln,
            })
        return results

    @staticmethod
    def _extract_data_items_from_lines(lines: List[str], start_line: int = 1):
        """Generic COBOL data-item parser. Reads lines starting at start_line,
        returns a list of dicts: {field_name, level, picture, usage, value, parent,
        line_number, occurs, redefines}.

        Works on copybook .cpy files OR a slice of a .cbl file (e.g. an FD block).
        """
        import re

        # COBOL data declaration: <level> <name> [PIC ...] [USAGE ...] [VALUE ...]
        # Levels: 01-49, 66, 77, 88
        decl_pat = re.compile(
            r"^\s*(\d{2})\s+([A-Z][A-Z0-9-]*)\b(.*?)(?:\.\s*$|$)",
            re.IGNORECASE,
        )
        pic_pat = re.compile(r"\bPIC(?:TURE)?\s+(?:IS\s+)?(\S+)", re.IGNORECASE)
        usage_pat = re.compile(r"\b(?:USAGE\s+(?:IS\s+)?)?(COMP|COMP-3|COMP-4|COMP-5|BINARY|PACKED-DECIMAL|DISPLAY)\b", re.IGNORECASE)
        value_pat = re.compile(r"\bVALUE\s+(?:IS\s+)?([^.]+)", re.IGNORECASE)
        occurs_pat = re.compile(r"\bOCCURS\s+(\d+)", re.IGNORECASE)
        redef_pat = re.compile(r"\bREDEFINES\s+([A-Z][A-Z0-9-]*)", re.IGNORECASE)

        items = []
        # Stack of (level_number, field_name) for parent tracking
        parent_stack = []
        # We sometimes need to join continuation lines (statement runs until period)
        buf = ""
        buf_line_num = 0

        def _strip_seq(line: str) -> str:
            if len(line) > 6 and line[6] == "*":
                return ""
            body = line[6:] if len(line) > 6 else line
            return body[:66] if len(body) > 66 else body

        for idx, raw in enumerate(lines):
            line_num = start_line + idx
            body = _strip_seq(raw)
            if not body.strip():
                continue
            if not buf:
                buf = body
                buf_line_num = line_num
            else:
                buf += " " + body
            # If buffer doesn't end with period yet, keep accumulating
            if "." not in buf:
                continue
            # Process complete statements (split on period, keep last incomplete part as buf)
            parts = buf.split(".")
            buf = parts[-1]
            for part in parts[:-1]:
                m = decl_pat.match(part)
                if not m:
                    continue
                lvl = int(m.group(1))
                name = m.group(2).upper()
                if name in ("FILLER",):
                    continue
                # Skip non-data items
                if name in ("FD", "SD", "WORKING-STORAGE", "LINKAGE", "FILE",
                             "PROCEDURE", "DIVISION", "SECTION", "COPY"):
                    continue
                clauses = m.group(3) or ""
                pic = (pic_pat.search(clauses) or [None, None])[1] if pic_pat.search(clauses) else None
                use_m = usage_pat.search(clauses)
                usage = use_m.group(1).upper() if use_m else None
                val_m = value_pat.search(clauses)
                value = val_m.group(1).strip().rstrip(".") if val_m else None
                occ_m = occurs_pat.search(clauses)
                occurs = int(occ_m.group(1)) if occ_m else None
                redef_m = redef_pat.search(clauses)
                redefines = redef_m.group(1).upper() if redef_m else None

                # Maintain parent stack by level
                while parent_stack and parent_stack[-1][0] >= lvl:
                    parent_stack.pop()
                parent = parent_stack[-1][1] if parent_stack else None

                items.append({
                    "field_name": name,
                    "level": lvl,
                    "picture": pic,
                    "usage": usage,
                    "value": value,
                    "parent": parent,
                    "line_number": buf_line_num,
                    "occurs": occurs,
                    "redefines": redefines,
                })

                if pic is None and lvl < 50:
                    parent_stack.append((lvl, name))

            buf_line_num = line_num
        return items

    @staticmethod
    def _extract_copybook_fields_from_source(file_path: str) -> List[Dict]:
        """Parse a .cpy file and return field-level dictionary entries."""
        from pathlib import Path
        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        return SQLiteLoader._extract_data_items_from_lines(content.split("\n"))

    @staticmethod
    def _extract_file_records_from_source(file_path: str) -> List[Dict]:
        """Find each `FD <file-name>` block in a COBOL program and return
        the data items that follow until the next FD or section break."""
        import re
        from pathlib import Path
        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        lines = content.split("\n")

        def _strip_seq(line: str) -> str:
            if len(line) > 6 and line[6] == "*":
                return ""
            body = line[6:] if len(line) > 6 else line
            return body[:66] if len(body) > 66 else body

        fd_pat = re.compile(r"^\s*FD\s+([A-Z][A-Z0-9-]*)\b", re.IGNORECASE)
        section_break_pat = re.compile(
            r"^\s*(WORKING-STORAGE|LINKAGE|PROCEDURE|LOCAL-STORAGE)\s+SECTION", re.IGNORECASE)

        results = []
        i = 0
        while i < len(lines):
            body = _strip_seq(lines[i])
            m = fd_pat.match(body)
            if not m:
                i += 1
                continue
            fd_name = m.group(1).upper()
            block_start = i + 1
            j = block_start
            # Walk forward until next FD/SD or section break
            while j < len(lines):
                b = _strip_seq(lines[j])
                if fd_pat.match(b) or section_break_pat.match(b):
                    break
                j += 1
            block_lines = lines[block_start:j]
            items = SQLiteLoader._extract_data_items_from_lines(block_lines, start_line=block_start + 1)
            # Identify the 01-level "record" that anchors this FD
            record_name = None
            for it in items:
                if it["level"] == 1:
                    record_name = it["field_name"]
                    break
            for it in items:
                results.append({
                    "file_name": fd_name,
                    "record_name": record_name,
                    "field_name": it["field_name"],
                    "level_number": it["level"],
                    "picture": it["picture"],
                    "usage": it["usage"],
                    "parent_name": it["parent"],
                    "line_number": it["line_number"],
                })
            i = j
        return results

    @staticmethod
    def _extract_movements_from_source(file_path: str, paragraphs: List[Dict]) -> List[Dict]:
        """Extract MOVE statements: source -> destination pairs.
        Only captures simple cases: MOVE <src> TO <dst>[, <dst2>, ...].
        Skips arithmetic / reference modifications."""
        import re
        from pathlib import Path
        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        lines = content.split("\n")

        def _strip_seq(line: str) -> str:
            if len(line) > 6 and line[6] == "*":
                return ""
            body = line[6:] if len(line) > 6 else line
            return body[:66] if len(body) > 66 else body

        def _find_paragraph(line_num):
            for p in paragraphs:
                start = p.get("line_start", 0)
                end = p.get("line_end", 0)
                if start and end and start <= line_num <= end:
                    return p.get("name")
            return None

        # MOVE <src> TO <dst1> [<dst2>...]   src can be 'literal', "literal", number, or identifier
        move_pat = re.compile(
            r"\bMOVE\s+("
            r"'[^']*'|\"[^\"]*\"|[+-]?\d+(?:\.\d+)?|[A-Z][A-Z0-9-]*(?:\([^)]+\))?"
            r")\s+TO\s+([A-Z][A-Z0-9-]*(?:\s*,?\s*[A-Z][A-Z0-9-]*)*)",
            re.IGNORECASE,
        )

        results = []
        for idx, raw in enumerate(lines):
            body = _strip_seq(raw)
            if "MOVE" not in body.upper():
                continue
            for m in move_pat.finditer(body):
                src_field = m.group(1).strip()
                dst_block = m.group(2).strip()
                is_literal = 1 if (src_field.startswith(("'", '"')) or src_field.lstrip("+-").replace(".", "").isdigit()) else 0
                # Split multiple destinations
                for dst in re.split(r"[,\s]+", dst_block):
                    dst = dst.strip().rstrip(",")
                    if not dst:
                        continue
                    results.append({
                        "source_field": src_field.strip("'\""),
                        "destination_field": dst.upper(),
                        "paragraph": _find_paragraph(idx + 1),
                        "line_number": idx + 1,
                        "is_literal": is_literal,
                    })
        return results

    @staticmethod
    def _extract_sql_from_source(file_path: str, paragraphs: List[Dict]) -> List[Dict]:
        """Extract EXEC SQL (DB2) statements directly from COBOL source.
        Returns list of {command, table_name, cursor_name, paragraph, line_number, sql_text}."""
        import re
        from pathlib import Path

        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []

        lines = content.split("\n")

        source_ranges = SQLiteLoader._source_paragraph_ranges(file_path, paragraphs)

        def _find_paragraph(line_num):
            for pname, (start, end) in source_ranges.items():
                if start <= line_num <= end:
                    return pname
            for p in paragraphs or []:
                start = p.get("line_start", 0)
                end = p.get("line_end", 0)
                if start and end and start <= line_num <= end:
                    return p.get("name") or p.get("paragraph_name")
            return None

        results = []
        i = 0
        while i < len(lines):
            line = lines[i]
            line_num = i + 1
            if len(line) > 6 and line[6] == "*":
                i += 1
                continue
            upper = line.upper()
            if "EXEC SQL" not in upper:
                i += 1
                continue

            # Collect block until END-EXEC
            block_lines = [line]
            j = i + 1
            while j < len(lines):
                block_lines.append(lines[j])
                if "END-EXEC" in lines[j].upper():
                    break
                j += 1
            i = j + 1

            # Strip column 1-6 sequence area AND trailing column-73-80 area.
            def _trim(l):
                body = l[6:] if len(l) > 6 else l
                return body[:66] if len(body) > 66 else body
            block = " ".join(_trim(l) for l in block_lines)
            block = re.sub(r"\s+", " ", block).strip()
            block_no_end = re.sub(r"END-EXEC\.?\s*$", "", block, flags=re.IGNORECASE).strip()

            # Identify the SQL command (first keyword after EXEC SQL)
            m = re.search(r"EXEC\s+SQL\s+(\w+)", block_no_end, re.IGNORECASE)
            cmd = m.group(1).upper() if m else "UNKNOWN"

            # Special case: DECLARE <cursor> CURSOR FOR <query>
            cursor_name = None
            table_name = None
            if cmd == "DECLARE":
                cm = re.search(r"DECLARE\s+(\S+)\s+CURSOR\s+FOR", block_no_end, re.IGNORECASE)
                if cm:
                    cursor_name = cm.group(1)
                # also find FROM <table> inside the declared SELECT
                fm = re.search(r"\bFROM\s+([A-Z0-9_.$]+)", block_no_end, re.IGNORECASE)
                if fm:
                    table_name = fm.group(1)
            elif cmd in ("OPEN", "FETCH", "CLOSE"):
                cm = re.search(rf"{cmd}\s+(\S+)", block_no_end, re.IGNORECASE)
                if cm:
                    cursor_name = cm.group(1).strip(",;")
            else:
                # SELECT/INSERT/UPDATE/DELETE — find the table
                tm = (
                    re.search(r"\bFROM\s+([A-Z0-9_.$]+)", block_no_end, re.IGNORECASE)
                    or re.search(r"\bINTO\s+([A-Z0-9_.$]+)", block_no_end, re.IGNORECASE)
                    or re.search(r"\bUPDATE\s+([A-Z0-9_.$]+)", block_no_end, re.IGNORECASE)
                )
                if tm:
                    table_name = tm.group(1)

            # Trim sql_text for storage
            sql_text = block_no_end[:300]

            para_name = _find_paragraph(line_num)
            results.append({
                "command": cmd,
                "table_name": table_name,
                "cursor_name": cursor_name,
                "paragraph": para_name,
                "line_number": line_num,
                "sql_text": sql_text,
            })

        return results

    @staticmethod
    def _extract_cics_from_source(file_path: str, paragraphs: List[Dict]) -> List[Dict]:
        """Extract EXEC CICS commands directly from COBOL source when ProLeap gives empty raw_text."""
        import re
        from pathlib import Path

        src = Path(file_path)
        if not src.exists():
            return []

        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []

        lines = content.split("\n")

        source_ranges = SQLiteLoader._source_paragraph_ranges(file_path, paragraphs)

        def _find_paragraph(line_num):
            for pname, (start, end) in source_ranges.items():
                if start <= line_num <= end:
                    return pname
            for p in paragraphs or []:
                start = p.get("line_start", 0)
                end = p.get("line_end", 0)
                if start and end and start <= line_num <= end:
                    return p.get("name") or p.get("paragraph_name")
            return None

        results = []
        i = 0
        while i < len(lines):
            line = lines[i]
            line_num = i + 1

            # Skip comment lines (column 7 = *)
            if len(line) > 6 and line[6] == "*":
                i += 1
                continue

            upper = line.upper()
            if "EXEC CICS" not in upper:
                i += 1
                continue

            # Collect the full EXEC CICS block (may span multiple lines until END-EXEC)
            block_lines = [line]
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                block_lines.append(next_line)
                if "END-EXEC" in next_line.upper():
                    break
                j += 1
            i = j + 1

            # Join and extract command + parameters
            # Strip column 1-6 sequence area AND trailing column-73-80 area.
            def _trim_cics(l):
                body = l[6:] if len(l) > 6 else l
                return body[:66] if len(body) > 66 else body
            block = " ".join(_trim_cics(l) for l in block_lines)
            block = re.sub(r"\s+", " ", block).strip()

            m = re.search(r"EXEC\s+CICS\s+(\w+)", block, re.IGNORECASE)
            cmd = m.group(1).upper() if m else "UNKNOWN"

            details = {}
            for param in ["MAP", "MAPSET", "PROGRAM", "DATASET", "FILE", "TRANSID",
                          "FROM", "INTO", "LENGTH", "RIDFLD", "COMMAREA", "QUEUE",
                          "RESP", "CURSOR", "ERASE"]:
                pm = re.search(rf"{param}\s*\(\s*([^)]+)\s*\)", block, re.IGNORECASE)
                if pm:
                    details[param.lower()] = pm.group(1).strip().strip("'\"")

            para_name = _find_paragraph(line_num)
            results.append({
                "command": cmd,
                "line_number": line_num,
                "paragraph": para_name,
                "details": details,
            })

        return results

    @staticmethod
    def _extract_ims_from_source(file_path: str, paragraphs: List[Dict],
                                  data_items: List[Dict] = None) -> List[Dict]:
        """Extract IMS DL/I CALL 'CBLTDLI' statements from COBOL source.
        Pattern: CALL 'CBLTDLI' USING <fn>, <PCB-name>, <area>, <SSA-name>
        Also detects ENTRY 'DLITCBL' as an IMS batch program marker.
        Returns list of {function_code, function_name, pcb_name, segment_area,
                         ssa_name, ssa_segment, ssa_qualifier, paragraph, line_number, raw_text}.
        """
        import re
        from pathlib import Path

        # IMS function code → human-readable name
        IMS_FUNCTIONS = {
            "GU":   "Get Unique",
            "GHU":  "Get Hold Unique",
            "GN":   "Get Next",
            "GHN":  "Get Hold Next",
            "GNP":  "Get Next in Parent",
            "GHNP": "Get Hold Next in Parent",
            "ISRT": "Insert",
            "REPL": "Replace",
            "DLET": "Delete",
            "CHKP": "Checkpoint",
            "XRST": "Extended Restart",
            "ROLB": "Rollback",
            "ROLL": "Roll",
            "PCB":  "PCB Call",
            "STAT": "Statistics",
            "LOG":  "Log",
            "DEQ":  "Dequeue",
            "POS":  "Position",
            "FLD":  "Field Call",
        }

        src = Path(file_path)
        if not src.exists():
            return []
        try:
            content = src.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []

        lines = content.split("\n")

        # Strip COBOL sequence area + comments
        def _trim(l):
            if len(l) > 6 and l[6] == "*":
                return ""
            body = l[6:] if len(l) > 6 else l
            return body[:66] if len(body) > 66 else body

        # Parser line numbers can drift after COPY expansion. For source-file
        # extractors, map paragraphs by scanning real COBOL labels in the file.
        paragraph_names = []
        for p in paragraphs or []:
            pname = (p.get("name") or p.get("paragraph_name") or "").upper()
            if pname:
                paragraph_names.append(pname)
        paragraph_starts = []
        for idx, raw_line in enumerate(lines, 1):
            body = _trim(raw_line).strip().upper()
            for pname in paragraph_names:
                if re.match(rf"^{re.escape(pname)}\s*\.", body):
                    paragraph_starts.append((idx, pname))
                    break
        paragraph_starts.sort()
        source_ranges = []
        for pos, (start, pname) in enumerate(paragraph_starts):
            end = paragraph_starts[pos + 1][0] - 1 if pos + 1 < len(paragraph_starts) else len(lines)
            source_ranges.append((start, end, pname))

        def _find_paragraph(line_num):
            for start, end, pname in source_ranges:
                if start <= line_num <= end:
                    return pname
            for p in paragraphs or []:
                start = p.get("line_start", 0)
                end = p.get("line_end", 0)
                if start and end and start <= line_num <= end:
                    return p.get("name") or p.get("paragraph_name")
            return None

        def _extract_ssa_layouts():
            layouts = {}
            current = None
            fields = []

            def flush():
                if not current:
                    return
                segment = None
                key_field = None
                rel_oper = None
                for fname, literal in fields:
                    lit = (literal or "").strip()
                    if not lit or lit in ("(", ")", " "):
                        continue
                    if fname.endswith("SEG-NAME") or (segment is None and len(lit) >= 4):
                        segment = lit
                    if fname.endswith("KEY-FIELD"):
                        key_field = lit.strip()
                    if fname.endswith("REL-OPER"):
                        rel_oper = lit.strip()
                qualifier = None
                if key_field and rel_oper:
                    qualifier = f"{key_field} {rel_oper} QUAL-SSA-KEY-VALUE"
                layouts[current] = {"segment": segment, "qualifier": qualifier}

            for raw_line in lines:
                body = _trim(raw_line).strip().upper()
                if not body:
                    continue
                m01 = re.match(r"^01\s+([A-Z0-9-]*SSA)\s*\.", body)
                if m01:
                    flush()
                    current = m01.group(1)
                    fields = []
                    continue
                if current and re.match(r"^01\s+", body):
                    flush()
                    current = None
                    fields = []
                    continue
                if current:
                    mf = re.match(
                        r"^\d+\s+([A-Z0-9-]+|FILLER)\b.*?\bVALUE\s+['\"]([^'\"]*)['\"]",
                        body,
                    )
                    if mf:
                        fields.append((mf.group(1), mf.group(2)))
            flush()
            return layouts

        ssa_layouts = _extract_ssa_layouts()

        results = []
        i = 0
        while i < len(lines):
            line = lines[i]
            line_num = i + 1
            body = _trim(line).upper()

            if not body:
                i += 1
                continue

            # Detect ENTRY 'DLITCBL' — IMS batch program marker
            if "ENTRY" in body and "DLITCBL" in body:
                results.append({
                    "function_code": "ENTRY",
                    "function_name": "IMS Batch Entry Point (DLITCBL)",
                    "pcb_name": None,
                    "segment_area": None,
                    "ssa_name": None,
                    "ssa_segment": None,
                    "ssa_qualifier": None,
                    "paragraph": _find_paragraph(line_num),
                    "line_number": line_num,
                    "raw_text": _trim(line).strip(),
                })
                i += 1
                continue

            # Detect CALL 'CBLTDLI' USING ...
            if "CBLTDLI" not in body:
                i += 1
                continue

            # Collect the full statement (may span multiple lines until period or next statement)
            block_parts = [_trim(line)]
            j = i + 1
            while j < len(lines):
                next_body = _trim(lines[j])
                if not next_body:
                    j += 1
                    continue
                # Stop at period, next paragraph, or next statement keyword
                block_parts.append(next_body)
                if "." in next_body:
                    break
                j += 1
            i = j + 1

            block = " ".join(block_parts)
            block = re.sub(r"\s+", " ", block).strip()

            # Parse: CALL 'CBLTDLI' USING <fn>, <PCB>, <area> [, <SSA1> [, <SSA2> ...]]
            # Arguments may be separated by commas or spaces
            m = re.search(
                r"CALL\s+['\"]CBLTDLI['\"]\s+USING\s+(.*?)(?:\.|$)",
                block, re.IGNORECASE
            )
            if not m:
                continue

            args_str = m.group(1).strip().rstrip(".")
            # Split on commas or whitespace, filtering out empty and COBOL keywords
            args = [a.strip().rstrip(",") for a in re.split(r"[,\s]+", args_str)
                    if a.strip() and a.strip().upper() not in ("BY", "REFERENCE", "CONTENT", "VALUE")]

            fn_var = args[0].upper() if len(args) > 0 else "UNKNOWN"
            pcb = args[1].upper() if len(args) > 1 else None
            area = args[2].upper() if len(args) > 2 else None
            ssa = args[3].upper() if len(args) > 3 else None

            # Resolve function code: it might be a variable name containing the
            # function code, or a literal like 'GU'. Strip quotes.
            fn_code = fn_var.strip("'\"")
            if fn_code.startswith("FUNC-"):
                candidate = fn_code[5:]
                if candidate in IMS_FUNCTIONS:
                    fn_code = candidate

            # Map known function codes
            fn_name = IMS_FUNCTIONS.get(fn_code)
            if not fn_name:
                # It might be a variable — check if there's a MOVE 'GU' TO <var> somewhere
                # For now just record the raw name
                fn_name = None

            # Look up SSA segment and qualifier from source declarations.
            ssa_layout = ssa_layouts.get(ssa, {}) if ssa else {}
            ssa_seg = ssa_layout.get("segment")
            ssa_qual = ssa_layout.get("qualifier")

            raw = block[:200]

            results.append({
                "function_code": fn_code,
                "function_name": fn_name,
                "pcb_name": pcb,
                "segment_area": area,
                "ssa_name": ssa,
                "ssa_segment": ssa_seg,
                "ssa_qualifier": ssa_qual,
                "paragraph": _find_paragraph(line_num),
                "line_number": line_num,
                "raw_text": raw,
            })

        return results

    def load_copybook_fields(self, repo_path: str = None):
        """Scan all .cpy / .CPY files in the repo, parse field-level dictionaries,
        and load them into copybook_fields. Also populates copybooks.file_path
        for any rows that don't have it set yet."""
        from pathlib import Path
        if not repo_path:
            return
        cursor = self.conn.cursor()

        cpy_files = list(Path(repo_path).rglob("*.cpy")) + list(Path(repo_path).rglob("*.CPY"))
        loaded = 0
        for fp in cpy_files:
            cb_name = fp.stem.upper()
            try:
                fields = self._extract_copybook_fields_from_source(str(fp))
            except Exception:
                continue

            # Ensure the copybook row exists with a file_path
            cursor.execute("INSERT OR IGNORE INTO copybooks (copybook_name, file_path) VALUES (?, ?)",
                            (cb_name, str(fp)))
            cursor.execute("UPDATE copybooks SET file_path = ? WHERE copybook_name = ? AND (file_path IS NULL OR file_path = '')",
                            (str(fp), cb_name))

            # Replace any existing fields for this copybook
            cursor.execute("DELETE FROM copybook_fields WHERE copybook_name = ?", (cb_name,))
            for f in fields:
                cursor.execute("""
                    INSERT INTO copybook_fields (
                        copybook_name, field_name, level_number, picture, usage,
                        value, parent_name, line_number, occurs_count, redefines_target
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cb_name,
                    f.get("field_name"),
                    f.get("level"),
                    f.get("picture"),
                    f.get("usage"),
                    f.get("value"),
                    f.get("parent"),
                    f.get("line_number"),
                    f.get("occurs"),
                    f.get("redefines"),
                ))
            if fields:
                loaded += 1
        self.conn.commit()
        console.print(f"[green]OK - Loaded copybook field dictionaries for {loaded}/{len(cpy_files)} .cpy files[/green]")

    # Convenient retrieval helpers
    def get_copybook_fields(self, copybook_name: str) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT field_name, level_number, picture, usage, value, parent_name, line_number,
                   occurs_count, redefines_target
            FROM copybook_fields
            WHERE copybook_name = ?
            ORDER BY line_number, level_number
        """, (copybook_name,))
        return [dict(r) for r in cursor.fetchall()]

    def get_program_file_records(self, program_id: str) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT file_name, record_name, field_name, level_number, picture, usage,
                   parent_name, line_number
            FROM file_records
            WHERE program_id = ?
            ORDER BY file_name, line_number, level_number
        """, (program_id,))
        return [dict(r) for r in cursor.fetchall()]

    def get_program_parameters(self, program_id: str) -> List[Dict]:
        """For each parameter declared in PROCEDURE DIVISION USING, also trace
        where it (or any of its sub-fields) is referenced in the source code."""
        cur = self.conn.cursor()
        try:
            cur.execute("""
                SELECT position, parameter_name, source, line_number
                FROM program_parameters WHERE program_id = ?
                ORDER BY source, position
            """, (program_id,))
            params = [dict(r) for r in cur.fetchall()]
        except Exception:
            return []
        if not params:
            return []

        # For each parameter, find usage sites (data_movements + statements)
        # plus sub-fields of any group structure with the same prefix.
        usages_by_param = {}
        for p in params:
            name = p["parameter_name"]
            usage = []
            # MOVE flows where this parameter (or a sub-field) is source or destination
            try:
                cur.execute("""
                    SELECT DISTINCT paragraph_name, line_number, source_field, destination_field
                    FROM data_movements
                    WHERE program_id = ?
                      AND (source_field = ? OR destination_field = ?
                           OR source_field LIKE ? OR destination_field LIKE ?)
                    ORDER BY line_number LIMIT 8
                """, (program_id, name, name, f"{name}-%", f"{name}-%"))
                for r in cur.fetchall():
                    role = "source" if r[2] == name or (r[2] or "").startswith(f"{name}-") else "destination"
                    other = r[3] if role == "source" else r[2]
                    usage.append({
                        "kind": "MOVE",
                        "role": role,
                        "other_field": other,
                        "paragraph": r[0],
                        "line_number": r[1],
                    })
            except Exception:
                pass
            # Statement references
            try:
                cur.execute("""
                    SELECT DISTINCT paragraph_name, line_number, statement_type
                    FROM statements
                    WHERE program_id = ?
                      AND (details_json LIKE ? OR details_json LIKE ?)
                    ORDER BY line_number LIMIT 6
                """, (program_id, f"%{name}%", f"%{name}-%"))
                for r in cur.fetchall():
                    usage.append({
                        "kind": r[2],
                        "role": "ref",
                        "other_field": None,
                        "paragraph": r[0],
                        "line_number": r[1],
                    })
            except Exception:
                pass
            p["usage_sites"] = usage[:10]
        return params

    def get_program_file_operations(self, program_id: str) -> List[Dict]:
        cur = self.conn.cursor()
        try:
            cur.execute("""
                SELECT file_name, operation, mode, paragraph_name, line_number
                FROM file_operations WHERE program_id = ?
                ORDER BY line_number
            """, (program_id,))
            return [dict(r) for r in cur.fetchall()]
        except Exception:
            return []

    def get_program_mq_calls(self, program_id: str) -> List[Dict]:
        cur = self.conn.cursor()
        try:
            cur.execute("""
                SELECT function_code, function_name, queue_name, queue_manager,
                       object_descriptor, message_descriptor, options_area,
                       paragraph_name, line_number
                FROM mq_calls WHERE program_id = ?
                ORDER BY line_number
            """, (program_id,))
            return [dict(r) for r in cur.fetchall()]
        except Exception:
            return []

    def get_program_evaluates(self, program_id: str) -> List[Dict]:
        cur = self.conn.cursor()
        try:
            cur.execute("""
                SELECT evaluate_id, subject, branch_index, when_condition,
                       action_summary, paragraph_name, line_number, is_default
                FROM evaluate_branches WHERE program_id = ?
                ORDER BY evaluate_id, branch_index
            """, (program_id,))
            return [dict(r) for r in cur.fetchall()]
        except Exception:
            return []

    def get_program_cics_handles(self, program_id: str) -> List[Dict]:
        cur = self.conn.cursor()
        try:
            cur.execute("""
                SELECT handle_type, condition_name, target_paragraph,
                       paragraph_name, line_number
                FROM cics_handles WHERE program_id = ?
                ORDER BY line_number
            """, (program_id,))
            return [dict(r) for r in cur.fetchall()]
        except Exception:
            return []

    def get_program_cursor_lifecycles(self, program_id: str) -> List[Dict]:
        """Pair DECLARE / OPEN / FETCH(es) / CLOSE for each cursor by name.
        Returns one row per cursor with the four phase line numbers."""
        cur = self.conn.cursor()
        try:
            cur.execute("""
                SELECT command, cursor_name, paragraph_name, line_number, table_name
                FROM exec_sql
                WHERE program_id = ? AND cursor_name IS NOT NULL
                ORDER BY cursor_name, line_number
            """, (program_id,))
            rows = [dict(r) for r in cur.fetchall()]
        except Exception:
            return []

        from collections import defaultdict
        by_cursor = defaultdict(lambda: {
            "cursor_name": None,
            "declare": None, "open": None,
            "fetch_paragraphs": [], "fetch_lines": [],
            "close": None, "table_name": None,
        })
        for r in rows:
            entry = by_cursor[r["cursor_name"]]
            entry["cursor_name"] = r["cursor_name"]
            cmd = (r["command"] or "").upper()
            if cmd == "DECLARE":
                entry["declare"] = {"paragraph": r["paragraph_name"], "line": r["line_number"]}
                entry["table_name"] = r["table_name"]
            elif cmd == "OPEN":
                entry["open"] = {"paragraph": r["paragraph_name"], "line": r["line_number"]}
            elif cmd == "FETCH":
                entry["fetch_paragraphs"].append(r["paragraph_name"])
                entry["fetch_lines"].append(r["line_number"])
            elif cmd == "CLOSE":
                entry["close"] = {"paragraph": r["paragraph_name"], "line": r["line_number"]}
        return list(by_cursor.values())

    def get_data_flow_chains(self, max_hops: int = 4) -> List[Dict]:
        """Trace end-to-end data lineage:
            JCL → program → (writes file) → program → (writes file) → ...
        Walks files written by one program back to programs that read the same name.
        Returns list of {chain: [...], starts_with_jcl: bool}."""
        cur = self.conn.cursor()
        # Build maps: who writes / reads each file (by file_name OR ddname)
        try:
            cur.execute("SELECT program_id, file_name, access_mode FROM files")
            file_rows = [dict(r) for r in cur.fetchall()]
        except Exception:
            return []

        from collections import defaultdict
        writers = defaultdict(set)   # file -> {program}
        readers = defaultdict(set)
        for r in file_rows:
            mode = (r.get("access_mode") or "").upper()
            # SEQUENTIAL access alone doesn't tell us read vs write — we use OPEN
            # statements as additional source. Heuristic: if there's any WRITE
            # in statements for that program/file, it's a writer.
            cur.execute(
                "SELECT 1 FROM statements WHERE program_id = ? AND statement_type IN ('WRITE','REWRITE') AND details_json LIKE ? LIMIT 1",
                (r["program_id"], f"%{r['file_name']}%"),
            )
            is_writer = bool(cur.fetchone())
            cur.execute(
                "SELECT 1 FROM statements WHERE program_id = ? AND statement_type='READ' AND details_json LIKE ? LIMIT 1",
                (r["program_id"], f"%{r['file_name']}%"),
            )
            is_reader = bool(cur.fetchone())
            if is_writer:
                writers[r["file_name"]].add(r["program_id"])
            if is_reader:
                readers[r["file_name"]].add(r["program_id"])
            # If we couldn't infer, assume reader (most cards-demo programs read)
            if not (is_writer or is_reader):
                readers[r["file_name"]].add(r["program_id"])

        # Map JCL job → program
        try:
            cur.execute("SELECT DISTINCT job_name, program FROM jcl_steps WHERE program IS NOT NULL")
            jcl_to_prog = [dict(r) for r in cur.fetchall()]
        except Exception:
            jcl_to_prog = []

        chains = []
        seen_chains = set()

        def _walk(prog, path, depth):
            if depth > max_hops:
                return
            # All files written by `prog` lead to readers of those files
            for fname, ws in writers.items():
                if prog not in ws:
                    continue
                for next_prog in readers.get(fname, set()):
                    if next_prog == prog or next_prog in path:
                        continue  # avoid cycles
                    new_path = path + [{"file": fname, "program": next_prog}]
                    key = "->".join([(p.get("program") or p.get("job") or p.get("file") or "?") for p in new_path])
                    if key not in seen_chains:
                        seen_chains.add(key)
                        chains.append({
                            "starts_with_jcl": new_path[0].get("job") is not None,
                            "chain": new_path,
                        })
                    _walk(next_prog, new_path, depth + 1)

        for jp in jcl_to_prog:
            start_path = [
                {"job": jp["job_name"]},
                {"program": jp["program"]},
            ]
            key = "->".join([(p.get("program") or p.get("job") or "?") for p in start_path])
            if key not in seen_chains:
                seen_chains.add(key)
                chains.append({
                    "starts_with_jcl": True,
                    "chain": start_path,
                })
            _walk(jp["program"], start_path, depth=2)

        # Also include orphan write→read pairs that aren't reached from JCL
        for fname, ws in writers.items():
            for w in ws:
                # If we never started from this writer via JCL, kick off a walk
                if not any(c["chain"] and c["chain"][-1].get("program") == w
                            for c in chains if c["starts_with_jcl"]):
                    _walk(w, [{"program": w}], depth=1)

        # Limit the size of the response
        return chains[:200]

    def get_program_anomalies(self, program_id: str) -> List[Dict]:
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT severity, category, rule_id, title, description,
                       paragraph_name, line_number, snippet, suggestion
                FROM code_anomalies
                WHERE program_id = ?
                ORDER BY CASE severity
                    WHEN 'BUG' THEN 1 WHEN 'WARNING' THEN 2 ELSE 3 END,
                    line_number
            """, (program_id,))
            return [dict(r) for r in cursor.fetchall()]
        except Exception:
            return []

    def get_program_data_movements(self, program_id: str, limit: int = 50) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT source_field, destination_field, paragraph_name, line_number, is_literal
            FROM data_movements
            WHERE program_id = ?
            ORDER BY line_number
            LIMIT ?
        """, (program_id, limit))
        return [dict(r) for r in cursor.fetchall()]

    def load_screens(self, screens: List[Dict]):
        """Load BMS screen definitions."""
        cursor = self.conn.cursor()

        # Screen rows have no natural UNIQUE constraint in the original schema.
        # Clear them before reloading so repeated pipeline runs stay idempotent.
        cursor.execute("DELETE FROM screen_fields")
        cursor.execute("DELETE FROM screens")

        for screen_data in screens:
            mapset = screen_data.get("mapset_name", "")
            for map_info in screen_data.get("maps", []):
                map_name = map_info.get("map_name", "")
                # Try to find associated program (skip FK if not found)
                prog = None
                for suffix in ["C", ""]:
                    candidate = mapset + suffix
                    cursor.execute("SELECT program_id FROM programs WHERE program_id = ?", (candidate,))
                    if cursor.fetchone():
                        prog = candidate
                        break

                cursor.execute("""
                    INSERT OR REPLACE INTO screens (
                        screen_name, map_name, mapset_name, file_path,
                        associated_program, business_name
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    map_name, map_name, mapset,
                    screen_data.get("file_path"),
                    prog, map_name
                ))

                screen_id = cursor.lastrowid

                 # Insert fields
                for fld in map_info.get("fields", []):
                    cursor.execute("""
                        INSERT OR REPLACE INTO screen_fields (
                            screen_id, field_name, field_type, length,
                            row_position, col_position, attributes,
                            business_name, description
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        screen_id,
                        fld.get("field_name"),
                        fld.get("field_type"),
                        fld.get("length"),
                        fld.get("row_position"),
                        fld.get("col_position"),
                        fld.get("attributes"),
                        fld.get("field_name"),
                        fld.get("initial_value", "")
                    ))

        self.conn.commit()
        console.print(f"[green]OK - Loaded {len(screens)} screens[/green]")

    def load_business_rules(self, rules: List[Dict]):
        """Load business rules into the database."""
        cursor = self.conn.cursor()
        for rule in rules:
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO business_rules (
                        rule_id, rule_name, rule_statement, category,
                        program_id, paragraph_name, line_start, line_end,
                        condition_text, action_text, source_code
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    rule.get("rule_id"), rule.get("rule_name"),
                    rule.get("rule_statement"), rule.get("category"),
                    rule.get("program_id"), rule.get("paragraph_name"),
                    rule.get("line_start"), rule.get("line_end"),
                    rule.get("condition"), rule.get("action"),
                    rule.get("source_code")
                ))
            except Exception as e:
                pass

        self.conn.commit()
        console.print(f"[green]OK - Loaded {len(rules)} business rules[/green]")

    def load_from_json(self, programs_json=None, rules_json=None,
                       enriched_json=None, screens_json=None):
        """Load data from JSON files."""
        if enriched_json:
            enriched_path = Path(enriched_json)
            if (enriched_path / "enriched_programs.json").exists():
                programs_json = str(enriched_path / "enriched_programs.json")
            if (enriched_path / "business_rules.json").exists():
                rules_json = str(enriched_path / "business_rules.json")

        if programs_json and Path(programs_json).exists():
            with open(programs_json, 'r') as f:
                raw = json.load(f)
            # Deduplicate: keep the entry with the most enrichment (has business_purpose)
            seen = {}
            for p in raw:
                pid = p.get("program_id", "")
                if pid not in seen or (p.get("business_purpose") and not seen[pid].get("business_purpose")):
                    seen[pid] = p
            self.load_programs(list(seen.values()))

        if rules_json and Path(rules_json).exists():
            with open(rules_json, 'r') as f:
                self.load_business_rules(json.load(f))

        if screens_json and Path(screens_json).exists():
            with open(screens_json, 'r') as f:
                self.load_screens(json.load(f))

    # ================================================================
    # Query Methods
    # ================================================================

    def get_generated_doc(self, mode: str, subject: str) -> Optional[str]:
        """Retrieve a previously saved generated document, or None if not found."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "SELECT document_text FROM generated_docs WHERE mode = ? AND subject = ?",
                (mode, subject)
            )
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception:
            return None

    def get_generated_doc_metadata(self, mode: str, subject: str) -> Dict:
        """Retrieve saved context / coverage metadata for a generated document."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
                SELECT context_metadata_json, coverage_ledger_json
                FROM generated_docs
                WHERE mode = ? AND subject = ?
                """,
                (mode, subject),
            )
            row = cursor.fetchone()
            if not row:
                return {}
            context_meta = json.loads(row[0] or "{}")
            coverage = json.loads(row[1] or "{}")
            return {"context_metadata": context_meta, "coverage_ledger": coverage}
        except Exception:
            return {}

    def save_generated_doc(self, mode: str, subject: str, text: str,
                           context_metadata: Optional[Dict] = None,
                           coverage_ledger: Optional[Dict] = None):
        """Save or overwrite a generated document in the DB."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO generated_docs (
                mode, subject, document_text, context_metadata_json, coverage_ledger_json, generated_at
            )
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (
            mode,
            subject,
            text,
            json.dumps(context_metadata or {}, default=str),
            json.dumps(coverage_ledger or {}, default=str),
        ))
        self.conn.commit()

    def get_all_programs(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT program_id, file_path, program_type, line_count,
                   business_name, business_purpose, user_role, business_process,
                   migration_complexity, complexity_reason, modern_equivalent,
                   suggested_service, migration_approach, data_contracts, migration_risks
            FROM programs ORDER BY program_id
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_program_details(self, program_id: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM programs WHERE program_id = ?", (program_id,))
        program = cursor.fetchone()
        if not program:
            return None
        result = dict(program)

        for key, query in [
            ("paragraphs", "SELECT * FROM paragraphs WHERE program_id = ? ORDER BY line_start"),
            ("data_items", "SELECT * FROM data_items WHERE program_id = ? ORDER BY line_number"),
            ("files", "SELECT * FROM files WHERE program_id = ?"),
            ("statements", "SELECT * FROM statements WHERE program_id = ? ORDER BY line_number"),
            ("calls", "SELECT * FROM program_calls WHERE caller_program = ?"),
            ("called_by", "SELECT * FROM program_calls WHERE called_program = ?"),
            ("copybooks", "SELECT * FROM copybook_usage WHERE program_id = ? ORDER BY copybook_name"),
            ("performs", "SELECT * FROM performs WHERE program_id = ?"),
            ("business_rules", "SELECT * FROM business_rules WHERE program_id = ?"),
            ("exec_cics", "SELECT * FROM exec_cics WHERE program_id = ? ORDER BY line_number"),
            ("exec_sql",  "SELECT * FROM exec_sql  WHERE program_id = ? ORDER BY line_number"),
            ("ims_calls", "SELECT * FROM ims_calls WHERE program_id = ? ORDER BY line_number"),
        ]:
            cursor.execute(query, (program_id,))
            result[key] = [dict(row) for row in cursor.fetchall()]

        return result

    def get_call_graph(self) -> List[Dict]:
        """Return call edges. If called_program == 'UNKNOWN' but resolved_target is set,
        substitute the resolved target so downstream consumers see a real program ID."""
        cursor = self.conn.cursor()
        # COALESCE picks resolved_target when called_program is UNKNOWN
        cursor.execute("""
            SELECT pc.caller_program,
                   p1.business_name as caller_name,
                   CASE
                     WHEN pc.called_program = 'UNKNOWN' AND pc.resolved_target IS NOT NULL
                     THEN pc.resolved_target
                     ELSE pc.called_program
                   END as called_program,
                   p2.business_name as called_name,
                   pc.line_number,
                   pc.resolved_target,
                   pc.called_program as raw_target
            FROM program_calls pc
            LEFT JOIN programs p1 ON pc.caller_program = p1.program_id
            LEFT JOIN programs p2 ON
                (CASE
                   WHEN pc.called_program = 'UNKNOWN' AND pc.resolved_target IS NOT NULL
                   THEN pc.resolved_target ELSE pc.called_program END
                ) = p2.program_id
            ORDER BY pc.caller_program
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_all_business_rules(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT br.*, p.business_name as program_business_name
            FROM business_rules br
            LEFT JOIN programs p ON br.program_id = p.program_id
            ORDER BY br.category, br.rule_id
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_data_dictionary(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT di.name, di.picture, di.section, di.level_number,
                   di.parent_name, di.business_name, di.description,
                   di.program_id, p.business_name as program_business_name
            FROM data_items di
            LEFT JOIN programs p ON di.program_id = p.program_id
            ORDER BY di.name
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_all_screens(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT s.*, GROUP_CONCAT(sf.field_name, ', ') as field_names
            FROM screens s
            LEFT JOIN screen_fields sf ON s.id = sf.screen_id
            GROUP BY s.id
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_screen_details(self, screen_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM screens WHERE id = ?", (screen_id,))
        screen = cursor.fetchone()
        if not screen:
            return None
        result = dict(screen)
        cursor.execute("SELECT * FROM screen_fields WHERE screen_id = ? ORDER BY row_position, col_position",
                       (screen_id,))
        result["fields"] = [dict(row) for row in cursor.fetchall()]
        return result

    def get_program_statements(self, program_id: str, stmt_type: str = None) -> List[Dict]:
        """Get statements for a program, optionally filtered by type."""
        cursor = self.conn.cursor()
        if stmt_type:
            cursor.execute("""
                SELECT * FROM statements WHERE program_id = ? AND statement_type = ?
                ORDER BY line_number
            """, (program_id, stmt_type))
        else:
            cursor.execute("""
                SELECT * FROM statements WHERE program_id = ? ORDER BY line_number
            """, (program_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_all_modules(self) -> List[Dict]:
        """Get all modules with their programs."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT m.id, m.module_name, m.business_name, m.description, m.business_purpose
            FROM modules m ORDER BY m.module_name
        """)
        modules = []
        for row in cursor.fetchall():
            mod = dict(row)
            cursor.execute("""
                SELECT mp.program_id, p.program_type, p.line_count,
                       p.business_name, p.business_purpose
                FROM module_programs mp
                LEFT JOIN programs p ON mp.program_id = p.program_id
                WHERE mp.module_id = ?
                ORDER BY mp.program_id
            """, (mod["id"],))
            mod["programs"] = [dict(r) for r in cursor.fetchall()]
            modules.append(mod)
        return modules

    def get_module_details(self, module_id: int) -> Optional[Dict]:
        """Get full module details including programs, calls, files."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM modules WHERE id = ?", (module_id,))
        row = cursor.fetchone()
        if not row:
            return None
        mod = dict(row)

        # Get programs in module
        cursor.execute("""
            SELECT mp.program_id, p.program_type, p.line_count, p.file_path,
                   p.business_name, p.business_purpose, p.user_role
            FROM module_programs mp
            LEFT JOIN programs p ON mp.program_id = p.program_id
            WHERE mp.module_id = ?
            ORDER BY mp.program_id
        """, (module_id,))
        mod["programs"] = [dict(r) for r in cursor.fetchall()]

        # Get inter-module calls (calls from programs in this module)
        prog_ids = [p["program_id"] for p in mod["programs"]]
        if prog_ids:
            placeholders = ",".join("?" * len(prog_ids))
            cursor.execute(f"""
                SELECT DISTINCT pc.caller_program, pc.called_program, pc.line_number
                FROM program_calls pc
                WHERE pc.caller_program IN ({placeholders})
                ORDER BY pc.caller_program, pc.called_program
            """, prog_ids)
            mod["calls"] = [dict(r) for r in cursor.fetchall()]

            # Files used by module programs
            cursor.execute(f"""
                SELECT DISTINCT f.file_name, f.file_type, f.access_mode, f.program_id
                FROM files f
                WHERE f.program_id IN ({placeholders})
                ORDER BY f.file_name
            """, prog_ids)
            mod["files"] = [dict(r) for r in cursor.fetchall()]

            # Screens associated with module programs
            cursor.execute(f"""
                SELECT s.id, s.screen_name, s.map_name, s.mapset_name,
                       s.associated_program, s.business_name
                FROM screens s
                WHERE s.associated_program IN ({placeholders})
            """, prog_ids)
            mod["screens"] = [dict(r) for r in cursor.fetchall()]
        else:
            mod["calls"] = []
            mod["files"] = []
            mod["screens"] = []

        return mod

    def get_copybooks(self) -> List[Dict]:
        """Get all copybooks with usage info."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.copybook_name, c.file_path, c.business_name, c.description,
                   GROUP_CONCAT(cu.program_id, ', ') as used_by
            FROM copybooks c
            LEFT JOIN copybook_usage cu ON c.copybook_name = cu.copybook_name
            GROUP BY c.copybook_name
            ORDER BY c.copybook_name
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_statement_summary(self, program_id: str) -> Dict[str, int]:
        """Get summary counts of statement types for a program."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT statement_type, COUNT(*) as cnt
            FROM statements WHERE program_id = ?
            GROUP BY statement_type ORDER BY cnt DESC
        """, (program_id,))
        return {row[0]: row[1] for row in cursor.fetchall()}

    # ================================================================
    # Graph-Based Module Detection (Swimm-style)
    # ================================================================

    def detect_modules(self) -> List[Dict]:
        """
        Detect logical modules using call graph analysis, naming patterns,
        and data access similarity -- not just 2-char prefix matching.
        """
        cursor = self.conn.cursor()

        # Ensure module tables exist even if the database was created
        # with an older schema that didn't include them.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_name TEXT NOT NULL,
                business_name TEXT,
                description TEXT,
                business_purpose TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS module_programs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id INTEGER NOT NULL,
                program_id TEXT NOT NULL,
                FOREIGN KEY(module_id) REFERENCES modules(id) ON DELETE CASCADE,
                FOREIGN KEY(program_id) REFERENCES programs(program_id) ON DELETE CASCADE
            )
        """)

        # Get all programs
        cursor.execute("SELECT program_id, program_type, file_path FROM programs")
        all_programs = {row[0]: {"type": row[1], "path": row[2]} for row in cursor.fetchall()}

        # Get call graph
        cursor.execute("SELECT caller_program, called_program FROM program_calls")
        calls = cursor.fetchall()

        # Get file usage
        cursor.execute("SELECT program_id, file_name FROM files")
        file_usage = defaultdict(set)
        for row in cursor.fetchall():
            file_usage[row[0]].add(row[1])

        # Build adjacency for clustering
        connected = defaultdict(set)
        for caller, called in calls:
            connected[caller].add(called)
            connected[called].add(caller)

        # Strategy 1: Name-based functional grouping — fully generic.
        #
        # Algorithm:
        #  (a) Group programs by their longest meaningful prefix. We try a 5-char
        #      prefix first; if a 5-char prefix has fewer than 2 members, fall
        #      back to 4-char, then 3-char, then 2-char.
        #  (b) Programs whose 2-char prefix has >= 2 members are kept under that
        #      key; loners go to a single "OTHER" bucket.
        #
        # This works on any codebase — no hardcoded application-specific strings.
        func_groups = defaultdict(list)

        # Pre-compute prefix counts at multiple lengths
        from collections import Counter
        prefix_counts = {n: Counter(p[:n] for p in all_programs if len(p) >= n)
                          for n in (5, 4, 3, 2)}

        for pid in all_programs:
            assigned_prefix = None
            for n in (5, 4, 3, 2):
                if len(pid) < n:
                    continue
                pref = pid[:n]
                if prefix_counts[n].get(pref, 0) >= 2:
                    assigned_prefix = pref
                    break
            if assigned_prefix:
                func_groups[assigned_prefix.upper()].append(pid)
            else:
                func_groups["OTHER"].append(pid)

        # Strategy 2: Module names. Three signals, in priority order:
        #   (a) LLM-enriched business_name shared across the group
        #   (b) Common token across paragraph names of all programs in the group
        #       (e.g. CBACT* programs all have paragraphs containing 'ACCT')
        #   (c) Fall back to "Module <prefix>"
        import re
        cursor.execute("SELECT program_id, business_name FROM programs")
        biz_names = {r[0]: (r[1] or "") for r in cursor.fetchall()}

        cursor.execute("SELECT program_id, paragraph_name FROM paragraphs")
        paras_by_prog = defaultdict(list)
        for r in cursor.fetchall():
            paras_by_prog[r[0]].append(r[1])

        STOP_WORDS = {
            "the", "and", "for", "with", "from", "into", "this", "that", "exit",
            "main", "open", "close", "read", "write", "init", "process", "control",
            "end", "loop", "next", "find", "get", "set", "put", "out", "step",
            "abend", "display", "status",
        }

        def _common_token_from_strings(strings):
            tokens_sets = []
            for s in strings:
                toks = [t.lower() for t in re.split(r"[\s\-_,.0-9]+", s or "")
                         if len(t) >= 3 and t.isalnum()]
                toks = [t for t in toks if t not in STOP_WORDS]
                if toks:
                    tokens_sets.append(set(toks))
            if not tokens_sets:
                return None
            common = set.intersection(*tokens_sets) if len(tokens_sets) > 1 else tokens_sets[0]
            return max(common, key=len) if common else None

        def _shared_name(group):
            # (a) From business_name
            tok = _common_token_from_strings([biz_names.get(p, "") for p in group])
            if tok:
                return tok.title()
            # (b) From paragraph names — collect ALL paragraphs and find a token
            #     present in every program of the group
            tokens_per_prog = []
            for pid in group:
                pset = set()
                for pname in paras_by_prog.get(pid, []):
                    for t in re.split(r"[\s\-_,.0-9]+", pname or ""):
                        tl = t.lower()
                        if len(tl) >= 3 and tl.isalnum() and tl not in STOP_WORDS:
                            pset.add(tl)
                if pset:
                    tokens_per_prog.append(pset)
            if tokens_per_prog:
                common = set.intersection(*tokens_per_prog) if len(tokens_per_prog) > 1 else tokens_per_prog[0]
                if common:
                    return max(common, key=len).title()
            return None

        module_names = {}
        for key, group in func_groups.items():
            label = _shared_name(group)
            if label:
                # Disambiguate when multiple groups derive the same label
                base = label
                idx = 2
                while label in module_names.values():
                    label = f"{base} ({key})"
                    idx += 1
                    if idx > 5: break
                module_names[key] = label
            elif key == "OTHER":
                module_names[key] = "Other Programs"
            else:
                module_names[key] = f"Module {key}"

        # Build result
        modules = []
        for mod_id, progs in sorted(func_groups.items()):
            if not progs:
                continue
            modules.append({
                "module_id": mod_id,
                "module_name": module_names.get(mod_id, f"Module: {mod_id}"),
                "programs": sorted(progs),
                "program_count": len(progs),
            })

        # Save to DB (tables might not exist in very old DBs)
        try:
            cursor.execute("DELETE FROM modules")
        except Exception:
            pass
        try:
            cursor.execute("DELETE FROM module_programs")
        except Exception:
            pass
        # Best-effort persistence of detected modules.
        # If the schema doesn't match (older DB), skip writing but still
        # return the in-memory modules list so callers can proceed.
        try:
            for mod in modules:
                cursor.execute("""
                    INSERT INTO modules (module_name, business_name, description, business_purpose)
                    VALUES (?, ?, ?, ?)
                """, (mod["module_id"], mod["module_name"], "", mod["module_name"]))
                mod_db_id = cursor.lastrowid
                for pid in mod["programs"]:
                    try:
                        cursor.execute(
                            "INSERT INTO module_programs (module_id, program_id) VALUES (?, ?)",
                            (mod_db_id, pid),
                        )
                    except Exception:
                        # Ignore individual mapping failures
                        pass
            self.conn.commit()
        except Exception as e:
            # Log and continue without failing module detection
            console.print(f"[yellow]Warning: module persistence skipped due to schema issue: {e}[/yellow]")

        return modules

    # ================================================================
    # Full-Text Search
    # ================================================================

    def full_text_search(self, query: str) -> Dict[str, List]:
        cursor = self.conn.cursor()
        results = {}
        for table, fields in [
            ("programs_fts", "program_id, business_name, business_purpose"),
            ("data_items_fts", "name, business_name, description"),
            ("business_rules_fts", "rule_name, rule_statement"),
        ]:
            try:
                cursor.execute(f"SELECT {fields} FROM {table} WHERE {table} MATCH ?", (query,))
                results[table.replace("_fts", "")] = [dict(row) for row in cursor.fetchall()]
            except:
                results[table.replace("_fts", "")] = []
        return results

    # ================================================================
    # Dependency & Impact Analysis (for doc generation)
    # ================================================================

    def get_program_dependencies(self, program_id: str) -> Dict:
        """Get direct callers and callees with business context."""
        cursor = self.conn.cursor()

        # Direct callers
        cursor.execute("""
            SELECT pc.caller_program, pc.call_location, pc.line_number,
                   p.business_name, p.program_type, p.business_purpose
            FROM program_calls pc
            LEFT JOIN programs p ON pc.caller_program = p.program_id
            WHERE pc.called_program = ?
            ORDER BY pc.caller_program
        """, (program_id,))
        callers = [dict(r) for r in cursor.fetchall()]

        # Direct callees
        cursor.execute("""
            SELECT pc.called_program, pc.call_location, pc.line_number,
                   p.business_name, p.program_type, p.business_purpose
            FROM program_calls pc
            LEFT JOIN programs p ON pc.called_program = p.program_id
            WHERE pc.caller_program = ?
            ORDER BY pc.called_program
        """, (program_id,))
        callees = [dict(r) for r in cursor.fetchall()]

        return {"callers": callers, "callees": callees}

    def get_shared_data_context(self, program_id: str) -> Dict:
        """Get copybooks and files used by this program with co-users."""
        cursor = self.conn.cursor()

        # Copybooks used by this program + other programs sharing them
        cursor.execute("""
            SELECT cu.copybook_name
            FROM copybook_usage cu
            WHERE cu.program_id = ?
            ORDER BY cu.copybook_name
        """, (program_id,))
        my_copybooks = [row[0] for row in cursor.fetchall()]

        shared_copybooks = []
        for cb in my_copybooks:
            cursor.execute("""
                SELECT cu.program_id, p.business_name
                FROM copybook_usage cu
                LEFT JOIN programs p ON cu.program_id = p.program_id
                WHERE cu.copybook_name = ? AND cu.program_id != ?
                ORDER BY cu.program_id
            """, (cb, program_id))
            co_users = [dict(r) for r in cursor.fetchall()]
            shared_copybooks.append({
                "copybook_name": cb,
                "co_users": co_users,
                "co_user_count": len(co_users),
            })

        # Files used by this program + other programs sharing them
        cursor.execute("""
            SELECT f.file_name, f.file_type, f.access_mode
            FROM files f
            WHERE f.program_id = ?
            ORDER BY f.file_name
        """, (program_id,))
        my_files = [dict(r) for r in cursor.fetchall()]

        shared_files = []
        for f in my_files:
            cursor.execute("""
                SELECT f2.program_id, p.business_name, f2.access_mode
                FROM files f2
                LEFT JOIN programs p ON f2.program_id = p.program_id
                WHERE f2.file_name = ? AND f2.program_id != ?
                ORDER BY f2.program_id
            """, (f["file_name"], program_id))
            co_users = [dict(r) for r in cursor.fetchall()]
            shared_files.append({
                **f,
                "co_users": co_users,
                "co_user_count": len(co_users),
            })

        return {"shared_copybooks": shared_copybooks, "shared_files": shared_files}

    def get_impact_analysis(self, program_id: str) -> Dict:
        """Compute transitive impact: what breaks if this program changes."""
        cursor = self.conn.cursor()

        # Build full adjacency from DB
        cursor.execute("SELECT caller_program, called_program FROM program_calls")
        calls_out = defaultdict(set)
        called_by = defaultdict(set)
        for row in cursor.fetchall():
            calls_out[row[0]].add(row[1])
            called_by[row[1]].add(row[0])

        # Build copybook coupling
        cursor.execute("SELECT copybook_name, program_id FROM copybook_usage")
        cb_to_progs = defaultdict(set)
        prog_to_cbs = defaultdict(set)
        for row in cursor.fetchall():
            cb_to_progs[row[0]].add(row[1])
            prog_to_cbs[row[1]].add(row[0])

        # All known programs
        cursor.execute("SELECT program_id FROM programs")
        all_programs = set(row[0] for row in cursor.fetchall())

        def transitive(pid, graph):
            visited = set()
            stack = list(graph.get(pid, set()))
            while stack:
                nxt = stack.pop()
                if nxt not in visited and nxt in all_programs:
                    visited.add(nxt)
                    stack.extend(graph.get(nxt, set()) - visited)
            return visited

        def cb_impact(pid):
            affected = set()
            for cb in prog_to_cbs.get(pid, set()):
                affected.update(cb_to_progs.get(cb, set()))
            affected.discard(pid)
            return affected

        direct_callers = called_by.get(program_id, set()) & all_programs
        trans_callers = transitive(program_id, called_by)
        direct_callees = calls_out.get(program_id, set()) & all_programs
        trans_callees = transitive(program_id, calls_out)
        coupling = cb_impact(program_id)
        total_impact = len(trans_callers | coupling)

        if total_impact >= 10:
            risk = "HIGH"
        elif total_impact >= 5:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        return {
            "direct_callers": sorted(direct_callers),
            "transitive_callers": sorted(trans_callers),
            "direct_callees": sorted(direct_callees),
            "transitive_callees": sorted(trans_callees),
            "copybook_coupling": sorted(coupling),
            "total_impact": total_impact,
            "risk": risk,
        }

    def get_linked_clusters(self) -> List[Dict]:
        """Find connected components in the call + copybook graph."""
        cursor = self.conn.cursor()

        cursor.execute("SELECT program_id, business_name, program_type FROM programs")
        all_programs = {row[0]: {"business_name": row[1], "program_type": row[2]}
                        for row in cursor.fetchall()}

        # Build undirected adjacency from calls
        adj = defaultdict(set)
        cursor.execute("SELECT caller_program, called_program FROM program_calls")
        for row in cursor.fetchall():
            if row[0] in all_programs and row[1] in all_programs:
                adj[row[0]].add(row[1])
                adj[row[1]].add(row[0])

        # Add copybook coupling edges
        cursor.execute("SELECT copybook_name, program_id FROM copybook_usage")
        cb_map = defaultdict(set)
        for row in cursor.fetchall():
            if row[1] in all_programs:
                cb_map[row[0]].add(row[1])
        for cb, progs in cb_map.items():
            prog_list = list(progs)
            for i in range(len(prog_list)):
                for j in range(i + 1, len(prog_list)):
                    adj[prog_list[i]].add(prog_list[j])
                    adj[prog_list[j]].add(prog_list[i])

        # BFS to find connected components
        visited = set()
        clusters = []
        for pid in sorted(all_programs.keys()):
            if pid in visited:
                continue
            component = set()
            queue = [pid]
            while queue:
                node = queue.pop(0)
                if node in visited:
                    continue
                visited.add(node)
                component.add(node)
                queue.extend(adj.get(node, set()) - visited)
            clusters.append(sorted(component))

        # Build cluster details
        result = []
        for idx, members in enumerate(clusters, 1):
            # Gather inter-cluster calls
            member_set = set(members)
            cursor.execute(
                "SELECT caller_program, called_program, line_number FROM program_calls "
                "WHERE caller_program IN ({seq}) AND called_program IN ({seq})".format(
                    seq=",".join("?" * len(members))),
                members + members)
            internal_calls = [dict(r) for r in cursor.fetchall()]

            # Shared copybooks within cluster
            if members:
                cursor.execute(
                    "SELECT copybook_name, GROUP_CONCAT(program_id) as programs "
                    "FROM copybook_usage WHERE program_id IN ({seq}) "
                    "GROUP BY copybook_name HAVING COUNT(DISTINCT program_id) > 1".format(
                        seq=",".join("?" * len(members))),
                    members)
                shared_cbs = [dict(r) for r in cursor.fetchall()]
            else:
                shared_cbs = []

            result.append({
                "cluster_id": idx,
                "members": members,
                "member_details": [
                    {"program_id": m, **all_programs.get(m, {})} for m in members
                ],
                "size": len(members),
                "internal_calls": internal_calls,
                "shared_copybooks": shared_cbs,
                "is_standalone": len(members) == 1,
            })

        # Sort: largest clusters first, standalones last
        result.sort(key=lambda c: (-c["size"], c["cluster_id"]))
        return result


    # ================================================================
    # JCL Loading & Queries
    # ================================================================

    def load_jcl(self, jcl_jobs: List[Dict]):
        """Load parsed JCL jobs, steps, and datasets into SQLite."""
        if not jcl_jobs:
            return
        cursor = self.conn.cursor()

        # Ensure JCL tables exist (schema may have been created before JCL support)
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS jcl_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name TEXT UNIQUE NOT NULL,
                file_name TEXT, file_path TEXT, file_hash TEXT,
                job_description TEXT, job_class TEXT, msg_class TEXT,
                header_comments TEXT, programs_called TEXT,
                input_datasets TEXT, output_datasets TEXT,
                step_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS jcl_steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name TEXT NOT NULL, step_name TEXT NOT NULL, step_order INTEGER,
                program TEXT, proc TEXT, step_type TEXT,
                step_comments TEXT, cond TEXT, line_number INTEGER, sysin_data TEXT,
                UNIQUE(job_name, step_name)
            );
            CREATE TABLE IF NOT EXISTS jcl_datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name TEXT NOT NULL, step_name TEXT NOT NULL, dd_name TEXT,
                dsn TEXT, disp TEXT, disposition_normal TEXT, disposition_abnormal TEXT,
                direction TEXT, recfm TEXT, lrecl TEXT, unit TEXT, space TEXT,
                is_inline INTEGER DEFAULT 0
            );
        """)
        self.conn.commit()

        for job in jcl_jobs:
            job_name = job.get("job_name", "")
            if not job_name:
                continue

            # Upsert job row
            cursor.execute("DELETE FROM jcl_datasets WHERE job_name = ?", (job_name,))
            cursor.execute("DELETE FROM jcl_steps    WHERE job_name = ?", (job_name,))
            cursor.execute("DELETE FROM jcl_jobs     WHERE job_name = ?", (job_name,))

            steps = job.get("steps") or []
            cursor.execute("""
                INSERT INTO jcl_jobs (
                    job_name, file_name, file_path, file_hash,
                    job_description, job_class, msg_class, header_comments,
                    programs_called, input_datasets, output_datasets, step_count
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                job_name,
                job.get("file_name"), job.get("file_path"), job.get("file_hash"),
                job.get("job_description"), job.get("job_class"), job.get("msg_class"),
                "\n".join(job.get("comment_lines") or []),
                json.dumps(job.get("programs_called") or []),
                json.dumps(job.get("input_datasets") or []),
                json.dumps(job.get("output_datasets") or []),
                len(steps),
            ))

            for order, step in enumerate(steps, 1):
                step_name = step.get("step_name", f"STEP{order}")
                cursor.execute("""
                    INSERT OR REPLACE INTO jcl_steps (
                        job_name, step_name, step_order, program, proc,
                        step_type, step_comments, cond, line_number, sysin_data
                    ) VALUES (?,?,?,?,?,?,?,?,?,?)
                """, (
                    job_name, step_name, order,
                    step.get("program"), step.get("proc"),
                    step.get("step_type"),
                    "\n".join(step.get("comment_lines") or []),
                    step.get("cond"), step.get("line_number"),
                    json.dumps(step.get("sysin_data") or []),
                ))

                for ds in (step.get("datasets") or []):
                    cursor.execute("""
                        INSERT INTO jcl_datasets (
                            job_name, step_name, dd_name, dsn, disp,
                            disposition_normal, disposition_abnormal, direction,
                            recfm, lrecl, unit, space, is_inline
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (
                        job_name, step_name,
                        ds.get("dd_name"), ds.get("dsn"), ds.get("disp"),
                        ds.get("disposition_normal"), ds.get("disposition_abnormal"),
                        ds.get("direction"), ds.get("recfm"), ds.get("lrecl"),
                        ds.get("unit"), ds.get("space"),
                        1 if ds.get("is_inline") else 0,
                    ))

        self.conn.commit()
        console.print(f"[green]OK - Loaded {len(jcl_jobs)} JCL jobs into database[/green]")

    def get_all_jcl_jobs(self) -> List[Dict]:
        """Return all JCL jobs with their parsed programs_called / datasets."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT job_name, file_name, file_path, job_description,
                       job_class, msg_class, header_comments,
                       programs_called, input_datasets, output_datasets, step_count
                FROM jcl_jobs ORDER BY job_name
            """)
            rows = [dict(r) for r in cursor.fetchall()]
            for row in rows:
                for f in ("programs_called", "input_datasets", "output_datasets"):
                    try:
                        row[f] = json.loads(row[f] or "[]")
                    except Exception:
                        row[f] = []
            return rows
        except Exception:
            return []

    def get_jcl_job_details(self, job_name: str) -> Optional[Dict]:
        """Return a JCL job with all its steps and datasets."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM jcl_jobs WHERE job_name = ?", (job_name,))
            row = cursor.fetchone()
            if not row:
                return None
            job = dict(row)
            for f in ("programs_called", "input_datasets", "output_datasets"):
                try:
                    job[f] = json.loads(job.get(f) or "[]")
                except Exception:
                    job[f] = []

            cursor.execute("""
                SELECT * FROM jcl_steps WHERE job_name = ? ORDER BY step_order
            """, (job_name,))
            steps = [dict(r) for r in cursor.fetchall()]
            for step in steps:
                try:
                    step["sysin_data"] = json.loads(step.get("sysin_data") or "[]")
                except Exception:
                    step["sysin_data"] = []
                cursor.execute("""
                    SELECT * FROM jcl_datasets
                    WHERE job_name = ? AND step_name = ? ORDER BY id
                """, (job_name, step["step_name"]))
                step["datasets"] = [dict(r) for r in cursor.fetchall()]
            job["steps"] = steps
            return job
        except Exception:
            return None

    def get_program_jcl_jobs(self, program_id: str) -> List[Dict]:
        """Return all JCL jobs that execute a given COBOL program."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT j.job_name, j.file_name, j.job_description,
                                s.step_name, s.step_order, s.step_comments
                FROM jcl_jobs j
                JOIN jcl_steps s ON j.job_name = s.job_name
                WHERE UPPER(s.program) = UPPER(?)
                ORDER BY j.job_name, s.step_order
            """, (program_id,))
            return [dict(r) for r in cursor.fetchall()]
        except Exception:
            return []


# CLI
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Load COBOL data into SQLite")
    parser.add_argument("--db", default="data/cobol_knowledge.db")
    parser.add_argument("--schema", default="schemas/cobol_knowledge.sql")
    parser.add_argument("--programs", help="programs.json path")
    parser.add_argument("--screens", help="screens.json path")
    parser.add_argument("--rules", help="business_rules.json path")
    parser.add_argument("--enriched", help="enriched output directory")
    args = parser.parse_args()

    loader = SQLiteLoader(args.db, args.schema)
    loader.connect()
    loader.load_from_json(programs_json=args.programs, rules_json=args.rules,
                          enriched_json=args.enriched, screens_json=args.screens)
    if args.programs:
        modules = loader.detect_modules()
        print(f"Detected {len(modules)} modules")
    loader.close()
