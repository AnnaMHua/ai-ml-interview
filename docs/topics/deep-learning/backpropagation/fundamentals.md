# Fundamentals

## Why We Need Backpropagation

Neural networks are trained with gradient descent or another gradient-based
optimizer. A generic parameter update has the form

\[
\theta \leftarrow \theta-\eta\nabla_{\theta}\mathcal{L},
\]

where $\mathcal{L}$ is the scalar loss and $\eta$ is the learning rate.

Therefore, the main purpose of backpropagation is to efficiently compute

\[
\nabla_{\theta}\mathcal{L}
\]

for every trainable parameter in the network.

Consider one layer:

\[
x_l=f_l(x_{l-1},\theta_l),
\]

where $x_{l-1}$ is the layer input, $x_l$ is the layer output, and
$\theta_l$ denotes the parameters of the layer.

To compute a parameter gradient, backpropagation combines two pieces of
information:

1. the **local behavior** of the current layer;
1. the **upstream gradient**, which contains the effect of all later
   layers and the final loss.

## Machine-Learning and PyTorch Gradient Convention

Throughout this note, we use the common machine-learning and PyTorch
convention:

\[
\boxed{\nabla_z\mathcal{L}\text{ has the same shape as }z.}
\]

For example, if

\[
z\in\mathbb{R}^{n\times 1},
\]

then

\[
\nabla_z\mathcal{L}\in\mathbb{R}^{n\times 1}.
\]

If

\[
W\in\mathbb{R}^{m\times n},
\]

then

\[
\nabla_W\mathcal{L}\in\mathbb{R}^{m\times n}.
\]

For layer $l$, define the upstream gradient as

\[
g_l:=\nabla_{x_l}\mathcal{L}.
\]

Thus, $g_l$ has the same shape as $x_l$.

Under this convention, the vector differential standard form is

\[
\boxed{d\mathcal{L}=(\nabla_x\mathcal{L})^Tdx,}
\]

and the matrix differential standard form is

\[
\boxed{
d\mathcal{L}
=
\operatorname{tr}\!\left((\nabla_W\mathcal{L})^T dW\right).
}
\]

The trace form is the Frobenius inner product

\[
\operatorname{tr}(A^TB)=\sum_{i,j}A_{ij}B_{ij}.
\]

Therefore, it pairs each gradient entry with the corresponding entry of the
small matrix change.

## The Three Objects to Keep Separate

For the layer

\[
x_l=f_l(x_{l-1},\theta_l),
\]

three different objects appear in backpropagation:

\[
\underbrace{A_l:=\frac{\partial x_l}{\partial x_{l-1}}}_{\text{local input Jacobian}},
\qquad
\underbrace{g_l:=\nabla_{x_l}\mathcal{L}}_{\text{upstream gradient}},
\qquad
\underbrace{\nabla_{\theta_l}\mathcal{L}}_{\text{parameter gradient}}.
\]

We also define the local parameter Jacobian

\[
B_l:=\frac{\partial x_l}{\partial\theta_l}.
\]

The local Jacobians $A_l$ and $B_l$ depend only on the operation performed
by the current layer. The upstream gradient $g_l$ contains the effect of the
loss and every later layer. Backpropagation combines them.

For the abstract Jacobian equations, $\theta_l$ may be regarded as the vector
of all parameters in layer $l$. Matrix and tensor parameters can be flattened
conceptually for the derivation, while PyTorch returns the final gradient in the
same shape as the original parameter.

## Where Backpropagation Starts

Suppose the network contains $L$ layers:

\[
x_0\xrightarrow{f_1}x_1\xrightarrow{f_2}x_2
\longrightarrow\cdots\xrightarrow{f_L}x_L\longrightarrow\mathcal{L}.
\]

The final gradient

\[
g_L=\nabla_{x_L}\mathcal{L}
\]

is known directly from the loss function. Starting from $g_L$,
backpropagation computes

\[
g_L\longrightarrow g_{L-1}\longrightarrow g_{L-2}
\longrightarrow\cdots\longrightarrow g_0.
\]

At each layer, the upstream gradient is used to compute both the parameter
gradient and the gradient passed to the previous layer.

## Why We Use Differentials

Directly computing a derivative such as

\[
\frac{\partial x_l}{\partial\theta_l}
\]

may require constructing a very large Jacobian, especially when $x_l$ is a
vector and $\theta_l$ is a matrix or higher-order tensor.

