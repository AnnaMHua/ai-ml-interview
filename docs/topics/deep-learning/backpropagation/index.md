# Backpropagation

Backpropagation computes gradients efficiently by traversing a computation graph in reverse and repeatedly applying the chain rule. The key interview skill is not memorizing isolated formulas; it is tracking the upstream gradient, local derivative, tensor shapes, and all paths through which a value affects the loss.

## Artifacts

- [Fundamentals](fundamentals.md) — computation graphs, upstream gradients, activations, parameters, and shape rules.
- [Derivations](derivations.md) — matrix multiplication, affine layers, activations, and softmax with cross-entropy.
- [Interview Questions](interview-questions.md) — conceptual prompts with collapsible answers.
- [Coding Questions](coding-questions.md) — NumPy-style backward implementations and shape contracts.
- [Debugging](debugging.md) — finite differences, common bugs, and a practical checklist.
- [References](references.md) — books, framework documentation, and verification sources.

## Default reasoning pattern

For every operation, write the forward equation and shapes first. Name the incoming derivative `dOutput`, derive each local contribution, reduce any broadcast dimensions, and verify that every returned gradient has exactly the same shape as its corresponding forward input.
