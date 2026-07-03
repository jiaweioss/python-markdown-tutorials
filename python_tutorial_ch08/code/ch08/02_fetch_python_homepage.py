"""Fetch Python.org robots.txt gently with urllib."""
import ssl
import certifi
from urllib.request import Request, urlopen

url = "https://www.python.org/robots.txt"
request = Request(
    url,
    headers={
        "User-Agent": "Python tutorial learning script",
        "Accept-Encoding": "identity",
    },
)
context = ssl.create_default_context(cafile=certifi.where())
with urlopen(request, timeout=10, context=context) as response:
    html = response.read(800).decode("utf-8", errors="replace")
    print("状态码：", response.status)
    print("内容类型：", response.headers.get("Content-Type", "unknown"))
    print(html[:500])
