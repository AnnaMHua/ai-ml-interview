from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        path = ROOT / relative_path
        self.assertTrue(path.is_file(), f"missing required file: {relative_path}")
        return path.read_text(encoding="utf-8")

    def test_required_repository_files_exist(self) -> None:
        required = [
            ".github/workflows/build-site.yml",
            ".gitignore",
            "AGENT_ARTIFACT_GUIDE.md",
            "README.md",
            "mkdocs.yml",
            "requirements.txt",
            "docs/index.md",
            "docs/stylesheets/extra.css",
            "docs/javascripts/mathjax.js",
        ]
        for relative_path in required:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_backpropagation_topic_has_only_substantive_artifacts(self) -> None:
        topic = ROOT / "docs/topics/deep-learning/backpropagation"
        expected = {
            "index.md",
            "fundamentals.md",
            "derivations.md",
            "interview-questions.md",
            "coding-questions.md",
            "debugging.md",
            "references.md",
        }
        self.assertEqual({path.name for path in topic.glob("*.md")}, expected)
        for name in expected:
            with self.subTest(path=name):
                text = (topic / name).read_text(encoding="utf-8")
                self.assertGreater(len(text.split()), 35, f"{name} is not substantive")

    def test_mkdocs_enables_online_pages_search_and_math(self) -> None:
        config = self.read("mkdocs.yml")
        for required in [
            "site_url: https://annamhua.github.io/ai-ml-interview/",
            "repo_url: https://github.com/AnnaMHua/ai-ml-interview",
            "search",
            "pymdownx.arithmatex",
            "pymdownx.highlight",
            "pymdownx.superfences",
            "pymdownx.details",
            "javascripts/mathjax.js",
            "stylesheets/extra.css",
        ]:
            with self.subTest(setting=required):
                self.assertIn(required, config)
        for forbidden in [
            "offline",
            "use_directory_urls: false",
            "analytics:",
        ]:
            with self.subTest(setting=forbidden):
                self.assertNotIn(forbidden, config)

    def test_navigation_targets_exist(self) -> None:
        config = self.read("mkdocs.yml")
        targets = re.findall(
            r"^[ \t]*-[ \t]+[^:\n]+:[ \t]+([^#\n]+\.md)[ \t]*$",
            config,
            re.MULTILINE,
        )
        self.assertGreater(len(targets), 5)
        for target in targets:
            with self.subTest(target=target):
                self.assertTrue((ROOT / "docs" / target.strip()).is_file(), target)

    def test_project_records_are_excluded_from_reader_site(self) -> None:
        config = self.read("mkdocs.yml")
        self.assertIn("exclude_docs:", config)
        self.assertIn("design/**", config)
        self.assertIn("superpowers/**", config)

    def test_workflow_validates_and_deploys_github_pages(self) -> None:
        workflow = self.read(".github/workflows/build-site.yml")
        for required in [
            "pull_request:",
            "workflow_dispatch:",
            "branches: [main]",
            "contents: read",
            "pages: write",
            "id-token: write",
            'group: "pages"',
            "mkdocs build --strict --clean",
            "test -f site/index.html",
            "github.event_name != 'pull_request'",
            "uses: actions/configure-pages@v5",
            "uses: actions/upload-pages-artifact@v5",
            "uses: actions/deploy-pages@v5",
            "name: github-pages",
            "url: ${{ steps.deployment.outputs.page_url }}",
        ]:
            with self.subTest(fragment=required):
                self.assertIn(required, workflow)
        for forbidden in [
            "actions/upload-artifact",
            "ai-ml-interview-notes-site",
            "retention-days:",
            "deployments: write",
        ]:
            with self.subTest(fragment=forbidden):
                self.assertNotIn(forbidden, workflow)

    def test_dependencies_are_exactly_pinned(self) -> None:
        requirements = self.read("requirements.txt").splitlines()
        packages = [line for line in requirements if line and not line.startswith("#")]
        self.assertTrue(packages)
        self.assertTrue(all(re.fullmatch(r"[A-Za-z0-9_.-]+==[^=\s]+", line) for line in packages))

    def test_generated_site_is_ignored(self) -> None:
        ignore = self.read(".gitignore").splitlines()
        self.assertIn("site/", ignore)

    def test_readme_points_to_public_site(self) -> None:
        readme = self.read("README.md")
        self.assertIn("https://annamhua.github.io/ai-ml-interview/", readme)
        self.assertNotIn("download the `ai-ml-interview-notes-site` artifact", readme.lower())

    def test_interview_notation_is_preserved(self) -> None:
        coding = self.read("docs/topics/deep-learning/backpropagation/coding-questions.md")
        for notation in ["dA = dC @ B.T", "dB = A.T @ dC", "dX = dY @ W", "db = dY.sum(axis=0)"]:
            with self.subTest(notation=notation):
                self.assertIn(notation, coding)

    def test_fundamentals_preserves_complete_matrix_form_note(self) -> None:
        fundamentals = self.read(
            "docs/topics/deep-learning/backpropagation/fundamentals.md"
        )
        required_sections = [
            "## Why We Need Backpropagation",
            "## Machine-Learning and PyTorch Gradient Convention",
            "## The Three Objects to Keep Separate",
            "## Where Backpropagation Starts",
            "## Why We Use Differentials",
            "## Deriving the General Backpropagation Equations",
            "## How the General Rule Relates to a Concrete Layer",
            "## Example: A Linear Layer",
            "## Coding-Interview Notation Conventions",
            "## Summary",
            "## Reference",
        ]
        for heading in required_sections:
            with self.subTest(heading=heading):
                self.assertIn(heading, fundamentals)

        required_content = [
            r"g_{l-1}=A_l^Tg_l",
            r"\nabla_{\theta_l}\mathcal{L}=B_l^Tg_l",
            r"\nabla_W\mathcal{L}=g_yx^T",
            "dA = dC @ B.T",
            "dB = A.T @ dC",
            "dX = dY @ W",
            "dW = dY.T @ X",
            "db = dY.sum(axis=0)",
            "already contained in the upstream gradient",
            "https://visionbook.mit.edu/backpropagation.html",
        ]
        for fragment in required_content:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, fundamentals)


if __name__ == "__main__":
    unittest.main()
