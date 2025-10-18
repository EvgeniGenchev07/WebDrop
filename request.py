from http.client import HTTPResponse
from typing import Optional, Dict
from urllib import request, error
from urllib.parse import urlparse, urlsplit, quote, urlunsplit
from helper import _detect_charset
from proxy import request_through_proxy


def read_response(data:bytes,content_type:str) -> str | bytes:
    if content_type.startswith(('text/', 'application/javascript', 'application/json')):
        charset = _detect_charset(content_type) or 'utf-8'
        try:
            return data.decode(charset, errors='replace')
        except LookupError:
            return data.decode('utf-8', errors='replace')
    return data

def get_file(url: str, timeout: float = 15.0, headers: Optional[Dict[str, str]] = None,use_proxy = False) -> str:
    parts = urlsplit(url)
    encoded_path = quote(parts.path,safe='/:@?&=+$,#-%_.~')
    encoded_url = urlunsplit((parts.scheme, parts.netloc, encoded_path, parts.query, parts.fragment))
    req = request.Request(encoded_url, headers=headers, method="GET")
    print("encoded", encoded_url)
    if not use_proxy:
        try:
            with request.urlopen(req, timeout=timeout) as resp:
                data = read_response(resp.read(), resp.headers.get('Content-Type',''))
                return data
        except error.HTTPError as e:
            return ''
        except BaseException as e:
            print('Unable to fetch:', e)
    else:
        resp =  request_through_proxy(req,timeout)
        return read_response(resp['data'], resp['Content-Type'])
    print('returning nothing')
    return ''