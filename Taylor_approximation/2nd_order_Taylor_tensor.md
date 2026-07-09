## Function Description
Approximates a smooth quartic polynomial ($C^\infty$) (Rosenbrock function) at a new point using the second-order Taylor approximation.

## Mathematical Formulation
Let $f:\mathbb{R}^n \to \mathbb{R}$ be a scalar function, $x \in \mathbb{R}^n$ be a point, and $\mathbf{h} \in \mathbb{R}^n$ be a non-zero vector. $f$ is differentiable at $x$ if and only if there exists a unique covector $Df_x : \mathbf{h} \mapsto Df_x(\mathbf{h}),$ called the (total) derivative or differential of $f$ at $x$, such that

$$
\lim_{\mathbf{h} \to 0} \frac{f(x+\mathbf{h})-f(x)-Df_x(\mathbf{h})}{‖\mathbf{h}‖}=0.
$$

Function $f$ is called totally differentiable if its total derivative exists at every point in its domain.

---

Conceptually, the definition of the total derivative expresses the idea that $Df_x$ determines **the best linear approximation** to the change in $f$ near $x$. This can be made precise by quantifying the error in the linear approximation:

$$
f(x+\mathbf{h})=f(x)+Df_x(\mathbf{h})+\varepsilon(\mathbf{h}) \qquad \text{as } \mathbf{h} \to 0,
$$

where the approximation error satisfies $\varepsilon(\mathbf{h}) = o(‖\mathbf{h}‖)$, meaning $\varepsilon(\mathbf{h})$ is much smaller than $‖\mathbf{h}‖$. In other words $\frac{o(‖\mathbf{h}\|)}{‖\mathbf{h}‖} \to 0 \text{ as } \mathbf{h} \to 0$.

---

The differentiability formula above is precisely the first-order Taylor approximation. If $f$ is $l$ times continuously differentiable ($C^l$), then $l$-th order Taylor approximation is given by:

$$
f(x+\mathbf{h} ) = \sum_{k = 0}^{l} \frac {1}{k!} D^kf_{x}(\underbrace{\mathbf{h},…,\mathbf{h}}_{k \ times})+o(∥\mathbf{h}∥^l),
$$

in which $D^kf_{x}(\mathbf{h}^k)$ is the $k$-th derivative represented by a $k$-covariant tensor:

$$
D^kf_{x}(\mathbf{h}^k) = \langle D^kf_{x},\mathbf{h}^{\otimes k}\rangle = \sum_{i_{1},…,i_{k}}^{n} \frac{\partial^k f}{\partial x_{i_{1}}…\partial x_{i_{k}} }h_{i_{1}}…h_{i_{k}},
$$

where $D^kf_{x}$ is $k$-th order tensor, $\otimes$ is tensor outer product and $\langle,\rangle$ is tensor inner product.

Since the Jacobian $\mathbf{J}$ and Hessian $\mathbf{H}$ are the multi-dimensional generalizations of the first and second derivatives, the 2nd-order Taylor expansion becomes:

$$
f(x+\mathbf{h}) = f(x)+\mathbf{J}(x)\mathbf{h}+\frac{1}{2}\mathbf{h}^T\mathbf{H}(x)\mathbf{h}+o(‖\mathbf{h}‖^2),
$$

where $\mathbf{J}(x) = [\frac{\partial f}{\partial x_i}(x)]_{i=1}^{n}$ and $\mathbf{H}(x) = [\frac{\partial^2 f}{\partial x_i \partial x_j}(x)]_{i,j=1}^{n}$.

### Path A: First-Order Taylor Approximation

Let $x = (x^1, x^2)$, then the **Rosenbrock function** is given by

$$
f(x) = (1 - x^1)^2+ 100(x^2 - (x^1)^2)^2.
$$

The graph of the function is the smooth surface

$$
S = \\{(x^1, x^2, z) \in \mathbb{R}^3 : z = f(x^1, x^2)\\},
$$

which possesses a unique global minimum at $p_0 = (1, 1, 0)$. 

(NOTE: This function was introduced by Howard H. Rosenbrock as a benchmark surface for optimization algorithms; see citations.)

The **Jacobian** of $f$ is

