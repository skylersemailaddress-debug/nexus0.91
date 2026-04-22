from __future__ import annotations

import uvicorn

from .api_server import app


def run_desktop_backend() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8787, log_level="info")
