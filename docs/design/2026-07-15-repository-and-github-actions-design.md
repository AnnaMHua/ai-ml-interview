# AI/ML Interview Notes — Repository and GitHub Actions Design

**Date:** 2026-07-15
**Status:** Approved, revised for public GitHub Pages
**Scope:** Static-site build, validation, and public deployment

## Goal

Build Markdown interview notes with MkDocs Material and deploy them to:

```text
https://annamhua.github.io/ai-ml-interview/
```

## Architecture

```text
public GitHub repository
    -> Markdown and MkDocs configuration
    -> GitHub Actions strict build
    -> Pages-compatible artifact
    -> protected github-pages deployment
    -> public website
```

## Repository layout

```text
ai-ml-interview/
├── .github/workflows/build-site.yml
├── docs/
│   ├── index.md
│   ├── stylesheets/extra.css
│   ├── javascripts/mathjax.js
│   └── topics/
├── tests/
├── mkdocs.yml
├── requirements.txt
├── README.md
├── AGENT_ARTIFACT_GUIDE.md
└── .gitignore
```

Generated `site/` output is ignored and never committed.

## MkDocs configuration

`mkdocs.yml` defines the canonical `site_url`, GitHub repository link, Material theme, normal directory-style URLs, search, MathJax, syntax highlighting, admonitions, collapsible details, navigation, and local CSS/JavaScript.

Project design records and implementation plans remain in the repository but are excluded from the reader site and search index.

## Dependencies

Python dependencies are exactly pinned in `requirements.txt`. The same dependency file is used locally and in Actions. Do not add Node.js, Docker, or a second static-site tool without a demonstrated need.

## Workflow

`.github/workflows/build-site.yml` runs on pull requests, pushes to `main`, and manual dispatch.

Global minimum permissions:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

Concurrency uses the `pages` group and does not cancel an in-progress production deployment.

### Build job

All events:

```text
checkout
    -> set up Python with pip cache
    -> install pinned dependencies
    -> run repository contract tests
    -> mkdocs build --strict --clean
    -> verify site/index.html
    -> run generated-site tests
```

For non-pull-request events, the build job also runs `actions/configure-pages` and uploads `site/` with `actions/upload-pages-artifact`.

### Deploy job

Pushes to `main` and manual runs execute a dependent deployment job. It uses the `github-pages` environment, publishes with `actions/deploy-pages`, and records the resulting `page_url`. Pull requests never deploy.

## Failure behavior

The workflow fails when dependencies cannot install, configuration is invalid, strict mode emits a build warning, navigation targets are missing, required generated files are absent, output links do not resolve, or Pages upload/deployment fails. A failed build does not replace the last successful deployment.

## Testing

Run:

```bash
python -m unittest tests.test_repository_contract -v
mkdocs build --strict --clean
python -m unittest tests.test_site_output -v
```

Output tests verify generated assets, project-base routing, local link resolution, equations, code highlighting, and collapsible answers. After the first deployment, manually smoke-test the live URL in a modern browser, including search, navigation, light/dark mode, equations, and internal links.

## Security and publication

- The repository and site are public.
- No secrets are required.
- Only the standard Pages OIDC deployment permissions are granted.
- No generated HTML is committed.
- Public-content review is required before adding notes or assets.

## Repository settings

The repository owner must set visibility to **Public** and choose **GitHub Actions** as the Pages build source. These settings are intentionally outside the workflow source.

## Acceptance criteria

1. Strict build and both test suites pass.
2. Pull requests validate without deploying.
3. `main` and manual runs deploy to GitHub Pages.
4. The deployment uses the `github-pages` environment.
5. The live project URL serves the generated homepage and topic pages.
6. Search and internal navigation work under `/ai-ml-interview/`.
7. `site/` remains ignored.

## References

- https://docs.github.com/pages
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://www.mkdocs.org/user-guide/configuration/
- https://squidfunk.github.io/mkdocs-material/
