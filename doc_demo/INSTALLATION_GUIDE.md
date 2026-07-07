# COBOL Knowledge Base — Installation & Setup Guide

This guide provides step-by-step instructions to set up the COBOL Knowledge Base application from scratch on a Windows system.

## 1. Prerequisites

Ensure you have the following installed on your system:

- **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
- **Java 11+**: Required for the ProLeap COBOL Parser. [Download OpenJDK](https://adoptium.net/)
- **Git**: (Optional) For cloning the repository.
- **SQLite**: (Included with Python)

## 2. Environment Setup

### 1. Clone or Download the Project
```bash
# Navigate to your desired directory
cd C:\Users\ADMIN\OneDrive\Desktop
# Clone the repository (or extract the zip)
git clone <repository-url> doc_demo
cd doc_demo
```

### 2. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.
```powershell
# Create venv
python -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

## 3. Configuration

### 1. Environment Variables
Create a `.env` file in the root directory (or copy from `.env.example`).
```powershell
cp .env.example .env
```

Edit the `.env` file and add your configuration:
```ini
DB_PATH=data/cobol_knowledge.db
GROQ_API_KEY=your_api_key_here
```

## 4. Initializing the Database

If you are starting from scratch without a database, you need to run the initial parsing and loading pipeline.

### 1. Run the Pipeline
This command will parse the COBOL source code (in the `carddemo/` folder) and load it into SQLite.
```powershell
python run_pipeline.py
```
*Note: To enable AI enrichment during the initial load, ensure your `GROQ_API_KEY` is set and modify `run_pipeline.py` to set `skip_enrich=False`.*

## 5. Running the Application

### 1. Interactive Dashboard (Streamlit)
To launch the web-based dashboard with visual diagrams and Program Explorer:
```powershell
streamlit run app.py
```
The dashboard will be available at `http://localhost:8501`.

### 2. Chat Assistant (CLI)
To use the AI-powered chat interface directly from your terminal:
```powershell
python src/chat_cli.py
```

## 6. Troubleshooting

- **Mermaid Syntax Error**: If diagrams fail to render, ensure you are using the latest `app.py` which includes robust ID sanitization and label quoting.
- **Java Errors**: If ProLeap fails, verify that `JAVA_HOME` is correctly set in your environment variables.
- **Integrity Error**: The current `sqlite_loader.py` uses `INSERT OR REPLACE` to handle duplicate data during re-runs.

---
*Created on 2026-02-10*
