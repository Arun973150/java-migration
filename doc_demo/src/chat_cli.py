"""
COBOL Knowledge Base Chat CLI
RAG-powered conversational interface over the SQLite knowledge base.

Features:
  - FTS5 full-text search across programs, data items, business rules
  - Smart query routing (detects "who calls X", "what does X do", etc.)
  - Groq LLM (Llama 3.1) for natural language answers
  - Search-only fallback when no API key is available
  - Interactive REPL with special commands

Usage:
  python src/chat_cli.py --db data/cobol_knowledge.db
  python src/chat_cli.py --db data/cobol_knowledge.db --no-llm
"""

import os
import re
import sys
import json
import sqlite3
import textwrap
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.text import Text
from rich import box

console = Console(force_terminal=True, highlight=False, legacy_windows=False)


# ============================================================
# Query Router — classifies user questions
# ============================================================

class QueryRouter:
    """Routes natural language queries to the best retrieval strategy."""

    PATTERNS = [
        # Program-specific queries
        (r"(?:what|tell me about|describe|explain)\s+(?:does\s+)?(\w+)\s*(?:do|program)?",
         "program_detail", 1),
        (r"(?:show|get|display)\s+(?:me\s+)?(?:program\s+)?(\w+)",
         "program_detail", 1),

        # Call graph queries
        (r"(?:who|what)\s+(?:calls?|invokes?)\s+(\w+)",
         "called_by", 1),
        (r"(?:what|which)\s+(?:programs?\s+)?(?:does\s+)?(\w+)\s+call",
         "calls_from", 1),
        (r"(?:call\s*(?:graph|tree|hierarchy)|dependencies)\s*(?:for|of)?\s*(\w+)?",
         "call_graph", 1),

        # Data items
        (r"(?:data\s*items?|variables?|fields?)\s+(?:in|for|of)\s+(\w+)",
         "data_items", 1),
        (r"(?:what\s+is|define|meaning\s+of)\s+(\w[\w-]+)",
         "data_lookup", 1),

        # Business rules
        (r"(?:business\s*rules?|rules?)\s+(?:in|for|of)\s+(\w+)",
         "business_rules", 1),
        (r"(?:validation|calculation|workflow|compliance)\s+rules?",
         "rules_by_category", 0),

        # Screens
        (r"(?:screen|map|bms)\s+(\w+)",
         "screen_detail", 1),

        # Paragraphs / control flow
        (r"(?:paragraphs?|sections?|control\s*flow)\s+(?:in|for|of)\s+(\w+)",
         "paragraphs", 1),

        # Files / IO
        (r"(?:files?|io|vsam|sequential)\s+(?:in|for|of|used\s+by)\s+(\w+)",
         "file_io", 1),

        # General / overview
        (r"(?:how\s+many|count|total|overview|summary|statistics)",
         "overview", 0),

        # JSON / parsed data queries
        (r"(?:show|get|display|view)\s+(?:raw\s+)?(?:json|parsed|ast)\s+(?:for\s+|of\s+)?(\w+)",
         "json_translate", 1),
        (r"(?:translate|explain)\s+(?:the\s+)?(?:json|parsed\s+data|parsed)\s+(?:for\s+|of\s+)?(\w+)",
         "json_translate", 1),

        # Neo4j graph queries
        (r"(?:shortest\s*path|path)\s+(?:between|from)\s+(\w+)\s+(?:and|to)\s+(\w+)",
         "graph_path", 1),
        (r"(?:blast\s*radius|full\s+impact|graph\s+impact)\s+(?:for\s+|of\s+)?(\w+)",
         "graph_impact", 1),
        (r"(?:graph|neo4j)\s+(?:deps?|dependencies)\s+(?:for\s+|of\s+)?(\w+)",
         "graph_deps", 1),
    ]

    @classmethod
    def route(cls, question: str, current_program: str = None) -> Tuple[str, Optional[str]]:
        """Return (strategy, target_id) for the question."""
        q = question.strip().lower()

        # Context injection
        if current_program:
            # Replace pronouns with the current program ID
            q = re.sub(r'\b(this program|this|it)\b', current_program.lower(), q)

        for pattern, strategy, group_idx in cls.PATTERNS:
            m = re.search(pattern, q, re.IGNORECASE)
            if m:
                target = m.group(group_idx).upper() if group_idx and m.lastindex >= group_idx else None
                return strategy, target
        return "fts_search", None


# ============================================================
# Knowledge Base Chat Engine
# ============================================================

