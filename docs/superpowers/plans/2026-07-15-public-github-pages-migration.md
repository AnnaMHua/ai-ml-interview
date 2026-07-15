# Public GitHub Pages Migration Plan

**Goal:** Replace private downloadable-site delivery with a public GitHub Pages site at `https://annamhua.github.io/ai-ml-interview/`.

**Architecture:** Markdown remains canonical and MkDocs Material remains the renderer. A push to `main` validates and builds `site/`, uploads a Pages-compatible artifact, and deploys it through the protected `github-pages` environment. Pull requests build and test without deploying.

## Task 1: Change the repository and site contracts

- Update source tests to require `site_url`, normal web routing, and no offline plugin.
- Require GitHub Pages permissions, environment metadata, official configure/upload/deploy actions, and concurrency.
- Remove assertions and documentation tied to a downloadable local ZIP.
- Run the tests and confirm they fail against the old implementation.

## Task 2: Implement online MkDocs configuration

- Set the canonical site URL and repository links.
- Remove `offline` and `use_directory_urls: false`.
- Keep search, MathJax, navigation, highlighting, light/dark mode, and content exclusions.
- Update generated-output tests for directory-style web URLs and base-path-safe links.

## Task 3: Implement the official Pages workflow

- Keep validation for pull requests, `main`, and manual runs.
- Grant only `contents: read`, `pages: write`, and `id-token: write`.
- Build and test in one job, then upload the Pages artifact only for non-PR runs.
- Deploy in a dependent job using the `github-pages` environment and expose the deployment URL.
- Use current official action majors: checkout v6, setup-python v6, configure-pages v5, upload-pages-artifact v5, and deploy-pages v5.

## Task 4: Update public-product documentation

- Rewrite README reading instructions around the live Pages URL.
- Update the product design, repository/Actions design, project handoff, and agent guide so privacy and offline-ZIP claims are removed.
- State clearly that repository source and generated site are public.
- Preserve Markdown content rules and the Backpropagation pilot.

## Task 5: Verify and publish

- Run source tests, strict clean build, output tests, link checks, and `git diff --check`.
- Commit the migration locally.
- Publish the complete tree as a fast-forward commit on remote `main`.
- Read back the workflow and MkDocs configuration from GitHub.
- Ask the user to change repository visibility to Public and select GitHub Actions as the Pages source because the connector does not expose repository settings.