The differential method avoids explicitly building that Jacobian. We:

1. compute the small change in the layer output;
1. substitute it into the small change in the loss;
1. rearrange the result into a standard differential form;
1. read off the gradient.

For a vector $x$,

\[
d\mathcal{L}=(\nabla_x\mathcal{L})^Tdx.
\]

For a matrix $W$,

\[
d\mathcal{L}
=
\operatorname{tr}\!\left((\nabla_W\mathcal{L})^TdW\right).
\]

Both forms express the same idea:

\[
\text{loss change}=\text{gradient inner product variable change}.
\]

## Deriving the General Backpropagation Equations

Consider one layer:

\[
x_l=f_l(x_{l-1},\theta_l).
\]

The output depends on both the layer input and the layer parameters. Therefore,
its differential is

\[
dx_l=A_l\,dx_{l-1}+B_l\,d\theta_l,
\]

where

\[
A_l:=\frac{\partial x_l}{\partial x_{l-1}},
\qquad
B_l:=\frac{\partial x_l}{\partial\theta_l}.
\]

Because

\[
g_l=\nabla_{x_l}\mathcal{L},
\]

the differential of the loss is

\[
d\mathcal{L}=g_l^Tdx_l.
\]

Substitute the layer differential:

\[
\begin{aligned}
d\mathcal{L}
&=g_l^T\left(A_l\,dx_{l-1}+B_l\,d\theta_l\right)\\
&=g_l^TA_l\,dx_{l-1}+g_l^TB_l\,d\theta_l.
\end{aligned}
\]

Using

\[
a^TB=(B^Ta)^T,
\]

we obtain

\[
d\mathcal{L}
=(A_l^Tg_l)^Tdx_{l-1}+(B_l^Tg_l)^Td\theta_l.
\]

The standard differential form for a scalar loss depending on
$x_{l-1}$ and $\theta_l$ is

\[
d\mathcal{L}
=(\nabla_{x_{l-1}}\mathcal{L})^Tdx_{l-1}
+(\nabla_{\theta_l}\mathcal{L})^Td\theta_l.
\]

Comparing the coefficients of $dx_{l-1}$ and $d\theta_l$ gives

\[
\nabla_{x_{l-1}}\mathcal{L}=A_l^Tg_l
\]

and

\[
\nabla_{\theta_l}\mathcal{L}=B_l^Tg_l.
\]

Since

\[
g_{l-1}:=\nabla_{x_{l-1}}\mathcal{L},
\]

the general backpropagation equations are

\[
\boxed{
g_{l-1}
=
A_l^Tg_l
=
\left(\frac{\partial x_l}{\partial x_{l-1}}\right)^Tg_l
}
\]

and

\[
\boxed{
\nabla_{\theta_l}\mathcal{L}
=
B_l^Tg_l
=
\left(\frac{\partial x_l}{\partial\theta_l}\right)^Tg_l.
}
\]

The first equation propagates the gradient to the previous layer. The second
computes the gradient of the current layer parameters.

In words:

\[
\boxed{
\text{input gradient}
=
\text{local input Jacobian}^T\times\text{upstream gradient}
}
\]

and

\[
\boxed{
\text{parameter gradient}
=
\text{local parameter Jacobian}^T\times\text{upstream gradient}.
}
\]

## How the General Rule Relates to a Concrete Layer

The general equations describe the structure of backward propagation, but they
do not automatically provide the most convenient implementation for every
operation. For a concrete layer, we must evaluate the required
Jacobian-transpose–gradient products.

For a simple variable such as a vector input, the local Jacobian may be easy to
write explicitly. For a matrix or tensor parameter, its full Jacobian can be
large and inconvenient. A layer-specific differential derivation computes the
same product directly without materializing that Jacobian.

Therefore, deriving the linear-layer backward equations below is not deriving
backpropagation a second time. It is evaluating the general backpropagation rule
for the specific operation $y=Wx+b$.

## Example: A Linear Layer

Consider

\[
y=Wx+b,
\]

with

\[
x\in\mathbb{R}^{n\times 1},\qquad
W\in\mathbb{R}^{m\times n},\qquad
b\in\mathbb{R}^{m\times 1},\qquad
y\in\mathbb{R}^{m\times 1}.
\]

Let the upstream gradient be

\[
g_y:=\nabla_y\mathcal{L}\in\mathbb{R}^{m\times 1}.
\]

The differential of the layer is

\[
dy=dW\,x+W\,dx+db.
\]

