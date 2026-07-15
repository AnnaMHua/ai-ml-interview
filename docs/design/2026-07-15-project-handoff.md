# AI/ML Interview Notes Website — Project Handoff

**Date:** 2026-07-15
**Status:** Public GitHub Pages migration approved
**Current phase:** Public site delivery
**Pilot topic:** Backpropagation

## Goal

Maintain a public, read-only AI/ML interview knowledge site. Research and refinement happen elsewhere; polished Markdown is committed to the public repository and deployed automatically through GitHub Pages.

## Approved product boundary

The product organizes artifacts, renders them clearly, and provides navigation and full-site search. Do not add chat, research workflows, tasks, study plans, progress tracking, recommendations, analytics, databases, accounts, or a custom application.

## Delivery

```text
Markdown on main
    -> GitHub Actions tests
    -> strict MkDocs build
    -> GitHub Pages artifact
    -> github-pages deployment
    -> https://annamhua.github.io/ai-ml-interview/
```

Pull requests validate without deploying. Pushes to `main` and manual workflow runs deploy.

## Content contract

Markdown is canonical. Every topic includes `index.md`, `fundamentals.md`, and `references.md`; optional pages exist only when useful. Agents preserve the user's notation and explanations, correct technical mistakes, verify formulas and code, use portable relative links, and follow `AGENT_ARTIFACT_GUIDE.md`.

Because the repository is public, do not add secrets, confidential employer information, private interview material, personal identifiers, copied copyrighted works, or unlicensed assets.

## Website experience

The homepage lists only existing subjects and topics. Topic pages link only to artifacts that exist. MkDocs Material provides the top bar, search, light/dark mode, left navigation, main Markdown content, and the current-page table of contents.

## Backpropagation pilot

The current pilot contains:

```text
index.md
fundamentals.md
derivations.md
interview-questions.md
coding-questions.md
debugging.md
references.md
```

It validates equations, code, collapsible answers, search, project-path routing, and topic organization.

## Repository-owner setup

After the migration commit is pushed:

1. change repository visibility to **Public**;
2. open **Settings → Pages**;
3. set **Build and deployment → Source** to **GitHub Actions**;
4. open **Actions** and run **Build and deploy interview notes** if the visibility change did not automatically trigger a run;
5. verify the live URL shown by the deployment.

## Acceptance criteria

1. The repository is public.
2. Source tests, strict build, and output tests pass.
3. GitHub Pages deploys from `main` through Actions.
4. The public URL loads without authentication.
5. Navigation, search, equations, code, and collapsible answers work online.
6. `site/` is not committed.
7. Future topics can be added without redesign.

## Current limitation

The original Backpropagation PDF/LaTeX source was not attached during implementation. The existing pilot is substantive starter Markdown based on the user's documented notation and interview style, not a claimed exact migration of unattached source files.
