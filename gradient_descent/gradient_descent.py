import numpy as np

def myGD(input_data: dict) -> dict:

    # Extract structural primitives from the input schema dictionary
    center_x = float(input_data.get("center_x", 5.0))
    center_y = float(input_data.get("center_y", 5.0))
    state_x = float(input_data["state_x"])
    state_y = float(input_data["state_y"])
    scale_ = float(input_data.get("scale_", 0.05))
    max_steps = int(input_data.get("max_steps", 5000))

    # 1. Nested helper function computing state value
    def surface_value(state_):
        radius_ = np.linalg.norm(state_ - center_)
        return radius_ - 10.0

    # 2. Nested helper function computing direction tracking
    def transition_direction(state_):
        radius_ = np.linalg.norm(state_ - center_)
        if 1e-10 <= radius_:
            return (state_ - center_) / radius_
        return np.zeros(2)

    # 3. Initialize center coordinates
    center_ = np.array([center_x, center_y])

    # 4. Initialize state coordinates
    state_ = np.array([state_x, state_y])

    # 5. PATH B: Compute angle between initial direction and basis vector e_y independently
    current_direction_ = transition_direction(state_)
    angle_ = np.arccos(current_direction_[1])
    sign_ = np.sign(current_direction_[0])
    angle_ = ((2*np.pi) + sign_ * angle_) % (2*np.pi)

    # 6. PATH A: Iterative Optimization Loop
    for step_idx_ in range(int(max_steps)):
        state_ = state_ - scale_ * current_direction_
        new_direction_ = transition_direction(state_)
        if np.isclose(current_direction_ @ new_direction_, -np.linalg.norm(new_direction_)**2, atol=1e-10, rtol=0):
            break
        current_direction_ = new_direction_

    # 7. Pipeline Combination Stage
    score_ = surface_value(state_) + angle_
    return {"score_": round(float(score_), 4)}
    