Because $\mathcal{L}$ is scalar,

\[
d\mathcal{L}=g_y^Tdy.
\]

Substitute $dy$:

\[
d\mathcal{L}=g_y^TdW\,x+g_y^TW\,dx+g_y^Tdb.
\]

### Gradient with Respect to the Input

The term involving $dx$ is

\[
g_y^TW\,dx=(W^Tg_y)^Tdx.
\]

Comparing with

\[
d\mathcal{L}=(\nabla_x\mathcal{L})^Tdx,
\]

we get

\[
\boxed{\nabla_x\mathcal{L}=W^Tg_y.}
\]

This is also obtained immediately from the general equation because

\[
\frac{\partial y}{\partial x}=W.
\]

### Gradient with Respect to the Weights

The term involving $dW$ is

\[
g_y^TdW\,x.
\]

Because it is scalar,

\[
g_y^TdW\,x
=
\operatorname{tr}(g_y^TdW\,x).
\]

Using the cyclic property of the trace,

\[
\operatorname{tr}(ABC)=\operatorname{tr}(BCA)=\operatorname{tr}(CAB),
\]

we obtain

\[
\operatorname{tr}(g_y^TdW\,x)
=
\operatorname{tr}(xg_y^TdW).
\]

Since

\[
xg_y^T=(g_yx^T)^T,
\]

we have

\[
d\mathcal{L}
=
\operatorname{tr}\!\left((g_yx^T)^TdW\right).
\]

Comparing with

\[
d\mathcal{L}
=
\operatorname{tr}\!\left((\nabla_W\mathcal{L})^TdW\right),
\]

we get

\[
\boxed{\nabla_W\mathcal{L}=g_yx^T.}
\]

The shape is

\[
(m\times 1)(1\times n)=m\times n,
\]

which matches the shape of $W$.

The differential method has directly evaluated the abstract quantity

\[
\left(\frac{\partial y}{\partial W}\right)^Tg_y
\]

without constructing the large Jacobian $\partial y/\partial W$.

### Gradient with Respect to the Bias

The term involving $db$ is

\[
g_y^Tdb.
\]

Comparing with

\[
d\mathcal{L}=(\nabla_b\mathcal{L})^Tdb,
\]

we get

\[
\boxed{\nabla_b\mathcal{L}=g_y.}
\]

This also agrees with the general equation because

\[
\frac{\partial y}{\partial b}=I.
\]

Therefore, for the linear layer

\[
y=Wx+b,
\]

the backward equations are

\[
\boxed{
\nabla_x\mathcal{L}=W^Tg_y,
\qquad
\nabla_W\mathcal{L}=g_yx^T,
\qquad
\nabla_b\mathcal{L}=g_y.
}
\]

## Coding-Interview Notation Conventions

Coding questions often use names such as `dA`, `dC`,
`dX`, and `dW`. In this programming context, the prefix
`d` usually means “gradient of the scalar loss with respect to this
variable”:

\[
\mathtt{dA}\equiv \nabla_A\mathcal{L}
=\frac{\partial\mathcal{L}}{\partial A},
\qquad
\mathtt{dC}\equiv \nabla_C\mathcal{L}.
\]

This is different from the differential notation used earlier in the note,
where $dA$ means a small perturbation of $A$. The same symbol is commonly
used in both contexts. In mathematical derivations below, we use $G_A$ and
$G_C$ for gradients when that avoids ambiguity, while interview code keeps
the conventional variable names `dA` and `dC`.

The most common coding symbols are:

- `@`: matrix multiplication in NumPy and PyTorch;
- `.T`: transpose for the two-dimensional matrices used here;
- `shape (M, K)`: a matrix with $M$ rows and $K$ columns;
- `sum(axis=0)`: sum over the rows, while retaining one value
   for each column;
- `dOutput`: the upstream gradient, with the same shape as the
   corresponding forward output.

For tensors with more than two dimensions, PyTorch code often uses
`transpose(-1, -2)` instead of `.T` to swap only the final two
axes.

### Matrix Multiplication Backward

A coding prompt may be written as follows:

```text
Given:

A: shape (M, K)
B: shape (K, N)
C = A @ B: shape (M, N)

Given upstream gradient dC of shape (M, N), compute and return:

dA = dC @ B.T: shape (M, K)
dB = A.T @ dC: shape (K, N)
```

Here, `dC` means

\[
G_C:=\nabla_C\mathcal{L},
\]

