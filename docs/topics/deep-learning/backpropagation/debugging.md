# Debugging Gradients

## Finite-difference gradient checking

For a scalar objective \(J(\theta)\), approximate one component with the centered difference

\[
\frac{\partial J}{\partial \theta_i}
\approx
\frac{J(\theta_i+\varepsilon)-J(\theta_i-\varepsilon)}{2\varepsilon}.
\]

Centered differences are usually more accurate than one-sided differences for comparable step sizes. Use double precision, a small deterministic problem, and a moderate `epsilon` such as `1e-5`. Very small values suffer floating-point cancellation; large values increase truncation error.

Compare analytic and numerical gradients with a scale-aware metric:

```python
def relative_error(analytic, numerical):
    numerator = np.linalg.norm(analytic - numerical)
    denominator = max(
        1e-12,
        np.linalg.norm(analytic) + np.linalg.norm(numerical),
    )
    return numerator / denominator
```

Do not gradient-check exactly at non-differentiable points such as ReLU at zero.

## Common failure patterns

| Symptom | Likely cause | First check |
|---|---|---|
| Correct values, wrong shape | Missing reduction or stray singleton axis | Compare every gradient with its forward input shape |
| Gradient off by batch size | Mean/sum mismatch | Inspect the loss reduction |
| Only shared branches fail | Gradient overwrite | Accumulate all downstream contributions |
| Bias gradient looks like `dY` | Broadcast not reversed | Sum over batch and other expanded axes |
| NaN in classification loss | Unstable softmax or `log(0)` | Shift logits and use a fused stable loss |
| Numerical check fails near zero | Non-smooth point | Move the test input away from the boundary |
| Training changes between backward calls | Cached tensor mutated | Copy before in-place edits or avoid mutation |

## Shape checklist

For every returned gradient, assert:

```text
dX.shape == X.shape
dW.shape == W.shape
db.shape == b.shape
```

Then check values using at least two of the following: a hand-computed tiny example, finite differences, framework autograd, known invariants, or comparison with a trusted implementation.

## Practical isolation order

1. Make the test deterministic and reduce it to one layer.
2. Check the forward output and loss reduction.
3. Supply a simple upstream gradient, often all ones.
4. Verify shapes and broadcasting reductions.
5. Compare each local backward rule independently.
6. Add branches, batching, and realistic values back one at a time.

This order distinguishes a wrong local derivative from an error elsewhere in the computation graph.
