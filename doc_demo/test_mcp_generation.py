#!/usr/bin/env python3
"""Test MCP generation with copybooks."""

import sys
from pathlib import Path

sys.path.insert(0, 'src')

from sqlite_loader import SQLiteLoader
from mcp_migration_generator import generate_mcp_package

# Initialize database loader
PROJECT_ROOT = Path.cwd()
db_path = PROJECT_ROOT / "data" / "cobol_knowledge.db"

print(f"Database path: {db_path}")
print(f"Project root: {PROJECT_ROOT}")
print()

loader = SQLiteLoader(str(db_path))
loader.connect()

print("Generating MCP package for CBACT01C...")
result = generate_mcp_package(
    loader=loader,
    program_id="CBACT01C",
    project_root=PROJECT_ROOT,
    use_llm=False  # Use fallback, no LLM
)

loader.close()

print(f"Program ID: {result.get('program_id')}")
print(f"MCP Code length: {len(result.get('mcp_code', ''))} chars")
print(f"Number of copybooks: {len(result.get('copybooks', []))}")
print()

copybooks = result.get('copybooks', [])
if copybooks:
    print("Copybooks found:")
    for cb_name, cb_code in copybooks:
        print(f"  - {cb_name}: {len(cb_code)} chars")
        print(f"    First 100 chars: {cb_code[:100]}")
else:
    print("ERROR: No copybooks found!")

print()
print("First 300 chars of program code:")
print(result.get('mcp_code', '')[:300])
