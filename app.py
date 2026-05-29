import re
import base64
from urllib.parse import urlparse, quote
from flask import Flask, request, Response, redirect
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

SESSION = requests.Session()
SESSION.verify = False

# =================== HEADERS ===================
HEADERS_TV = {
    "user-agent": "Mozilla/5.0 (WebOS; SmartTV)",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "tr-TR,tr;q=0.6",
    "referer": "https://inattv1309.xyz/",          # ← EKLENDİ
    "origin": "https://inattv1309.xyz"             # ← Opsiyonel ama faydalı
}

HEADERS_PROXY = {
    "User-Agent": "Mozilla/5.0 (compatible; Proxy/1.0)",
    "referer": "https://inattv1309.xyz/",           # ← Buraya da eklendi
}
# ===============================================

def get_self_url():
    scheme = request.scheme
    host = request.host
    path = request.path
    return f"{scheme}://{host}{path}"

@app.route("/health", methods=["GET"])
def health():
    return Response("OK", status=200, content_type="text/plain")

@app.route("/", methods=["GET"])
def index():
    cdn = request.args.get("CDN")
    live_id = request.args.get("ID")

    if cdn:
        resp = SESSION.get(cdn, headers=HEADERS_TV, allow_redirects=True, timeout=15)  # HEADERS_TV kullanıyoruz
        content_type = resp.headers.get("Content-Type", "")

        is_m3u8 = (
            "application/vnd.apple.mpegurl" in content_type
            or "application/x-mpegURL" in content_type
            or re.search(r"\.m3u8", cdn)
        )

        if is_m3u8:
            self_url = get_self_url()
            base_url = cdn[: cdn.rfind("/") + 1]
            lines = resp.text.split("\n")
            rewritten = []

            for line in lines:
                line = line.strip()
                if line == "" or line.startswith("#"):
                    rewritten.append(line)
                    continue

                # ... (kalan kod aynı kalabilir)
