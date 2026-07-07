
import os
import json
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

from langgraph_enricher import CobolEnricher
from sqlite_loader import SQLiteLoader

load_dotenv()

DB_PATH = "data/cobol_knowledge.db"
CORE_PROGRAMS = ["CBACT01C", "CBPAU01C", "CBMEN01C"]

def enrich_specimens():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    # 1. Initialize Enricher & Loader
    enricher = CobolEnricher(groq_api_key=api_key, model="llama-3.1-8b-instant", max_programs=5)
    loader = SQLiteLoader(DB_PATH)
    loader.connect()

    print(f"Starting specimen enrichment for: {', '.join(CORE_PROGRAMS)}")

    # 2. Fetch raw data for each program
    raw_programs = []
    for pid in CORE_PROGRAMS:
        print(f"  Fetching data for {pid}...")
        prog_data = loader.get_program_details(pid)
        if prog_data:
            # The enricher expects a specific structure, format it slightly
            raw_programs.append(prog_data)
        else:
            print(f"  Warning: {pid} not found in database.")

    if not raw_programs:
        print("No programs found to enrich.")
        return

    # 3. Run Enrichment
    # The enricher processes a list. We'll pass our 3 programs.
    results = enricher.enrich(raw_programs)
    
    # 4. Save results back to DB
    print("Saving enriched results to database...")
    loader.load_programs(results["programs"])
    loader.load_business_rules(results["business_rules"])

    print("Success! Specimen enrichment complete.")
    loader.close()

if __name__ == "__main__":
    enrich_specimens()