not a small change in $C$. Since

\[
C=AB,
\]

the differential is

\[
dC=dA\,B+A\,dB.
\]

Substituting into the loss differential gives

\[
\begin{aligned}
d\mathcal{L}
&=\operatorname{tr}(G_C^T dC)\\
&=\operatorname{tr}(G_C^T dA\,B)
 +\operatorname{tr}(G_C^T A\,dB)\\
&=\operatorname{tr}\!\left((G_CB^T)^T dA\right)
 +\operatorname{tr}\!\left((A^TG_C)^T dB\right).
\end{aligned}
\]

Therefore,

\[
\boxed{\nabla_A\mathcal{L}=G_CB^T}
\qquad\text{and}\qquad
\boxed{\nabla_B\mathcal{L}=A^TG_C.}
\]

In coding notation, these become

```python
dA = dC @ B.T
dB = A.T @ dC
```

The shapes verify the multiplication order:

\[
(M\times N)(N\times K)=M\times K
\]

for `dA`, and

\[
(K\times M)(M\times N)=K\times N
\]

for `dB`.

### Batched Linear-Layer Backward

In practical ML code, examples are commonly stored as rows. Let $B$ denote
the batch size, $D_{\mathrm{in}}$ the input dimension, and
$D_{\mathrm{out}}$ the output dimension. The forward operation is

```text
X: shape (B, D_in)
W: shape (D_out, D_in)
b: shape (D_out,)

Y = X @ W.T + b: shape (B, D_out)
```

Given the upstream gradient

```text
dY: shape (B, D_out)
```

the backward pass is

```python
dX = dY @ W
dW = dY.T @ X
db = dY.sum(axis=0)
```

Using mathematical gradient notation, the equations are

\[
\boxed{\nabla_X\mathcal{L}=G_YW,}
\]

\[
\boxed{\nabla_W\mathcal{L}=G_Y^TX,}
\]

and

\[
\boxed{
\nabla_b\mathcal{L}
=\sum_{i=1}^{B}G_{Y,i,:}.
}
\]

The shape of the input gradient is

\[
(B\times D_{\mathrm{out}})
(D_{\mathrm{out}}\times D_{\mathrm{in}})
=
B\times D_{\mathrm{in}},
\]

so `dX` has the same shape as `X`.

For the weight gradient,

\[
(D_{\mathrm{out}}\times B)
(B\times D_{\mathrm{in}})
=
D_{\mathrm{out}}\times D_{\mathrm{in}},
\]

so `dW` has the same shape as `W`. Each training example
contributes an outer product between its output gradient and its input:

\[
\nabla_W\mathcal{L}
=
\sum_{i=1}^{B}G_{Y,i,:}^{T}X_{i,:}.
\]

The matrix multiplication $G_Y^TX$ computes this entire sum at once.

The bias $b$ is broadcast to every row of the batch during the forward pass.
Consequently, every example contributes to the same bias parameter, and the
backward pass sums those contributions over the batch axis:

\[
\mathtt{db = dY.sum(axis=0)}.
\]

No additional division by the batch size should be inserted automatically. A
factor of $1/B$ appears only if it is introduced by a mean-reduced loss, and
in that case it is already contained in the upstream gradient $G_Y$.

## Summary

Backpropagation is needed because gradient-based optimizers require the
gradient of the loss with respect to every trainable parameter.

For each layer, backpropagation combines local Jacobians with an upstream
gradient. The recursion begins at the final layer, where the gradient is known
directly from the loss function.

Using the notation

\[
A_l:=\frac{\partial x_l}{\partial x_{l-1}},
\qquad
B_l:=\frac{\partial x_l}{\partial\theta_l},
\qquad
g_l:=\nabla_{x_l}\mathcal{L},
\]

the general equations are

\[
\boxed{g_{l-1}=A_l^Tg_l}
\]

and

\[
\boxed{\nabla_{\theta_l}\mathcal{L}=B_l^Tg_l.}
\]

The differential method avoids explicitly constructing large Jacobians. We
compute $d\mathcal{L}$, rearrange it into a standard form, and read off the
gradient.

Under the machine-learning and PyTorch convention, every gradient has the same
shape as the variable with respect to which it is computed.

## Reference

Antonio Torralba, Phillip Isola, and William Freeman,
*Foundations of Computer Vision*, Chapter 14, “Backpropagation,”
MIT Vision Book:
<https://visionbook.mit.edu/backpropagation.html>.
