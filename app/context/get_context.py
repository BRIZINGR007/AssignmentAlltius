from typing import cast
from app.interfaces.Context import Headers_PM
from app.context.vars import headers_context


class ContextUtils:
    @staticmethod
    def get_headers_details() -> Headers_PM:
        return cast(Headers_PM, headers_context.get())
