"""Fetch Python.org robots.txt gently with urllib."""
from urllib.request import Request, urlopen

url = "https://www.python.org/robots.txt"
request = Request(
    url,
    headers={
        "User-Agent": "Python tutorial learning script",
        "Accept-Encoding": "identity",
    },
)
with urlopen(request, timeout=10) as response:
    html = response.read(800).decode("utf-8", errors="replace")
    print("状态码：", response.status)
    print("内容类型：", response.headers.get("Content-Type", "unknown"))
    print(html[:500])
