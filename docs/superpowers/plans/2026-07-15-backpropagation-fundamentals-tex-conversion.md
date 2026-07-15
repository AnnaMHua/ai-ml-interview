# Backpropagation Fundamentals LaTeX Conversion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Replace the Backpropagation Fundamentals page with a faithful MkDocs Markdown conversion of the complete supplied LaTeX note.

**Architecture:** The uploaded LaTeX document is a one-time source input. A repository contract test locks down its sections, core equations, coding notation, scaling warning, and reference; the maintained output remains a single Markdown page at the existing navigation path.

**Tech Stack:** Python 3.12 unittest, MkDocs Material, PyMdown Extensions, MathJax 3

## Global Constraints

- Preserve the source document's instructional content, section order, equations, examples, coding notation, shapes, summary, and reference.
- Do not deduplicate or editorially rewrite content.
- Remove only LaTeX document scaffolding and convert presentation syntax to Markdown/MathJax.
- Keep the existing public URL and navigation target.
- Do not add the uploaded .tex file to the repository.

---

### Task 1: Add the Fundamentals content contract

**Files:**
- Modify: tests/test_repository_contract.py
- Test: tests/test_repository_contract.py

**Interfaces:**
- Consumes: RepositoryContractTests.read(relative_path: str) -> str
- Produces: RepositoryContractTests.test_fundamentals_preserves_complete_matrix_form_note()

- [ ] **Step 1: Write the failing test**

Add this method to RepositoryContractTests:

~~~python
def test_fundamentals_preserves_complete_matrix_form_note(self) -> None:
    fundamentals = self.read(
        "docs/topics/deep-learning/backpropagation/fundamentals.md"
    )
    required_sections = [
        "## Why We Need Backpropagation",
        "## Machine-Learning and PyTorch Gradient Convention",
        "## The Three Objects to Keep Separate",
        "## Where Backpropagation Starts",
        "## Why We Use Differentials",
        "## Deriving the General Backpropagation Equations",
        "## How the General Rule Relates to a Concrete Layer",
        "## Example: A Linear Layer",
        "## Coding-Interview Notation Conventions",
        "## Summary",
        "## Reference",
    ]
    for heading in required_sections:
        with self.subTest(heading=heading):
            self.assertIn(heading, fundamentals)

    required_content = [
        r"g_{l-1}=A_l^Tg_l",
        r"\nabla_{\theta_l}\mathcal{L}=B_l^Tg_l",
        r"\nabla_W\mathcal{L}=g_yx^T",
        "dA = dC @ B.T",
        "dB = A.T @ dC",
        "dX = dY @ W",
        "dW = dY.T @ X",
        "db = dY.sum(axis=0)",
        "already contained in the upstream gradient",
        "https://visionbook.mit.edu/backpropagation.html",
    ]
    for fragment in required_content:
        with self.subTest(fragment=fragment):
            self.assertIn(fragment, fundamentals)
~~~

- [ ] **Step 2: Run the focused test and verify RED**

Run:

~~~bash
python -m unittest \
  tests.test_repository_contract.RepositoryContractTests.test_fundamentals_preserves_complete_matrix_form_note \
  -v
~~~

Expected: FAIL because the existing short Fundamentals page lacks the first required source heading.

- [ ] **Step 3: Commit the failing contract test**

~~~bash
git add tests/test_repository_contract.py
git commit -m "test: require complete backpropagation fundamentals note"
~~~

### Task 2: Convert the complete LaTeX note to MkDocs Markdown

**Files:**
- Source input: ../upload/backpropagation_matrix_form_with_coding_notation.tex
- Modify: docs/topics/deep-learning/backpropagation/fundamentals.md
- Test: tests/test_repository_contract.py
- Test: tests/test_site_output.py

**Interfaces:**
- Consumes: the complete source input and the content contract from Task 1
- Produces: the public MkDocs page at topics/deep-learning/backpropagation/fundamentals/

- [ ] **Step 1: Replace the existing page with the complete converted source**

Perform these transformations over the entire source, without changing its prose, order, equations, code, or reference:

~~~text
Discard:
  \documentclass, \usepackage, \title, \author, \date,
  \begin{document}, \maketitle, \end{document}

Replace:
  document title                         -> # Fundamentals
  \section{Title}                        -> ## Title
  \subsection{Title}                     -> ### Title
  enumerate/itemize + each \item         -> Markdown numbered/bulleted lists
  \begin{verbatim}...\end{verbatim}      -> fenced text code block
  \textbf{value}                         -> Markdown bold
  \texttt{value}                         -> Markdown inline code
  LaTeX quotation syntax                 -> typographic quotation marks
  \emph{value}                           -> Markdown emphasis
  \url{URL}                              -> Markdown autolink
  \text{ prose inside mathematics }      -> retain as MathJax \text{...}
  \[...\]                                -> $$...$$
  \(...\)                                -> $...$

Retain inside MathJax:
  aligned environments, \boxed, \bm, \nabla, \partial, \operatorname,
  \underbrace, \qquad, matrices, dimensions, subscripts, and superscripts
~~~

Use text fences for shape/pseudocode prompts and python fences for executable interview formulas. Preserve every source section from “Why We Need Backpropagation” through “Reference”.

- [ ] **Step 2: Run the focused test and verify GREEN**

Run:

~~~bash
python -m unittest \
  tests.test_repository_contract.RepositoryContractTests.test_fundamentals_preserves_complete_matrix_form_note \
  -v
~~~

Expected: PASS.

- [ ] **Step 3: Run the full verification suite**

Run:

~~~bash
set -e
python -m unittest tests.test_repository_contract -v
PYTHONPATH="$PWD/.venv/lib/python3.12/site-packages" \
  python -m mkdocs build --strict --clean
python -m unittest tests.test_site_output -v
test -f site/topics/deep-learning/backpropagation/fundamentals/index.html
git check-ignore -q site/index.html
git diff --check
~~~

Expected: all repository and rendered-output tests pass; strict build and shell checks exit zero.

- [ ] **Step 4: Inspect the rendered page for source fidelity**

Run:

~~~bash
rg -n \
  'Why We Need Backpropagation|Machine-Learning and PyTorch|Example: A Linear Layer|Coding-Interview Notation|Summary|visionbook' \
  site/topics/deep-learning/backpropagation/fundamentals/index.html
~~~

Expected: matches for every named source section and the reference.

- [ ] **Step 5: Commit the converted page**

~~~bash
git add docs/topics/deep-learning/backpropagation/fundamentals.md
git commit -m "docs: expand backpropagation fundamentals"
~~~

- [ ] **Step 6: Publish the commits**

Publish the resulting tree to AnnaMHua/ai-ml-interview on main as a fast-forward commit through the connected GitHub app. Read back the committed Fundamentals file and the remote head SHA before reporting completion.
