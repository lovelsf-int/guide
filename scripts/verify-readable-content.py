"""Regression checks for the mirror's readable, independently completed lessons."""
from html.parser import HTMLParser
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
LESSONS = [
    "database/redis/redis-cluster",
    "database/elasticsearch/elasticsearch-questions-01",
    "java/collection/priorityqueue-source-code",
    "system-design/framework/netty",
    "system-design/framework/spring/springboot-knowledge-and-questions-summary",
    "system-design/framework/spring/springboot-source-code",
    "system-design/system-design-questions",
    "interview-preparation/self-test-of-common-interview-questions",
    "interview-preparation/interview-experience",
    "system-design/design-pattern",
    "zhuanlan/java-mian-shi-zhi-bei",
    "zhuanlan/back-end-interview-high-frequency-system-design-and-scenario-questions",
    "zhuanlan/source-code-reading",
    "zhuanlan/handwritten-rpc-framework",
    "zhuanlan/interview-guide",
    "ai/agent-source/deepseek-harness",
    "ai/agent-source/jev-sdk",
]


class Article(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.text = []
        self.headings = 0
        self.in_title = False
        self.title = ""
        self.canonical = ""

    def handle_starttag(self, tag, attrs):
        if tag == "link" and dict(attrs).get("rel") == "canonical":
            self.canonical = dict(attrs).get("href", "")
        if tag == "title":
            self.in_title = True
        if dict(attrs).get("id") == "markdown-content":
            self.depth = 1
        elif self.depth and tag not in {"img", "input", "br", "hr", "meta", "link", "source", "wbr"}:
            self.depth += 1
        if self.depth and tag in {"h2", "h3"}:
            self.headings += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.depth:
            self.text.append(data)


errors = []
promotion_markers = (
    "知识星球", "原站公开介绍", "上游公开介绍", "星球专属",
    "限时优惠", "公众号后台回复", "欢迎 Star", "免费完整讲解", "付费专栏",
    "gongzhonghaoxuanchuan", "gongzhonghao-javaguide",
    "xingqiuyouhuijuan", "xingqiufuwu", "interview-guide-banner.png",
)
for page_path in DIST.rglob("*.html"):
    html = page_path.read_text()
    found = [marker for marker in promotion_markers if marker in html]
    if found:
        errors.append([str(page_path.relative_to(DIST)), "promotional content", found])

for asset in list((DIST / "assets").glob("*.js")) + list((DIST / "assets").glob("*.css")):
    content = asset.read_text()
    if "unlock-global-style" in content or "data-unlock-target" in content:
        errors.append([str(asset.relative_to(DIST)), "runtime article clipping shipped"])

for route in LESSONS:
    path = DIST / f"{route}.html"
    if not path.exists():
        errors.append([route, "lesson missing"])
        continue
    article = Article()
    article.feed(path.read_text())
    text = "".join(article.text)
    if "付费" in article.title:
        errors.append([route, "still a paid placeholder title"])
    if len(text) < 1800 or article.headings < 5:
        errors.append([route, "substantive lesson absent", len(text), article.headings])
    if not article.canonical.startswith("https://lovelsf-int.github.io/guide/"):
        errors.append([route, "study lesson canonical URL missing"])

print(json.dumps({"required_lessons": len(LESSONS), "errors": errors}, ensure_ascii=False, indent=2))
sys.exit(bool(errors))
