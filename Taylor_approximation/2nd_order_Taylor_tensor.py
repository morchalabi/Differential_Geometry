import numpy as np

def myTaylor(input_data: dict) -> dict:
    
    # STEP 3: Read in input point p and weight α
    p_ = np.float64(input_data.get('p_', np.zeros(2)))
    a_ = np.float64(input_data.get('a_', 1.0))

    # step 3.1: extract the integer part of each component to new point x
    x_ = np.array([int(p_i) for p_i in p_])

    # step 3.2: extract the fractional part of each component to vector h
    h_ = p_ - x_

    # STEP 1: Define Rosenbrock function f(x)
    f_x = (1-x_[0])**2 + 100*(x_[1]-x_[0]**2)**2

    # STEP 2: Find Jacobian and Hessian of f(x)
    # step 2.1: find Jacobian of f(x)
    J_x = np.array([-2*(1-x_[0]) - 400*x_[0]*(x_[1]-x_[0]**2), 200*(x_[1]-x_[0]**2)])

    # step 2.2: find Hessian of f(x)
    H_x = np.array([[2 - 400*(x_[1]-3*x_[0]**2), -400*x_[0]],
                   [-400*x_[0],                 200]])

    # STEP 4 (PATH A): Compute the 1st-order Taylor approximation of f(x+h)
    pa_ = f_x + np.tensordot(J_x, h_, axes = J_x.ndim)

    # STEP 5 (PATH B): Compute the 2nd-order Taylor coefficient of f(x+h)
    h_2 = np.tensordot(h_, h_, axes = 0)
    pb_ = 0.5 * np.tensordot(H_x, h_2, axes = H_x.ndim)

    # STEP 6: Compute the 2nd-order Taylor approximation of f(x+h) (with twisted Pb)
    return {'score': round(pa_ + a_ * pb_, 4)}