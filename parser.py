import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="WebDrop is an app that clones the whole website structure as it is in the servers."
    )
    parser.add_argument(
        "-url",
        required=True,
        help="The URL to fetch (e.g., https://example.com)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to save the cloned website. If omitted, saves it in a default location with the same name as the URL.",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=15.0,
        help="Timeout in seconds (default: 15).",
    )
    parser.add_argument(
        "-H",
        "--headers",
        action="append",
        default={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            ),
            "Referer": "https://google.com",
            "Cache-Control": "no-cache",
        },
        help="Specifies custom headers (e.g., User-Agent, Content-Type). If omitted, uses default headers.",
    )
    parser.add_argument(
        "--use-proxy",
        action="store_true",
        help="Optional if you want to use proxies (default: False).",
    )
    parser.add_argument(
        "--analyse",
        action="store_true",
        help="Optional if you want to use proxies (default: False).",
    )
    parser.add_argument(
        "--nslook",
        action="store_true",
        help="Optional if you want to use proxies (default: False).",
    )
    return parser