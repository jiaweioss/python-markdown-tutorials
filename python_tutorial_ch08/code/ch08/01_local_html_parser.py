"""Parse a local HTML fragment safely."""
from html.parser import HTMLParser

HTML = """
<html><body>
<h1>Python 公开资料</h1>
<a href="https://www.python.org/">Python 官网</a>
<a href="https://docs.python.org/3/">Python 文档</a>
</body></html>
"""


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)
            self.links.append(attrs.get("href", ""))


parser = LinkParser()
parser.feed(HTML)
print(parser.links)
