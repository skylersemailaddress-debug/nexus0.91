from __future__ import annotations

import contextvars
import uuid

_request_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("request_id", default=None)
_trace_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("trace_id", default=None)


def _new_id() -> str:
    return uuid.uuid4().hex


def ensure_trace_context() -> tuple[str, str]:
    request_id = _request_id.get()
    trace_id = _trace_id.get()
    if request_id is None:
        request_id = _new_id()
        _request_id.set(request_id)
    if trace_id is None:
        trace_id = _new_id()
        _trace_id.set(trace_id)
    return request_id, trace_id


def set_trace_context(*, request_id: str | None = None, trace_id: str | None = None) -> tuple[str, str]:
    current_request_id, current_trace_id = ensure_trace_context()
    if request_id:
        current_request_id = request_id
        _request_id.set(request_id)
    if trace_id:
        current_trace_id = trace_id
        _trace_id.set(trace_id)
    return current_request_id, current_trace_id


def get_trace_context() -> dict[str, str]:
    request_id, trace_id = ensure_trace_context()
    return {"request_id": request_id, "trace_id": trace_id}
