import numpy as np

def myTensor(input_data: dict) -> dict:
    
    # Parse inputs
    x_ = np.array(input_data.get("x", np.zeros(3)), dtype = np.float64)
    w1_ = np.float64(input_data["w1"])
    w2_ = np.float64(input_data["w2"])

    # Fixed tensors
    F_ = np.array([[9, 9, 10],
                   [17, 27, 21],
                   [4, 7, 27]
                  ], dtype=float)

    G_ = np.array([[3, 1, 4],
                   [2, 1, 0],
                   [2, 2, 1]
                  ], dtype=float)

    # Path A: Quadratic contraction using einsum
    f_ = np.einsum('ij,i,j->', F_, x_, x_)

    # Path B: Fourth-order contraction using einsum (T = G ⊗ G)
    g_ = np.einsum('ij,kl,i,j,k,l->', G_, G_, x_, x_, x_, x_)

    # Merging stage
    denom = w1_ * f_ + w2_ * g_

    if abs(denom) < 1e-12:
        score_ = -1.0
    else:
        H_ = (2 * f_ * g_) / denom
        score_ = round(H_, 4)

    return {"score": score_}
