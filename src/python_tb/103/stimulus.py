import json


def create_sequence(reset_val, w_val):
    return {"reset": format(reset_val, "01b"), "w": format(w_val, "01b")}


def stimulus_gen():
    scenarios = []

    # Reset Verification
    reset_seq = {
        "scenario": "Reset Verification",
        "input variable": [
            create_sequence(1, 0),  # Assert reset
            create_sequence(1, 0),  # Keep reset
            create_sequence(1, 0),  # Keep reset
            create_sequence(0, 0),  # Release reset
        ],
    }
    scenarios.append(reset_seq)

    # Path to Output 1 (A->B->C->E)
    path_to_e = {
        "scenario": "Path to Output 1",
        "input variable": [
            create_sequence(1, 0),  # Reset to A
            create_sequence(0, 1),  # A->B
            create_sequence(0, 1),  # B->C
            create_sequence(0, 1),  # C->E
        ],
    }
    scenarios.append(path_to_e)

    # Path to Alternative Output 1 (A->B->C->D->F)
    path_to_f = {
        "scenario": "Path to Alternative Output 1",
        "input variable": [
            create_sequence(1, 0),  # Reset to A
            create_sequence(0, 1),  # A->B
            create_sequence(0, 1),  # B->C
            create_sequence(0, 0),  # C->D
            create_sequence(0, 1),  # D->F
        ],
    }
    scenarios.append(path_to_f)

    # State E Self-Loop
    e_loop = {
        "scenario": "State E Self-Loop",
        "input variable": [
            create_sequence(1, 0),  # Reset to A
            create_sequence(0, 1),  # A->B
            create_sequence(0, 1),  # B->C
            create_sequence(0, 1),  # C->E
            create_sequence(0, 1),  # E->E
            create_sequence(0, 1),  # E->E
        ],
    }
    scenarios.append(e_loop)

    # Return to Initial State
    return_to_a = {
        "scenario": "Return to Initial State",
        "input variable": [
            create_sequence(1, 0),  # Reset to A
            create_sequence(0, 1),  # A->B
            create_sequence(0, 0),  # B->D
            create_sequence(0, 0),  # D->A
            create_sequence(0, 1),  # A->B
            create_sequence(0, 1),  # B->C
            create_sequence(0, 1),  # C->E
            create_sequence(0, 0),  # E->D
            create_sequence(0, 0),  # D->A
        ],
    }
    scenarios.append(return_to_a)

    # Output Stability
    output_stability = {
        "scenario": "Output Stability",
        "input variable": [
            create_sequence(1, 0),  # Reset to A
            create_sequence(0, 1),  # A->B
            create_sequence(0, 1),  # B->C
            create_sequence(0, 1),  # C->E
            create_sequence(0, 1),  # E->E (stable z=1)
            create_sequence(0, 1),  # E->E (stable z=1)
        ],
    }
    scenarios.append(output_stability)

    # Reset During Operation
    reset_during_op = {
        "scenario": "Reset During Operation",
        "input variable": [
            create_sequence(1, 0),  # Reset to A
            create_sequence(0, 1),  # A->B
            create_sequence(0, 1),  # B->C
            create_sequence(0, 1),  # C->E
            create_sequence(1, 1),  # Assert reset while in E
            create_sequence(1, 0),  # Keep reset
            create_sequence(0, 0),  # Release reset
        ],
    }
    scenarios.append(reset_during_op)

    # Rapid Input Toggling
    rapid_toggle = {
        "scenario": "Rapid Input Toggling",
        "input variable": [
            create_sequence(1, 0),  # Reset to A
            create_sequence(0, 1),  # Toggle w
            create_sequence(0, 0),  # Toggle w
            create_sequence(0, 1),  # Toggle w
            create_sequence(0, 0),  # Toggle w
            create_sequence(0, 1),  # Toggle w
        ],
    }
    scenarios.append(rapid_toggle)

    return scenarios


if __name__ == "__main__":
    result = stimulus_gen()
    # 将结果转换为 JSON 字符串
    if isinstance(result, list):
        result = json.dumps(result, indent=4)
    elif not isinstance(result, str):
        result = json.dumps(result, indent=4)

    with open("stimulus.json", "w") as f:
        f.write(result)
