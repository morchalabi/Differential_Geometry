## Function Description
Given the components of a positive-definite metric tensor `g` (first fundamental form) and a symmetric (0,2)-tensor `h` (second fundamental form), compute the shape operator

$$
S = g^{-1} h
$$

and return the gap between its principal curvatures:

$$
\text{score} = \sqrt{ (\operatorname{tr} S)^2 - 4 \cdot \det(S) }
$$

rounded to exactly four decimal places. The only constants appearing in the formula (2 and 4) are definitional from the characteristic polynomial of a 2×2 matrix.

## Mathematical Formulation

Let

$$
g = \begin{pmatrix} g_{11} & g_{12} \\ g_{12} & g_{22} \end{pmatrix}, \qquad
h = \begin{pmatrix} h_{11} & h_{12} \\ h_{12} & h_{22} \end{pmatrix}
$$

be the matrices of the first and second fundamental forms respectively, with `det(g) > 0`.

**Step 1.** Compute the inverse metric $ g^{-1} $.

**Step 2.** Form the shape operator

$$
S = g^{-1} h.
$$

**Step 3.** Compute the trace and determinant of $ S $:

$$
\operatorname{tr}(S) = S_{11} + S_{22}, \quad \det(S) = S_{11}S_{22} - S_{12}S_{21}.
$$

**Step 4.** Return the principal curvature gap

$$
\text{score} = \sqrt{ (\operatorname{tr} S)^2 - 4 \cdot \det(S) }
$$

rounded to exactly four decimal places. (The expression under the square root is guaranteed to be non-negative when `g` is positive definite and `h` is symmetric.)

## Inputs
- `g11`, `g12`, `g22`: float ∈ $[-10.0, 10.0]$ (components of a positive-definite metric tensor, with `det(g) > 0`)
- `h11`, `h12`, `h22`: float ∈ $[-10.0, 10.0]$ (components of a symmetric (0,2)-tensor)

## Outputs
- `score`: float rounded to exactly 4 decimal places

## Pseudocode
1. Construct the matrices
   $
   g = \begin{pmatrix} g11 & g12 \\ g12 & g22 \end{pmatrix}, \quad
   h = \begin{pmatrix} h11 & h12 \\ h12 & h22 \end{pmatrix}.
   $
2. Compute `g_inv = inverse(g)`.
3. Compute the shape operator `S = g_inv @ h`.
4. Compute `tr_S = trace(S)` and `det_S = det(S)`.
5. Compute `Δ = tr_S**2 - 4*det_S`.
6. Return `round(sqrt(max(0.0, Δ)), 4)`.

## Assumptions
1. The metric tensor `g` is positive definite (`det(g) > 0`).
2. The tensor `h` is symmetric (`h12 = h21`).
3. All input values are finite and lie within the declared ranges.

## Limitations
- The function operates on 2-dimensional tangent spaces only.
- Degenerate metrics (`det(g) ≤ 0`) are not permitted.