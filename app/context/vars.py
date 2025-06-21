from contextvars import ContextVar
from typing import Any

headers_context: Any = ContextVar("headers_context", default=None)
