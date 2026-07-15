# Agent Artifact Guide — AI/ML Interview Notes

Use this guide when creating, converting, or updating artifacts for the user's personal AI/ML interview-notes website.

## 1. Goal

Produce polished knowledge artifacts that are:

- technically correct;
- easy to review;
- compatible with MkDocs Material;
- safe to publish on the public GitHub Pages site;
- faithful to the user's preferred explanations and notation;
- ready to place directly into the repository.

The website is only a reading and search interface. Do not add research workflows, tasks, progress tracking, or agent features.

## 2. Repository Context

The repository and generated GitHub Pages site are public. GitHub Actions validates the Markdown, builds the static site, and deploys it at `https://annamhua.github.io/ai-ml-interview/`.

Knowledge agents normally edit only files under:

```text
docs/topics/
```

Do not edit these site-level files unless the user explicitly requests a site implementation change:

```text
.github/workflows/
mkdocs.yml
requirements.txt
docs/stylesheets/
docs/javascripts/
```

Do not commit or generate the build output directory:

```text
site/
```

## 3. Canonical Format

Markdown is the only canonical knowledge format.

Use Markdown for prose, equations, code blocks, tables, links, images, and collapsible answers.

Do not create duplicate note versions as PDF or LaTeX.

Standalone code, notebooks, and images are allowed only when they provide something Markdown cannot replace.

## 4. What You May Deliver

You may deliver:

- a complete new topic;
- one new artifact for an existing topic;
- an update to an existing artifact;
- a Markdown conversion of existing notes, PDF, LaTeX, or conversation material.

Deliver complete Markdown files, not only outlines or fragments, unless the user explicitly requests brainstorming.

## 5. Topic Structure

Every topic contains:

```text
index.md
fundamentals.md
references.md
```

Optional pages may include:

```text
derivations.md
interview-questions.md
coding-questions.md
debugging.md
system-design.md
case-studies.md
experiments.md
```

Create an optional page only when it has meaningful independent content.

If the user did not request a new page, recommend it first and wait for approval before creating it.

## 6. File Responsibilities

### `index.md`

Keep it concise. Include a short topic introduction and links to artifacts that actually exist.

Use relative Markdown links that remain inside the repository. Do not link to future or placeholder pages.

### `fundamentals.md`

Use it for the main knowledge note: motivation, definitions, intuition, notation, mechanisms, mathematics, implementation connections, misconceptions, and summaries as appropriate.

Do not force every topic into the same rigid heading template.

### `references.md`

Record meaningful sources with:

- title;
- author or organization when known;
- link or file reference;
- a short note explaining what the source contributed.

Do not provide only unexplained raw URLs.

## 7. Naming

Use lowercase kebab-case.

```text
deep-learning/
backpropagation/
interview-questions.md
coding-questions.md
```

Avoid multiple files with nearly identical purposes.

Do not use spaces, uppercase letters, or unstable generated identifiers in paths.

## 8. Editing Existing Artifacts

Follow the mode selected by the user:

- **Local edit** — modify only the requested area.
- **Structural edit** — reorganize sections and remove duplication.
- **Complete rewrite** — rewrite the artifact while preserving all correct knowledge.

Do not assume permission for broad restructuring.

## 9. Preserve the User's Style

This is a personal knowledge base.

Preserve useful elements such as:

- preferred notation;
- explanations that resolved confusion;
- shape-oriented reasoning;
- links between mathematics and implementation;
- interview-style prompts;
- personal mental models.

Improve clarity, but do not replace the artifact with a generic textbook summary.

## 10. Correct Errors Directly

When source material contains a technical error:

- correct it in the final artifact;
- do not preserve the incorrect wording;
- do not add an error-history section;
- do not annotate what the user used to misunderstand.

## 11. Sources

Add all meaningful external sources to `references.md`.

Cite inside other pages when attribution is important for:

- a disputed or non-obvious claim;
- a formula or convention;
- official framework behavior;
- an interview report;
- a public reference implementation.

Do not treat forum reports as confirmed company policy.

External references remain ordinary web links. Do not copy external pages or binaries into the repository unless the user explicitly requests a local asset and has the right to publish it.

## 12. Formula Requirements

Before delivery:

- verify important equations;
- check dimensions and shapes;
- define symbols;
- keep notation consistent;
- make transposes, reductions, and broadcasting explicit when they matter.

Use MathJax-compatible notation.

```markdown
Given

$$
C = AB,
$$

and upstream gradient $dC$,

$$
dA = dC B^T, \qquad dB = A^T dC.
$$
```

Do not embed screenshots of equations when the equation can be represented as text.

## 13. Code Requirements

Code must be checked before publication.

Choose a verification method appropriate to the problem, such as:

