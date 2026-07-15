# AI/ML Interview Notes Website — Project Handoff

**Date:** 2026-07-15  
**Status:** Product and build design approved; ready for implementation planning  
**Phase:** Phase 1 — private repository and downloadable local website  
**Pilot topic:** Backpropagation

## 1. Project Goal

Build a simple personal website for reviewing AI/ML interview knowledge.

The site is not a research assistant, workflow manager, or learning tracker. Research and note preparation happen externally with books, online sources, and agents. The repository receives polished knowledge artifacts and renders them as a clean documentation website.

```text
Research and discuss elsewhere
    -> produce polished Markdown
    -> commit to private GitHub repository
    -> GitHub Actions builds the site
    -> download the workflow artifact
    -> extract and open index.html locally
```

## 2. Approved Product Boundary

The product does only three things:

1. organize artifacts by subject and topic;
2. render artifacts clearly;
3. provide navigation and full-site search.

Do not add:

- embedded AI chat;
- research workflows;
- tasks or study plans;
- progress, status, or priority tracking;
- recommendations or analytics;
- database or user accounts;
- GitHub Pages publishing in Phase 1;
- custom React or backend application.

## 3. Canonical Content Rule

Markdown is the only maintained knowledge format.

Use Markdown for:

- prose;
- MathJax-compatible equations;
- code blocks;
- tables;
- images;
- links;
- collapsible answers.

Existing PDF and LaTeX notes are converted into Markdown. After the user verifies that the conversion is complete and correct, the original PDF and LaTeX copies are deleted.

Supporting code, notebooks, and images may remain as separate files only when Markdown cannot replace them.

## 4. Website Experience

### Homepage

The homepage displays all existing subjects and topics directly. It does not show progress, status, statistics, or planned topics.

Example:

```text
Deep Learning
- Backpropagation
- Attention
- CNNs
- Transformers

Classical Machine Learning
- Linear Regression
- Trees and Ensembles

Math & Statistics
- Linear Algebra
- Probability
- Matrix Calculus

ML Systems
- Distributed Training
- Model Serving

Coding
- NumPy
- PyTorch
- Python
```

### Topic page

Each topic landing page is a concise table of contents. It shows only artifacts that exist.

Example:

```text
Backpropagation
- Fundamentals
- Derivations
- Interview Questions
- Coding Questions
- Debugging
- References
```

### Layout

Use the standard Material documentation layout:

```text
Top bar: title, search, light/dark mode
Left sidebar: subjects, topics, current topic artifacts
Main area: Markdown content
Right sidebar: current-page headings
```

## 5. Topic Artifact Structure

Every topic requires only:

```text
index.md
fundamentals.md
references.md
```

Optional pages are created only when they contain useful independent content:

```text
derivations.md
interview-questions.md
coding-questions.md
debugging.md
system-design.md
case-studies.md
experiments.md
```

Do not create empty pages.

## 6. Repository Structure

```text
ai-ml-interview-notes/
├── .github/
│   └── workflows/
│       └── build-site.yml
├── docs/
│   ├── index.md
│   ├── stylesheets/
│   │   └── extra.css
│   ├── javascripts/
│   │   └── mathjax.js
│   └── topics/
│       ├── deep-learning/
│       │   ├── index.md
│       │   └── backpropagation/
│       │       ├── index.md
│       │       ├── fundamentals.md
│       │       ├── references.md
│       │       ├── derivations.md
│       │       ├── interview-questions.md
│       │       ├── coding-questions.md
│       │       ├── debugging.md
│       │       └── assets/
│       ├── classical-ml/
│       ├── math-statistics/
│       ├── ml-systems/
│       └── coding/
├── mkdocs.yml
├── requirements.txt
├── README.md
├── AGENT_ARTIFACT_GUIDE.md
└── .gitignore
```

`site/` is generated output and must not be committed.

## 7. Technology Decisions

