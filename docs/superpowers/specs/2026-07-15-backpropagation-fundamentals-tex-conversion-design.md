# Backpropagation Fundamentals LaTeX Conversion Design

**Date:** 2026-07-15
**Status:** Approved for specification review

## Goal

Replace `docs/topics/deep-learning/backpropagation/fundamentals.md` with the complete content of `backpropagation_matrix_form_with_coding_notation.tex`, converted into the repository's MkDocs Markdown format.

## Content fidelity

The conversion preserves the source document's instructional content, section order, equations, examples, coding notation, shapes, summary, and reference. It does not deduplicate material that also appears on other topic pages and does not editorially rewrite the source.

Only format-specific transformations are allowed:

- remove the LaTeX document preamble and document wrapper;
- use `# Fundamentals` as the page title;
- convert `\section` and `\subsection` to Markdown headings;
- convert LaTeX lists to Markdown lists;
- convert `verbatim` blocks to fenced code blocks;
- convert `\textbf`, `\texttt`, quotation syntax, and the reference URL to Markdown equivalents;
- retain MathJax-compatible inline and display mathematics, including aligned and boxed equations;
- make only mechanical whitespace changes required for valid Markdown rendering.

## Repository integration

The converted page replaces the current Fundamentals page at its existing path, so MkDocs navigation and public URLs do not change. The original uploaded `.tex` file is an input only and is not added to the public repository.

## Validation

Before replacing the page, add a repository contract test that requires the converted page to contain:

- every top-level source section;
- the general input-gradient and parameter-gradient equations;
- the single-example linear-layer gradients;
- matrix-multiplication interview notation;
- batched linear-layer interview notation;
- the warning that mean-loss scaling must already be present in the upstream gradient;
- the source reference.

The test must fail against the current page before conversion and pass afterward. The full repository tests, strict MkDocs build, rendered-site tests, and whitespace checks must pass before publication to `main`.

## Non-goals

- Reorganizing or shortening the source
- Moving derivations to another page
- Removing duplication across topic pages
- Changing mathematical conventions
- Adding new explanations or examples
