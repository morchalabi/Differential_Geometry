import numpy as np

def myTensor(input_data: dict) -> dict:
    
    # Step 1: Reading in input data and initializing parameters
    u_ = np.array(input_data.get("u_", np.zeros((3))), dtype = float).reshape(3,1)
    v_ = np.array(input_data.get("v_", np.zeros((3))), dtype = float).reshape(3,1)
    a_ = float(input_data.get("a_",0.0))

    # Step 2: Prefixed order-2 tensor
    T_ = np.array([[9, 9 , 10],
                   [17, 27, 21],
                   [4, 7, 27]])

    # Step 3: Rank-1 order-2 tensor (tensor outer product)
    S_ = np.tensordot(u_.ravel(), v_.ravel(), axes = 0)           # shape (3,3)

    # Step 4: Path A: 2nd-order tensor (tensor inner product)
    T_uv = np.tensordot(T_, S_, axes = T_.ndim).item()          # scalar value from inner product of T and S

    # Step 5: Path B: Squared Frobenius norm
    S_F = np.linalg.norm(S_,'fro')**2

    # Step 6: Merging Path A and Path B
    score_ = T_uv - a_ * S_F

    return {"score": round(score_, 4)}