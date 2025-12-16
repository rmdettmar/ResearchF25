import json

from cocotb.binary import BinaryValue


def create_state_vector(state_num):
    state = ["0"] * 10
    state[state_num] = "1"
    return "".join(state)


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic State Transitions
    basic_transitions = {
        "scenario": "Basic State Transitions",
        "input variable": [
            {"in": "1", "state": create_state_vector(0)},
            {"in": "1", "state": create_state_vector(1)},
            {"in": "1", "state": create_state_vector(2)},
            {"in": "1", "state": create_state_vector(3)},
            {"in": "1", "state": create_state_vector(4)},
        ],
    }
    scenarios.append(basic_transitions)

    # Scenario 2: Output Verification
    output_verify = {
        "scenario": "Output Verification",
        "input variable": [
            {"in": "1", "state": create_state_vector(7)},  # S7 (0,1)
            {"in": "0", "state": create_state_vector(8)},  # S8 (1,0)
            {"in": "1", "state": create_state_vector(9)},  # S9 (1,1)
        ],
    }
    scenarios.append(output_verify)

    # Scenario 3: One-Hot Encoding Validation
    one_hot_validation = {
        "scenario": "One-Hot Encoding Validation",
        "input variable": [
            {"in": "0", "state": create_state_vector(i)} for i in range(10)
        ],
    }
    scenarios.append(one_hot_validation)

    # Scenario 4: Path to Special Output States
    special_paths = {
        "scenario": "Path to Special Output States",
        "input variable": [
            {"in": "1", "state": create_state_vector(0)},  # S0->S1
            {"in": "1", "state": create_state_vector(1)},  # S1->S2
            {"in": "1", "state": create_state_vector(2)},  # S2->S3
            {"in": "1", "state": create_state_vector(3)},  # S3->S4
            {"in": "1", "state": create_state_vector(4)},  # S4->S5
            {"in": "1", "state": create_state_vector(5)},  # S5->S6
        ],
    }
    scenarios.append(special_paths)

    # Scenario 5: State Reset Path
    reset_path = {
        "scenario": "State Reset Path",
        "input variable": [
            {"in": "0", "state": create_state_vector(i)}
            for i in range(10)
            if i not in [5, 6]
        ],
    }
    scenarios.append(reset_path)

    # Scenario 6: Holding Pattern
    holding_pattern = {
        "scenario": "Holding Pattern",
        "input variable": [
            {"in": "1", "state": create_state_vector(7)} for _ in range(5)
        ],
    }
    scenarios.append(holding_pattern)

    # Scenario 7: Multiple State Traversal
    multiple_traversal = {
        "scenario": "Multiple State Traversal",
        "input variable": [
            {"in": "1", "state": create_state_vector(0)},  # S0->S1
            {"in": "0", "state": create_state_vector(1)},  # S1->S0
            {"in": "1", "state": create_state_vector(0)},  # S0->S1
            {"in": "1", "state": create_state_vector(1)},  # S1->S2
            {"in": "1", "state": create_state_vector(2)},  # S2->S3
        ],
    }
    scenarios.append(multiple_traversal)

    # Scenario 8: Rapid Input Toggling
    rapid_toggle = {
        "scenario": "Rapid Input Toggling",
        "input variable": [
            {"in": "1", "state": create_state_vector(0)},
            {"in": "0", "state": create_state_vector(1)},
            {"in": "1", "state": create_state_vector(0)},
            {"in": "0", "state": create_state_vector(1)},
            {"in": "1", "state": create_state_vector(0)},
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
