import json
from datetime import datetime
from .models import *


def load_har(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _headers_to_dict(headers):
    return {h["name"]: h["value"] for h in headers}


def _parse_status(status):
    raw = str(status) if status is not None else None
    try:
        code = int(status)
    except Exception:
        code = None
    return code, raw


def parse_entry(entry):
    req = entry["request"]
    res = entry["response"]

    request = HttpRequest(
        name=req["url"].split("/")[-1] or "request",
        method=req["method"],
        url=req["url"],
        headers=_headers_to_dict(req.get("headers", [])),
        body=req.get("postData", {}).get("text"),
    )

    status_code, status_raw = _parse_status(res.get("status"))

    response = HttpResponse(
        status_code=status_code,
        status_raw=status_raw,
        status_text=res.get("statusText"),
        headers=_headers_to_dict(res.get("headers", [])),
        body=res.get("content", {}).get("text"),
        mime_type=res.get("content", {}).get("mimeType"),
    )

    start = datetime.fromisoformat(entry["startedDateTime"].replace("Z", "+00:00")).timestamp()

    return HttpExchange(request, response, start, entry.get("time", 0))


def parse_har(path: str) -> HarModel:
    har = load_har(path)
    entries = har["log"]["entries"]

    exchanges = [parse_entry(e) for e in entries]

    return HarModel(transactions=[Transaction("HAR Flow", exchanges)])
