# AI/ML Interview Notes Website — Product Design

**Date:** 2026-07-15
**Status:** Approved design, revised for public GitHub Pages delivery
**Audience:** Personal study; publicly readable

## Product

A simple, read-only website for reviewing personal AI/ML interview knowledge at:

```text
https://annamhua.github.io/ai-ml-interview/
```

Preparation happens outside the site:

```text
research and discussion
    -> polished Markdown artifacts
    -> public GitHub repository
    -> GitHub Actions validation and build
    -> GitHub Pages deployment
    -> read and search online
```

The site organizes, searches, and displays finished artifacts. It is not a research assistant, study tracker, or content-management application.

## Product principles

- Optimize for reading and refreshing knowledge.
- Use Markdown as the only maintained knowledge format.
- Preserve the user's explanations, notation, and mental models.
- Verify formulas and code before publication.
- Keep the build system smaller than the content system.
- Treat all committed source and rendered content as public.
- Add features only when they improve reading, correctness, or reliable delivery.

## Included

- Public GitHub repository
- Public GitHub Pages website
- Homepage showing subjects and existing topics
- Topic landing pages and Markdown content pages
- Full-site search
- MathJax equations
- Syntax-highlighted code
- Images and tables
- Collapsible interview answers
- Left navigation and page table of contents
- Light and dark modes
- Strict GitHub Actions build validation
- Automatic deployment from `main`

## Not included

- Embedded AI chat or research workflow
- Tasks, schedules, progress, priority, or analytics
- Database, accounts, or private content
- Custom React, Vue, or backend application
- Automatic scraping or content generation
- A committed generated `site/` directory
- A separate downloadable offline distribution

## Information architecture

The homepage lists only subjects and topics that contain real content. A topic landing page links only to artifacts that exist.

Every topic requires:

```text
index.md
fundamentals.md
references.md
```

Optional artifacts such as `derivations.md`, `interview-questions.md`, `coding-questions.md`, and `debugging.md` are created only when they contain useful independent material. Empty pages and future-topic placeholders are prohibited.

## Technology

Use MkDocs Material with ordinary web routing and the built-in search plugin. Configure the canonical project URL so generated links work below `/ai-ml-interview/`. Keep MathJax, code highlighting, admonitions, collapsible details, navigation, and color palettes.

Do not use the Material offline plugin. GitHub Pages, rather than a local `file://` bundle, is the supported reading environment.

## Canonical content format

Markdown is the only maintained knowledge format. It may contain prose, MathJax-compatible equations, fenced code, tables, images, links, and collapsible answers. Standalone source, notebooks, and assets remain separate only when Markdown cannot replace them.

Existing PDF or LaTeX notes are converted to Markdown, verified, and removed after the user confirms the conversion. Do not maintain duplicate note formats.

## Public-content rule

All repository files and rendered knowledge are public. Do not commit secrets, employer-confidential material, private interview reports, personal identifiers, copyrighted source copies, or assets the user does not have the right to publish. External sources remain attributed links.

## Agent boundary

Agents may create a complete topic or update one artifact. They preserve the user's style, correct technical errors, verify important formulas and code, record meaningful sources, and follow `AGENT_ARTIFACT_GUIDE.md`.

Site configuration, dependencies, workflows, and shared styles change only when the user explicitly requests a site-level change.

## Pilot topic

Backpropagation is the first complete topic and demonstrates fundamentals, derivations, interview questions, coding questions, debugging, references, equations, code, search, and navigation.

## Acceptance criteria

1. The repository is public.
2. The site is available at the configured GitHub Pages URL.
3. Pull requests run strict build and output validation without deploying.
4. Pushes to `main` and manual runs deploy through the `github-pages` environment.
5. Search, equations, code, navigation, collapsible answers, and color modes work online.
6. Markdown remains the sole maintained knowledge format.
7. `site/` is generated and never committed.
8. Backpropagation is complete enough to validate the content model.
9. A second topic can be added without redesign.

## Default rule

Prefer the simpler structure unless an addition clearly improves reading, correctness, or reliable public delivery.