class KnowledgeBaseChat:
    """RAG chat engine over the COBOL SQLite knowledge base."""

    def __init__(self, db_path: str, groq_api_key: str = None,
                 model: str = "llama-3.1-8b-instant", connection: sqlite3.Connection = None):
        self.db_path = db_path
        self.groq_api_key = groq_api_key
        self.model = model
        self.llm_client = None
        self.history: List[Dict[str, str]] = []
        self.neo4j_driver = None
        self.json_translator = None

        # Connect to SQLite
        if connection:
            self.conn = connection
        else:
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        # Initialize Groq client if key is available
        if groq_api_key:
            try:
                from groq import Groq
                self.llm_client = Groq(api_key=groq_api_key)
            except ImportError:
                console.print("[yellow]⚠ groq package not installed. Using search-only mode.[/yellow]")
                console.print("[dim]  Install with: pip install groq[/dim]")
            except Exception as e:
                console.print(f"[yellow]⚠ Could not initialize Groq: {e}. Using search-only mode.[/yellow]")

        # Initialize JSON translator
        try:
            from src.json_translator import JsonTranslator
            self.json_translator = JsonTranslator()
        except Exception:
            try:
                from json_translator import JsonTranslator
                self.json_translator = JsonTranslator()
            except Exception:
                pass  # JSON translator not available

        # Try connecting to Neo4j
        self._init_neo4j()

    def _init_neo4j(self):
        """Try to connect to Neo4j if credentials are available."""
        try:
            uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
            user = os.environ.get("NEO4J_USER", "neo4j")
            password = os.environ.get("NEO4J_PASSWORD", "password")
            from neo4j import GraphDatabase
            driver = GraphDatabase.driver(uri, auth=(user, password))
            with driver.session() as session:
                session.run("RETURN 1")
            self.neo4j_driver = driver
        except Exception:
            self.neo4j_driver = None  # Neo4j not available

    @property
    def neo4j_available(self) -> bool:
        return self.neo4j_driver is not None

    def close(self):
        if self.conn:
            self.conn.close()
        if self.neo4j_driver:
            self.neo4j_driver.close()

    # ────────────────────────────────────────────
    # Retrieval Methods
    # ────────────────────────────────────────────

    def search(self, query: str) -> Dict[str, List]:
        """Full-text search across all FTS5 tables."""
        cursor = self.conn.cursor()
        results = {}

        fts_tables = [
            ("programs_fts", "program_id, business_name, business_purpose"),
            ("data_items_fts", "name, business_name, description"),
            ("business_rules_fts", "rule_name, rule_statement, condition_text, action_text"),
        ]

        # Clean query for FTS5 — wrap terms in quotes for phrase matching
        clean_q = re.sub(r'[^\w\s]', '', query).strip()
        # Try each word as an OR search
        fts_query = " OR ".join(clean_q.split()) if clean_q else query

        for table, fields in fts_tables:
            try:
                cursor.execute(
                    f"SELECT {fields} FROM {table} WHERE {table} MATCH ? LIMIT 20",
                    (fts_query,)
                )
                results[table.replace("_fts", "")] = [dict(row) for row in cursor.fetchall()]
            except Exception:
                results[table.replace("_fts", "")] = []

        return results

    def get_program(self, program_id: str) -> Optional[Dict]:
        """Get full program details."""
        cursor = self.conn.cursor()
        pid = program_id.upper().strip()

        cursor.execute("""
            SELECT program_id, file_path, program_type, line_count,
                   business_name, business_purpose, user_role, business_process
            FROM programs WHERE program_id = ?
        """, (pid,))
        row = cursor.fetchone()
        if not row:
            # Try partial match
            cursor.execute("""
                SELECT program_id, file_path, program_type, line_count,
                       business_name, business_purpose, user_role, business_process
                FROM programs WHERE program_id LIKE ?
            """, (f"%{pid}%",))
            row = cursor.fetchone()

        if not row:
            return None

        program = dict(row)

        # Get paragraphs
        cursor.execute("""
            SELECT paragraph_name, line_start, line_end, business_name, narrative, purpose
            FROM paragraphs WHERE program_id = ? ORDER BY line_start
        """, (program["program_id"],))
        program["paragraphs"] = [dict(r) for r in cursor.fetchall()]

        # Get calls made by this program
        cursor.execute("""
            SELECT called_program, call_location, line_number
            FROM program_calls WHERE caller_program = ?
        """, (program["program_id"],))
        program["calls"] = [dict(r) for r in cursor.fetchall()]

        # Get callers of this program
        cursor.execute("""
            SELECT caller_program, call_location, line_number
            FROM program_calls WHERE called_program = ?
        """, (program["program_id"],))
        program["called_by"] = [dict(r) for r in cursor.fetchall()]

        # Get data items (top 20)
        cursor.execute("""
            SELECT name, level_number, picture, section, business_name, description
            FROM data_items WHERE program_id = ? ORDER BY line_number LIMIT 20
        """, (program["program_id"],))
        program["data_items"] = [dict(r) for r in cursor.fetchall()]

        # Get files
        cursor.execute("""
            SELECT file_name, file_type, access_mode
            FROM files WHERE program_id = ?
        """, (program["program_id"],))
        program["files"] = [dict(r) for r in cursor.fetchall()]

        return program

    def get_calls_from(self, program_id: str) -> List[Dict]:
        """Get programs called by a given program."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT pc.called_program, pc.call_location, pc.line_number,
                   p.business_name
            FROM program_calls pc
            LEFT JOIN programs p ON pc.called_program = p.program_id
            WHERE pc.caller_program = ?
        """, (program_id.upper(),))
        return [dict(r) for r in cursor.fetchall()]

    def get_called_by(self, program_id: str) -> List[Dict]:
        """Get programs that call a given program."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT pc.caller_program, pc.call_location, pc.line_number,
                   p.business_name
            FROM program_calls pc
            LEFT JOIN programs p ON pc.caller_program = p.program_id
            WHERE pc.called_program = ?
        """, (program_id.upper(),))
        return [dict(r) for r in cursor.fetchall()]

    def get_data_items(self, program_id: str) -> List[Dict]:
        """Get data items for a program."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name, level_number, picture, usage, value, section,
                   business_name, description
            FROM data_items WHERE program_id = ? ORDER BY line_number
        """, (program_id.upper(),))
        return [dict(r) for r in cursor.fetchall()]

    def get_business_rules(self, program_id: str = None) -> List[Dict]:
        """Get business rules, optionally filtered by program."""
        cursor = self.conn.cursor()
        if program_id:
            cursor.execute("""
                SELECT rule_id, rule_name, rule_statement, category,
                       paragraph_name, condition_text, action_text
                FROM business_rules WHERE program_id = ?
            """, (program_id.upper(),))
        else:
            cursor.execute("""
                SELECT rule_id, rule_name, rule_statement, category,
                       program_id, paragraph_name
                FROM business_rules LIMIT 50
            """)
        return [dict(r) for r in cursor.fetchall()]

    def get_paragraphs(self, program_id: str) -> List[Dict]:
        """Get paragraphs for a program."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT paragraph_name, line_start, line_end,
                   business_name, narrative, purpose
            FROM paragraphs WHERE program_id = ? ORDER BY line_start
        """, (program_id.upper(),))
        return [dict(r) for r in cursor.fetchall()]

    def get_screen(self, screen_name: str) -> Optional[Dict]:
        """Get screen details."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, screen_name, map_name, mapset_name, associated_program,
                   business_name, description
            FROM screens WHERE screen_name LIKE ?
        """, (f"%{screen_name.upper()}%",))
        row = cursor.fetchone()
        if not row:
            return None

        screen = dict(row)
        cursor.execute("""
            SELECT field_name, field_type, length, row_position, col_position,
                   business_name, description
            FROM screen_fields WHERE screen_id = ?
        """, (screen["id"],))
        screen["fields"] = [dict(r) for r in cursor.fetchall()]
        return screen

    def get_overview(self) -> Dict:
        """Get system overview stats."""
        cursor = self.conn.cursor()
        stats = {}
        for table in ["programs", "paragraphs", "data_items", "statements",
                       "program_calls", "business_rules", "screens", "copybooks", "modules"]:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]
            except Exception:
                stats[table] = 0
        return stats

    def get_file_io(self, program_id: str) -> List[Dict]:
        """Get file I/O operations for a program."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT file_name, file_type, access_mode, organization, record_name,
                   business_name, description
            FROM files WHERE program_id = ?
        """, (program_id.upper(),))
        return [dict(r) for r in cursor.fetchall()]

    # ────────────────────────────────────────────
    # Neo4j Graph Queries
    # ────────────────────────────────────────────

    def neo4j_shortest_path(self, from_id: str, to_id: str) -> str:
        """Find shortest call-path between two programs via Neo4j."""
        if not self.neo4j_driver:
            return "Neo4j is not connected. Set NEO4J_URI/NEO4J_USER/NEO4J_PASSWORD in .env."
        try:
            with self.neo4j_driver.session() as session:
                result = session.run("""
                    MATCH path = shortestPath(
                        (a:Program {id: $from})-[:CALLS*..10]-(b:Program {id: $to})
                    )
                    RETURN [n IN nodes(path) | n.id] AS nodes,
                           length(path) AS hops
                """, {"from": from_id.upper(), "to": to_id.upper()})
                record = result.single()
                if record:
                    nodes = record["nodes"]
                    hops = record["hops"]
                    chain = " → ".join(nodes)
                    return f"## Shortest Path ({hops} hops)\n\n{chain}"
                return f"No path found between {from_id} and {to_id}."
        except Exception as e:
            return f"Neo4j query error: {e}"

    def neo4j_blast_radius(self, program_id: str) -> str:
        """Find all programs affected by changing a program via Neo4j."""
        if not self.neo4j_driver:
            return "Neo4j is not connected. Set NEO4J_URI/NEO4J_USER/NEO4J_PASSWORD in .env."
        try:
            with self.neo4j_driver.session() as session:
                result = session.run("""
                    MATCH path = (caller:Program)-[:CALLS*1..5]->(target:Program {id: $pid})
                    RETURN DISTINCT caller.id AS callerId,
                           caller.businessName AS name,
                           length(path) AS distance
                    ORDER BY distance
                """, {"pid": program_id.upper()})
                rows = [dict(r) for r in result]
                if rows:
                    lines = [f"## Blast Radius for {program_id.upper()} ({len(rows)} programs affected)\n"]
                    for r in rows:
                        lines.append(f"- **{r['callerId']}** ({r.get('name') or '-'}) — {r['distance']} hop(s) away")
                    return "\n".join(lines)
                return f"No programs are affected by changes to {program_id}."
        except Exception as e:
            return f"Neo4j query error: {e}"

    def neo4j_dependencies(self, program_id: str, depth: int = 3) -> str:
        """Get dependency subgraph for a program via Neo4j."""
        if not self.neo4j_driver:
            return "Neo4j is not connected. Set NEO4J_URI/NEO4J_USER/NEO4J_PASSWORD in .env."
        try:
            with self.neo4j_driver.session() as session:
                result = session.run(f"""
                    MATCH path = (p:Program {{id: $pid}})-[:CALLS*1..{depth}]->(dep:Program)
                    RETURN DISTINCT dep.id AS depId,
                           dep.businessName AS name,
                           length(path) AS depth
                    ORDER BY depth
                """, {"pid": program_id.upper()})
                rows = [dict(r) for r in result]
                if rows:
                    lines = [f"## Dependencies of {program_id.upper()} ({len(rows)} programs, depth {depth})\n"]
                    for r in rows:
                        indent = "  " * r["depth"]
                        lines.append(f"{indent}→ **{r['depId']}** ({r.get('name') or '-'})")
                    return "\n".join(lines)
                return f"No downstream dependencies found for {program_id}."
        except Exception as e:
            return f"Neo4j query error: {e}"

    # ────────────────────────────────────────────
    # JSON Translation
    # ────────────────────────────────────────────

    def translate_json(self, program_id: str) -> Dict[str, str]:
        """Get JSON-to-English translation for a program. Uses LLM if available."""
        if not self.json_translator:
            return {
                "raw_json": "{}",
                "english": "JSON translator not available. Ensure parsed_output/ directory exists.",
                "found": False
            }
        result = self.json_translator.translate_program(program_id)
        if not result.get("found"):
            return result

        # If LLM is available, send the JSON to the LLM for a richer explanation
        if self.llm_client and result.get("raw_json"):
            try:
                llm_prompt = textwrap.dedent(f"""\
                    You are a COBOL legacy system expert. Below is the raw parsed JSON 
                    output from a COBOL parser for program {program_id.upper()}.
                    
                    Explain this program in clear, plain English. Cover:
                    1. What the program does (its purpose)
                    2. Its control flow (how paragraphs call each other via PERFORMs)
                    3. Key data structures and variables
                    4. File I/O operations
                    5. External program calls
                    6. Any copybook dependencies
                    
                    Be specific and reference paragraph names and line numbers.
                    Use markdown formatting for readability.
                    
                    ```json
                    {result['raw_json'][:4000]}
                    ```
                """)
                response = self.llm_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a COBOL documentation expert. Translate parsed COBOL JSON into clear English explanations."},
                        {"role": "user", "content": llm_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=2000,
                )
                result["english"] = response.choices[0].message.content
            except Exception as e:
                # Fall back to rule-based translation
                result["english"] = f"(LLM unavailable: {e})\n\n" + result["english"]

        return result

    # ────────────────────────────────────────────
    # Context Assembly
    # ────────────────────────────────────────────

    def _build_context(self, question: str, current_program: str = None) -> str:
        """Build a context string from retrieved knowledge for the LLM."""
        strategy, target = QueryRouter.route(question, current_program=current_program)
        sections = []

        if strategy == "program_detail" and target:
            prog = self.get_program(target)
            if prog:
                sections.append(self._format_program_context(prog))
            else:
                # Fall back to FTS
                results = self.search(target)
                sections.append(self._format_search_context(results, target))

        elif strategy == "called_by" and target:
            callers = self.get_called_by(target)
            sections.append(f"## Programs that call {target}\n")
            if callers:
                for c in callers:
                    sections.append(f"- {c['caller_program']} (business: {c.get('business_name', 'N/A')}) at line {c.get('line_number', '?')}")
            else:
                sections.append(f"No programs found that call {target}.")
            # Also get the program itself for context
            prog = self.get_program(target)
            if prog:
                sections.append("\n" + self._format_program_context(prog))

        elif strategy == "calls_from" and target:
            calls = self.get_calls_from(target)
            sections.append(f"## Programs called by {target}\n")
            if calls:
                for c in calls:
                    sections.append(f"- {c['called_program']} (business: {c.get('business_name', 'N/A')}) from {c.get('call_location', '?')} at line {c.get('line_number', '?')}")
            else:
                sections.append(f"{target} does not call any other programs.")

        elif strategy == "call_graph":
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT caller_program, called_program, line_number
                FROM program_calls ORDER BY caller_program LIMIT 50
            """)
            calls = [dict(r) for r in cursor.fetchall()]
            sections.append("## Full Call Graph\n")
            for c in calls:
                sections.append(f"- {c['caller_program']} → {c['called_program']} (line {c.get('line_number', '?')})")

        elif strategy == "data_items" and target:
            items = self.get_data_items(target)
            sections.append(f"## Data Items in {target}\n")
            if items:
                for item in items[:30]:
                    bname = item.get('business_name') or ''
                    sections.append(f"- {item['name']} (Level {item.get('level_number', '?')}, PIC {item.get('picture', '?')}, Section: {item.get('section', '?')}) {bname}")
            else:
                sections.append(f"No data items found for {target}.")

        elif strategy == "data_lookup" and target:
            results = self.search(target)
            sections.append(self._format_search_context(results, target))

        elif strategy == "business_rules" and target:
            rules = self.get_business_rules(target)
            sections.append(f"## Business Rules in {target}\n")
            if rules:
                for rule in rules:
                    sections.append(f"### {rule.get('rule_name', 'Rule')}\n- Statement: {rule.get('rule_statement', 'N/A')}\n- Category: {rule.get('category', 'N/A')}\n- Condition: {rule.get('condition_text', 'N/A')}\n- Action: {rule.get('action_text', 'N/A')}")
            else:
                sections.append(f"No business rules found for {target}.")

        elif strategy == "rules_by_category":
            rules = self.get_business_rules()
            sections.append("## All Business Rules\n")
            if rules:
                by_cat = {}
                for r in rules:
                    cat = r.get("category", "GENERAL")
                    by_cat.setdefault(cat, []).append(r)
                for cat, cat_rules in by_cat.items():
                    sections.append(f"\n### {cat}")
                    for rule in cat_rules[:10]:
                        sections.append(f"- [{rule.get('rule_id', '?')}] {rule.get('rule_name', '?')}: {rule.get('rule_statement', '')}")
            else:
                sections.append("No business rules have been extracted.")

        elif strategy == "screen_detail" and target:
            screen = self.get_screen(target)
            if screen:
                sections.append(f"## Screen: {screen.get('screen_name', target)}")
                sections.append(f"- Map: {screen.get('map_name', 'N/A')}, Mapset: {screen.get('mapset_name', 'N/A')}")
                sections.append(f"- Program: {screen.get('associated_program', 'N/A')}")
                if screen.get("fields"):
                    sections.append("\n### Fields:")
                    for f in screen["fields"]:
                        sections.append(f"- {f['field_name']} ({f.get('field_type', '?')}) at Row {f.get('row_position', '?')}, Col {f.get('col_position', '?')}")
            else:
                sections.append(f"No screen found matching '{target}'.")

        elif strategy == "paragraphs" and target:
            paras = self.get_paragraphs(target)
            sections.append(f"## Paragraphs in {target}\n")
            if paras:
                for p in paras:
                    bname = p.get("business_name") or ""
                    narrative = p.get("narrative") or p.get("purpose") or ""
                    sections.append(f"### {p['paragraph_name']} {('(' + bname + ')') if bname else ''}")
                    sections.append(f"Lines {p.get('line_start', '?')} - {p.get('line_end', '?')}")
                    if narrative:
                        sections.append(narrative)
            else:
                sections.append(f"No paragraphs found for {target}.")

        elif strategy == "file_io" and target:
            files = self.get_file_io(target)
            sections.append(f"## File I/O in {target}\n")
            if files:
                for f in files:
                    sections.append(f"- {f['file_name']} ({f.get('file_type', '?')}, Access: {f.get('access_mode', '?')})")
            else:
                sections.append(f"No file operations found for {target}.")

        elif strategy == "overview":
            stats = self.get_overview()
            sections.append("## System Overview Statistics\n")
            for name, count in stats.items():
                sections.append(f"- {name}: {count}")

        elif strategy == "json_translate" and target:
            result = self.translate_json(target)
            if result.get("found"):
                sections.append(result["english"])
                sections.append("\n---\n### Raw Parsed JSON (summary):\n```json")
                # Include only first 80 lines of JSON to keep context manageable
                json_lines = result["raw_json"].split("\n")[:80]
                sections.append("\n".join(json_lines))
                sections.append("```")
            else:
                sections.append(result["english"])

        elif strategy == "graph_path" and target:
            # Extract second program from the question
            import re as _re
            m = _re.search(r'(?:and|to)\s+(\w+)', question, _re.IGNORECASE)
            target2 = m.group(1).upper() if m else None
            if target2:
                sections.append(self.neo4j_shortest_path(target, target2))
            else:
                sections.append("Please specify two programs: e.g. 'shortest path between PROG1 and PROG2'")

        elif strategy == "graph_impact" and target:
            sections.append(self.neo4j_blast_radius(target))

        elif strategy == "graph_deps" and target:
            sections.append(self.neo4j_dependencies(target))

        else:
            # Default: FTS search
            results = self.search(question)
            sections.append(self._format_search_context(results, question))

        return "\n".join(sections)

    def _format_program_context(self, prog: Dict) -> str:
        """Format a complete program into context text."""
        lines = [
            f"## Program: {prog['program_id']}",
            f"- Business Name: {prog.get('business_name', 'N/A')}",
            f"- Type: {prog.get('program_type', 'N/A')}",
            f"- Lines: {prog.get('line_count', 'N/A')}",
            f"- File: {prog.get('file_path', 'N/A')}",
            f"- Purpose: {prog.get('business_purpose', 'Not yet enriched')}",
            f"- User Role: {prog.get('user_role', 'N/A')}",
            f"- Business Process: {prog.get('business_process', 'N/A')}",
        ]

        if prog.get("paragraphs"):
            lines.append("\n### Paragraphs:")
            for p in prog["paragraphs"][:15]:
                bname = p.get("business_name") or ""
                purpose = p.get("purpose") or p.get("narrative") or ""
                lines.append(f"- {p['paragraph_name']} (lines {p.get('line_start', '?')}-{p.get('line_end', '?')}) {bname}")
                if purpose:
                    lines.append(f"  {purpose[:200]}")

        if prog.get("calls"):
            lines.append("\n### Calls to other programs:")
            for c in prog["calls"]:
                lines.append(f"- CALL {c['called_program']} from {c.get('call_location', '?')} (line {c.get('line_number', '?')})")

        if prog.get("called_by"):
            lines.append("\n### Called by:")
            for c in prog["called_by"]:
                lines.append(f"- {c['caller_program']} (line {c.get('line_number', '?')})")

        if prog.get("data_items"):
            lines.append(f"\n### Data Items ({len(prog['data_items'])} shown):")
            for d in prog["data_items"][:10]:
                lines.append(f"- {d['name']} (Level {d.get('level_number', '?')}, PIC {d.get('picture', '?')})")

        if prog.get("files"):
            lines.append("\n### File I/O:")
            for f in prog["files"]:
                lines.append(f"- {f['file_name']} ({f.get('file_type', '?')}, {f.get('access_mode', '?')})")

        return "\n".join(lines)

    def _format_search_context(self, results: Dict, query: str) -> str:
        """Format FTS search results into context text."""
        lines = [f"## Search results for '{query}'\n"]

        if results.get("programs"):
            lines.append("### Programs:")
            for p in results["programs"][:10]:
                lines.append(f"- {p.get('program_id', '?')}: {p.get('business_name', '')} — {p.get('business_purpose', '')}")

        if results.get("data_items"):
            lines.append("\n### Data Items:")
            for d in results["data_items"][:10]:
                lines.append(f"- {d.get('name', '?')}: {d.get('business_name', '')} — {d.get('description', '')}")

        if results.get("business_rules"):
            lines.append("\n### Business Rules:")
            for r in results["business_rules"][:10]:
                lines.append(f"- {r.get('rule_name', '?')}: {r.get('rule_statement', '')}")

        if not any(results.values()):
            lines.append("No results found in the knowledge base.")

        return "\n".join(lines)

    # ────────────────────────────────────────────
    # LLM Answer Generation
    # ────────────────────────────────────────────

    SYSTEM_PROMPT = textwrap.dedent("""\
        You are a COBOL legacy system documentation assistant. You help engineers
        understand a mainframe COBOL application by querying a structured
        knowledge base extracted from its source code.
        
        You have access to a knowledge base containing:
        - Program details (ID, business purpose, type, paragraphs, control flow)
        - Call graph (which programs call which)
        - Data items (COBOL variables with their PIC clauses and business names)
        - Business rules (extracted validation/calculation/workflow logic)
        - Screen definitions (BMS maps with fields)
        - File I/O (VSAM, sequential files used by each program)
        
        When answering:
        1. Be specific — reference program IDs, paragraph names, line numbers
        2. Explain COBOL concepts in modern terms when helpful
        3. If the knowledge base doesn't have enough info, say so honestly
        4. Use markdown formatting for readability
        5. Keep answers concise but thorough
    """)

    def ask(self, question: str, current_program: str = None) -> str:
        """Ask a question and get an answer (LLM or search-only)."""
        # Build context from knowledge base
        context = self._build_context(question, current_program=current_program)

        if not self.llm_client:
            # Search-only mode — return formatted results
            return context

        # Build messages for LLM
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

        # Add conversation history (last 4 turns)
        for turn in self.history[-4:]:
            messages.append({"role": "user", "content": turn["question"]})
            messages.append({"role": "assistant", "content": turn["answer"]})

        # Inject contextual info if provided (even if not explicitly searched for)
        current_ctx_snippet = f"\nCurrently looking at program: {current_program}\n" if current_program else ""

        # Current question with context
        user_msg = f"""Based on the following information from the COBOL knowledge base, answer the user's question.{current_ctx_snippet}

