# AI/ML Interview Notes

Private, read-only AI/ML interview knowledge rendered from Markdown with MkDocs Material. GitHub Actions validates the source and packages a downloadable website; GitHub Pages is intentionally not used.

## Read the generated site

1. Open the repository's **Actions** tab.
2. Open the latest successful **Build interview notes site** run on `main`.
3. Download the `ai-ml-interview-notes-site` artifact.
4. Extract the ZIP and keep the entire extracted directory together.
5. Double-click the extracted `index.html`.

No Python environment or local server is required for reading. Internal navigation and search are built for `file://` use. MathJax is initially loaded from a pinned CDN, so equations require internet access until the runtime is bundled in a future change.

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

## Trigger a manual artifact build

In **Actions**, select **Build interview notes site**, choose **Run workflow**, and run it from `main`. Pull requests run the same validation but do not upload a reading artifact. Pushes to `main` and manual runs retain the artifact for 30 days.

## Repository boundaries

This repository organizes, searches, and renders polished notes. It does not contain an AI chat, study tracker, database, analytics, or deployment configuration. Markdown is the only maintained knowledge format.
