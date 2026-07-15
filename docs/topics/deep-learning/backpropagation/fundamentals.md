# Fundamentals

## What backpropagation computes

Let a scalar objective be \(J\). Backpropagation computes derivatives such as \(\partial J / \partial W\) for all trainable parameters. It is reverse-mode automatic differentiation: one reverse traversal efficiently obtains many parameter gradients from one scalar output.

For an operation \(y=f(x)\), the backward pass receives an **upstream gradient**

\[
\frac{\partial J}{\partial y}
\]

and combines it with the operation's local derivative to produce

\[
\frac{\partial J}{\partial x}
=
\frac{\partial J}{\partial y}
\frac{\partial y}{\partial x}.
\]

In tensor code, this combination is often a multiplication, matrix multiplication, reduction, or reshape rather than an explicitly constructed Jacobian.

## Computation graph view

Suppose:

```text
x, W, b -> affine -> z -> ReLU -> a -> loss -> J
```

The forward pass stores values needed by local backward rules. The reverse pass begins with `dJ = 1` and moves right to left. Each node answers a narrow question: given the gradient of the final objective with respect to my output, what are the gradients with respect to each of my inputs?

When a value feeds multiple downstream paths, its total gradient is the **sum** of the contribution from every path. This is why residual connections and shared parameters require gradient accumulation.

## Activations versus parameters

**Activations** are data-dependent values produced while processing an input: layer inputs, pre-activations such as \(z\), and post-activations such as \(a\). In Chinese, activation is usually translated as **激活值**; the activation function is **激活函数**.

**Parameters** are learned values such as weights and biases. Activations change from batch to batch. Parameters persist across batches and are updated by an optimizer using their accumulated gradients.

## Shape-first reasoning

Consider an affine layer in the common machine-learning row-batch convention:

```text
X:  (B, D_in)
W:  (D_out, D_in)
b:  (D_out,)
Y = X @ W.T + b: (B, D_out)
```

If `dY` has shape `(B, D_out)`, each backward result must match its forward variable:

```text
dX: (B, D_in)
dW: (D_out, D_in)
db: (D_out,)
```

Shapes are not a substitute for the derivative, but they catch many transposition and reduction mistakes immediately.

## Why gradients use `dX` notation

In interview code, `dX` is shorthand for the derivative of the final scalar objective with respect to `X`:

\[
dX \equiv \frac{\partial J}{\partial X}.
\]

It does not mean that `X` is differentiated in isolation. Every backward variable implicitly includes the effect of all downstream computation through the upstream gradient.

!!! note "A reliable mental model"
    Backpropagation is vector-Jacobian product propagation. The algorithm applies the incoming gradient to a local derivative without materializing the usually enormous Jacobian.
