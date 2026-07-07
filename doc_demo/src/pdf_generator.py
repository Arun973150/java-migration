"""
PDF Report Generator for COBOL Knowledge Base
Generates downloadable PDF reports for programs, chat conversations, and analysis.
"""

import io
import os
import json
import textwrap
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class PDFReportGenerator:
    """Generates PDF reports from COBOL knowledge base data."""

    def __init__(self):
        try:
            from fpdf import FPDF
            self._fpdf_available = True
        except ImportError:
            self._fpdf_available = False

    def _check_fpdf(self):
        if not self._fpdf_available:
            raise ImportError(
                "fpdf2 is required for PDF generation. Install with: pip install fpdf2"
            )

    # ────────────────────────────────────────────
    # Core PDF building helpers
    # ────────────────────────────────────────────

    def _create_pdf(self):
        """Create a new PDF with standard settings."""
        from fpdf import FPDF

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()

        # Title bar
        pdf.set_fill_color(15, 15, 35)
        pdf.rect(0, 0, 210, 30, "F")
        pdf.set_text_color(88, 166, 255)
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_y(8)
        pdf.cell(0, 14, "COBOL Knowledge Base", align="C")
        pdf.ln(20)

        # Reset text color
        pdf.set_text_color(30, 30, 30)
        return pdf

    def _add_section_header(self, pdf, title: str):
        """Add a styled section header."""
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_fill_color(30, 30, 63)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)
        pdf.ln(3)

    def _add_key_value(self, pdf, key: str, value: str):
        """Add a key-value row."""
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(50, 7, f"{key}:")
        pdf.set_font("Helvetica", "", 10)
        # Truncate very long values
        val = str(value or "-")
        if len(val) > 120:
            val = val[:117] + "..."
        pdf.cell(0, 7, val, new_x="LMARGIN", new_y="NEXT")

    def _add_paragraph_text(self, pdf, text: str):
        """Add a wrapped paragraph of text."""
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, str(text or ""))
        pdf.ln(2)

    def _add_table(self, pdf, headers: List[str], rows: List[List[str]],
                   col_widths: List[int] = None):
        """Add a simple table."""
        if not col_widths:
            available = 190
            col_widths = [available // len(headers)] * len(headers)

        # Header
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(33, 38, 45)
        pdf.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            pdf.cell(col_widths[i], 8, h, border=1, fill=True)
        pdf.ln()

        # Rows
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(30, 30, 30)
        for row in rows[:50]:  # Cap at 50 rows
            for i, cell in enumerate(row):
                val = str(cell or "")[:40]
                pdf.cell(col_widths[i], 7, val, border=1)
            pdf.ln()
        pdf.ln(3)

    # ────────────────────────────────────────────
    # Public: Generate Program Report
    # ────────────────────────────────────────────

    def generate_program_report(self, program_data: Dict,
                                calls_from: List[Dict] = None,
                                called_by: List[Dict] = None,
                                business_rules: List[Dict] = None,
                                paragraphs: List[Dict] = None) -> bytes:
        """
        Generate a PDF report for a single program.

        Returns:
            PDF file content as bytes.
        """
        self._check_fpdf()
        pdf = self._create_pdf()

        pid = program_data.get("program_id", "UNKNOWN")

        # Program header
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, f"Program Report: {pid}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)
        pdf.ln(5)

        # Overview section
        self._add_section_header(pdf, "Program Overview")
        self._add_key_value(pdf, "Program ID", pid)
        self._add_key_value(pdf, "Business Name", program_data.get("business_name"))
        self._add_key_value(pdf, "Type", program_data.get("program_type"))
        self._add_key_value(pdf, "Lines of Code", program_data.get("line_count"))
        self._add_key_value(pdf, "File Path", program_data.get("file_path"))
        self._add_key_value(pdf, "User Role", program_data.get("user_role"))
        self._add_key_value(pdf, "Business Process", program_data.get("business_process"))
        pdf.ln(3)

        # Business Purpose
        purpose = program_data.get("business_purpose")
        if purpose:
            self._add_section_header(pdf, "Business Purpose")
            self._add_paragraph_text(pdf, purpose)

        # Call relationships
        if calls_from:
            self._add_section_header(pdf, f"Programs Called by {pid}")
            rows = [[c.get("called_program", "?"),
                      c.get("business_name", "-"),
                      str(c.get("line_number", "-"))]
                     for c in calls_from]
            self._add_table(pdf, ["Called Program", "Business Name", "Line #"],
                            rows, [70, 80, 40])

        if called_by:
            self._add_section_header(pdf, f"Programs That Call {pid}")
            rows = [[c.get("caller_program", "?"),
                      c.get("business_name", "-"),
                      str(c.get("line_number", "-"))]
                     for c in called_by]
            self._add_table(pdf, ["Caller Program", "Business Name", "Line #"],
                            rows, [70, 80, 40])

        # Paragraphs
        if paragraphs:
            self._add_section_header(pdf, "Paragraphs & Control Flow")
            rows = [[p.get("paragraph_name", "?"),
                      p.get("business_name", "-"),
                      str(p.get("line_start", "?")),
                      str(p.get("line_end", "?")),
                      (p.get("purpose") or "-")[:60]]
                     for p in paragraphs]
            self._add_table(pdf, ["Paragraph", "Business Name", "Start", "End", "Purpose"],
                            rows, [45, 35, 20, 20, 70])

        # Business Rules
        if business_rules:
            self._add_section_header(pdf, "Business Rules")
            for rule in business_rules[:20]:
                pdf.set_font("Helvetica", "B", 10)
                rule_name = rule.get("rule_name", "Rule")
                category = rule.get("category", "")
                pdf.cell(0, 7, f"{rule_name} ({category})",
                         new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("Helvetica", "", 9)
                statement = rule.get("rule_statement", "")
                if statement:
                    pdf.multi_cell(0, 5, f"  Statement: {statement}")
                condition = rule.get("condition_text", "")
                if condition:
                    pdf.multi_cell(0, 5, f"  Condition: {condition}")
                action = rule.get("action_text", "")
                if action:
                    pdf.multi_cell(0, 5, f"  Action: {action}")
                pdf.ln(2)

        # Footer
        pdf.ln(10)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 5, "COBOL Knowledge Base — Auto-generated report",
                 align="C")

        return bytes(pdf.output())

    # ────────────────────────────────────────────
    # Public: Generate Chat Conversation PDF
    # ────────────────────────────────────────────

    def generate_chat_pdf(self, messages: List[Dict],
                          program_context: str = None) -> bytes:
        """
        Generate a PDF from a chat conversation.

        Args:
            messages: List of {"role": "user"/"assistant", "content": "..."}
            program_context: Optional program ID for context header

        Returns:
            PDF file content as bytes.
        """
        self._check_fpdf()
        pdf = self._create_pdf()

        # Title
        title = f"Chat Export"
        if program_context:
            title += f" - {program_context}"
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 6, f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(30, 30, 30)
        pdf.ln(5)

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "user":
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(31, 111, 235)
                pdf.cell(0, 7, "You:", new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(63, 185, 80)
                pdf.cell(0, 7, "Assistant:", new_x="LMARGIN", new_y="NEXT")

            pdf.set_text_color(30, 30, 30)
            pdf.set_font("Helvetica", "", 10)
            # Handle encoding
            safe_content = content.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 6, safe_content)
            pdf.ln(4)

        return bytes(pdf.output())
