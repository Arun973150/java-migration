-- COBOL Knowledge Database Schema
-- SQLite schema for storing parsed COBOL analysis

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- ============================================
-- Table: programs
-- Core COBOL program information
-- ============================================
CREATE TABLE IF NOT EXISTS programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT UNIQUE NOT NULL,
    file_path TEXT NOT NULL,
    file_hash TEXT,  -- For incremental updates
    program_type TEXT,  -- ONLINE, BATCH, UTILITY
    line_count INTEGER,
    
    -- LLM Enriched fields
    business_name TEXT,
    business_purpose TEXT,
    user_role TEXT,
    business_process TEXT,

    -- Migration fields (LLM enriched)
    migration_complexity INTEGER,           -- 1-5 score
    complexity_reason TEXT,
    modern_equivalent TEXT,
    suggested_service TEXT,
    migration_approach TEXT,
    data_contracts TEXT,
    migration_risks TEXT,
    dependencies_to_migrate_first TEXT,     -- JSON array of program IDs

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_programs_type ON programs(program_type);

-- ============================================
-- Table: paragraphs
-- Executable sections within programs
-- ============================================
CREATE TABLE IF NOT EXISTS paragraphs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    paragraph_name TEXT NOT NULL,
    line_start INTEGER,
    line_end INTEGER,
    
    -- LLM Enriched fields
    business_name TEXT,
    narrative TEXT,
    purpose TEXT,
    
    FOREIGN KEY (program_id) REFERENCES programs(program_id),
    UNIQUE(program_id, paragraph_name)
);

CREATE INDEX IF NOT EXISTS idx_paragraphs_program ON paragraphs(program_id);

-- ============================================
-- Table: data_items
-- Variables (Working-Storage, Linkage, File Section)
-- ============================================
CREATE TABLE IF NOT EXISTS data_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    name TEXT NOT NULL,
    level_number INTEGER,
    picture TEXT,
    usage TEXT,
    value TEXT,
    section TEXT,  -- WORKING-STORAGE, LINKAGE, FILE
    parent_name TEXT,  -- For hierarchical structures
    line_number INTEGER,
    
    -- LLM Enriched fields
    business_name TEXT,
    description TEXT,
    data_type_description TEXT,
    
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_data_items_program ON data_items(program_id);
CREATE INDEX IF NOT EXISTS idx_data_items_name ON data_items(name);

-- ============================================
-- Table: files
-- VSAM/Sequential files used by programs
-- ============================================
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT,  -- VSAM, SEQUENTIAL, INDEXED
    organization TEXT,
    access_mode TEXT,
    record_name TEXT,
    
    -- LLM Enriched fields
    business_name TEXT,
    description TEXT,
    
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_files_program ON files(program_id);

-- ============================================
-- Table: statements
-- Every executable statement
-- ============================================
CREATE TABLE IF NOT EXISTS statements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    paragraph_name TEXT,
    statement_type TEXT NOT NULL,  -- CALL, PERFORM, IF, MOVE, READ, WRITE, EVALUATE
    line_number INTEGER,
    details_json TEXT,  -- JSON with condition, parameters, etc.
    raw_text TEXT,      -- Original source statement text for regeneration/conversion
    normalized_text TEXT, -- Source statement after COBOL sequence/comment cleanup
    
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_statements_program ON statements(program_id);
CREATE INDEX IF NOT EXISTS idx_statements_type ON statements(statement_type);
CREATE INDEX IF NOT EXISTS idx_statements_paragraph ON statements(paragraph_name);

-- ============================================
-- Table: program_calls
-- Inter-program dependencies (CALL statements)
-- ============================================
CREATE TABLE IF NOT EXISTS program_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caller_program TEXT NOT NULL,
    called_program TEXT NOT NULL,
    call_location TEXT,  -- Paragraph where call occurs
    line_number INTEGER,
    parameters_json TEXT,
    
    FOREIGN KEY (caller_program) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_calls_caller ON program_calls(caller_program);