Use MkDocs Material.

Required capabilities:

- Material theme;
- full-site search;
- built-in offline plugin;
- MathJax-compatible equations;
- syntax highlighting;
- admonitions and collapsible answers;
- light and dark mode;
- standard navigation.

The Material offline plugin is required because the user downloads the generated site and opens `index.html` directly through `file://`. It packages search for local-file use and generates explicit `.html` links.

Do not enable instant navigation, analytics, versioning, or comments.

Phase 1 is local-file capable, not necessarily air-gapped. External references and the initial MathJax runtime may require internet access.

## 8. GitHub Actions Design

The private repository contains one workflow:

```text
.github/workflows/build-site.yml
```

Triggers:

```text
pull requests
pushes to main
manual workflow runs
```

All runs:

```text
checkout
-> set up Python
-> install requirements.txt
-> mkdocs build --strict --clean
-> verify site/index.html
```

Successful pushes to `main` and manual runs also upload:

```text
artifact name: ai-ml-interview-notes-site
contents: complete site/ directory
retention: 30 days
```

Pull requests validate the build but do not need to upload a reading artifact.

Workflow permissions:

```yaml
permissions:
  contents: read
```

Do not add Pages, deployment, or repository write permissions.

## 9. User Reading Flow

```text
Open latest successful main/manual workflow run
-> download ai-ml-interview-notes-site
-> extract the ZIP
-> keep the full directory together
-> double-click index.html
```

No local Python environment or web server is required for reading.

## 10. Agent Content Contract

Agents may create a full topic or update one artifact.

They must:

- deliver complete Markdown files;
- preserve the user's preferred explanations and notation;
- correct technical errors directly;
- verify formulas and code before delivery;
- choose verification methods appropriate to the problem;
- record meaningful external sources in `references.md`;
- use portable relative links and assets;
- avoid server-dependent embeds and custom scripts;
- avoid creating optional pages without user approval;
- avoid editing site-level configuration unless explicitly asked.

For updates, the user chooses:

- local edit;
- structural edit;
- complete rewrite.

See `AGENT_ARTIFACT_GUIDE.md` for the full contract.

## 11. Backpropagation Pilot

The first complete topic is:

```text
backpropagation/
├── index.md
├── fundamentals.md
├── references.md
├── derivations.md
├── interview-questions.md
├── coding-questions.md
├── debugging.md
└── assets/
```

It should prove:

- navigation and topic organization;
- Markdown migration from existing notes;
- equations;
- code blocks;
- collapsible answers;
- search;
- direct local-file opening;
- GitHub Actions build and artifact download.

## 12. MVP Acceptance Criteria

1. The repository is private.
2. MkDocs Material builds with pinned dependencies.
3. GitHub Actions runs on pull requests, `main`, and manual trigger.
4. `mkdocs build --strict --clean` succeeds.
5. A successful `main` or manual run uploads `ai-ml-interview-notes-site`.
6. The artifact can be extracted and opened by double-clicking `index.html`.
7. Internal navigation and search work through `file://`.
8. No GitHub Pages deployment exists.
9. Markdown is the only maintained note format.
10. Existing Backpropagation material is migrated and verified.
11. A second topic can be added without redesign.

## 13. Approved Design Documents

Implementation should follow these documents:

```text
2026-07-15-ai-ml-interview-notes-product-design.md
2026-07-15-repository-and-github-actions-design.md
AGENT_ARTIFACT_GUIDE.md
```

If a future decision conflicts with this handoff, update all four documents together.

## 14. Next Step

The next agent should create an implementation plan before writing repository files.

The implementation plan should cover:

1. repository scaffolding;
2. MkDocs and offline configuration;
3. GitHub Actions workflow;
4. minimal homepage and subject navigation;
5. Backpropagation skeleton and content migration;
6. strict build validation;
7. downloaded artifact browser smoke test;
8. documentation for adding future topics.
