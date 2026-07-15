from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


class SiteOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.index_path = SITE / "index.html"
        if not cls.index_path.is_file():
            raise AssertionError("site/index.html must be generated before output tests run")
        cls.index = cls.index_path.read_text(encoding="utf-8")

    def test_pages_build_contains_required_assets(self) -> None:
        self.assertTrue((SITE / "search/search_index.json").is_file())
        self.assertTrue((SITE / "stylesheets/extra.css").is_file())
        self.assertTrue((SITE / "javascripts/mathjax.js").is_file())

    def test_homepage_internal_links_use_web_routes(self) -> None:
        parser = LinkCollector()
        parser.feed(self.index)
        internal = [
            link for link in parser.links
            if not re.match(r"(?:[a-z]+:|//|#)", link) and not link.startswith("assets/")
        ]
        self.assertTrue(internal)
        self.assertTrue(any(link.endswith("/") for link in internal))
        self.assertFalse(any(link.endswith(".html") for link in internal))

    def test_all_local_html_links_resolve(self) -> None:
        failures: list[str] = []
        for page in SITE.rglob("*.html"):
            parser = LinkCollector()
            parser.feed(page.read_text(encoding="utf-8"))
            for link in parser.links:
                clean = link.split("#", 1)[0].split("?", 1)[0]
                if not clean or re.match(r"(?:[a-z]+:|//)", clean):
                    continue
                if clean.startswith("/ai-ml-interview/"):
                    target = SITE / clean.removeprefix("/ai-ml-interview/")
                elif clean.startswith("/"):
                    target = SITE / clean.lstrip("/")
                else:
                    target = page.parent / clean
                target = target.resolve()
                if not target.exists():
                    failures.append(f"{page.relative_to(SITE)} -> {link}")
        self.assertEqual(failures, [])

    def test_pilot_renders_equations_code_and_collapsible_answers(self) -> None:
        pages = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (SITE / "topics/deep-learning/backpropagation").rglob("*.html")
        )
        self.assertIn("arithmatex", pages)
        self.assertIn("highlight", pages)
        self.assertIn("<details", pages)

    def test_fundamentals_renders_display_math(self) -> None:
        fundamentals = (
            SITE
            / "topics/deep-learning/backpropagation/fundamentals/index.html"
        ).read_text(encoding="utf-8")
        self.assertNotIn("$$", fundamentals)
        self.assertIn(
            '<div class="arithmatex">\\[\n'
            r"\boxed{\nabla_z\mathcal{L}\text{ has the same shape as }z.}",
            fundamentals,
        )
        self.assertEqual(fundamentals.count('<div class="arithmatex">'), 82)


if __name__ == "__main__":
    unittest.main()