CREATE INDEX IF NOT EXISTS idx_calls_called ON program_calls(called_program);

-- ============================================
-- Table: performs
-- Intra-program control flow (PERFORM statements)
-- ============================================
CREATE TABLE IF NOT EXISTS performs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    source_paragraph TEXT NOT NULL,
    target_paragraph TEXT NOT NULL,
    perform_type TEXT,  -- SIMPLE, THRU, UNTIL, TIMES, VARYING
    line_number INTEGER,
    condition TEXT,
    
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_performs_program ON performs(program_id);
CREATE INDEX IF NOT EXISTS idx_performs_source ON performs(source_paragraph);
CREATE INDEX IF NOT EXISTS idx_performs_target ON performs(target_paragraph);

-- ============================================
-- Table: copybooks
-- Shared data structures
-- ============================================
CREATE TABLE IF NOT EXISTS copybooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    copybook_name TEXT UNIQUE NOT NULL,
    file_path TEXT,
    file_hash TEXT,
    
    -- LLM Enriched fields
    business_name TEXT,
    description TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_copybooks_name ON copybooks(copybook_name);

-- ============================================
-- Table: copybook_usage
-- Which programs include which copybooks
-- ============================================
CREATE TABLE IF NOT EXISTS copybook_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    copybook_name TEXT NOT NULL,
    line_number INTEGER,
    
    FOREIGN KEY (program_id) REFERENCES programs(program_id),
    FOREIGN KEY (copybook_name) REFERENCES copybooks(copybook_name)
);

CREATE INDEX IF NOT EXISTS idx_copybook_usage_program ON copybook_usage(program_id);

-- ============================================
-- Table: business_rules
-- Extracted business logic (LLM populated)
-- ============================================
CREATE TABLE IF NOT EXISTS business_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id TEXT UNIQUE NOT NULL,
    rule_name TEXT NOT NULL,
    rule_statement TEXT NOT NULL,
    category TEXT,  -- VALIDATION, CALCULATION, WORKFLOW, COMPLIANCE
    program_id TEXT,
    paragraph_name TEXT,
    line_start INTEGER,
    line_end INTEGER,
    condition_text TEXT,
    action_text TEXT,
    source_code TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_rules_program ON business_rules(program_id);
CREATE INDEX IF NOT EXISTS idx_rules_category ON business_rules(category);

-- ============================================
-- Table: screens
-- BMS map definitions
-- ============================================
CREATE TABLE IF NOT EXISTS screens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT,
    screen_name TEXT NOT NULL,
    map_name TEXT,
    mapset_name TEXT,
    file_path TEXT,
    associated_program TEXT,
    
    -- LLM Enriched fields
    business_name TEXT,
    description TEXT,
    
    FOREIGN KEY (associated_program) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_screens_transaction ON screens(transaction_id);
CREATE INDEX IF NOT EXISTS idx_screens_program ON screens(associated_program);

-- ============================================
-- Table: screen_fields
-- Fields within BMS screens
-- ============================================
CREATE TABLE IF NOT EXISTS screen_fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    screen_id INTEGER NOT NULL,
    field_name TEXT NOT NULL,
    field_type TEXT,  -- INPUT, OUTPUT, BOTH
    length INTEGER,
    row_position INTEGER,
    col_position INTEGER,
    attributes TEXT,
    
    -- LLM Enriched fields
    business_name TEXT,
    description TEXT,
    
    FOREIGN KEY (screen_id) REFERENCES screens(id)
);

-- ============================================
-- Table: modules
-- Logical groupings (auto-detected or manual)
-- ============================================
CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_name TEXT UNIQUE NOT NULL,
    
    -- LLM Enriched fields
    business_name TEXT,
    description TEXT,
    business_purpose TEXT
);

