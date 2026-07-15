# References

These sources support the mathematical conventions, automatic-differentiation model, and implementation behavior used throughout this topic. The notes remain written in the user's shape-first interview style rather than reproducing source text.

## Primary learning references

- [MIT Vision Book — Backpropagation](https://visionbook.mit.edu/backpropagation.html) — computation graphs, derivatives, and a visual explanation of reverse propagation.
- [Deep Learning, Chapter 6](https://www.deeplearningbook.org/contents/mlp.html) by Goodfellow, Bengio, and Courville — feedforward networks and backpropagation.
- [The Matrix Cookbook](https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf) — compact matrix derivative identities and notation.

## Framework and verification references

- [PyTorch autograd mechanics](https://docs.pytorch.org/docs/stable/notes/autograd.html) — reverse-mode graph construction, saved tensors, non-differentiable functions, and gradient behavior.
- [PyTorch `gradcheck`](https://docs.pytorch.org/docs/stable/generated/torch.autograd.gradcheck.html) — finite-difference checking and important limitations near non-differentiable points.
- [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) — the forward broadcasting rules whose backward pass requires reductions.

## Conventions used here

Matrices represent batches by rows. A PyTorch-style affine layer is written `Y = X @ W.T + b`, with `W` shaped `(D_out, D_in)`. Symbols such as `dX` mean the derivative of the final scalar objective with respect to `X`, not merely the local derivative of the immediately following operation.
