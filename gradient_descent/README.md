# Proposal

## Function Name
compute_score

## Domain
Math

## Sub-domain
Mathematical Optimization and Nonlinear Dynamical Systems

## Function Description
Evaluates a continuous two-dimensional input coordinate space using an iterative, deterministic numeric procedure. The framework integrates a trajectory-dependent state machine with a parallel independent spatial orientation reduction to return a single integrated scalar performance metric.

## Mathematical Formulation
The black-box method optimizes (minimizes) a right circular cone function defined by $f(s)=‖s-c‖_2+b$, where $s = [state\_x,state\_y]$ is the state vector, $c=[5.0,5.0]$ is the center and $b=-10$ is the vertical bias. The system is governed by two entirely decoupled, non-sequential mathematical paths that merge into a single scalar output space.

### Path A: Iterative Trajectory Vector Field
The system initializes a continuous trajectory at $s_0 = [state\_x,state\_y]$. At any discrete iteration step $t$, the direction vector field $\nabla_{s_t}f$ is defined as the gradient of the radial circular cone surface $f$:

$$\nabla f(s_t) = \begin{cases}
\frac{s_t - c}{‖s_t - c‖_2}, & \text{if } s_t \neq c \\\\
[0.0, 0.0], & \text{otherwise}
\end{cases}$$

The state vectors transition dynamically by steps scaled by parameter $\alpha$ (represented by `scale_`):
$$s_{t+1} = s_t - \alpha \nabla_{s_t}f$$

The dynamical system runs until it exhausts $t =$ `max_steps` or satisfies an acute directional inversion criteria, indicating it has overshot the optimal minimum and entered a steady-state toggle:
$$\nabla_{s_{t+1}}f \cdot \nabla_{s_t}f = - ‖\nabla_{s_{t+1}}f‖^2$$

The terminal loop baseline evaluation maps the terminal trajectory state $s_T$ back to the radial distance metric field $f(s)$:
$$v_T = f(s_T) = ‖s_T - c‖_2 - 10.0$$

### Path B: Independent Boundary Orientation Map
Operating completely in parallel and evaluated exclusively at initialization ($t=0$), Path B captures the orientation of the initial gradient vector $\nabla_{s_0}f=(\partial_{x},\partial_{y})$. The raw input vector is projected relative to the basis vector $e_y = [0, 1]$:

$$\theta = \arccos\left(\frac{\nabla_{s_0}f \cdot e_y}{‖\nabla_{s_0}f‖‖e_y‖} \right),$$
$$s = \text{sign}(\partial_{x}),$$
$$\Theta =\left(2\pi + s\theta\right)\bmod (2\pi), \quad \Theta \in [0,2\pi).$$

### Pipeline Merging Stage

The final scalar value returned under the generic output wrapper `score_` is an integrated additive combination of both isolated domains:

`score_`$$= v_T+\Theta$$

## Inputs
- `center_x`
    - Type: float
    - Description: Center coordinate along the primary system axis. Valid range: [-100.0, 100.0]
- `center_y`
    - Type: float
    - Description: Center coordinate along the secondary system axis. Valid range: [-100.0, 100.0]
- `state_x`
    - Type: float
    - Description: Initial state's coordinate along the primary system axis. Valid range: [-100.0, 100.0].
- `state_y`
    - Type: float
    - Description: Initial state's coordinate along the secondary system axis. Valid range: [-100.0, 100.0].
- `scale_`
    - Type: float
    - Description: Adjustable scaling modifier controlling localized state transformation steps. Valid range: [0.01, 1.0].
- `max_steps`
    - Type: integer
    - Description: Upper iteration limit on permitted system state updates. Valid range: [1, 5000].

## Outputs
- `score_`
    - Type: float
    - Description: The final integrated combined scalar output value, rounded to exactly 4 decimal places.

## Pseudocode
1. Define a nested helper function $f(s)$ tracking a radial scalar distance field from center $c=[center\_x = 5.0, center\_y = 5.0]$: $f(s) = ‖s - c‖_2 - 10.0$.
2. Define a nested helper function $\nabla f(s)$ calculating normalized spatial displacement vectors:
   - If $s \neq c$, return $(s - c)/‖s - c‖_2$.
   - Otherwise, return a zero vector $[0.0, 0.0]$.
3. Initialize the continuous 2D tracking state vector: $s_0 = [state\_x,state\_y]$.
4. **Path B: Raw Input Spatial Component (Independent Parallel Path)**
   - a. Capture the initial normalized transition direction vector at step zero: $\nabla_{s_0}f = \nabla f(s_0)$.
   - b. Compute the geometric angular alignment of $\nabla_{s_0}f = (\partial_{x},\partial_{y})$ relative to the basis vector $e_y$ :

$$\theta = \arccos\left(\frac{\nabla_{s_0}f \cdot e_y}{‖\nabla_{s_0}f‖‖e_y‖} \right),$$
$$s = \text{sign}(\partial_{x}),$$
$$\Theta =\left(2\pi + s\theta\right)\bmod (2\pi), \quad \Theta \in [0,2\pi).$$
   

