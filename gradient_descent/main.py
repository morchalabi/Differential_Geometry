import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import alpha

# Definition of right circular cone function with bias f(x,y) = sqrt((x-5)^2 + (y-5)^2) - 10 ------------
# Inputs:
# x_: point at which to compute cone value (numpy array)
# Outputs:
# f_: cone value at x_ (float)
def cone_f(x_):
    center_ = np.array([5, 5])                      # center of cone
    r_ = np.sqrt(sum((x_ - center_)**2))            # radius from center to point x_
    f_ = r_ - 10
    return f_

# Gradient of the right circular cone function ----------------------------------------------------------
# Inputs:
# x_: point at which to compute gradient (numpy array)
# Outputs:
# grad_: gradient of cone function at x_ (numpy array)
def grad_f(x_):
    center_ = np.array([5, 5])                      # center of cone
    r_ = np.sqrt(sum((x_ - center_)**2))            # radius from center to point x_
    if 1e-10 <= r_:                                  # due to floating point precision in python: if not at the origin, return gradient
        grad_ = (x_ - center_)/r_                   # gradient of cone function away from the origin
        return grad_
    else:
        subgrad_ = np.array([0.0, 0.0])         # cone is non-differentiable at the origin, so we can use a subgradient like [0, 0]
        return subgrad_

# Optimization method
# Inputs:
# x_: initial point (numpy array)
# alpha_: learning rate (float)
# num_iters: number of iterations (int)
# print_cost: whether to print cone values every 100 iterations (boolean)
# Outputs:
# x_: optimal point found (numpy array)
# fs_: list of cone values at each iteration (list of floats)
# xs_: list of points at each iteration (list of numpy arrays)
def optimize_cone(x_, alpha_ = 0.05, num_iters = 500, print_cost = True):

    # Gradient descent loop ---------------------------------------------------------------------------------
    fs_ = [cone_f(x_)]                  # list to hold cone values at each iteration
    xs_ = [x_]                          # list to hold points at each iteration
    for i_ in range(num_iters):
        alpha_eff = 0.6*(alpha_ + np.tanh(cone_f(x_)+10))           # radius r = sqrt(x-5)^2 + (y-5)^2, so cone_f(x)+10 = r (r >= 0)
                                                                    # rule: ‖update step‖ = α + ‖grad‖ should be ~ α; as ‖grad‖ = 1 and tanh(r) ~ 1 for large r, ‖update step‖ ~ (1+α) for large r
                                                                    # That's why 0.6*(α + np.tanh(r) to make sure the effective learning rate is close to α for large r
        
        x_ = x_ - alpha_eff * grad_f(x_)                            # gradient descent step
        
        xs_.append(x_)                                              # append current point to list
        f_ = cone_f(x_)                                             # cone value at x_
        fs_.append(f_)                                              # append cone value to list

        # print cone values every 100 iteratations
        if print_cost and i_ % 100 == 0:
            print('cone value at iteration %i is: %.4f' % (i_, f_))

        if np.isclose(grad_f(xs_[-1]) @ grad_f(xs_[-2]), -np.linalg.norm(grad_f(xs_[-1]))**2, atol = 1e-10, rtol = 0):          # if convergence reached (gradient vector inversion), break loop
            print('Convergence reachead at iteration %i.'% i_)
            num_iters = i_
            break

    return x_, fs_, xs_, num_iters

if __name__ == '__main__':

    alpha_ = 0.05                       # learning rate
    num_iters = 5000                    # number of iterations
    x_ = np.array([11, -10])            # initial point
    x_, fs_, xs_, num_iters = optimize_cone(x_, alpha_ = alpha_, num_iters = num_iters, print_cost = True)

    print('After %i iterations:' % num_iters,
          '\noptimal point is: (%.4f, %.4f)' % (x_[0], x_[1]),
          '\nthe minimum cone value is: %.4f' % fs_[-1])

# Plotting cone values over iterations

plt.figure(figsize=(12, 6))                         # make it wide enough
plt.plot(fs_, linewidth = 1.5, alpha = 0.8)         # with thicker line and less transparency
plt.title('Plot of %i Values' % num_iters)
plt.xlabel('Index')
plt.ylabel('Value')
plt.grid(True, alpha=0.3)
plt.show()