-- ============================================
-- Table: module_programs
-- Programs belonging to each module
-- ============================================
CREATE TABLE IF NOT EXISTS module_programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    program_id TEXT NOT NULL,
    
    FOREIGN KEY (module_id) REFERENCES modules(id),
    FOREIGN KEY (program_id) REFERENCES programs(program_id),
    UNIQUE(module_id, program_id)
);

-- ============================================
-- Table: jcl_jobs
-- One row per JCL file (job definition)
-- ============================================
CREATE TABLE IF NOT EXISTS jcl_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name TEXT UNIQUE NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_hash TEXT,
    job_description TEXT,
    job_class TEXT,
    msg_class TEXT,
    header_comments TEXT,           -- Full block of //* header comments
    programs_called TEXT,           -- JSON array of PGM= values (COBOL programs only)
    input_datasets TEXT,            -- JSON array of input DSNs
    output_datasets TEXT,           -- JSON array of output DSNs
    step_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_jcl_jobs_name ON jcl_jobs(job_name);

-- ============================================
-- Table: jcl_steps
-- One row per EXEC step inside a JCL job
-- ============================================
CREATE TABLE IF NOT EXISTS jcl_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name TEXT NOT NULL,
    step_name TEXT NOT NULL,
    step_order INTEGER NOT NULL,
    program TEXT,                   -- PGM= value (COBOL program or utility)
    proc TEXT,                      -- PROC= value
    step_type TEXT,                 -- PGM | PROC | UTIL | UNKNOWN
    step_comments TEXT,             -- //* lines immediately above this EXEC
    cond TEXT,                      -- COND= value
    line_number INTEGER,
    sysin_data TEXT,                -- Inline SYSIN content (JSON array of lines)
    FOREIGN KEY (job_name) REFERENCES jcl_jobs(job_name) ON DELETE CASCADE,
    UNIQUE(job_name, step_name)
);

CREATE INDEX IF NOT EXISTS idx_jcl_steps_job ON jcl_steps(job_name);
CREATE INDEX IF NOT EXISTS idx_jcl_steps_program ON jcl_steps(program);

-- ============================================
-- Table: jcl_datasets
-- DD cards — files/datasets per step
-- ============================================
CREATE TABLE IF NOT EXISTS jcl_datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_name TEXT NOT NULL,
    step_name TEXT NOT NULL,
    dd_name TEXT NOT NULL,
    dsn TEXT,
    disp TEXT,
    disposition_normal TEXT,
    disposition_abnormal TEXT,
    direction TEXT,                 -- INPUT | OUTPUT | SYSTEM | INLINE
    recfm TEXT,
    lrecl TEXT,
    unit TEXT,
    space TEXT,
    is_inline INTEGER DEFAULT 0,
    FOREIGN KEY (job_name) REFERENCES jcl_jobs(job_name) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_jcl_datasets_job ON jcl_datasets(job_name);
CREATE INDEX IF NOT EXISTS idx_jcl_datasets_dsn ON jcl_datasets(dsn);

-- ============================================
-- Table: exec_cics
-- EXEC CICS commands found in programs
-- ============================================
CREATE TABLE IF NOT EXISTS exec_cics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    command TEXT NOT NULL,           -- SEND, RECEIVE, READ, WRITE, REWRITE, DELETE, XCTL, LINK, RETURN, etc.
    paragraph_name TEXT,
    line_number INTEGER,
    details_json TEXT,               -- JSON with resource, mapset, dataset, transid, etc.
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_exec_cics_program ON exec_cics(program_id);
CREATE INDEX IF NOT EXISTS idx_exec_cics_command ON exec_cics(command);

