"""
Dependency Analysis Generator
Creates comprehensive call graph, dependency, and impact analysis documentation.

Generates:
  docs/diagrams/call-graph.md           — Full inter-program call graph
  docs/diagrams/dependency-matrix.md    — Dependency matrix + shared resources
  docs/diagrams/impact-analysis.md      — Impact analysis for every program  
  docs/diagrams/copybook-dependencies.md — Copybook sharing graph
  docs/diagrams/data-flow.md            — Data flow through files/VSAM
"""

import sqlite3
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

from rich.console import Console

console = Console(force_terminal=True, highlight=False, legacy_windows=False)


class DependencyAnalyzer:
    """Generates comprehensive dependency documentation from the knowledge base."""

    def __init__(self, db_path: str, output_dir: str = "docs/diagrams"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    def close(self):
        self.conn.close()

    def generate_all(self):
        """Generate all dependency analysis documents."""
        console.print("[bold cyan]Generating Dependency Analysis Documentation...[/bold cyan]")
        self._generate_call_graph()
        self._generate_dependency_matrix()
        self._generate_impact_analysis()
        self._generate_copybook_dependencies()
        self._generate_data_flow()
        console.print("[bold green]✓ All dependency docs generated.[/bold green]")

    # ════════════════════════════════════════════
    # 1. FULL CALL GRAPH
    # ════════════════════════════════════════════

    def _generate_call_graph(self):
        console.print("  [cyan]1/5 Call Graph[/cyan]")
        c = self.conn.cursor()

        # Get all calls
        c.execute("""
            SELECT pc.caller_program, pc.called_program, pc.call_location, pc.line_number,
                   p1.business_name as caller_name, p1.program_type as caller_type,
                   p2.business_name as called_name, p2.program_type as called_type
            FROM program_calls pc
            LEFT JOIN programs p1 ON pc.caller_program = p1.program_id
            LEFT JOIN programs p2 ON pc.called_program = p2.program_id
            ORDER BY pc.caller_program
        """)
        all_calls = [dict(r) for r in c.fetchall()]

        # Get all programs
        c.execute("SELECT program_id, business_name, program_type, line_count FROM programs")
        programs = {r["program_id"]: dict(r) for r in c.fetchall()}

        # Unique call edges
        edges = {}
        for call in all_calls:
            key = f"{call['caller_program']}->{call['called_program']}"
            if key not in edges:
                edges[key] = call
                edges[key]["count"] = 1
            else:
                edges[key]["count"] += 1

        # Classify programs
        called_set = set(call["called_program"] for call in all_calls)
        caller_set = set(call["caller_program"] for call in all_calls)
        all_ids = set(programs.keys())
        entry_points = sorted(all_ids - called_set)
        leaf_programs = sorted(all_ids - caller_set)
        hub_programs = sorted(caller_set & called_set)

        # Identify external calls (programs not in our codebase)
        internal = set(programs.keys())
        external_targets = sorted(called_set - internal)

        # Build Mermaid — group by module for better visualization
        c.execute("""
            SELECT m.module_name, mp.program_id
            FROM modules m JOIN module_programs mp ON m.id = mp.module_id
        """)
        prog_to_module = {}
        module_names = set()
        for r in c.fetchall():
            prog_to_module[r["program_id"]] = r["module_name"]
            module_names.add(r["module_name"])

        # Build the document
        lines = [
            "# Program Call Hierarchy",
            "",
            "> Complete inter-program call relationships across the application.",
            "",
            "## System Statistics",
            "",
            "| Metric | Count |",
            "|--------|-------|",
            f"| Total Programs | {len(programs)} |",
            f"| Total Call Relationships | {len(edges)} |",
            f"| Total Call Instances | {len(all_calls)} |",
            f"| Entry Points (not called by others) | {len(entry_points)} |",
            f"| Leaf Programs (don't call others) | {len(leaf_programs)} |",
            f"| Hub Programs (both call and are called) | {len(hub_programs)} |",
            f"| External Targets | {len(external_targets)} |",
            "",
            "## Visual Call Graph",
            "",
            "```mermaid",
            "graph LR",
        ]

        # Add subgraphs per module
        for mod_name in sorted(module_names):
            safe_mod = mod_name.replace(" ", "_").replace("-", "_")
            lines.append(f'    subgraph {safe_mod}["{mod_name}"]')
            for pid, mod in sorted(prog_to_module.items()):
                if mod == mod_name:
                    safe_pid = pid.replace("-", "_")
                    ptype = programs.get(pid, {}).get("program_type", "")
                    if ptype and ptype.upper() == "ONLINE":
                        lines.append(f'        {safe_pid}["{pid}"]:::online')
                    else:
                        lines.append(f'        {safe_pid}["{pid}"]:::batch')
            lines.append("    end")

        # Programs not in any module
        unmodded = set(programs.keys()) - set(prog_to_module.keys())
        if unmodded:
            lines.append('    subgraph UNASSIGNED["Other Programs"]')
            for pid in sorted(unmodded):
                safe_pid = pid.replace("-", "_")
                lines.append(f'        {safe_pid}["{pid}"]')
            lines.append("    end")

        # External targets
        if external_targets:
            lines.append('    subgraph EXTERNAL["External / MQ Programs"]')
            for ext in external_targets:
                safe = ext.replace("-", "_")
                lines.append(f'        {safe}["{ext}"]:::external')
            lines.append("    end")

        # Add edges
        seen_edges = set()
        for key, edge in sorted(edges.items()):
            caller = edge["caller_program"].replace("-", "_")
            called = edge["called_program"].replace("-", "_")
            edge_key = f"{caller}->{called}"
            if edge_key not in seen_edges:
                count_label = f"|{edge['count']}x|" if edge["count"] > 1 else ""
                lines.append(f"    {caller} -->{count_label} {called}")
                seen_edges.add(edge_key)

        # Styles
        lines.extend([
            "",
            "    classDef online fill:#4CAF50,stroke:#2E7D32,color:#fff",
            "    classDef batch fill:#2196F3,stroke:#1565C0,color:#fff",
            "    classDef external fill:#FF9800,stroke:#E65100,color:#fff",
            "```",
            "",
        ])

        # Call Matrix — detailed table
        lines.extend([
            "## Call Matrix",
            "",
            "| Caller | Called | Location | Line | Instances |",
            "|--------|--------|----------|------|-----------|",
        ])
        for key, edge in sorted(edges.items()):
            caller = edge["caller_program"]
            called = edge["called_program"]
            loc = edge.get("call_location") or "-"
            ln = edge.get("line_number") or "-"
            cnt = edge["count"]
            caller_link = f"[{caller}](../programs/{caller}.md)" if caller in programs else caller
            called_link = f"[{called}](../programs/{called}.md)" if called in programs else f"`{called}`"
            lines.append(f"| {caller_link} | {called_link} | `{loc}` | {ln} | {cnt} |")

        # Entry Points with details
        lines.extend([
            "",
            "## Entry Points",
            "",
            "Programs not called by any other program — likely **top-level entry points**, CICS transaction starters, or batch job drivers.",
            "",
            "| Program | Type | Lines | Business Name |",
            "|---------|------|-------|---------------|",
        ])
        for pid in entry_points:
            p = programs.get(pid, {})
            lines.append(f"| [{pid}](../programs/{pid}.md) | {p.get('program_type', '-')} | {p.get('line_count', '-')} | {p.get('business_name') or '-'} |")

        # Leaf Programs
        lines.extend([
            "",
            "## Leaf Programs",
            "",
            "Programs that don't call any other program — utility or terminal logic.",
            "",
            "| Program | Type | Lines | Business Name |",
            "|---------|------|-------|---------------|",
        ])
        for pid in leaf_programs:
            p = programs.get(pid, {})
            lines.append(f"| [{pid}](../programs/{pid}.md) | {p.get('program_type', '-')} | {p.get('line_count', '-')} | {p.get('business_name') or '-'} |")

        # Hub programs
        if hub_programs:
            lines.extend([
                "",
                "## Hub Programs",
                "",
                "Programs that both **call** and **are called by** others — central to the architecture.",
                "",
                "| Program | Calls Out | Called By | Type |",
                "|---------|-----------|----------|------|",
            ])
            for pid in hub_programs:
                out_count = len([e for e in edges.values() if e["caller_program"] == pid])
                in_count = len([e for e in edges.values() if e["called_program"] == pid])
                p = programs.get(pid, {})
                lines.append(f"| [{pid}](../programs/{pid}.md) | {out_count} | {in_count} | {p.get('program_type', '-')} |")

        # External targets
        if external_targets:
            lines.extend([
                "",
                "## External Programs",
                "",
                "Targets of CALL statements not found in the codebase (MQ, CICS, utilities).",
                "",
            ])
            for ext in external_targets:
                callers = [e["caller_program"] for e in edges.values() if e["called_program"] == ext]
                lines.append(f"- **{ext}** — called by: {', '.join(sorted(set(callers)))}")

        lines.extend(["", "---", "", f"*Generated {self.generated}*"])
        (self.output_dir / "call-graph.md").write_text("\n".join(lines), encoding="utf-8")
        console.print(f"    [green]✓ call-graph.md ({len(edges)} edges, {len(programs)} programs)[/green]")

    # ════════════════════════════════════════════
    # 2. DEPENDENCY MATRIX
    # ════════════════════════════════════════════

    def _generate_dependency_matrix(self):
        console.print("  [cyan]2/5 Dependency Matrix[/cyan]")
        c = self.conn.cursor()

        # Build dependency types per program
        deps = defaultdict(lambda: {
            "calls_out": [], "called_by": [], "copybooks": [],
            "files": [], "screens": [], "performs_count": 0
        })

        # Calls
        c.execute("SELECT caller_program, called_program FROM program_calls")
        for r in c.fetchall():
            deps[r["caller_program"]]["calls_out"].append(r["called_program"])
            deps[r["called_program"]]["called_by"].append(r["caller_program"])

        # Copybooks
        c.execute("SELECT program_id, copybook_name FROM copybook_usage")
        for r in c.fetchall():
            deps[r["program_id"]]["copybooks"].append(r["copybook_name"])

        # Files
        c.execute("SELECT program_id, file_name FROM files")
        for r in c.fetchall():
            deps[r["program_id"]]["files"].append(r["file_name"])

        # Screens
        c.execute("SELECT associated_program, screen_name FROM screens WHERE associated_program IS NOT NULL")
        for r in c.fetchall():
            deps[r["associated_program"]]["screens"].append(r["screen_name"])

        # Performs
        c.execute("SELECT program_id, COUNT(*) as cnt FROM performs GROUP BY program_id")
        for r in c.fetchall():
            deps[r["program_id"]]["performs_count"] = r["cnt"]

        # Programs info
        c.execute("SELECT program_id, business_name, program_type FROM programs")
        programs = {r["program_id"]: dict(r) for r in c.fetchall()}

        lines = [
            "# Dependency Matrix",
            "",
            "> Complete dependency overview for every program in the system.",
            "> Shows calls, copybooks, files, screens, and internal control flow complexity.",
            "",
            "## Program Dependency Summary",
            "",
            "| Program | Type | Calls Out | Called By | Copybooks | Files | Screens | PERFORMs |",
            "|---------|------|-----------|----------|-----------|-------|---------|----------|",
        ]

        for pid in sorted(programs.keys()):
            d = deps[pid]
            p = programs[pid]
            lines.append(
                f"| [{pid}](../programs/{pid}.md) | {p.get('program_type', '-')} "
                f"| {len(set(d['calls_out']))} | {len(set(d['called_by']))} "
                f"| {len(set(d['copybooks']))} | {len(set(d['files']))} "
                f"| {len(d['screens'])} | {d['performs_count']} |"
            )

        # Shared copybooks section
        c.execute("""
            SELECT cu.copybook_name, GROUP_CONCAT(DISTINCT cu.program_id) as programs,
                   COUNT(DISTINCT cu.program_id) as prog_count
            FROM copybook_usage cu
            GROUP BY cu.copybook_name
            ORDER BY prog_count DESC
        """)
        copybooks = [dict(r) for r in c.fetchall()]

        lines.extend([
            "",
            "## Shared Copybooks (Data Coupling)",
            "",
            "Copybooks shared by multiple programs create **data coupling** — changes to a copybook affect ALL programs using it.",
            "",
            "| Copybook | Used By (count) | Programs |",
            "|----------|----------------|----------|",
        ])
        for cb in copybooks:
            progs = cb["programs"].split(",")
            prog_links = ", ".join(f"[{p}](../programs/{p}.md)" if p in programs else p for p in sorted(progs))
            impact = "🔴" if cb["prog_count"] >= 10 else "🟡" if cb["prog_count"] >= 5 else "🟢"
            lines.append(f"| `{cb['copybook_name']}` | {impact} {cb['prog_count']} | {prog_links} |")

        # Shared files section
        c.execute("""
            SELECT f.file_name, GROUP_CONCAT(DISTINCT f.program_id) as programs,
                   COUNT(DISTINCT f.program_id) as prog_count,
                   GROUP_CONCAT(DISTINCT f.access_mode) as access_modes
            FROM files f
            GROUP BY f.file_name
            ORDER BY prog_count DESC
        """)
        shared_files = [dict(r) for r in c.fetchall()]

        if shared_files:
            lines.extend([
                "",
                "## Shared Files (Data Flow Coupling)",
                "",
                "Files accessed by multiple programs — changes to file layout affect all readers/writers.",
                "",
                "| File | Access | Used By | Programs |",
                "|------|--------|---------|----------|",
            ])
            for sf in shared_files:
                progs = sf["programs"].split(",")
                prog_links = ", ".join(f"[{p}](../programs/{p}.md)" if p in programs else p for p in sorted(progs))
                lines.append(f"| `{sf['file_name']}` | {sf.get('access_modes', '-')} | {sf['prog_count']} | {prog_links} |")

        lines.extend(["", "---", "", f"*Generated {self.generated}*"])
        (self.output_dir / "dependency-matrix.md").write_text("\n".join(lines), encoding="utf-8")
        console.print(f"    [green]✓ dependency-matrix.md ({len(programs)} programs)[/green]")

    # ════════════════════════════════════════════
    # 3. IMPACT ANALYSIS
    # ════════════════════════════════════════════

    def _generate_impact_analysis(self):
        console.print("  [cyan]3/5 Impact Analysis[/cyan]")
        c = self.conn.cursor()

        # Build adjacency lists
        c.execute("SELECT caller_program, called_program FROM program_calls")
        calls_out = defaultdict(set)
        called_by = defaultdict(set)
        for r in c.fetchall():
            calls_out[r["caller_program"]].add(r["called_program"])
            called_by[r["called_program"]].add(r["caller_program"])

        # Copybook sharing (programs sharing data structures)
        c.execute("SELECT copybook_name, program_id FROM copybook_usage")
        cb_to_progs = defaultdict(set)
        prog_to_cbs = defaultdict(set)
        for r in c.fetchall():
            cb_to_progs[r["copybook_name"]].add(r["program_id"])
            prog_to_cbs[r["program_id"]].add(r["copybook_name"])

        # File sharing
        c.execute("SELECT file_name, program_id FROM files")
        file_to_progs = defaultdict(set)
        for r in c.fetchall():
            file_to_progs[r["file_name"]].add(r["program_id"])

        # Programs
        c.execute("SELECT program_id, business_name, program_type FROM programs")
        programs = {r["program_id"]: dict(r) for r in c.fetchall()}

        def _transitive_callers(pid, visited=None):
            """Find ALL programs that transitively call pid."""
            if visited is None:
                visited = set()
            for caller in called_by.get(pid, set()):
                if caller not in visited and caller in programs:
                    visited.add(caller)
                    _transitive_callers(caller, visited)
            return visited

        def _transitive_callees(pid, visited=None):
            """Find ALL programs transitively called by pid."""
            if visited is None:
                visited = set()
            for callee in calls_out.get(pid, set()):
                if callee not in visited and callee in programs:
                    visited.add(callee)
                    _transitive_callees(callee, visited)
            return visited

        def _copybook_impact(pid):
            """Programs affected through shared copybooks."""
            affected = set()
            for cb in prog_to_cbs.get(pid, set()):
                affected.update(cb_to_progs.get(cb, set()))
            affected.discard(pid)
            return affected

        lines = [
            "# Impact Analysis",
            "",
            "> For each program: what happens if you change it? Who is affected?",
            "> Covers **direct calls**, **transitive dependencies**, and **data coupling** through shared copybooks/files.",
            "",
            "## Impact Summary",
            "",
            "| Program | Type | Direct Callers | Transitive Callers | Direct Callees | Transitive Callees | Copybook Coupling |",
            "|---------|------|---------------|-------------------|----------------|-------------------|-------------------|",
        ]

        impact_data = {}
        for pid in sorted(programs.keys()):
            direct_callers = called_by.get(pid, set()) & set(programs.keys())
            trans_callers = _transitive_callers(pid)
            direct_callees = calls_out.get(pid, set()) & set(programs.keys())
            trans_callees = _transitive_callees(pid)
            cb_impact = _copybook_impact(pid)

            impact_data[pid] = {
                "direct_callers": direct_callers,
                "trans_callers": trans_callers,
                "direct_callees": direct_callees,
                "trans_callees": trans_callees,
                "cb_impact": cb_impact,
                "total_impact": len(trans_callers | cb_impact),
            }

            p = programs[pid]
            lines.append(
                f"| [{pid}](../programs/{pid}.md) | {p.get('program_type', '-')} "
                f"| {len(direct_callers)} | {len(trans_callers)} "
                f"| {len(direct_callees)} | {len(trans_callees)} "
                f"| {len(cb_impact)} |"
            )

        # Top 10 highest impact programs
        by_impact = sorted(impact_data.items(), key=lambda x: x[1]["total_impact"], reverse=True)
        high_impact = [item for item in by_impact if item[1]["total_impact"] > 0]

        if high_impact:
            lines.extend([
                "",
                "## Highest Impact Programs",
                "",
                "> Changing these programs has the widest ripple effect.",
                "",
            ])
            for pid, data in high_impact[:15]:
                p = programs[pid]
                total = data["total_impact"]
                risk = "🔴 **HIGH**" if total >= 10 else "🟡 **MEDIUM**" if total >= 5 else "🟢 LOW"
                lines.extend([
                    f"### {pid} — {p.get('business_name') or 'N/A'}",
                    "",
                    f"- **Risk Level:** {risk} ({total} programs affected)",
                    f"- **Type:** {p.get('program_type', 'N/A')}",
                ])
                if data["direct_callers"]:
                    lines.append(f"- **Direct Callers:** {', '.join(sorted(data['direct_callers']))}")
                if data["trans_callers"] - data["direct_callers"]:
                    lines.append(f"- **Transitive Callers:** {', '.join(sorted(data['trans_callers'] - data['direct_callers']))}")
                if data["cb_impact"]:
                    lines.append(f"- **Copybook Coupling:** {', '.join(sorted(data['cb_impact']))}")
                lines.append("")

        # Detailed per-program impact
        lines.extend([
            "",
            "## Per-Program Impact Details",
            "",
        ])
        for pid in sorted(programs.keys()):
            data = impact_data[pid]
            if data["total_impact"] == 0 and not data["direct_callees"]:
                continue  # Skip isolated programs

            p = programs[pid]
            lines.extend([
                f"### [{pid}](../programs/{pid}.md)",
                "",
            ])

            if data["direct_callers"]:
                callers = ", ".join(f"[{c}](../programs/{c}.md)" for c in sorted(data["direct_callers"]))
                lines.append(f"- **Called by:** {callers}")
            if data["direct_callees"]:
                callees = ", ".join(f"[{c}](../programs/{c}.md)" for c in sorted(data["direct_callees"]))
                lines.append(f"- **Calls:** {callees}")
            if data["cb_impact"]:
                coupled = ", ".join(f"[{c}](../programs/{c}.md)" for c in sorted(data["cb_impact"]))
                cbs = ", ".join(f"`{cb}`" for cb in sorted(prog_to_cbs.get(pid, set())))
                lines.append(f"- **Data-coupled via copybooks** ({cbs}): {coupled}")

            lines.append("")

        lines.extend(["---", "", f"*Generated {self.generated}*"])
        (self.output_dir / "impact-analysis.md").write_text("\n".join(lines), encoding="utf-8")
        console.print(f"    [green]✓ impact-analysis.md ({len(programs)} programs analyzed)[/green]")

    # ════════════════════════════════════════════
    # 4. COPYBOOK DEPENDENCIES
    # ════════════════════════════════════════════

    def _generate_copybook_dependencies(self):
        console.print("  [cyan]4/5 Copybook Dependencies[/cyan]")
        c = self.conn.cursor()

        c.execute("""
            SELECT cu.copybook_name, cu.program_id, cu.line_number,
                   cb.business_name, cb.description
            FROM copybook_usage cu
            LEFT JOIN copybooks cb ON cu.copybook_name = cb.copybook_name
            ORDER BY cu.copybook_name
        """)
        usages = [dict(r) for r in c.fetchall()]

        c.execute("SELECT program_id FROM programs")
        all_programs = set(r["program_id"] for r in c.fetchall())

        # Group by copybook
        by_cb = defaultdict(list)
        for u in usages:
            by_cb[u["copybook_name"]].append(u)

        lines = [
            "# Copybook Dependency Graph",
            "",
            "> Copybooks are shared data structures `COPY` included by multiple programs.",
            "> They are the primary mechanism for **data coupling** in COBOL systems.",
            "",
            f"> **Total Copybooks:** {len(by_cb)}  ",
            f"> **Total COPY Statements:** {len(usages)}",
            "",
            "## Copybook Sharing Graph",
            "",
            "```mermaid",
            "graph LR",
        ]

        # Add copybook nodes
        for cb_name in sorted(by_cb.keys()):
            safe = cb_name.replace("-", "_").replace(".", "_")
            prog_count = len(set(u["program_id"] for u in by_cb[cb_name]))
            lines.append(f'    {safe}(("{cb_name}<br/>({prog_count} programs)")):::copybook')

        # Add edges
        for cb_name, cb_usages in sorted(by_cb.items()):
            safe_cb = cb_name.replace("-", "_").replace(".", "_")
            for u in cb_usages:
                if u["program_id"] in all_programs:
                    safe_prog = u["program_id"].replace("-", "_")
                    lines.append(f"    {safe_prog}[\"{u['program_id']}\"] --> {safe_cb}")

        lines.extend([
            "",
            "    classDef copybook fill:#FFC107,stroke:#F57F17,color:#000",
            "```",
            "",
            "## Copybook Details",
            "",
        ])

        for cb_name in sorted(by_cb.keys()):
            cb_usages = by_cb[cb_name]
            progs = sorted(set(u["program_id"] for u in cb_usages))
            bname = cb_usages[0].get("business_name") or ""
            desc = cb_usages[0].get("description") or ""

            lines.extend([
                f"### `{cb_name}` {('— ' + bname) if bname else ''}",
                "",
            ])
            if desc:
                lines.append(f"> {desc}")
                lines.append("")

            lines.append(f"**Used by {len(progs)} programs:**")
            lines.append("")
            lines.append("| Program | COPY Line |")
            lines.append("|---------|-----------|")
            for u in sorted(cb_usages, key=lambda x: x["program_id"]):
                pid = u["program_id"]
                ln = u.get("line_number") or "-"
                link = f"[{pid}](../programs/{pid}.md)" if pid in all_programs else pid
                lines.append(f"| {link} | {ln} |")
            lines.append("")

        lines.extend(["---", "", f"*Generated {self.generated}*"])
        (self.output_dir / "copybook-dependencies.md").write_text("\n".join(lines), encoding="utf-8")
        console.print(f"    [green]✓ copybook-dependencies.md ({len(by_cb)} copybooks)[/green]")

    # ════════════════════════════════════════════
    # 5. DATA FLOW
    # ════════════════════════════════════════════

    def _generate_data_flow(self):
        console.print("  [cyan]5/5 Data Flow Analysis[/cyan]")
        c = self.conn.cursor()

        # Get file usage
        c.execute("""
            SELECT f.program_id, f.file_name, f.file_type, f.access_mode,
                   f.organization, f.record_name, f.business_name,
                   p.program_type, p.business_name as prog_business_name
            FROM files f
            LEFT JOIN programs p ON f.program_id = p.program_id
            ORDER BY f.file_name
        """)
        file_usages = [dict(r) for r in c.fetchall()]

        # Group by file
        by_file = defaultdict(list)
        for fu in file_usages:
            by_file[fu["file_name"]].append(fu)

        # Get WRITE/READ statements as supplementary data
        c.execute("""
            SELECT program_id, statement_type, COUNT(*) as cnt
            FROM statements
            WHERE statement_type IN ('READ', 'WRITE', 'REWRITE', 'OPEN', 'CLOSE')
            GROUP BY program_id, statement_type
            ORDER BY program_id
        """)
        io_stmts = defaultdict(dict)
        for r in c.fetchall():
            io_stmts[r["program_id"]][r["statement_type"]] = r["cnt"]

        lines = [
            "# Data Flow Analysis",
            "",
            "> How data flows through the system — VSAM files, sequential files, DB2 tables, and I/O patterns.",
            "",
            f"> **Total Files:** {len(by_file)}  ",
            f"> **Total File Usages:** {len(file_usages)}  ",
            f"> **Programs with I/O:** {len(io_stmts)}",
            "",
            "## Data Flow Diagram",
            "",
            "```mermaid",
            "graph LR",
        ]

        # File nodes
        for fname in sorted(by_file.keys()):
            safe = fname.replace("-", "_").replace(".", "_")
            ftype = by_file[fname][0].get("file_type") or "FILE"
            lines.append(f'    {safe}[("{fname}<br/>({ftype})")]:::file')

        # Program-to-file edges with access mode
        for fname, fusages in sorted(by_file.items()):
            safe_f = fname.replace("-", "_").replace(".", "_")
            for fu in fusages:
                safe_p = fu["program_id"].replace("-", "_")
                access = fu.get("access_mode") or "?"
                lines.append(f'    {safe_p}["{fu["program_id"]}"] -->|"{access}"| {safe_f}')

        lines.extend([
            "",
            "    classDef file fill:#E1BEE7,stroke:#6A1B9A,color:#000",
            "```",
            "",
            "## File Details",
            "",
            "| File | Type | Organization | Programs | Access Modes |",
            "|------|------|-------------|----------|--------------|",
        ])

        for fname in sorted(by_file.keys()):
            fusages = by_file[fname]
            ftype = fusages[0].get("file_type") or "-"
            org = fusages[0].get("organization") or "-"
            progs = ", ".join(f"[{fu['program_id']}](../programs/{fu['program_id']}.md)" for fu in sorted(fusages, key=lambda x: x["program_id"]))
            accesses = ", ".join(sorted(set(fu.get("access_mode") or "?" for fu in fusages)))
            lines.append(f"| `{fname}` | {ftype} | {org} | {progs} | {accesses} |")

        # I/O Statement Profile
        if io_stmts:
            lines.extend([
                "",
                "## I/O Statement Profile",
                "",
                "| Program | READs | WRITEs | REWRITEs | OPENs | CLOSEs |",
                "|---------|-------|--------|----------|-------|--------|",
            ])
            for pid in sorted(io_stmts.keys()):
                stmts = io_stmts[pid]
                lines.append(
                    f"| [{pid}](../programs/{pid}.md) "
                    f"| {stmts.get('READ', 0)} "
                    f"| {stmts.get('WRITE', 0)} "
                    f"| {stmts.get('REWRITE', 0)} "
                    f"| {stmts.get('OPEN', 0)} "
                    f"| {stmts.get('CLOSE', 0)} |"
                )

        lines.extend(["", "---", "", f"*Generated {self.generated}*"])
        (self.output_dir / "data-flow.md").write_text("\n".join(lines), encoding="utf-8")
        console.print(f"    [green]✓ data-flow.md ({len(by_file)} files tracked)[/green]")


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate dependency analysis documentation")
    parser.add_argument("--db", default="data/cobol_knowledge.db", help="Database path")
    parser.add_argument("--output", "-o", default="docs/diagrams", help="Output directory")

    args = parser.parse_args()

    analyzer = DependencyAnalyzer(args.db, args.output)
    analyzer.generate_all()
    analyzer.close()
