import numpy as np

def myCurvature(input_data: dict) -> dict:

    # Extract inputs
    p_u = float(input_data.get("p_u", 0.0))
    p_v = float(input_data.get("p_v", 0.0))
    tx = float(input_data.get("tangent_x", 0.0))
    ty = float(input_data.get("tangent_y", 0.0))
    delta = float(input_data.get("delta", 0.1))
    mix = float(input_data.get("mix", 1.0))

    # Monkey Saddle surface and derivatives
    def f(u, v):
        return u**3 - 3 * u * v**2

    def fu(u, v):
        return 3 * u**2 - 3 * v**2

    def fv(u, v):
        return -6 * u * v

    def fuu(u, v):
        return 6 * u

    def fuv(u, v):
        return -6 * v

    def fvv(u, v):
        return -6 * u

    X = np.array([tx, ty], dtype=float)
    norm_X = np.linalg.norm(X)

    # Path A: Orthogonal Projection Transport
    if norm_X < 1e-14:
        theta = 0.0
    else:
        X_hat = X / norm_X

        # Push forward to 3D tangent vector at p
        ru_p = np.array([1.0, 0.0, fu(p_u, p_v)])
        rv_p = np.array([0.0, 1.0, fv(p_u, p_v)])
        V_start = X_hat[0] * ru_p + X_hat[1] * rv_p

        # Endpoint in parameter space
        g_u = p_u + delta * X_hat[0]
        g_v = p_v + delta * X_hat[1]

        # Unit normal at endpoint
        ru_g = np.array([1.0, 0.0, fu(g_u, g_v)])
        rv_g = np.array([0.0, 1.0, fv(g_u, g_v)])
        n = np.cross(ru_g, rv_g)
        n_norm = np.linalg.norm(n)
        if n_norm < 1e-14:
            n = np.array([0.0, 0.0, 1.0])
        else:
            n = n / n_norm

        # Orthogonal projection onto tangent plane at gamma(1)
        V_proj = V_start - np.dot(V_start, n) * n
        vproj_norm = np.linalg.norm(V_proj)

        if vproj_norm < 1e-12:
            theta = 0.0
        else:
            V_start_unit = V_start / np.linalg.norm(V_start)
            cos_theta = np.dot(V_start_unit, V_proj) / vproj_norm
            cos_theta = np.clip(cos_theta, -1.0, 1.0)
            theta = np.arccos(cos_theta)

    # Path B: Gaussian Curvature at original point p
    fu_p = fu(p_u, p_v)
    fv_p = fv(p_u, p_v)
    fuu_p = fuu(p_u, p_v)
    fuv_p = fuv(p_u, p_v)
    fvv_p = fvv(p_u, p_v)

    denom = (1 + fu_p**2 + fv_p**2)**2
    if abs(denom) < 1e-14:
        K = 0.0
    else:
        K = (fuu_p * fvv_p - fuv_p**2) / denom

    # Merge
    score = theta + mix * K * (delta ** 2)
    return {"score": round(score, 4)}