-- ============================================
-- Table: exec_sql
-- EXEC SQL (DB2) statements found in programs
-- ============================================
CREATE TABLE IF NOT EXISTS exec_sql (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    command TEXT NOT NULL,           -- SELECT, INSERT, UPDATE, DELETE, DECLARE, OPEN, FETCH, CLOSE, INCLUDE
    table_name TEXT,                 -- primary table referenced (best effort)
    cursor_name TEXT,                -- for DECLARE/OPEN/FETCH/CLOSE
    paragraph_name TEXT,
    line_number INTEGER,
    sql_text TEXT,                   -- compact form of the SQL block
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_exec_sql_program ON exec_sql(program_id);
CREATE INDEX IF NOT EXISTS idx_exec_sql_command ON exec_sql(command);
CREATE INDEX IF NOT EXISTS idx_exec_sql_table   ON exec_sql(table_name);

-- ============================================
-- Table: copybook_fields
-- Field-level dictionary for each copybook
-- ============================================
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
    redefines_target TEXT,
    FOREIGN KEY (copybook_name) REFERENCES copybooks(copybook_name)
);
CREATE INDEX IF NOT EXISTS idx_copybook_fields_name ON copybook_fields(copybook_name);

-- ============================================
-- Table: file_records
-- FD record layouts (file descriptions) per program
-- ============================================
CREATE TABLE IF NOT EXISTS file_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    file_name TEXT NOT NULL,             -- the FD name
    record_name TEXT,                    -- the 01-level record name
    field_name TEXT,                     -- nested field name
    level_number INTEGER,
    picture TEXT,
    usage TEXT,
    parent_name TEXT,
    line_number INTEGER,
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);
CREATE INDEX IF NOT EXISTS idx_file_records_program ON file_records(program_id);
CREATE INDEX IF NOT EXISTS idx_file_records_file ON file_records(file_name);

-- ============================================
-- Table: data_movements
-- MOVE source -> destination (data lineage)
-- ============================================
CREATE TABLE IF NOT EXISTS data_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    source_field TEXT NOT NULL,
    destination_field TEXT NOT NULL,
    paragraph_name TEXT,
    line_number INTEGER,
    is_literal INTEGER DEFAULT 0,
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);
CREATE INDEX IF NOT EXISTS idx_data_movements_program ON data_movements(program_id);
CREATE INDEX IF NOT EXISTS idx_data_movements_source ON data_movements(source_field);
CREATE INDEX IF NOT EXISTS idx_data_movements_dest ON data_movements(destination_field);

-- ============================================
-- Table: code_anomalies
-- Suspicious patterns / known issues detected by static analysis
-- (e.g. duplicate IF condition, unused variable, name mismatches)
-- ============================================
CREATE TABLE IF NOT EXISTS code_anomalies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    severity TEXT NOT NULL,              -- BUG | WARNING | NOTICE
    category TEXT NOT NULL,              -- LOGIC | DEAD_CODE | NAMING | STYLE | INCOMPLETE
    rule_id TEXT NOT NULL,               -- short identifier (e.g. "DUPLICATE_AND_CONDITION")
    title TEXT NOT NULL,
    description TEXT,
    paragraph_name TEXT,
    line_number INTEGER,
    snippet TEXT,                        -- short code excerpt around the issue
    suggestion TEXT,                     -- recommended fix or migration note
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);
CREATE INDEX IF NOT EXISTS idx_code_anomalies_program ON code_anomalies(program_id);
CREATE INDEX IF NOT EXISTS idx_code_anomalies_severity ON code_anomalies(severity);

-- ============================================
-- Table: mq_calls
-- IBM MQ API calls (MQOPEN/MQGET/MQPUT/MQCLOSE/MQCONN/MQDISC/MQCMIT/MQBACK)
-- ============================================
CREATE TABLE IF NOT EXISTS mq_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    function_code TEXT NOT NULL,        -- MQOPEN, MQGET, MQPUT, MQCLOSE, MQCONN, MQDISC, MQCMIT, MQBACK
    function_name TEXT,                 -- friendly description
    queue_name TEXT,                    -- target queue, where derivable
    queue_manager TEXT,                 -- queue manager name (from MQCONN)
    object_descriptor TEXT,             -- MQOD area
    message_descriptor TEXT,            -- MQMD area
    options_area TEXT,                  -- MQGMO/MQPMO/MQCNO area
    paragraph_name TEXT,
    line_number INTEGER,
    raw_text TEXT,
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);
CREATE INDEX IF NOT EXISTS idx_mq_calls_program ON mq_calls(program_id);
CREATE INDEX IF NOT EXISTS idx_mq_calls_function ON mq_calls(function_code);
CREATE INDEX IF NOT EXISTS idx_mq_calls_queue ON mq_calls(queue_name);