6. **Path A: Iterative Trajectory State Update Loop**
   - Iterate a maximum of `max_steps` times, where index $t$ ranges from $0$ to `max_steps`:
      - i. update the current state by stepping along the direction vector scaled by `scale_`$=\alpha$: $s_{t+1} = s_t - \alpha \times \nabla_{s_t}f$.
      - ii. compute the new transition direction: $\nabla_{s_{t+1}}f = \nabla f(s_{t+1})$.
      - iii. evaluate the inner dot-product directional reversal condition:
             If $\nabla_{s_{t+1}}f \cdot \nabla_{s_t}f = -‖\nabla_{s_{t+1}}f‖^2$, break out of the iteration loop immediately.
      - v. set the current transition direction for next iteration $\nabla_{s_{t}}f = \nabla_{s_{t+1}}f$.
8. **Pipeline Combination Stage**
   - a. Evaluate the terminal state value: $v_T = f(s_T)$.
   - b. Return the independent paths by combining them into `score_` $= v_T + \Theta$ rounded to exactly 4 decimal places.

## Assumptions
- Continuous input parameters map to real coordinates within an open, bounded simulation plane.
- Arithmetic transitions preserve absolute determinism and replication properties under uniform IEEE 754 floating-point runtime environments.
- Vector division rules incorporate static safety floor bounds to guarantee numerical stability near the coordinate center.

## Limitations
- The current method employs a fixed base learning rate $\alpha$, which can lead to convergence failures when starting from initial states located far from the optimum. In such cases, the trajectory may stall, resulting in a final state that remains significantly distant from the target. This limitation can be effectively addressed by making the learning rate radius-dependent. For instance, defining an adaptive learning rate as $\alpha' = \frac{1}{k}\bigl(\alpha + \tanh(r)\bigr),$ where $r = ‖s - c‖_2$ is the Euclidean distance from the current state to the cone center and $1 < k$ is a scaling hyperparameter, allows for larger steps when far from the optimum and naturally smaller steps near the target.

## Citations
1. Boyd, S., & Mutapcic, A. (2008). "Subgradient Methods." *Stanford University Lecture Notes*.
2. Nesterov, Y. (2018). *Lectures on Convex Optimization*. Springer.
3. Polyak, B. T. (1987). *Introduction to Optimization*. Optimization Software.
4. Marsden, J. E., & Tromba, A. J. (2012). *Vector Calculus*. W. H. Freeman.

## Edge Cases
- **Absolute Target Center:** Initializing at `state_x = 5.0`, `state_y = 5.0`, `scale_ = 0.05`, `max_steps = 5000`. Path A terminates on step 0, giving $v_T = -10.0$. Path B calculates a zero direction vector, resulting in an angle component of $\Theta = 0.0$. Expected output: `{"score_": -10.0000}`.
- **Asymmetric Convergence & Oscillation Overshoot:** Initializing at `state_x = 5.1`, `state_y = 5.1`, `scale_ = 1.0`, `max_steps = 5000`. Path A overshoots the origin on step 1, triggering immediate early termination via directional vector inversion ($v_T = -9.1414$). Path B calculates the initial quadrant angle from the raw inputs ($\Theta = 0.7854$). Expected output: `{"score_": -8.3560}`.
- **Point Symmetry Invariance Check:** Comparing `state_x = 3.0`, `state_y = 3.0` vs. `state_x = 7.0`, `state_y = 7.0` with `scale_ = 0.05`, `max_steps = 5000`. Path A yields an identical matching trajectory count because Euclidean distance metrics are perfectly symmetric around $c=[5.0, 5.0]$. However, Path B calculates completely different angular orientation profiles ($\Theta_1 = 3.9270$ vs. $\Theta_2 = 0.7854$), isolating Path B from Path A. Expected output (for `3.0, 3.0`): `{"score_": -6.0514}`.
- **Small Scale Slow-Walk Tracker:** Initializing far out at the extreme grid edge `state_x = -100.0`, `state_y = -100.0` with the absolute minimum step scale `scale_ = 0.01` and `max_steps = 5000`. The system slowly steps toward the center but runs out of steps long before reaching the core, testing the loop's structural deceleration patterns. Expected output: `{"score_": 92.4194}`.
- **Maximum Grid Coordinate Boundary:** Initializing at the maximum allowable coordinate corner `state_x = -100.0`, `state_y = -100.0` with a large step scale of `scale_ = 1.0` and `max_steps = 5000`. Verifies system precision behavior across the maximum continuous path length allowed by the schema bounds. Expected output: `{"score_": -5.5654}`.

## What Makes This Hard?
This task employs a non-sequential, two-path architectural pipeline. Path A computes an iterative state transformation trajectory, while Path B independently extracts a raw coordinate angular direction vector at initialization. Because the final scalar score combines both distinct mathematical properties ($v_T + \theta$), an AI model cannot infer variables through isolated input-output mapping. Varying `scale_` affects only the loop convergence path, while changing coordinates at a fixed distance isolates Path B's orientation-sensitive angular calculation, forcing the model to systematically decouple both distinct algorithms to succeed.