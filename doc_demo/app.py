"""Streamlit launcher for the COBOL Documentation Dashboard.

This wrapper lets the documented command `streamlit run app.py` work from the
project root while keeping the implementation in `src/app.py`.
"""

from src.app import *  # noqa: F401,F403
