# DjangoLiveStreaming/dtos.py
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ResponseDTO:
    code: int
    message: str
    data: Optional[Any] = None
