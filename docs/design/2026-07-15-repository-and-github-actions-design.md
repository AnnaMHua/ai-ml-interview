# AI/ML Interview Notes — Repository and GitHub Actions Design

**Date:** 2026-07-15  
**Status:** Approved design  
**Scope:** Empty repository initialization, static-site build, and private artifact delivery

## 1. Goal

Turn a private GitHub repository containing Markdown interview notes into a downloadable website that can be extracted and opened by double-clicking `index.html`.

The first version does not publish to GitHub Pages and does not require a local web server for reading.

## 2. Architecture

```text
Private GitHub repository
    -> Markdown and MkDocs configuration
    -> GitHub Actions
    -> mkdocs build --strict --clean
    -> generated site/ directory
    -> workflow artifact ZIP
    -> download and extract
    -> open index.html through file://
```

## 3. Why Code Is Still Required

This is not a custom web application, but it still needs a small build system.

The repository contains:

- Markdown knowledge content;
- MkDocs configuration;
- theme customization;
- math initialization;
- pinned Python dependencies;
- one GitHub Actions workflow.

MkDocs Material supplies the page templates, navigation, search, and static-site generation. No React frontend, backend server, API, or database is needed.

## 4. Repository Layout

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

The generated `site/` directory is excluded by `.gitignore` and never committed.

## 5. Build Configuration

### MkDocs Material

`mkdocs.yml` enables:

- Material theme;
- search;
- built-in offline plugin;
- light and dark palettes;
- navigation and page table of contents;
- syntax highlighting;
- admonitions and collapsible answers;
- MathJax-compatible equations;
- local CSS and JavaScript configuration files.

### Direct local-file support

The built-in `offline` plugin is mandatory for the distributed build.

It provides two critical behaviors:

1. generated links point to explicit `.html` files instead of relying on directory routing;
2. the search index is packaged in a way that continues to work from `file://`.

Do not enable Material instant navigation, analytics, versioning, or comments in this build because they are not compatible with the intended local-file delivery model.

### Math rendering

The content uses `pymdownx.arithmatex` and a small `docs/javascripts/mathjax.js` configuration file.

The initial design may load the pinned MathJax runtime from an external source. This keeps the repository and build simple. Internal navigation, content, code, and search remain local; math rendering and external reference links may require internet access.

A fully bundled math runtime is explicitly deferred unless the user later requires air-gapped reading.

## 6. Dependency Management

`requirements.txt` pins the Python packages required to build the site.

At minimum, it includes a pinned compatible version of:

```text
mkdocs-material
```

MkDocs and the commonly used Markdown extensions are installed through that dependency chain unless implementation testing shows that another explicit pin is required.

Rules:

- use exact versions in the initial repository;
- upgrade intentionally in a separate change;
- use the same file locally and in GitHub Actions;
- do not add Node.js, Docker, or a second build tool without a demonstrated need.

## 7. GitHub Actions Workflow

### File

```text
.github/workflows/build-site.yml
```

### Triggers

```yaml
on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:
```

### Permissions

```yaml
permissions:
  contents: read
```

No repository write, Pages, deployment, package, or release permission is needed.

### Build job

The workflow uses a single Ubuntu job:

```text
checkout
    -> setup Python
    -> cache pip downloads when convenient
    -> pip install -r requirements.txt
    -> mkdocs build --strict --clean
    -> verify site/index.html exists
```

`--strict` turns MkDocs warnings into build failures. `--clean` removes stale output before each build.

### Artifact upload

For a successful push to `main` or a successful manual run:

```text
upload site/
artifact name: ai-ml-interview-notes-site
retention: 30 days
```

GitHub automatically presents the workflow artifact as a downloadable archive.

Pull requests run the complete build validation but do not upload the long-lived reading artifact by default.

## 8. Suggested Workflow Shape

The implementation should remain close to this structure:

