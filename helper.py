import threading
import time
from typing import Optional, Dict
import re
import sys

def get_page_detection_pattern(domain:str) -> str:
    return rf'(?ix)<a\s+[^>]*href=[\"\']((?:(?:https?:\/\/(?:www\.)?{re.escape(domain)}(?:\/[%\w\-/]+)*\/?(?:[%\w\-]+(?:\.html?)?|[%\w\-/]+\/)?)|(?:(?:\.(?:\/|\.\.\/)+|(?:\.\.\/)+)[%\w\-/]+(?:\.html?|\/)?)|(?:\/[%\w\-/]+(?:\.html?|\/)?)|(?:[%\w\-/]+(?:\.html?|\/)?))|(?:(?:https?:\/\/(?:www\.)?{re.escape(domain)}(?:\/[%\w\-/]+)*\/?(?:[%\w\-]+(?:\.html?)?|[%\w\-/]+\/)?)|(?:(?:\.(?:\/|\.\.\/)+|(?:\.\.\/)+)[%\w\-/]+(?:\.html?|\/)?)|(?:\/[%\w\-/]+(?:\.html?|\/)?)|(?:[%\w\-/]+(?:\.html?|\/)?))[?].*)[\"\']'

def get_resource_detection_pattern(domain:str) -> str:
    return rf'(?:href|src)=[\'\"]((?:https?://(?:www\.)?{re.escape(domain)}[^\s\'\"]+\.[^/\s\'\".\\]+|(?:\.\./|\./)+[^\s\'\"]+\.(?!html\b)[^/\s\'\".\\]+))[\'\"]'

def get_analyser_pattern() -> str:
    return re.compile(r"(?ix)(?P<email>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})|(?P<phone>(?:\+?\d{1,3}[\s.\-]?)?(?:\(\d{4}\)|\d{1,4})[\s.\-]?\d{4}[\s.\-]?\d{4}(?:[\s.\-]?\d{1,9})?(?:\s*(?:ext\.?|x)?\s*\d{1,5})?)|(?P<address>\b\d{1,4}\s+[A-Za-z0-9.\- ]{3,60}\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Square|Sq|ул\.|бул\.|ж\.к\.)\b[^\n]{0,80})|(?P<link>\b(?:https?:\/\/|www\.)[A-Za-z0-9\-._~:/?#\[\]@|!$&*,+;=%]+)",re.MULTILINE | re.IGNORECASE).pattern

def _detect_charset(content_type: Optional[str]) -> Optional[str]:
    """Extract charset from a Content-Type header if present."""
    if not content_type:
        return None
    parts = [p.strip() for p in content_type.split(';')]
    for p in parts[1:]:  # skip the mime type
        if p.lower().startswith('charset='):
            return p.split('=', 1)[1].strip().strip('"').strip("'")
    return None

def clear_feed(lines:int,timeout:float) -> None:
    def _clear_feed() -> None:
        time.sleep(timeout)
        for _ in range(lines):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
    threading.Thread(target=_clear_feed, daemon=True).start()

