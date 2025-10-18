from http.client import HTTPResponse
from urllib import request, error
from urllib import request
from urllib.request import Request

from helper import _detect_charset

PROXY_SOURCE = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=5000&ssl=all"



def get_proxies() -> list:
    req = request.Request(PROXY_SOURCE, method="GET")
    data =''
    try:
        with request.urlopen(req, timeout=12) as resp:
            data = resp.read()
            content_type = resp.headers.get('Content-Type', '')
            if content_type.startswith(('text/', 'application/javascript', 'application/json')):
                charset = _detect_charset(resp.headers.get('Content-Type')) or 'utf-8'
            data = data.decode(charset, errors='replace')
        raw = data.strip().splitlines()
        return [p.strip() for p in raw if p and ":" in p]
    except BaseException as e:
        print('Unable to fetch proxies:',e )
        return []

curr_proxy_index = 0
proxies = get_proxies()

def request_through_proxy(req:Request,timeout:float) -> dict:
    global curr_proxy_index
    while True:
        for proxy_index in range(curr_proxy_index, len(proxies)):
            proxy = proxies[proxy_index]
            print('Connecting to:', proxy)
            proxy_url = f"http://{proxy}"
            handlers = {
                "http": proxy_url,
                "https": proxy_url,
            }
            proxy_handler = request.ProxyHandler(handlers)
            opener = request.build_opener(proxy_handler)
            try:
                with opener.open(req, timeout=timeout) as resp:
                    curr_proxy_index = proxy_index
                    return {
                        'data':resp.read(),
                        'Content-Type': resp.headers.get('Content-Type', '')
                    }
            except error.HTTPError as e:
                print('Unable tos fetch:', e)
            except Exception as e:
                print('Unable to connect to proxy:', type(e).__name__, e)
                # clear_feed(lines=2,timeout=0.5)
        print('No more proxies')
        curr_proxy_index = 0