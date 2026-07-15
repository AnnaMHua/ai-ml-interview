# AI/ML Interview Notes

Public, read-only AI/ML interview knowledge rendered from Markdown with MkDocs Material and deployed through GitHub Pages.

## Read the site

Open **https://annamhua.github.io/ai-ml-interview/**.

No download, Python environment, or local server is required for reading. GitHub Actions rebuilds and redeploys the site after each successful push to `main`.

## Add or update a topic

Knowledge source lives under `docs/topics/<subject>/<topic>/`. Every topic has:

```text
index.md
fundamentals.md
references.md
```

Add an optional page such as `derivations.md`, `coding-questions.md`, or `debugging.md` only when it has useful independent content. Never add an empty placeholder. Then add the real page to `nav` in `mkdocs.yml` and link the topic from its subject page and the homepage.

Follow [AGENT_ARTIFACT_GUIDE.md](AGENT_ARTIFACT_GUIDE.md) when an agent creates or edits note content.

## Build locally

Local building is optional but useful when editing:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

For the same strict build used in CI:

```bash
python -m unittest tests.test_repository_contract -v
mkdocs build --strict --clean
python -m unittest tests.test_site_output -v
```

The generated `site/` directory is ignored by Git and must not be committed.

## Trigger a manual deployment

In **Actions**, select **Build and deploy interview notes**, choose **Run workflow**, and run it from `main`. Pull requests run build validation without deploying. Pushes to `main` and manual runs publish through the protected `github-pages` environment.

## Repository boundaries

This public repository organizes, searches, and renders polished notes. It does not contain an AI chat, study tracker, database, or analytics. Markdown is the only maintained knowledge format.
