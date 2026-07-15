# AI/ML Interview Notes Initial Implementation Plan

**Goal:** Build the approved private, read-only MkDocs Material knowledge site in a repository named `ai-ml-interview`, with a downloadable GitHub Actions artifact that works through `file://`.

**Architecture:** Markdown is the only maintained knowledge format. MkDocs Material compiles the repository into `site/`; its offline plugin produces explicit HTML links and local search assets. A single read-only GitHub Actions workflow validates every pull request and `main` push, and uploads the generated site after `main` or manual builds.

**Technology:** Python 3.12, MkDocs Material 9.7.6, Material offline/search plugins, MathJax 3, GitHub Actions.

---

## Task 1: Initialize the private-source repository structure

**Files:**

- Create: `.gitignore`
- Create: `docs/index.md`
- Create: `docs/topics/deep-learning/index.md`
- Create: empty directories only when backed by committed content
- Add: approved design records under `docs/design/`

**Steps:**

1. Initialize Git with `main` as the default branch.
2. Add ignore rules for `site/`, Python caches, virtual environments, editor files, and OS metadata.
3. Copy the approved design, build design, handoff, and agent artifact guide into stable repository paths, renaming files to canonical names.
4. Confirm no generated `site/` output or duplicate PDF/LaTeX note source is tracked.
5. Commit the plan and design records together as the implementation baseline.

## Task 2: Add failing repository-contract tests

**Files:**

- Create: `tests/test_repository_contract.py`
- Create: `tests/test_site_output.py`

**Steps:**

1. Write tests that require the approved repository files, Backpropagation artifacts, and exact navigation targets.
2. Write workflow-contract tests for triggers, `contents: read`, strict build, artifact name, 30-day retention, and no Pages/deploy permissions.
3. Write output tests for `site/index.html`, explicit `.html` internal links, packaged search data, local CSS/JS, and absence of generated directory-style topic URLs.
4. Run the test suite and confirm it fails because implementation files do not exist yet.

## Task 3: Implement the MkDocs build system

**Files:**

- Create: `mkdocs.yml`
- Create: `requirements.txt`
- Create: `docs/stylesheets/extra.css`
- Create: `docs/javascripts/mathjax.js`

**Steps:**

1. Pin `mkdocs-material==9.7.6`.
2. Configure Material palettes, navigation tabs/sections, page table of contents, search, and offline plugins.
3. Configure `pymdownx.arithmatex`, highlighting, superfences, admonitions, details, tables, attributes, and MathJax initialization.
4. Avoid instant navigation, analytics, versioning, comments, Pages configuration, and custom application code.
5. Run repository-contract tests and keep only expected content/workflow failures.

## Task 4: Implement the site and Backpropagation pilot

**Files:**

- Create: `docs/index.md`
- Create: `docs/topics/deep-learning/index.md`
- Create: `docs/topics/deep-learning/backpropagation/index.md`
- Create: `docs/topics/deep-learning/backpropagation/fundamentals.md`
- Create: `docs/topics/deep-learning/backpropagation/derivations.md`
- Create: `docs/topics/deep-learning/backpropagation/interview-questions.md`
- Create: `docs/topics/deep-learning/backpropagation/coding-questions.md`
- Create: `docs/topics/deep-learning/backpropagation/debugging.md`
- Create: `docs/topics/deep-learning/backpropagation/references.md`

**Steps:**

1. Build the homepage from subjects/topics that actually have content; do not present planned topics as existing.
2. Create the Deep Learning and Backpropagation landing pages with links only to real artifacts.
3. Populate the pilot with substantive Backpropagation content using the user's preferred interview notation (`dA`, `dB`, `dX`, `dW`, `db`), shape-first explanations, Markdown/code-block presentation, and collapsible answers.
4. Cover computation graphs, chain rule, matrix multiplication, affine layers, activations, softmax/cross-entropy, numerical checking, implementation questions, and debugging.
5. Record the MIT Vision Book Backpropagation chapter and other meaningful primary references in `references.md`.
6. Run tests and a strict clean build.

## Task 5: Add GitHub Actions delivery

**Files:**

- Create: `.github/workflows/build-site.yml`

**Steps:**

1. Configure pull request, `main` push, and manual triggers.
2. Set workflow permissions to `contents: read` only.
3. Use current official action majors, Python 3.12, pip caching, pinned requirements, and `mkdocs build --strict --clean`.
4. Verify `site/index.html` before artifact upload.
5. Upload `site/` as `ai-ml-interview-notes-site` for non-PR runs, with 30-day retention and missing-file failure.
6. Run workflow-contract tests.

## Task 6: Document use and agent contribution rules

**Files:**

- Create: `README.md`
- Create: `AGENT_ARTIFACT_GUIDE.md`

**Steps:**

1. Explain local preview/build, manual workflow triggering, artifact download/extraction, and `file://` reading.
2. Make clear that GitHub Pages is intentionally absent and the full extracted directory must stay together.
3. Install the approved agent artifact contract at the repository root and align repository-name examples with `ai-ml-interview`.
4. Document the exact process for adding a second topic without creating empty optional pages.

## Task 7: Verify the complete implementation

**Steps:**

1. Create an isolated Python virtual environment and install `requirements.txt`.
2. Run `python -m unittest discover -s tests -v`.
3. Run `mkdocs build --strict --clean`.
4. Re-run output-contract tests against the generated site.
5. Serve the generated output only for automated browser smoke checks; separately inspect generated links to verify `file://` compatibility.
6. Confirm search assets, theme toggle controls, equation markup/runtime, collapsible answers, code blocks, and all internal links are present.
7. Run `git status --short` and verify `site/` remains ignored.

## Task 8: Publish to GitHub

**Steps:**

1. Create a private GitHub repository named `ai-ml-interview` with `main` as its default branch.
2. Commit only the verified repository files.
3. Push `main` to the new remote.
4. Inspect the first GitHub Actions run and confirm the strict build and artifact upload succeed.
5. Report the repository URL, commit SHA, workflow status, artifact name, and any limitation in the initial Backpropagation content source.

## Explicit implementation assumptions

- The user-specified repository name `ai-ml-interview` overrides the older layout examples that used `ai-ml-interview-notes`.
- The repository is private, as required by every approved design document.
- The attached files contain design and process material but not the original Backpropagation PDF/LaTeX notes. The pilot will therefore be substantive starter Markdown based on the user's documented notation and prior interview-note preferences; it must not be described as a byte-for-byte migration of unattached source notes.
- No license is added because this is a private personal-notes repository and the approved design does not request one.
