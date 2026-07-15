# Coding Questions

The prompt style here is intentionally plain-text and shape-first, matching what is practical in a coding interview. Assume NumPy arrays and a scalar objective downstream of the provided upstream gradient.

## Matrix multiplication backward

Given:

```text
A: shape (M, K)
B: shape (K, N)
C = A @ B: shape (M, N)
```

Given upstream gradient `dC` of shape `(M, N)`, compute and return:

```text
dA = dC @ B.T: shape (M, K)
dB = A.T @ dC: shape (K, N)
```

```python
def matmul_backward(dC, A, B):
    """Return gradients for C = A @ B."""
    if dC.shape != (A.shape[0], B.shape[1]):
        raise ValueError("dC has an incompatible shape")
    if A.shape[1] != B.shape[0]:
        raise ValueError("A and B cannot be multiplied")

    dA = dC @ B.T
    dB = A.T @ dC
    return dA, dB
```

## Affine layer backward

Given:

```text
X: shape (B, D_in)
W: shape (D_out, D_in)
b: shape (D_out,)
Y = X @ W.T + b: shape (B, D_out)
```

Given `dY` of shape `(B, D_out)`, compute:

```text
dX = dY @ W
dW = dY.T @ X
db = dY.sum(axis=0)
```

```python
def linear_backward(dY, X, W):
    """Return gradients for Y = X @ W.T + b."""
    expected = (X.shape[0], W.shape[0])
    if dY.shape != expected:
        raise ValueError(f"expected dY shape {expected}, got {dY.shape}")

    dX = dY @ W
    dW = dY.T @ X
    db = dY.sum(axis=0)
    return dX, dW, db
```

## ReLU backward

Implement the backward pass for `Y = maximum(0, X)`:

```python
def relu_backward(dY, X):
    """Use zero as the ReLU subgradient at X == 0."""
    if dY.shape != X.shape:
        raise ValueError("dY and X must have the same shape")
    return dY * (X > 0)
```

## Stable softmax-cross-entropy

For integer class labels, subtract the row maximum before exponentiation, compute probabilities, and apply mean reduction consistently:

```python
def softmax_cross_entropy_backward(logits, labels):
    """Return mean loss and dLogits for integer labels."""
    shifted = logits - logits.max(axis=1, keepdims=True)
    exp = np.exp(shifted)
    probs = exp / exp.sum(axis=1, keepdims=True)

    batch = logits.shape[0]
    loss = -np.log(probs[np.arange(batch), labels]).mean()
    dLogits = probs.copy()
    dLogits[np.arange(batch), labels] -= 1
    dLogits /= batch
    return loss, dLogits
```

## What the interviewer is checking

- Does each gradient match its corresponding input shape?
- Do you use the upstream gradient rather than return only a local derivative?
- Do you reverse broadcasting with the correct sum?
- Do you match mean versus sum reduction?
- Do you avoid mutating cached forward values unexpectedly?
- Can you explain each transpose instead of guessing from memorized formulas?