```yaml
name: Build interview notes site

on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<pinned-major>
      - uses: actions/setup-python@<pinned-major>
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt
      - run: mkdocs build --strict --clean
      - run: test -f site/index.html
      - uses: actions/upload-artifact@v4
        if: github.event_name != 'pull_request'
        with:
          name: ai-ml-interview-notes-site
          path: site/
          retention-days: 30
          if-no-files-found: error
```

The exact action major versions should be selected from current official releases during implementation.

## 9. Download and Reading Experience

The user workflow is:

1. open the latest successful `main` or manual workflow run;
2. download `ai-ml-interview-notes-site` from the Artifacts section;
3. extract the downloaded ZIP;
4. keep all extracted files and directories together;
5. double-click `index.html`;
6. browse using the sidebar or search.

Do not move only `index.html` elsewhere. The page depends on adjacent generated assets and content files.

## 10. README Requirements

The root `README.md` should explain:

- what the repository contains;
- where knowledge artifacts live;
- how to add or update a topic;
- how to trigger the workflow manually;
- how to download the latest artifact;
- how to extract and open `index.html`;
- that GitHub Pages is intentionally disabled;
- that the entire extracted directory must be kept together.

Local MkDocs commands may be documented as an optional developer convenience, but they are not part of the normal reading flow.

## 11. Failure Behavior

The workflow fails when:

- dependencies cannot be installed;
- `mkdocs.yml` is invalid;
- a strict-mode warning occurs;
- a configured page does not exist;
- Markdown extensions cannot load;
- the build does not produce `site/index.html`;
- the artifact upload receives an empty path.

A failed workflow does not replace or remove a previously downloaded site. The user fixes the repository and reruns the build.

## 12. Security and Privacy

- The source repository remains private.
- The workflow has read-only repository permission.
- No GitHub Pages site is created.
- No secrets are required.
- The generated artifact is accessible only through the repository and its workflow permissions.
- Knowledge pages do not contain analytics or third-party comments.
- External links are ordinary references and may contact their destination only when the user opens them.

## 13. Testing Strategy

### Build validation

Run:

```bash
mkdocs build --strict --clean
```

### Output validation

Confirm:

```text
site/index.html exists
all navigation targets are present
offline search files are generated
local CSS and JavaScript files are included
```

### Browser smoke test

On at least one macOS browser:

1. extract the artifact;
2. open `index.html` through `file://`;
3. open a topic and multiple artifact pages;
4. use full-site search;
5. expand a collapsed answer;
6. switch light and dark mode;
7. inspect equations, code blocks, images, and internal links.

Chrome is the primary expected browser. A second modern browser may be checked during initial implementation.

## 14. MVP Acceptance Criteria

1. The repository can start empty and be scaffolded with the files in this design.
2. A pull request runs a strict build check.
3. A push to `main` runs the same strict build.
4. A successful `main` build uploads `ai-ml-interview-notes-site`.
5. The workflow uses only read access to repository contents.
6. No Pages or deployment step exists.
7. The downloaded archive contains `index.html` and all required generated assets.
8. The extracted website opens by double-clicking `index.html`.
9. Internal navigation and search work through `file://`.
10. A failed build does not upload a misleading successful artifact.
11. `site/` is not committed to the repository.

## 15. Deferred Decisions

Do not add these in the first version:

- GitHub Pages;
- private hosted deployment;
- custom domain;
- Docker build;
- Node frontend;
- automated content generation;
- automatic navigation generation;
- advanced link crawlers;
- artifact signing or attestations;
- fully air-gapped MathJax packaging;
- release attachments.

## 16. Technical References

- Material for MkDocs built-in offline plugin: https://squidfunk.github.io/mkdocs-material/plugins/offline/
- MkDocs configuration, including `use_directory_urls` and strict mode: https://www.mkdocs.org/user-guide/configuration/
- GitHub Actions workflow artifacts: https://docs.github.com/en/actions/tutorials/store-and-share-data
- GitHub Actions workflow permissions: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

## 17. Default Rule

The build system should remain smaller than the content system. Add automation only when it prevents a real failure or materially simplifies downloading and reading the knowledge artifacts.
