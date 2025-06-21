from datetime import datetime
from typing import TypedDict


class HeaderPayloadTH(TypedDict):
    userId: str
    email: str
    name: str
    exp: datetime
