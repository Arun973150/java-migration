"""
Context assembly helpers for large COBOL documentation prompts.

This module sits between SQLite-backed fact retrieval and the LLM writer:
it turns a raw context string into token-budgeted semantic chunks and
produces a lightweight coverage ledger that can be persisted with the
generated document.
"""

from __future__ import annotations

import math
import os
import re
from dataclasses import dataclass
from typing import Dict, List


TOKEN_CHARS_APPROX = 4.0


def estimate_tokens(text: str) -> int:
    """Cheap token estimate without adding a tokenizer dependency."""
    if not text:
        return 0
    return max(1, math.ceil(len(text) / TOKEN_CHARS_APPROX))


@dataclass
class ContextChunk:
    chunk_id: str
    heading: str
    text: str
    fact_ids: List[str]
    order: int

    @property
    def tokens(self) -> int:
        return estimate_tokens(self.text)


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    try:
        return int(raw) if raw else default
    except Exception:
        return default


def _section_heading_prefix(mode: str) -> str:
    return "## Program:" if mode in ("Program", "Module") else "## "


def _split_into_sections(raw_context: str, mode: str) -> List[Dict[str, str]]:
    lines = raw_context.splitlines()
    marker = _section_heading_prefix(mode)

    sections: List[Dict[str, str]] = []
    current_lines: List[str] = []
    current_heading = "INTRO"
    current_id = "intro"
    seen_heading = False

    for line in lines:
        if line.startswith(marker):
            if current_lines:
                sections.append(
                    {
                        "id": current_id,
                        "heading": current_heading,
                        "text": "\n".join(current_lines).strip(),
                    }
                )
            seen_heading = True
            current_heading = line.strip()
            current_id = re.sub(r"[^a-z0-9]+", "_", current_heading.lower()).strip("_") or "section"
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append(
            {
                "id": current_id if seen_heading else "intro",
                "heading": current_heading,
                "text": "\n".join(current_lines).strip(),
            }
        )

    return [s for s in sections if s["text"].strip()]


def _split_body_into_groups(body_lines: List[str]) -> List[List[str]]:
    groups: List[List[str]] = []
    current: List[str] = []
    starters = ("- ", "### ", "#### ", "* ")

    for line in body_lines:
        stripped = line.lstrip()
        is_starter = stripped.startswith(starters)
        if is_starter and current:
            groups.append(current)
            current = [line]
        else:
            current.append(line)

    if current:
        groups.append(current)
    return groups


def _chunk_section(section_id: str, heading: str, text: str, fact_ids: List[str], mode: str,
                   section_token_budget: int) -> List[ContextChunk]:
    if estimate_tokens(text) <= section_token_budget:
        return [ContextChunk(f"{section_id}__0", heading, text, fact_ids, 0)]

    lines = text.splitlines()
    if not lines:
        return [ContextChunk(f"{section_id}__0", heading, text, fact_ids, 0)]

    heading_lines = [lines[0]]
    body_lines = lines[1:]
    groups = _split_body_into_groups(body_lines)

    chunks: List[ContextChunk] = []
    chunk_index = 0
    current_groups: List[List[str]] = []

    def flush() -> None:
        nonlocal chunk_index, current_groups
        if not current_groups:
            return
        chunk_lines = heading_lines[:]
        if len(groups) > 1:
            chunk_lines.append(f"- Context Chunk: {chunk_index + 1}/{max(1, len(groups))}")
        for group in current_groups:
            chunk_lines.extend(group)
        chunk_text = "\n".join(chunk_lines).strip()
        chunk_fact_ids = _extract_fact_ids(chunk_text, mode, fallback_subject=heading)
        chunks.append(
            ContextChunk(
                chunk_id=f"{section_id}__{chunk_index}",
                heading=heading,
                text=chunk_text,
                fact_ids=chunk_fact_ids or fact_ids,
                order=chunk_index,
            )
        )
        chunk_index += 1
        current_groups = []

    current_tokens = estimate_tokens("\n".join(heading_lines))
    for group in groups:
        group_text = "\n".join(group)
        group_tokens = estimate_tokens(group_text)
        if current_groups and current_tokens + group_tokens > section_token_budget:
            flush()
            current_tokens = estimate_tokens("\n".join(heading_lines))
        if group_tokens > section_token_budget:
            # Last-resort line chunking for very dense groups.
            temp_lines: List[str] = []
            temp_tokens = current_tokens
            for line in group:
                line_tokens = estimate_tokens(line)
                if temp_lines and temp_tokens + line_tokens > section_token_budget:
                    current_groups.append(temp_lines)
                    flush()
                    temp_lines = [line]
                    temp_tokens = estimate_tokens("\n".join(heading_lines)) + line_tokens
                else:
                    temp_lines.append(line)
                    temp_tokens += line_tokens
            if temp_lines:
                current_groups.append(temp_lines)
                current_tokens = temp_tokens
            continue

        current_groups.append(group)
        current_tokens += group_tokens

    flush()
    return chunks or [ContextChunk(f"{section_id}__0", heading, text, fact_ids, 0)]


