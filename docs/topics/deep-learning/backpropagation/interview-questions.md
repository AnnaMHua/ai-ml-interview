# Interview Questions

Try to answer each prompt aloud before expanding the explanation. A strong answer states the forward operation, upstream gradient, local rule, output shapes, and any broadcasting or reduction behavior.

## Why is reverse mode a good fit for neural-network training?

??? question "Show answer"
    Training usually maps many parameters to one scalar loss. Reverse mode starts from that scalar and obtains gradients for all upstream parameters in roughly one backward traversal. Forward mode would be preferable when there are very few inputs and many outputs, which is not the usual training geometry.

## Why does backpropagation not build full Jacobian matrices?

??? question "Show answer"
    Each node only needs a vector-Jacobian product: the upstream gradient multiplied by the node's local Jacobian. Computing this product directly uses the structure of the operation and avoids storing a Jacobian whose size could be the product of the input and output element counts.

## What happens when one tensor is used twice?

??? question "Show answer"
    Its final gradient is the sum of the contributions from both downstream paths. For `y = x * x`, the two input edges each contribute, giving `dy/dx = x + x = 2x`. A computation-graph engine must accumulate both contributions rather than overwrite the first one.

## Why is the bias gradient a sum over the batch?

??? question "Show answer"
    A bias vector is broadcast into every row during the forward pass. Each output row therefore contributes to the same bias element. The backward pass reverses that broadcast by summing the upstream gradient over the batch dimension: `db = dY.sum(axis=0)`.

## What must be cached for a backward pass?

??? question "Show answer"
    Cache only values required by the local derivative. Matrix multiplication needs its inputs; ReLU needs its pre-activation or an equivalent mask; sigmoid can reuse its output. Caching everything wastes memory, while recomputing selected cheap values trades compute for memory. Modern frameworks make this trade-off through activation checkpointing.

## What is the difference between `dJ`, a partial derivative, and a gradient?

??? question "Show answer"
    `dJ` in differential derivations represents an infinitesimal change in the scalar objective. A partial derivative describes change with respect to one variable while holding others fixed. The gradient `∇_X J` collects all partial derivatives with respect to the entries of `X` and has the same shape as `X` under the usual machine-learning convention.

## Why can gradients vanish or explode?

??? question "Show answer"
    Deep backpropagation repeatedly multiplies local derivatives and weight transformations. Products with singular values mostly below one shrink signals; products above one can amplify them. Saturating activations, poor initialization, depth, and recurrent reuse can worsen the effect. Residual paths, normalization, suitable initialization, non-saturating activations, and gradient clipping address different parts of the problem.