- comparison with PyTorch, NumPy, JAX, or another trusted framework;
- official documentation or implementation;
- a reliable public reference implementation;
- unit and edge-case tests;
- shape, dtype, device, and broadcasting checks;
- autograd comparison;
- finite differences when suitable;
- known examples or mathematical invariants;
- numerical-stability or complexity checks.

Finite differences are not mandatory when another method is more relevant.

Do not claim code was executed if it was only reviewed.

Do not place verification logs or internal verification labels in the final website content.

## 14. Interview Questions

Write prompts in a realistic text-based interview style.

Prefer:

- visible function signature;
- explicit inputs and outputs;
- explicit shapes;
- clear constraints;
- plain-text wording.

Example:

````markdown
## Matrix Multiplication Backward

Implement:

```python
def matmul_backward(dC, A, B):
    ...
```

Inputs:

- `A`: shape `(M, K)`
- `B`: shape `(K, N)`
- `dC`: upstream gradient, shape `(M, N)`

Return:

- `dA`: shape `(M, K)`
- `dB`: shape `(K, N)`

??? answer "Show answer"

    Put the explanation and reference implementation here.
````

A useful answer may include reasoning, derivation, shape analysis, code, common mistakes, and likely follow-ups. Include only the parts that improve the artifact.

## 15. Code Style

Prefer code that is easy to understand in an interview:

- explicit variable names;
- visible shape assumptions;
- concise comments for non-obvious logic;
- minimal dependencies;
- no unnecessary abstractions.

Avoid clever one-liners and production scaffolding around small interview problems.

## 16. Converting Existing PDF or LaTeX

When converting existing material:

1. preserve the actual knowledge and useful personal explanations;
2. remove print-only layout and boilerplate;
3. convert formulas to MathJax-compatible Markdown;
4. convert code to fenced code blocks;
5. follow the user's selected editing mode;
6. correct technical errors;
7. verify formulas and code;
8. check that no important content disappeared;
9. confirm the Markdown renders correctly.

After the user confirms the conversion, the original PDF and LaTeX copies are deleted. Do not keep duplicate versions in an archive unless the user changes this rule.

## 17. Assets

Place supporting files in the topic's `assets/` directory.

```text
assets/computational-graph.svg
assets/gradient-check.py
```

Use relative links from Markdown. Relative links and image paths must remain valid after MkDocs generates `.html` pages for direct local opening.

Do not place duplicate versions of the note in `assets/`.

Prefer text, SVG, or ordinary image files over embedded online widgets. Avoid iframes, scripts, remote notebooks, or interactive components that depend on a running server.

## 18. Offline-Safe Content Rules

The generated website is hosted under the GitHub Pages project path `/ai-ml-interview/`.

Therefore:

- use normal Markdown links and relative local asset paths;
- do not hard-code `http://localhost` URLs;
- do not depend on API calls or the browser Fetch API;
- do not add custom JavaScript to knowledge pages;
- use portable relative links and do not assume server-side application routing;
- do not add analytics, comments, or embedded login-dependent tools;
- keep external references as ordinary links.

If an artifact requires an interactive runtime, provide it as a separate source file or notebook and explain how it is used. Do not make the reading page depend on that runtime.

## 19. Metadata and Navigation

Do not add status, progress, priority, review dates, spaced-repetition fields, or agent verification fields.

List only existing topics and artifacts. Do not create placeholder links for future content.

Use front matter only when the site implementation has a concrete display need for it.

When adding a new topic or page, update the relevant topic or subject index. Do not edit global MkDocs navigation unless the repository's current implementation explicitly requires it and the user authorizes that change.

## 20. Delivery Checklist

Before delivery, confirm:

- [ ] The output is a complete Markdown file.
- [ ] It uses the requested topic and filename.
- [ ] The filename uses lowercase kebab-case.
- [ ] The requested editing mode was followed.
- [ ] Useful personal explanations and notation were preserved.
- [ ] Technical errors were corrected.
- [ ] Important formulas were checked.
- [ ] Code was checked with a suitable method.
- [ ] No false execution claim was made.
- [ ] Sources were recorded appropriately.
- [ ] No duplicate PDF or LaTeX note was created.
- [ ] No unnecessary metadata or workflow feature was added.
- [ ] No unapproved optional page was created.
- [ ] No site-level configuration file was changed without explicit permission.
- [ ] No `site/` build output was committed.
- [ ] Links and assets use portable relative paths.
- [ ] The page does not depend on a local server, API, or custom runtime.
- [ ] Equations, code fences, and collapsible sections are valid.
- [ ] The artifact is ready to place directly into the repository.

## 21. Default Rule

When uncertain, choose the simpler structure. Focus on making the user's knowledge clearer and more correct, not on adding files, metadata, dependencies, or product features.