--- KNOWLEDGE BASE CONTEXT ---
{context}
--- END CONTEXT ---

User Question: {question}
"""
        messages.append({"role": "user", "content": user_msg})

        try:
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=1500,
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"⚠ LLM error: {e}\n\nHere are the raw search results:\n\n{context}"

        # Save to history
        self.history.append({"question": question, "answer": answer})

        return answer


# ============================================================
# Interactive REPL
# ============================================================

HELP_TEXT = """\
[bold cyan]COBOL Knowledge Base Chat[/bold cyan]
[dim]Ask questions about the loaded COBOL application in natural language.[/dim]

[bold]Special Commands:[/bold]
  [green]/search[/green] [dim]<query>[/dim]    — Full-text search across the knowledge base
  [green]/program[/green] [dim]<id>[/dim]      — Show full details for a program (e.g., /program CBACT01C)
  [green]/calls[/green] [dim]<id>[/dim]        — Show call graph for a program
  [green]/data[/green] [dim]<id>[/dim]         — Show data items for a program
  [green]/rules[/green] [dim][id][/dim]        — Show business rules (optionally for a program)
  [green]/stats[/green]              — Show system overview statistics
  [green]/pdf[/green] [dim]<id>[/dim]          — Generate a PDF report for a program
  [green]/json[/green] [dim]<id>[/dim]         — Show parsed JSON → English translation
  [green]/graph[/green] [dim]<id>[/dim]        — Show Neo4j graph dependencies for a program
  [green]/help[/green]               — Show this help message
  [green]/quit[/green]               — Exit the chat