def _extract_fact_ids(text: str, mode: str, fallback_subject: str = "") -> List[str]:
    facts = set()
    upper = text.upper()

    for pid in re.findall(r"## PROGRAM:\s+([A-Z0-9-]+)", upper):
        facts.add(f"program:{pid}")

    for line in text.splitlines():
        stripped = line.strip()
        upper_line = stripped.upper()

        if upper_line.startswith("- CALLS:"):
            for token in stripped.split(":", 1)[1].split(","):
                name = token.strip().strip("`.")
                if name and name not in ("UNKNOWN", "NONE"):
                    facts.add(f"call:{name.upper()}")

        if "SHARED DATA (COPYBOOKS)" in upper_line or "SOURCE COPY STATEMENTS" in upper_line:
            rhs = stripped.split(":", 1)[1] if ":" in stripped else ""
            for token in rhs.split(","):
                name = token.strip().strip("`.")
                if name and "NONE" not in name.upper():
                    facts.add(f"copybook:{name.upper()}")

        if upper_line.startswith("- FILES ACCESSED:"):
            rhs = stripped.split(":", 1)[1] if ":" in stripped else ""
            for token in rhs.split(","):
                name = token.strip().strip("`.")
                if name:
                    facts.add(f"file:{name.upper()}")

        for job in re.findall(r"\bJOB\s+([A-Z0-9#$@_-]+)\s*,\s*STEP\b", upper_line):
            facts.add(f"jcl:{job}")
        if upper_line.startswith("- "):
            job_line = re.match(r"-\s+([A-Z0-9#$@_-]+)\s+\(\d+\s+STEPS?\)", upper_line)
            if job_line:
                facts.add(f"jcl:{job_line.group(1)}")

        for func in re.findall(r"CALL\s+'CBLTDLI'\s+([A-Z0-9-]+)", upper_line):
            facts.add(f"ims:{func}")

        for para in re.findall(r"`([A-Z0-9][A-Z0-9-]{2,})`", upper_line):
            if "-" in para:
                facts.add(f"paragraph:{para}")

        for prog in re.findall(r"\b(?:XCTL|LINK)\b[^A-Z0-9]+(?:PROGRAM\s*\(?\s*)?([A-Z0-9-]{3,})", upper_line):
            facts.add(f"cics_target:{prog}")

        if "CODE ANOMALIES / KNOWN ISSUES" in upper_line:
            for rule in re.findall(r"\[[A-Z]+\]\s+([A-Z0-9_]+)\s", upper_line):
                facts.add(f"anomaly:{rule}")

    if mode == "Application" and fallback_subject:
        facts.add(f"application:{fallback_subject.upper()}")

    return sorted(facts)


