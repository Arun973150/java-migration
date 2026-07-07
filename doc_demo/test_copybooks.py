#!/usr/bin/env python3
"""Test script to verify copybook extraction."""

import sqlite3
from pathlib import Path

db_path = Path('data/cobol_knowledge.db')
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    
    # Check tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]
    print('Available tables:', ', '.join(tables))
    print()
    
    # Check copybook_usage table
    if 'copybook_usage' in tables:
        cur.execute('SELECT COUNT(*) FROM copybook_usage')
        count = cur.fetchone()[0]
        print(f'Total copybook_usage records: {count}')
        
        # Check for CBACT01C
        cur.execute('SELECT copybook_name FROM copybook_usage WHERE program_id = ?', ('CBACT01C',))
        copybooks = [row[0] for row in cur.fetchall()]
        print(f'Copybooks referenced by CBACT01C: {copybooks}')
        
        if copybooks:
            print('\nCopybook details:')
            for cb in copybooks:
                cur.execute('SELECT file_path FROM copybooks WHERE copybook_name = ?', (cb,))
                result = cur.fetchone()
                path = result[0] if result else 'Not found'
                print(f'  - {cb}: {path}')
    else:
        print('ERROR: copybook_usage table not found!')
    
    conn.close()
else:
    print(f'ERROR: Database not found at {db_path.resolve()}')