-- ============================================
-- Table: evaluate_branches
-- EVALUATE / WHEN decision tables
-- ============================================
CREATE TABLE IF NOT EXISTS evaluate_branches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    evaluate_id TEXT NOT NULL,           -- "<program>:<paragraph>:<line>" identifier
    subject TEXT,                        -- what's being evaluated (TRUE / variable / expression)
    branch_index INTEGER,                -- order: 0,1,2,... ; -1 for WHEN OTHER
    when_condition TEXT,                 -- the WHEN expression
    action_summary TEXT,                 -- first executable line of the branch
    paragraph_name TEXT,
    line_number INTEGER,
    is_default INTEGER DEFAULT 0,        -- 1 for WHEN OTHER
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);
CREATE INDEX IF NOT EXISTS idx_evaluate_branches_program ON evaluate_branches(program_id);
CREATE INDEX IF NOT EXISTS idx_evaluate_branches_eval ON evaluate_branches(evaluate_id);

-- ============================================
-- Table: cics_handles
-- EXEC CICS HANDLE CONDITION routing (condition -> error paragraph)
-- ============================================
CREATE TABLE IF NOT EXISTS cics_handles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    handle_type TEXT NOT NULL,           -- CONDITION | AID | ABEND
    condition_name TEXT NOT NULL,        -- e.g. ERROR, NOTFND, MAPFAIL
    target_paragraph TEXT,               -- routing destination (NULL = SUSPEND/continue)
    paragraph_name TEXT,                 -- paragraph containing the HANDLE statement
    line_number INTEGER,
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);
CREATE INDEX IF NOT EXISTS idx_cics_handles_program ON cics_handles(program_id);
CREATE INDEX IF NOT EXISTS idx_cics_handles_target ON cics_handles(target_paragraph);

-- ============================================
-- Table: program_parameters
-- PROCEDURE DIVISION USING parameters (external runtime inputs)
-- ============================================
CREATE TABLE IF NOT EXISTS program_parameters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    position INTEGER,
    parameter_name TEXT NOT NULL,
    source TEXT,
    line_number INTEGER,
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);
CREATE INDEX IF NOT EXISTS idx_program_parameters_program ON program_parameters(program_id);

-- ============================================
-- Table: file_operations
-- Every OPEN/CLOSE with the explicit mode (INPUT/OUTPUT/I-O/EXTEND)
-- ============================================
CREATE TABLE IF NOT EXISTS file_operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    mode TEXT,
    paragraph_name TEXT,
    line_number INTEGER,
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);
CREATE INDEX IF NOT EXISTS idx_file_ops_program ON file_operations(program_id);
CREATE INDEX IF NOT EXISTS idx_file_ops_file ON file_operations(file_name);

-- ============================================
-- Table: ims_calls
-- IMS DL/I CALL 'CBLTDLI' statements found in programs
-- ============================================
CREATE TABLE IF NOT EXISTS ims_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    program_id TEXT NOT NULL,
    function_code TEXT NOT NULL,      -- GU, GHN, GNP, GN, ISRT, REPL, DLET, CHKP, etc.
    function_name TEXT,               -- "Get Unique", "Get Hold Next", etc.
    pcb_name TEXT,                    -- PCB variable name
    segment_area TEXT,                -- I/O area variable
    ssa_name TEXT,                    -- SSA variable name (if any)
    ssa_segment TEXT,                 -- Segment name from SSA layout (if extractable)
    ssa_qualifier TEXT,               -- Qualified SSA field (if any)
    paragraph_name TEXT,
    line_number INTEGER,
    raw_text TEXT,                    -- Compact form of the CALL statement
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
);

