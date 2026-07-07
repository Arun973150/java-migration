"""
Neo4j Graph-Based LLM Enrichment
Enriches COBOL codebase by reading from Neo4j graph and writing enrichment back.
Uses LLM to analyze graph structure (dependencies, data flow) for richer context.
"""

import os
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console(force_terminal=True, highlight=False, legacy_windows=False)


class Neo4jEnricher:
    """Enriches COBOL programs using Neo4j graph structure and LLM."""
    
    def __init__(self, neo4j_driver=None, model: str = "gemini-2.0-flash"):
        """
        Initialize Neo4j enricher.
        
        Args:
            neo4j_driver: neo4j.GraphDatabase driver (must be pre-connected)
            model: LLM model name (default: Gemini)
        """
        self.driver = neo4j_driver
        self.model = model
        self.llm = ChatGoogleGenerativeAI(model=model, temperature=0.3)
        self.enriched_programs = []
        self.business_rules = []
        self.errors = []
    
    def get_program_graph_context(self, program_id: str) -> Dict[str, Any]:
        """Extract program context from Neo4j graph."""
        with self.driver.session() as session:
            # Get program node
            prog_result = session.run(
                """
                MATCH (p:Program {id: $pid})
                RETURN p
                """,
                pid=program_id
            )
            prog_record = prog_result.single()
            if not prog_record:
                return {}
            
            prog_node = dict(prog_record["p"])
            
            # Get callers (programs that call this one)
            callers_result = session.run(
                """
                MATCH (caller:Program)-[:CALLS]->(p:Program {id: $pid})
                RETURN caller.id, caller.name
                LIMIT 10
                """,
                pid=program_id
            )
            callers = [dict(record) for record in callers_result]
            
            # Get callees (programs this one calls)
            callees_result = session.run(
                """
                MATCH (p:Program {id: $pid})-[:CALLS]->(called:Program)
                RETURN called.id, called.name
                LIMIT 10
                """,
                pid=program_id
            )
            callees = [dict(record) for record in callees_result]
            
            # Get data items used
            data_result = session.run(
                """
                MATCH (p:Program {id: $pid})-[:USES]->(d:DataItem)
                RETURN d.name, d.picture_clause
                LIMIT 20
                """,
                pid=program_id
            )
            data_items = [dict(record) for record in data_result]
            
            # Get files accessed
            file_result = session.run(
                """
                MATCH (p:Program {id: $pid})-[:ACCESSES]->(f:File)
                RETURN f.name, f.record_length
                LIMIT 10
                """,
                pid=program_id
            )
            files = [dict(record) for record in file_result]
            
            # Get business rules in this program
            rule_result = session.run(
                """
                MATCH (p:Program {id: $pid})-[:CONTAINS_RULE]->(r:BusinessRule)
                RETURN r.name, r.description
                LIMIT 20
                """,
                pid=program_id
            )
            rules = [dict(record) for record in rule_result]
            
            return {
                "program": prog_node,
                "callers": callers,
                "callees": callees,
                "data_items": data_items,
                "files": files,
                "rules": rules
            }
    
    def enrich_program(self, program_id: str, graph_context: Dict) -> Dict:
        """Use LLM to enrich a program based on graph context."""
        if not graph_context:
            return None
        
        prog = graph_context.get("program", {})
        callers = graph_context.get("callers", [])
        callees = graph_context.get("callees", [])
        data_items = graph_context.get("data_items", [])
        files = graph_context.get("files", [])
        rules = graph_context.get("rules", [])
        
        prompt = f"""
You are a COBOL mainframe architect analyzing a system dependency graph.
Using the program's position in the call graph and data dependencies, 
provide migration insights and business context.

Program: {prog.get('id', 'UNKNOWN')} ({prog.get('program_type', 'UNKNOWN')})
Line Count: {prog.get('line_count', 'N/A')}

UPSTREAM (Programs calling this):
{json.dumps(callers, indent=2)}

DOWNSTREAM (Programs this calls):
{json.dumps(callees, indent=2)}

Key Data Items:
{json.dumps(data_items[:10], indent=2)}

Files Accessed:
{json.dumps(files, indent=2)}

Extracted Rules:
{json.dumps(rules[:5], indent=2)}

Based on this graph structure, provide enrichment:
{{
  "graph_position": "Is this central hub, leaf node, or middle layer? What role does it play?",
  "integration_points": "List key dependencies and what data flows through them",
  "migration_complexity": "SIMPLE | MODERATE | COMPLEX",
  "migration_rationale": "Why is it at this complexity level?",
  "risk_factors": "What aspects make migration risky?",
  "refactoring_opportunities": "How could this be refactored in modern architecture?",
  "data_contract": "What is the contract between this and its callers?"
}}
"""
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="Respond with valid JSON only. No markdown."),
                HumanMessage(content=prompt)
            ])
            
            result_text = response.content.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            enrichment = json.loads(result_text.strip())
            enrichment["program_id"] = program_id
            
            return enrichment
        
        except Exception as e:
            self.errors.append(f"Error enriching {program_id}: {e}")
            return None
    
    def enrich_from_neo4j(self, program_ids: List[str] = None) -> Dict:
        """
        Enrich programs by reading from Neo4j.
        
        Args:
            program_ids: List of program IDs to enrich (None = all)
            
        Returns:
            Dict with enriched_programs and enrichment_metadata
        """
        if program_ids is None:
            # Get all programs
            with self.driver.session() as session:
                result = session.run("MATCH (p:Program) RETURN p.id")
                program_ids = [record[0] for record in result]
        
        self.enriched_programs = []
        self.errors = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(
                f"[cyan]Enriching {len(program_ids)} programs from Neo4j...",
                total=len(program_ids),
            )
            
            for program_id in program_ids:
                try:
                    context = self.get_program_graph_context(program_id)
                    if context:
                        enrichment = self.enrich_program(program_id, context)
                        if enrichment:
                            self.enriched_programs.append(enrichment)
                except Exception as e:
                    self.errors.append(f"Failed to process {program_id}: {e}")
                finally:
                    progress.update(task, advance=1)
        
        return {
            "enriched_programs": self.enriched_programs,
            "total_enriched": len(self.enriched_programs),
            "errors": self.errors,
            "model": self.model
        }
    
    def save_enrichment_to_neo4j(self):
        """Write enrichment back into Neo4j as program properties."""
        if not self.driver:
            raise ValueError("Neo4j driver not connected")
        
        with self.driver.session() as session:
            for enrichment in self.enriched_programs:
                program_id = enrichment.pop("program_id")
                
                # Build SET clause from enrichment dict
                set_items = ", ".join([
                    f"p.{key} = ${key}"
                    for key in enrichment.keys()
                ])
                
                query = f"""
                MATCH (p:Program {{id: $program_id}})
                SET {set_items}
                """
                
                params = {"program_id": program_id}
                params.update(enrichment)
                
                try:
                    session.run(query, **params)
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not write enrichment for {program_id}: {e}[/yellow]")
        
        console.print(f"[green]OK - Wrote {len(self.enriched_programs)} enrichments to Neo4j[/green]")
    
    def export_enrichment_files(self, output_dir: str):
        """Export enrichments as JSON files (for compatibility)."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        enrichment_file = output_path / "neo4j_enrichments.json"
        with open(enrichment_file, "w") as f:
            json.dump(self.enriched_programs, f, indent=2)
        
        console.print(f"[green]Exported enrichments to {enrichment_file}[/green]")
