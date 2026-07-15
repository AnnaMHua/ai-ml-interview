# AI/ML Interview Notes Website — Product Design

**Date:** 2026-07-15  
**Status:** Approved design, revised for private GitHub Actions delivery  
**Audience:** Personal use only

## 1. Product

A simple, read-only website for reviewing personal AI/ML interview knowledge.

The preparation work happens elsewhere:

```text
Read and research
    -> discuss and refine with an agent
    -> produce polished Markdown artifacts
    -> add them to the private repository
    -> let GitHub Actions build the website
    -> download and open the generated site locally
```

The website only organizes, searches, and displays finished artifacts.

## 2. Product Principles

- Keep the product simple and direct.
- Optimize for reading and refreshing knowledge.
- Display the user's artifacts without adding workflow features around them.
- Use Markdown as the only maintained knowledge format.
- Preserve the user's explanations, notation, and mental models.
- Verify formulas and code before publishing.
- Keep the repository private.
- Build a downloadable local site instead of publishing it publicly.
- Do not add metadata or features without a clear reading benefit.

## 3. Included

- Private GitHub repository
- Downloadable static website
- Direct local opening through `index.html`
- Homepage showing all subjects and topics
- Topic landing pages
- Markdown content pages
- Full-site search that works from the downloaded site
- Math equations
- Syntax-highlighted code
- Images and tables
- Collapsible interview answers
- Left navigation and page table of contents
- Light and dark modes
- GitHub Actions build validation
- GitHub Actions workflow artifact containing the generated site

## 4. Not Included

- GitHub Pages publishing in the first version
- Public website
- Embedded agent or chat
- Research workflow
- Task management
- Study schedules
- Progress or status tracking
- Priority labels
- Recommendations or analytics
- Database
- Accounts or multiple users
- Automatic scraping
- Custom admin interface
- Custom React, Vue, or backend application
- A local server requirement for reading the downloaded site

## 5. Main User Flow

```text
Open the private repository
    -> update or merge Markdown artifacts
    -> GitHub Actions validates and builds the site
    -> download the latest site artifact
    -> extract the complete folder
    -> double-click index.html
    -> browse or search the knowledge base
```

The user must keep the complete extracted folder together. `index.html` depends on the adjacent generated pages, JavaScript, CSS, and search files.

## 6. Information Architecture

### Homepage

Show every existing topic directly under its subject area.

```text
AI/ML Interview Notes

Deep Learning
- Backpropagation
- Attention
- CNNs
- Transformers

Classical Machine Learning
- Linear Regression
- Trees and Ensembles
- Clustering

Math & Statistics
- Linear Algebra
- Probability
- Matrix Calculus

ML Systems
- Distributed Training
- Model Serving
- Evaluation

Coding
- NumPy
- PyTorch
- Python
```

Do not show status, progress, planned topics, statistics, or recommendations.

### Topic landing page

A topic page is a concise table of contents.

```text
Backpropagation

- Fundamentals
- Derivations
- Interview Questions
- Coding Questions
- Debugging
- References
```

Only artifacts that exist are displayed.

### Artifact pages

Artifact pages contain the actual notes, equations, code, questions, debugging cases, diagrams, and references.

## 7. Layout

Use a standard documentation-site layout.

```text
Top bar
- Website title
- Search
- Light/dark mode

Left sidebar
- Subjects and topics
- Current topic artifacts

Main area
- Markdown content

Right sidebar
- Current page headings
```

## 8. Technology

Use MkDocs Material.

```text
Markdown
    -> MkDocs Material
    -> generated site/ directory
    -> GitHub Actions artifact
    -> local browser through file://
```

MkDocs Material provides navigation, search, MathJax integration, code highlighting, collapsible sections, and static generation without requiring a custom application.

Use the built-in Material `offline` plugin so internal navigation and search work when the generated `index.html` is opened directly from the local file system. The plugin also disables directory-style URLs for the offline build.

The first version does not require a fully air-gapped site. External reference links require an internet connection, and the selected math-rendering library may be loaded from a pinned external source. A self-contained math runtime can be added later only if offline math rendering becomes necessary.

Do not enable features known to conflict with direct local-file use, including instant navigation, analytics, versioning, or comments.

## 9. Canonical Artifact Format

Markdown is the only maintained knowledge format.

Markdown may contain:

- prose;
- MathJax-compatible LaTeX equations;
- fenced code blocks;
- tables;
- images;
- links;
- collapsible answers.

Other files are used only when Markdown cannot replace them:

```text
.py or other source files   standalone runnable code
.ipynb                      real executable experiments
.png / .jpg / .svg          diagrams and images
```

Do not maintain duplicate PDF or LaTeX versions of the same note.

## 10. Existing Artifact Migration

Existing PDF and LaTeX notes will be converted into Markdown.

The conversion must:

- preserve the knowledge and useful personal explanations;
- convert formulas and code correctly;
- remove print-only formatting;
- correct technical errors;
- split material into appropriate artifact pages when needed;
- verify the rendered Markdown.

After the Markdown version is confirmed complete and correct, the original PDF and LaTeX copies are deleted.

## 11. Repository Structure

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

The generated `site/` directory is build output. It is not committed to Git.

## 12. Repository File Responsibilities