$$
\mathbf{J}(x) = \begin{bmatrix} -2(1 - x^1) - 400x^1 (x^2 - (x^1)^2) & 200(x^2 - (x^1)^2) \end{bmatrix},
$$

and its **Hessian** is

$$
\mathbf{H}(x) = \begin{bmatrix} 1200(x^1)^2 - 400x^2 + 2 & -400x^1 \\
                                -400x^1                  & 200
                \end{bmatrix}.
$$

This path computes $P_{A} = f(x)+\mathbf{J}(x)\mathbf{h}$.

### Path B: Second-order Taylor Coefficient

This path computes: $P_{B} = \frac{1}{2}\mathbf{h}^T\mathbf{H}(x)\mathbf{h}$.

### Merging Path A and Path B

The final scalar value returned is `score` $ = P_{A} + \alpha P_{B}$ which uses a non-standard weighting on the 2nd-order Taylor coefficient. When $\alpha = 1$, this is the 2nd-order Taylor approximation.

## Inputs
- `p`
   - Type: numpy.ndarray
   - Description: Real-valued point $p = (p^1, p^2)$ with shape (2,) at which $f$ will be approximated using the 2nd-order Taylor approximation. Range: $ -5.0 \leq p^i \le 5.0$.
- `α`
   - Type: float
   - Description: Weight for the 2nd-order Taylor coefficient. Range: [0,1].

## Outputs
- `score`
    - Type: float
    - Description: The final approximation value, rounded to exactly 4 decimal places.

## Pseudocode

1. Read in input point $p = (p^1, p^2)$.
   - 3.1 Extract the integer part of $p$ and store it in a new point: *$x$ = np.array( [int($p^i$) for $p^i$ in $p$] )*.
   - 3.2 Extract the fractional part of $p$ and store it in a vector: $\mathbf{h} = p-x. \\$
      Now $x$ is an integer point and $\mathbf{h}$ is its displacement vector.

2. Define the smooth quartic polynomial $ f(x) = (1 - x^1)^2+ 100(x^2 - (x^1)^2)^2. \\$

3. Find the tensor fields $Df(x) = \mathbf{J}(x)$ and $D^2f(x)= \mathbf{H}(x)$.

4. ### Path A
   - 4.1 Compute $P_{A} = f(x)+\mathbf{J}(x)\mathbf{h}. \\$
   NOTE: this step will be implemented by tensor inner product from Numpy:
   
      - *$P_{A}$ = $f(x)$ + np.tensordot($\mathbf{J}$, $\mathbf{h}$ , axes = $\mathbf{J}$.ndim)*.


5. ### Path B
   - 5.1 Compute $P_{B} = \frac{1}{2}\mathbf{h}^T\mathbf{H}(x)\mathbf{h}.\\$
   NOTE: this step will by implemented by tensor outer then inner products from Numpy $:\\$
      - *$\mathbf{h} \otimes \mathbf{h} $ = np.tensordot($\mathbf{h}$, $\mathbf{h}$ , axes = 0) $\\$*
      - *$P_{B}$ = 0.5 \* np.tensordot($\mathbf{H}$, $\mathbf{h} \otimes \mathbf{h}$ , axes = $\mathbf{H}$.ndim).*

6. ### Merging
   - 6.1 Compute and return `score` $= P_{A} + \alpha P_{B}$.

## Assumptions
 - Input point $p \in \mathbb{R}^2$.
 - The fractional part of component $p^i$ forms the $i$-th component of the displacement vector $\mathbf{h}.$  

## Limitations
- The input space is restricted to two-dimensional real-valued vectors.
- The approximation is based on first- and second-order Taylor information and therefore does not generally reproduce the exact Rosenbrock function value.
- The expansion point is not supplied directly by the user. Instead, it is determined implicitly through the integer-displacement decomposition $p=x+\mathbf{h}$.
- The weighting parameter $\alpha$ modifies the contribution of the second-order Taylor coefficient. Consequently, the returned value coincides with the standard second-order Taylor approximation only when $\alpha=1$.
- Numerical evaluation is subject to deterministic floating-point arithmetic and the final output is rounded to exactly four decimal places.