def build_context_package(raw_context: str, mode: str, subject: str) -> Dict[str, object]:
    """
    Turn a raw context string into a token-budgeted prompt plus metadata.

    The current repository usually stays below budget already, but this makes the
    overflow path deterministic and observable when future contexts get larger.
    """
    budget_tokens = _env_int("DOC_CONTEXT_MAX_TOKENS", 12000)
    section_budget = _env_int("DOC_SECTION_MAX_TOKENS", max(1200, budget_tokens // 3))

    sections = _split_into_sections(raw_context, mode)
    chunks: List[ContextChunk] = []
    for idx, section in enumerate(sections):
        fact_ids = _extract_fact_ids(section["text"], mode, fallback_subject=subject)
        for chunk in _chunk_section(section["id"], section["heading"], section["text"], fact_ids, mode, section_budget):
            chunks.append(
                ContextChunk(
                    chunk_id=chunk.chunk_id,
                    heading=chunk.heading,
                    text=chunk.text,
                    fact_ids=chunk.fact_ids,
                    order=len(chunks),
                )
            )

    used_chunks: List[ContextChunk] = []
    omitted_chunks: List[str] = []
    consumed_tokens = 0
    for chunk in chunks:
        chunk_tokens = chunk.tokens
        if used_chunks and consumed_tokens + chunk_tokens > budget_tokens:
            omitted_chunks.append(chunk.chunk_id)
            continue
        used_chunks.append(chunk)
        consumed_tokens += chunk_tokens

    final_context = "\n\n".join(chunk.text for chunk in used_chunks).strip()
    expected_fact_ids = _extract_fact_ids(raw_context, mode, fallback_subject=subject)
    prompt_fact_ids = sorted({fact for chunk in used_chunks for fact in chunk.fact_ids})

    coverage_ledger = {
        "mode": mode,
        "subject": subject,
        "expected_fact_ids": expected_fact_ids,
        "prompt_fact_ids": prompt_fact_ids,
        "document_fact_ids": [],
        "expected_count": len(expected_fact_ids),
        "prompt_count": len(prompt_fact_ids),
        "document_count": 0,
        "prompt_missing_fact_ids": sorted(set(expected_fact_ids) - set(prompt_fact_ids)),
        "document_missing_fact_ids": expected_fact_ids[:],
        "prompt_coverage_pct": round((len(prompt_fact_ids) / len(expected_fact_ids) * 100.0), 2)
        if expected_fact_ids else 100.0,
        "document_coverage_pct": 0.0,
    }

    metadata = {
        "raw_chars": len(raw_context),
        "raw_tokens_est": estimate_tokens(raw_context),
        "final_chars": len(final_context),
        "final_tokens_est": estimate_tokens(final_context),
        "budget_tokens": budget_tokens,
        "section_budget_tokens": section_budget,
        "section_count": len(sections),
        "chunk_count": len(chunks),
        "used_chunk_count": len(used_chunks),
        "omitted_chunk_ids": omitted_chunks,
        "chunking_applied": len(chunks) > len(sections),
        "budget_hit": bool(omitted_chunks),
    }

    return {
        "context": final_context,
        "metadata": metadata,
        "coverage_ledger": coverage_ledger,
    }


def apply_document_coverage(coverage_ledger: Dict[str, object], document_text: str) -> Dict[str, object]:
    """Update prompt coverage metadata with what the final document actually mentioned."""
    ledger = dict(coverage_ledger or {})
    expected = set(ledger.get("expected_fact_ids") or [])
    document_facts = set(_extract_fact_ids(document_text or "", str(ledger.get("mode") or ""), str(ledger.get("subject") or "")))
    ledger["document_fact_ids"] = sorted(document_facts)
    ledger["document_count"] = len(document_facts)
    ledger["document_missing_fact_ids"] = sorted(expected - document_facts)
    ledger["document_coverage_pct"] = round((len(document_facts) / len(expected) * 100.0), 2) if expected else 100.0
    return ledger
