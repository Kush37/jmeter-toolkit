from dataclasses import dataclass, field
from typing import Optional, Dict, List, Set


@dataclass
class HttpRequest:
    name: str
    method: str
    url: str
    headers: Dict[str, str]
    body: Optional[str] = None


@dataclass
class HttpResponse:
    status_code: Optional[int]
    status_raw: Optional[str]
    status_text: Optional[str]
    headers: Dict[str, str]
    body: Optional[str]
    mime_type: Optional[str]
    size_bytes: Optional[int] = None


@dataclass
class HttpExchange:
    request: HttpRequest
    response: HttpResponse
    start_time: float
    duration_ms: float
    tags: Set[str] = field(default_factory=set)


@dataclass
class Transaction:
    name: str
    exchanges: List[HttpExchange]
    think_time_ms: Optional[float] = None


@dataclass
class HarModel:
    transactions: List[Transaction]
    metadata: Optional[dict] = None
