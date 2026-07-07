"""
Export: COBOL Programs JSON with English Explanations
------------------------------------------------------
Merges parsed structure (parsed_output/programs.json)
with LLM enrichment (enriched_output/enriched_programs.json)
into a single clean JSON: data/programs_english.json

Run after enrichment completes:
  python export_english.py
"""

import json
import sys
from pathlib import Path

PARSED_JSON   = Path("parsed_output/programs.json")
ENRICHED_JSON = Path("enriched_output/enriched_programs.json")
RULES_JSON    = Path("enriched_output/business_rules.json")
OUTPUT_JSON   = Path("data/programs_english.json")


def build_export():
    # Load parsed (structural) data
    raw_programs = {p["program_id"]: p for p in json.loads(PARSED_JSON.read_text(encoding="utf-8"))}

    # Load enriched data (English explanations)
    enriched_programs = {}
    if ENRICHED_JSON.exists():
        for p in json.loads(ENRICHED_JSON.read_text(encoding="utf-8")):
            enriched_programs[p["program_id"]] = p

    # Load business rules
    rules_by_program = {}
    if RULES_JSON.exists():
        for rule in json.loads(RULES_JSON.read_text(encoding="utf-8")):
            pid = rule.get("program_id", "")
            rules_by_program.setdefault(pid, []).append(rule)

    results = []

    all_program_ids = set(raw_programs) | set(enriched_programs)
    for pid in sorted(all_program_ids):
        raw = raw_programs.get(pid, {})
        enr = enriched_programs.get(pid, {})

        # English explanations (from enrichment)
        english = {
            "business_name":      enr.get("business_name") or "",
            "business_purpose":   enr.get("business_purpose") or "",
            "user_role":          enr.get("user_role") or "",
            "business_process":   enr.get("business_process") or "",
            "migration_complexity": enr.get("migration_complexity"),
            "complexity_reason":  enr.get("complexity_reason") or "",
            "modern_equivalent":  enr.get("modern_equivalent") or "",
            "suggested_service":  enr.get("suggested_service") or "",
            "migration_approach": enr.get("migration_approach") or "",
            "data_contracts":     enr.get("data_contracts") or "",
            "migration_risks":    enr.get("migration_risks") or "",
            "dependencies_to_migrate_first": enr.get("dependencies_to_migrate_first") or [],
        }

        # Paragraphs with English narratives (merged from enrichment)
        enr_paragraphs = {p.get("paragraph_name") or p.get("name"): p for p in enr.get("paragraphs", [])}
        paragraphs = []
        for para in (enr.get("paragraphs") or raw.get("paragraphs", [])):
            ep = enr_paragraphs.get(para.get("paragraph_name") or para.get("name"), {})
            paragraphs.append({
                "name":          para.get("paragraph_name") or para.get("name"),
                "line_start":    para.get("line_start"),
                "line_end":      para.get("line_end"),
                "english_name":  ep.get("business_name") or "",
                "narrative":     ep.get("narrative") or "",
                "purpose":       ep.get("purpose") or "",
                "statement_count": para.get("statement_count", 0),
            })

        # Business rules extracted for this program
        rules = [
            {
                "rule_id":    r.get("rule_id"),
                "rule_type":  r.get("rule_type"),
                "description": r.get("description"),
                "condition":  r.get("condition"),
                "action":     r.get("action"),
            }
            for r in rules_by_program.get(pid, [])
        ]

        entry = {
            # Identity
            "program_id":    pid,
            "file_path":     raw.get("file_path") or enr.get("file_path", ""),
            "program_type":  raw.get("program_type") or enr.get("program_type", ""),
            "line_count":    raw.get("line_count") or enr.get("line_count", 0),

            # English explanations (LLM generated)
            "english": english,

            # Paragraphs with narratives
            "paragraphs": paragraphs,

            # Business rules
            "business_rules": rules,

            # Raw structural data
            "structure": {
                "calls":      raw.get("calls", []),
                "performs":   raw.get("performs", []),
                "copybooks":  raw.get("copybooks", []),
                "files":      raw.get("files", []),
                "exec_cics":  raw.get("exec_cics", []),
                "statements": raw.get("statements", {}),
            },
        }
        results.append(entry)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return results


if __name__ == "__main__":
    print(f"Reading: {PARSED_JSON}")
    print(f"Reading: {ENRICHED_JSON}")

    results = build_export()

    enriched_count = sum(1 for p in results if p["english"]["business_purpose"])
    print(f"\nExported {len(results)} programs → {OUTPUT_JSON}")
    print(f"  {enriched_count} have English explanations")
    print(f"  {len(results) - enriched_count} still need enrichment")

    # Preview first enriched program
    for p in results:
        if p["english"]["business_purpose"]:
            print(f"\n--- Preview: {p['program_id']} ---")
            print(f"Name:    {p['english']['business_name']}")
            print(f"Purpose: {p['english']['business_purpose'][:300]}")
            print(f"Role:    {p['english']['user_role']}")
            print(f"Process: {p['english']['business_process']}")
            print(f"Rules:   {len(p['business_rules'])}")
            break