CREATE INDEX IF NOT EXISTS idx_ims_calls_program ON ims_calls(program_id);
CREATE INDEX IF NOT EXISTS idx_ims_calls_function ON ims_calls(function_code);

-- ============================================
-- Full-Text Search Tables (FTS5)
-- ============================================
CREATE VIRTUAL TABLE IF NOT EXISTS programs_fts USING fts5(
    program_id,
    business_name,
    business_purpose,
    content='programs',
    content_rowid='id'
);

CREATE VIRTUAL TABLE IF NOT EXISTS data_items_fts USING fts5(
    name,
    business_name,
    description,
    content='data_items',
    content_rowid='id'
);

CREATE VIRTUAL TABLE IF NOT EXISTS business_rules_fts USING fts5(
    rule_name,
    rule_statement,
    condition_text,
    action_text,
    content='business_rules',
    content_rowid='id'
);

-- ============================================
-- FTS Triggers for auto-sync
-- ============================================
CREATE TRIGGER IF NOT EXISTS programs_ai AFTER INSERT ON programs BEGIN
    INSERT INTO programs_fts(rowid, program_id, business_name, business_purpose)
    VALUES (NEW.id, NEW.program_id, NEW.business_name, NEW.business_purpose);
END;

CREATE TRIGGER IF NOT EXISTS programs_ad AFTER DELETE ON programs BEGIN
    INSERT INTO programs_fts(programs_fts, rowid, program_id, business_name, business_purpose)
    VALUES ('delete', OLD.id, OLD.program_id, OLD.business_name, OLD.business_purpose);
END;

CREATE TRIGGER IF NOT EXISTS programs_au AFTER UPDATE ON programs BEGIN
    INSERT INTO programs_fts(programs_fts, rowid, program_id, business_name, business_purpose)
    VALUES ('delete', OLD.id, OLD.program_id, OLD.business_name, OLD.business_purpose);
    INSERT INTO programs_fts(rowid, program_id, business_name, business_purpose)
    VALUES (NEW.id, NEW.program_id, NEW.business_name, NEW.business_purpose);
END;

CREATE TRIGGER IF NOT EXISTS data_items_ai AFTER INSERT ON data_items BEGIN
    INSERT INTO data_items_fts(rowid, name, business_name, description)
    VALUES (NEW.id, NEW.name, NEW.business_name, NEW.description);
END;

CREATE TRIGGER IF NOT EXISTS business_rules_ai AFTER INSERT ON business_rules BEGIN
    INSERT INTO business_rules_fts(rowid, rule_name, rule_statement, condition_text, action_text)
    VALUES (NEW.id, NEW.rule_name, NEW.rule_statement, NEW.condition_text, NEW.action_text);
END;

-- ============================================
-- Useful Views
-- ============================================

-- View: Program call hierarchy
CREATE VIEW IF NOT EXISTS v_call_hierarchy AS
SELECT 
    pc.caller_program,
    p1.business_name as caller_business_name,
    pc.called_program,
    p2.business_name as called_business_name,
    pc.line_number
FROM program_calls pc
LEFT JOIN programs p1 ON pc.caller_program = p1.program_id
LEFT JOIN programs p2 ON pc.called_program = p2.program_id;

-- View: Program with file operations
CREATE VIEW IF NOT EXISTS v_program_files AS
SELECT 
    p.program_id,
    p.business_name as program_business_name,
    f.file_name,
    f.file_type,
    f.access_mode,
    f.business_name as file_business_name
FROM programs p
JOIN files f ON p.program_id = f.program_id;

-- View: Business rules by program
CREATE VIEW IF NOT EXISTS v_program_rules AS
SELECT 
    p.program_id,
    p.business_name as program_business_name,
    br.rule_id,
    br.rule_name,
    br.rule_statement,
    br.category
FROM programs p
JOIN business_rules br ON p.program_id = br.program_id;