### `mkdocs.yml`

Defines:

- site title;
- Material theme and palettes;
- navigation;
- offline and search plugins;
- Markdown extensions;
- math support;
- code highlighting;
- collapsible answers;
- additional CSS and JavaScript.

### `requirements.txt`

Pins the Python packages used by both local builds and GitHub Actions. Exact versions are chosen during implementation and upgraded intentionally.

### `.github/workflows/build-site.yml`

Validates and builds the site, then uploads the generated `site/` directory as a downloadable GitHub Actions artifact.

### `README.md`

Explains how to add artifacts, trigger the build, download the site, extract it, and open `index.html`.

### `AGENT_ARTIFACT_GUIDE.md`

Defines the content contract for agents creating or editing Markdown artifacts.

## 13. Topic Artifact Rules

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

## 14. Sources

All meaningful external sources belong in `references.md`.

Other pages cite sources only when a conclusion, formula, convention, framework behavior, or interview claim needs clear attribution. Dense citation on every sentence is not required.

External links remain links and are not copied into the generated site unless they are deliberate local assets.

## 15. Agent Boundary

Agents work outside the website.

They may create a full topic or update a single artifact. Their work is governed by `AGENT_ARTIFACT_GUIDE.md`.

For updates to existing artifacts, the user chooses one mode:

- **Local edit** — change only the requested section.
- **Structural edit** — reorganize sections and remove duplication.
- **Complete rewrite** — rewrite the page while preserving its correct knowledge.

An agent may recommend a new optional page, but must receive approval before creating it.

Agents creating knowledge artifacts do not edit `mkdocs.yml`, GitHub Actions workflows, dependency files, or shared styles unless the user explicitly requests a site-level change.

## 16. Correctness

Before publication:

- formulas must be mathematically and dimensionally correct;
- code must be checked with a method appropriate to the problem;
- checks may use official implementations, trusted public implementations, framework comparisons, unit tests, edge cases, autograd, finite differences, known examples, invariants, or numerical-stability analysis;
- an agent must not claim execution that did not happen.

Verification details are not displayed in the final website.

## 17. Writing Style

The artifacts should preserve the user's preferred explanations, notation, interview framing, and mental models.

Agents may improve clarity and organization, but should not turn the notes into generic textbook summaries.

Technical mistakes are corrected directly. The final artifact does not retain an error history.

## 18. GitHub Actions Delivery

The private repository uses one build workflow.

### Triggers

```text
pull_request
push to main
workflow_dispatch
```

### Behavior

All runs:

```text
checkout repository
    -> set up Python
    -> install pinned dependencies
    -> run mkdocs build --strict --clean
    -> confirm site/index.html exists
```

For `push` to `main` and manual runs:

```text
upload the complete site/ directory
    -> artifact name: ai-ml-interview-notes-site
```

Pull requests validate that the website builds but do not need to upload a permanent reading artifact.

### Permissions

The workflow receives only:

```yaml
permissions:
  contents: read
```

It does not receive Pages, deployment, release, or repository write permissions.

### Artifact retention

Use a modest retention period, initially 30 days. The repository remains the permanent source of truth; the generated website can always be rebuilt.

## 19. Local Reading Contract

After downloading the workflow artifact:

1. extract the ZIP archive;
2. keep the entire extracted directory together;
3. open the extracted `index.html` in a modern browser;
4. use the left navigation or full-site search.

No Python environment or local web server is required for reading the downloaded build.

## 20. Pilot Topic

Backpropagation is the first complete topic:

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

It validates navigation, equations, code, collapsible answers, search, direct `file://` reading, GitHub Actions builds, and migration from the existing artifacts.

## 21. MVP Acceptance Criteria

The first version is complete when:

1. The content and configuration live in a private GitHub repository.
2. MkDocs Material builds successfully with pinned dependencies.
3. The homepage shows all existing subjects and topics.
4. Backpropagation appears under Deep Learning.
5. Topic pages link only to artifacts that exist.
6. Markdown is the sole maintained knowledge format.
7. Equations and code render correctly under the expected reading conditions.
8. Interview answers can be collapsed.
9. Full-site search works after opening the downloaded `index.html` directly.
10. Existing Backpropagation material has been migrated to Markdown.
11. `mkdocs build --strict --clean` succeeds.
12. GitHub Actions uploads the complete generated site after a successful `main` or manual build.
13. The downloaded artifact can be extracted and read without running a server.
14. No GitHub Pages deployment occurs.
15. A second topic can be added without redesigning the site.

## 22. Future Hosting

Online hosting is deliberately deferred.

If the user later chooses to publish or privately host the site, the content model remains unchanged. Only the build and delivery layer should be revisited.

## 23. Technical References

- Material for MkDocs built-in offline plugin: https://squidfunk.github.io/mkdocs-material/plugins/offline/
- MkDocs `use_directory_urls` and strict builds: https://www.mkdocs.org/user-guide/configuration/
- GitHub Actions workflow artifacts: https://docs.github.com/en/actions/tutorials/store-and-share-data
- GitHub Actions workflow permissions: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

## 24. Default Product Rule

When deciding whether to add a feature, file, dependency, or metadata field, prefer the simpler option unless it clearly improves reading, correctness, or reliable delivery of the knowledge artifacts.
