"""Small OpenTelemetry helpers for the demo app."""

from __future__ import annotations

import logging
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


_SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "cobol-migration-hub")
_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4319")
_LOG_PATH = Path(os.getenv("APP_LOG_PATH", r"C:\observability\app-logs\demo-app.log"))
_INITIALIZED = False


def _configure_logging() -> logging.Logger:
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("demo_app.observability")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(_LOG_PATH, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
    return logger


def setup_observability() -> tuple[trace.Tracer, metrics.Meter, logging.Logger]:
    global _INITIALIZED

    resource = Resource.create({"service.name": _SERVICE_NAME})
    if not _INITIALIZED:
        tracer_provider = TracerProvider(resource=resource)
        tracer_provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=_OTLP_ENDPOINT, insecure=True))
        )
        trace.set_tracer_provider(tracer_provider)

        metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(endpoint=_OTLP_ENDPOINT, insecure=True),
            export_interval_millis=5000,
        )
        metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[metric_reader]))
        _INITIALIZED = True

    return trace.get_tracer("doc_demo"), metrics.get_meter("doc_demo"), _configure_logging()


tracer, meter, logger = setup_observability()
doc_generation_counter = meter.create_counter(
    "doc_generation_runs",
    description="Number of document generation attempts.",
)
doc_generation_duration = meter.create_histogram(
    "doc_generation_duration_seconds",
    unit="s",
    description="Duration of document generation attempts.",
)
java_generation_counter = meter.create_counter(
    "java_generation_runs",
    description="Number of Java generation attempts.",
)
java_generation_duration = meter.create_histogram(
    "java_generation_duration_seconds",
    unit="s",
    description="Duration of Java generation attempts.",
)
java_generation_source_lines = meter.create_histogram(
    "java_generation_source_lines",
    description="COBOL source lines used for Java generation.",
)
java_generation_evidence_facts = meter.create_histogram(
    "java_generation_evidence_facts",
    description="Structured facts used as Java generation evidence.",
)
java_generation_output_lines = meter.create_histogram(
    "java_generation_output_lines",
    description="Non-empty Java lines generated.",
)
java_generation_methods = meter.create_histogram(
    "java_generation_methods",
    description="Java methods generated.",
)
java_generation_types = meter.create_histogram(
    "java_generation_types",
    description="Java top-level or nested types generated.",
)
java_generation_llm_duration = meter.create_histogram(
    "java_generation_llm_duration_seconds",
    unit="s",
    description="Duration of Gemini calls during Java generation.",
)
java_generation_prompt_tokens = meter.create_histogram(
    "java_generation_prompt_tokens",
    description="Prompt tokens sent to Gemini during Java generation.",
)
java_generation_output_tokens = meter.create_histogram(
    "java_generation_output_tokens",
    description="Output tokens returned by Gemini during Java generation.",
)
java_generation_total_tokens = meter.create_histogram(
    "java_generation_total_tokens",
    description="Total tokens used by Gemini during Java generation.",
)


@contextmanager
def observe_doc_generation(mode: str, subject: str) -> Iterator[None]:
    start = time.perf_counter()
    attributes = {"doc.mode": mode, "doc.subject": subject}
    doc_generation_counter.add(1, attributes)

    with tracer.start_as_current_span("doc_generation", attributes=attributes) as span:
        try:
            logger.info("doc_generation_started mode=%s subject=%s", mode, subject)
            yield
        except Exception as exc:
            span.record_exception(exc)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
            logger.exception("doc_generation_failed mode=%s subject=%s", mode, subject)
            raise
        else:
            logger.info("doc_generation_completed mode=%s subject=%s", mode, subject)
        finally:
            doc_generation_duration.record(time.perf_counter() - start, attributes)


@contextmanager
def observe_java_generation(program_id: str, use_llm: bool) -> Iterator[dict]:
    start = time.perf_counter()
    attributes = {"program.id": program_id, "llm.used": str(use_llm).lower()}
    measurements: dict[str, int] = {}
    java_generation_counter.add(1, attributes)

    with tracer.start_as_current_span("java_generation", attributes=attributes) as span:
        try:
            logger.info("java_generation_started program_id=%s use_llm=%s", program_id, use_llm)
            yield measurements
        except Exception as exc:
            span.record_exception(exc)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
            logger.exception("java_generation_failed program_id=%s use_llm=%s", program_id, use_llm)
            raise
        else:
            logger.info("java_generation_completed program_id=%s use_llm=%s", program_id, use_llm)
        finally:
            java_generation_duration.record(time.perf_counter() - start, attributes)
            if measurements:
                java_generation_source_lines.record(measurements.get("source_lines", 0), attributes)
                java_generation_evidence_facts.record(measurements.get("evidence_facts", 0), attributes)
                java_generation_output_lines.record(measurements.get("output_lines", 0), attributes)
                java_generation_methods.record(measurements.get("methods", 0), attributes)
                java_generation_types.record(measurements.get("types", 0), attributes)
                if measurements.get("llm_duration_seconds") is not None:
                    java_generation_llm_duration.record(measurements["llm_duration_seconds"], attributes)
                if measurements.get("prompt_tokens") is not None:
                    java_generation_prompt_tokens.record(measurements["prompt_tokens"], attributes)
                if measurements.get("output_tokens") is not None:
                    java_generation_output_tokens.record(measurements["output_tokens"], attributes)
                if measurements.get("total_tokens") is not None:
                    java_generation_total_tokens.record(measurements["total_tokens"], attributes)
