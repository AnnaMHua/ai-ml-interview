# Derivations

## Matrix multiplication

Given

```text
A: (M, K)
B: (K, N)
C = A @ B: (M, N)
dC: (M, N)
```

use the differential

\[
dC = dA\,B + A\,dB.
\]

For scalar \(J\), write

\[
dJ = \operatorname{tr}\!\left((\nabla_C J)^T dC\right).
\]

Substitute `dC`, cycle trace factors until `dA` or `dB` is last, and match coefficients:

\[
\nabla_A J = (\nabla_C J)B^T,
\qquad
\nabla_B J = A^T(\nabla_C J).
\]

In interview notation:

```text
dA = dC @ B.T     # (M, K)
dB = A.T @ dC     # (K, N)
```

## Affine layer

Using the row-batch convention:

```text
X: (B, D_in)
W: (D_out, D_in)
b: (D_out,)
Y = X @ W.T + b
dY: (B, D_out)
```

Treat `X @ W.T` as matrix multiplication and remember that the bias was broadcast across the batch:

```text
dX = dY @ W              # (B, D_in)
dW = dY.T @ X            # (D_out, D_in)
db = dY.sum(axis=0)       # (D_out,)
```

The bias gradient is a sum because each row of `Y` depends on the same `b`. More generally, undo broadcasting by summing over every axis that was added or expanded in the forward pass.

## Elementwise activation

For \(a=f(z)\), the local Jacobian is diagonal, so the vector-Jacobian product becomes elementwise multiplication:

\[
dZ = dA \odot f'(Z).
\]

For ReLU:

```text
dZ = dA * (Z > 0)
```

At exactly zero, ReLU is not differentiable. Frameworks choose a subgradient convention, commonly zero. State the convention if an interview question depends on that edge case.

For sigmoid \(S=\sigma(Z)\), reuse the forward output:

\[
dZ = dS \odot S \odot (1-S).
\]

## Softmax with cross-entropy

For one example with logits \(z\), probabilities \(p=\operatorname{softmax}(z)\), and one-hot target \(y\):

\[
L=-\sum_i y_i\log p_i.
\]

Although the softmax Jacobian contains diagonal and cross-class terms, combining it with cross-entropy simplifies to

\[
\frac{\partial L}{\partial z}=p-y.
\]

For a mean-reduced batch loss of size \(B\):

```text
dLogits = (probs - one_hot_targets) / B
```

Do not divide by `B` when the loss uses a sum reduction. Backward scaling must match the exact forward reduction.

## Branches and accumulation

If \(x\) affects \(J\) through two branches, \(u=f(x)\) and \(v=g(x)\), then

\[
\frac{\partial J}{\partial x}
=
\frac{\partial J}{\partial u}\frac{\partial u}{\partial x}
+
\frac{\partial J}{\partial v}\frac{\partial v}{\partial x}.
\]

Autograd engines implement this by accumulating contributions into the same gradient buffer. Overwriting instead of accumulating is a classic bug in a hand-built computation graph.