[bold]Example Questions:[/bold]
  • What does CBACT01C do?
  • Who calls CBTRN02C?
  • What programs does CBSTM03A call?
  • Show me data items in CBACT04C
  • What business rules are in the system?
  • Show parsed JSON for CBACT01C
  • Blast radius for CBTRN02C
  • Shortest path between CBACT01C and CBSTM03A
"""


def run_chat(db_path: str, groq_api_key: str = None, model: str = "llama-3.1-8b-instant"):
    """Run the interactive chat REPL."""

    # Verify database exists
    if not Path(db_path).exists():
        console.print(f"[red]✗ Database not found: {db_path}[/red]")
        console.print("[dim]  Run the pipeline first: python run_pipeline.py[/dim]")
        sys.exit(1)

    chat = KnowledgeBaseChat(db_path, groq_api_key=groq_api_key, model=model)

    # Header
    mode = "[green]AI-powered[/green] (Groq)" if chat.llm_client else "[yellow]Search-only[/yellow] (no API key)"
    console.print(Panel(
        f"[bold cyan]🔍 COBOL Knowledge Base Chat[/bold cyan]\n"
        f"[dim]Database: {db_path}[/dim]\n"
        f"Mode: {mode}\n"
        f"[dim]Type /help for commands, /quit to exit[/dim]",
        box=box.ROUNDED,
        border_style="cyan",
    ))
    console.print()

    while True:
        try:
            question = console.input("[bold green]you >[/bold green] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if not question:
            continue

        # Handle special commands
        cmd = question.lower()

        if cmd in ("/quit", "/exit", "/q"):
            console.print("[dim]Goodbye![/dim]")
            break

        elif cmd == "/help":
            console.print(HELP_TEXT)
            continue

        elif cmd == "/stats":
            stats = chat.get_overview()
            table = Table(title="System Overview", box=box.ROUNDED, border_style="cyan")
            table.add_column("Entity", style="bold")
            table.add_column("Count", justify="right", style="green")
            for name, count in stats.items():
                table.add_row(name.replace("_", " ").title(), str(count))
            console.print(table)
            continue

        elif cmd.startswith("/search "):
            query = question[8:].strip()
            results = chat.search(query)
            _display_search_results(results, query)
            continue

        elif cmd.startswith("/program "):
            pid = question[9:].strip().upper()
            prog = chat.get_program(pid)
            if prog:
                _display_program(prog)
            else:
                console.print(f"[red]Program '{pid}' not found.[/red]")
            continue

        elif cmd.startswith("/calls "):
            pid = question[7:].strip().upper()
            calls_from = chat.get_calls_from(pid)
            called_by = chat.get_called_by(pid)
            _display_call_graph(pid, calls_from, called_by)
            continue

        elif cmd.startswith("/data "):
            pid = question[6:].strip().upper()
            items = chat.get_data_items(pid)
            _display_data_items(pid, items)
            continue

        elif cmd.startswith("/rules"):
            pid = question[6:].strip().upper() if len(question) > 6 else None
            rules = chat.get_business_rules(pid if pid else None)
            _display_rules(rules, pid)
            continue

        elif cmd.startswith("/pdf "):
            pid = question[5:].strip().upper()
            with console.status("[cyan]Generating PDF report...[/cyan]"):
                try:
                    from src.pdf_generator import PDFReportGenerator
                except ImportError:
                    from pdf_generator import PDFReportGenerator
                gen = PDFReportGenerator()
                prog = chat.get_program(pid)
                if prog:
                    calls_from = chat.get_calls_from(pid)
                    called_by_list = chat.get_called_by(pid)
                    rules = chat.get_business_rules(pid)
                    paras = chat.get_paragraphs(pid)
                    pdf_bytes = gen.generate_program_report(
                        prog, calls_from, called_by_list, rules, paras
                    )
                    out_path = Path(f"{pid}_report.pdf")
                    out_path.write_bytes(pdf_bytes)
                    console.print(f"[green]✓ PDF saved: {out_path.absolute()}[/green]")
                else:
                    console.print(f"[red]Program '{pid}' not found.[/red]")
            continue

        elif cmd.startswith("/json "):
            pid = question[6:].strip().upper()
            result = chat.translate_json(pid)
            if result.get("found"):
                # Show English translation
                console.print()
                console.print(Panel(
                    Markdown(result["english"]),
                    title=f"[bold cyan]English Translation — {pid}[/bold cyan]",
                    box=box.ROUNDED,
                    border_style="green",
                    padding=(1, 2),
                ))
                # Show raw JSON (collapsed)
                console.print()
                console.print(Panel(
                    result["raw_json"],
                    title=f"[bold cyan]Raw Parsed JSON — {pid}[/bold cyan]",
                    box=box.ROUNDED,
                    border_style="yellow",
                    padding=(1, 2),
                ))
            else:
                console.print(f"[red]{result['english']}[/red]")
            continue

        elif cmd.startswith("/graph "):
            pid = question[7:].strip().upper()
            if chat.neo4j_available:
                with console.status("[cyan]Querying Neo4j graph...[/cyan]"):
                    deps = chat.neo4j_dependencies(pid)
                    impact = chat.neo4j_blast_radius(pid)
                console.print()
                console.print(Panel(
                    Markdown(deps),
                    title=f"[bold cyan]Graph Dependencies — {pid}[/bold cyan]",
                    box=box.ROUNDED,
                    border_style="green",
                    padding=(1, 2),
                ))
                console.print(Panel(
                    Markdown(impact),
                    title=f"[bold cyan]Blast Radius — {pid}[/bold cyan]",
                    box=box.ROUNDED,
                    border_style="red",
                    padding=(1, 2),
                ))
            else:
                console.print("[yellow]⚠ Neo4j is not connected. Set NEO4J_URI/NEO4J_USER/NEO4J_PASSWORD in .env[/yellow]")
            continue

        # Regular question — use RAG
        with console.status("[cyan]Searching knowledge base...[/cyan]"):
            answer = chat.ask(question)

        console.print()
        console.print(Panel(
            Markdown(answer),
            title="[bold cyan]assistant[/bold cyan]",
            box=box.ROUNDED,
            border_style="blue",
            padding=(1, 2),
        ))
        console.print()

    chat.close()


# ============================================================
# Display Helpers
# ============================================================

def _display_search_results(results: Dict, query: str):
    """Display FTS search results in a rich table."""
    console.print(f"\n[bold cyan]Search results for:[/bold cyan] {query}\n")

    found_any = False
    for category, items in results.items():
        if not items:
            continue
        found_any = True
        table = Table(
            title=f"{category.replace('_', ' ').title()} ({len(items)} results)",
            box=box.SIMPLE,
            border_style="dim",
        )
        for key in items[0].keys():
            table.add_column(key.replace("_", " ").title(), max_width=50)
        for item in items[:10]:
            table.add_row(*[str(v or "")[:50] for v in item.values()])
        console.print(table)
        console.print()

    if not found_any:
        console.print("[yellow]No results found.[/yellow]")


def _display_program(prog: Dict):
    """Display detailed program info."""
    console.print()
    table = Table(title=f"Program: {prog['program_id']}", box=box.ROUNDED, border_style="cyan")
    table.add_column("Attribute", style="bold")
    table.add_column("Value")
    table.add_row("Business Name", prog.get("business_name") or "-")
    table.add_row("Type", prog.get("program_type") or "-")
    table.add_row("Lines", str(prog.get("line_count") or "-"))
    table.add_row("Purpose", (prog.get("business_purpose") or "-")[:200])
    table.add_row("User Role", prog.get("user_role") or "-")
    table.add_row("File", prog.get("file_path") or "-")
    table.add_row("Paragraphs", str(len(prog.get("paragraphs", []))))
    table.add_row("Calls Out", ", ".join(c["called_program"] for c in prog.get("calls", [])) or "None")
    table.add_row("Called By", ", ".join(c["caller_program"] for c in prog.get("called_by", [])) or "None")
    console.print(table)

    if prog.get("paragraphs"):
        para_table = Table(title="Paragraphs", box=box.SIMPLE, border_style="dim")
        para_table.add_column("Name", style="bold")
        para_table.add_column("Lines")
        para_table.add_column("Business Name")
        for p in prog["paragraphs"][:20]:
            para_table.add_row(
                p["paragraph_name"],
                f"{p.get('line_start', '?')}-{p.get('line_end', '?')}",
                p.get("business_name") or "-",
            )
        console.print(para_table)
    console.print()


def _display_call_graph(pid: str, calls_from: List, called_by: List):
    """Display call relationships."""
    console.print(f"\n[bold cyan]Call Graph for {pid}[/bold cyan]\n")

    if calls_from:
        table = Table(title=f"{pid} calls →", box=box.SIMPLE, border_style="green")
        table.add_column("Called Program", style="bold")
        table.add_column("From Paragraph")
        table.add_column("Line")
        table.add_column("Business Name")
        for c in calls_from:
            table.add_row(
                c["called_program"],
                c.get("call_location") or "-",
                str(c.get("line_number") or "-"),
                c.get("business_name") or "-",
            )
        console.print(table)
    else:
        console.print(f"[dim]{pid} does not call any other programs.[/dim]")

    if called_by:
        table = Table(title=f"→ {pid} called by", box=box.SIMPLE, border_style="yellow")
        table.add_column("Calling Program", style="bold")
        table.add_column("From Paragraph")
        table.add_column("Line")
        table.add_column("Business Name")
        for c in called_by:
            table.add_row(
                c["caller_program"],
                c.get("call_location") or "-",
                str(c.get("line_number") or "-"),
                c.get("business_name") or "-",
            )
        console.print(table)
    else:
        console.print(f"[dim]No other programs call {pid}.[/dim]")
    console.print()


def _display_data_items(pid: str, items: List):
    """Display data items for a program."""
    console.print(f"\n[bold cyan]Data Items in {pid}[/bold cyan]\n")
    if not items:
        console.print("[yellow]No data items found.[/yellow]")
        return

    table = Table(box=box.SIMPLE, border_style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Level")
    table.add_column("PIC")
    table.add_column("Section")
    table.add_column("Business Name")
    for item in items[:40]:
        table.add_row(
            item["name"],
            str(item.get("level_number") or "-"),
            item.get("picture") or "-",
            item.get("section") or "-",
            item.get("business_name") or "-",
        )
    if len(items) > 40:
        console.print(f"[dim]Showing 40 of {len(items)}. Use full-text search for more.[/dim]")
    console.print(table)
    console.print()


def _display_rules(rules: List, pid: str = None):
    """Display business rules."""
    title = f"Business Rules for {pid}" if pid else "All Business Rules"
    console.print(f"\n[bold cyan]{title}[/bold cyan]\n")
    if not rules:
        console.print("[yellow]No business rules found. Run LLM enrichment to extract rules.[/yellow]")
        return

    table = Table(box=box.SIMPLE, border_style="dim")
    table.add_column("Rule ID", style="bold")
    table.add_column("Name")
    table.add_column("Statement", max_width=60)
    table.add_column("Category")
    for rule in rules[:30]:
        table.add_row(
            rule.get("rule_id") or "-",
            rule.get("rule_name") or "-",
            (rule.get("rule_statement") or "-")[:60],
            rule.get("category") or "-",
        )
    console.print(table)
    console.print()


# ============================================================
# CLI Entry Point
# ============================================================

if __name__ == "__main__":
    import argparse
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser(
        description="COBOL Knowledge Base Chat — Ask questions about your COBOL codebase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python src/chat_cli.py --db data/cobol_knowledge.db
              python src/chat_cli.py --db data/cobol_knowledge.db --no-llm
              python src/chat_cli.py --db data/cobol_knowledge.db --model llama-3.1-70b-versatile
        """),
    )
    parser.add_argument("--db", default="data/cobol_knowledge.db", help="Path to SQLite knowledge base")
    parser.add_argument("--model", default="llama-3.1-8b-instant", help="Groq model to use")
    parser.add_argument("--no-llm", action="store_true", help="Disable LLM, use search-only mode")

    args = parser.parse_args()

    api_key = None if args.no_llm else os.environ.get("GROQ_API_KEY")

    run_chat(
        db_path=args.db,
        groq_api_key=api_key,
        model=args.model,
    )
