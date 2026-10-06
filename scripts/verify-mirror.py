"""Check the built GitHub Pages site without requesting external services."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import sys


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.assets = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag in ("img", "script") and attrs.get("src"):
            self.assets.append(attrs["src"])
        if tag == "link" and attrs.get("rel") in ("stylesheet", "modulepreload", "icon"):
            self.assets.append(attrs["href"])


root = Path(__file__).resolve().parents[1]
dist = root / "dist"
errors = []
html_files = list(dist.rglob("*.html"))
for source in html_files:
    page = Page()
    page.feed(source.read_text())
    for kind, urls in (("asset", page.assets), ("link", page.links)):
        for url in urls:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = unquote(parsed.path)
            if path.startswith("/"):
                if not path.startswith("/guide/"):
                    errors.append([str(source.relative_to(dist)), "outside base", url])
                    continue
                target = dist / path[len("/guide/"):]
            else:
                target = source.parent / path
            if path.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                errors.append([str(source.relative_to(dist)), "missing " + kind, url])

article = dist / "ai/system-design/ai-application-architecture.html"
if article.exists():
    page = Page()
    page.feed(article.read_text())
    if "一个最小请求链路" not in page.ids:
        errors.append([str(article), "requested anchor missing"])
else:
    errors.append([str(article), "requested article missing"])
if len(html_files) < 400:
    errors.append(["dist", "unexpectedly incomplete build", len(html_files)])
for name in ("LICENSE.txt", "NOTICE.txt", "index.html", "home.html", "sitemap.xml"):
    if not (dist / name).exists():
        errors.append([name, "required output missing"])
search_indexes = list((root / "docs/.vuepress/.temp").glob("internal/searchIndex.js"))
if not search_indexes or "ai-application-architecture.html" not in search_indexes[0].read_text():
    errors.append(["search", "requested article absent from local search index"])
print(json.dumps({"html_pages": len(html_files), "errors": errors}, ensure_ascii=False, indent=2))
sys.exit(bool(errors))
