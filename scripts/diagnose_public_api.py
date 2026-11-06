#!/usr/bin/env python3
"""Non-secret network diagnostics for the public ShopPlus staging URL.
Shows which public paths a browser is loading. No cookies, tokens or POSTs.
"""
import re
from urllib.request import Request, urlopen
from urllib.parse import urljoin

BASE = "https://shopplus-haiti-pilote-ub21b4.v2.appdeploy.ai/"

def get(url: str):
    req = Request(url, headers={"User-Agent": "ShopPlus-QA-Probe/1.0"})
    with urlopen(req, timeout=15) as res:
        return res.status, res.headers.get("Content-Type", ""), res.read(3_000_000).decode("utf-8", "replace")

status, mime, html = get(BASE)
print("Landing:", status, mime, "size", len(html))
print("Script URLs:", re.findall(r'<script[^>]+src=["\']([^"\']+)', html)[:8])
print("Meta data:", re.findall(r'<meta[^>]+(?:name|content)=["\'][^"\']+', html)[:8])
for src in re.findall(r'<script[^>]+src=["\']([^"\']+)', html):
    if "overlay" in src: continue
    url = urljoin(BASE, src)
    try: code, typ, bundle = get(url)
    except Exception as e:
        print("Could not inspect public JS asset:", type(e).__name__); continue
    print("JS asset", url.split("?")[0][:160], "status", code, "mime", typ, "size", len(bundle))
    for pat in ("__appdeploy", "apiBaseUrl", "appdeploy.ai/api", "api-v2.appdeploy.ai", "backend", "/_api/", "fetchBase", "baseURL", "serviceEndpoint"):
        match = re.search(re.escape(pat), bundle, flags=re.I)
        if match:
            snippet = bundle[max(0,match.start()-125):match.end()+145].replace("\n", " ")
            print("  ", pat, "=", snippet[:300])
    break
