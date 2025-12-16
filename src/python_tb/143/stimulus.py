import json

from cocotb.binary import BinaryValue


def create_input_sequence(x4, x3, x2, x1):
    # Convert 4 bits to binary string format
    return {"x": f"{x4}{x3}{x2}{x1}"}


def stimulus_gen():
    scenarios = []

    # Scenario 1: K-map True Output Cases
    true_cases = [
        {
            "scenario": "K-map True Output Cases",
            "input variable": [
                create_input_sequence(0, 0, 0, 0),
                create_input_sequence(0, 0, 1, 0),
                create_input_sequence(1, 0, 0, 0),
                create_input_sequence(1, 0, 0, 1),
                create_input_sequence(1, 0, 1, 0),
                create_input_sequence(1, 1, 0, 0),
                create_input_sequence(1, 1, 0, 1),
                create_input_sequence(1, 1, 1, 0),
            ],
        }
    ]
    scenarios.extend(true_cases)

    # Scenario 2: K-map False Output Cases
    false_cases = [
        {
            "scenario": "K-map False Output Cases",
            "input variable": [
                create_input_sequence(0, 0, 0, 1),
                create_input_sequence(0, 1, 0, 0),
                create_input_sequence(0, 1, 0, 1),
                create_input_sequence(0, 1, 1, 0),
                create_input_sequence(0, 1, 1, 1),
                create_input_sequence(1, 0, 1, 1),
                create_input_sequence(1, 1, 1, 1),
            ],
        }
    ]
    scenarios.extend(false_cases)

    # Scenario 3: Adjacent Cell Transitions
    adjacent_transitions = [
        {
            "scenario": "Adjacent Cell Transitions",
            "input variable": [
                create_input_sequence(0, 0, 0, 0),
                create_input_sequence(0, 0, 0, 1),
                create_input_sequence(0, 0, 1, 1),
                create_input_sequence(0, 0, 1, 0),
                create_input_sequence(0, 1, 1, 0),
            ],
        }
    ]
    scenarios.extend(adjacent_transitions)

    # Scenario 4: All Zeros Input
    all_zeros = [
        {
            "scenario": "All Zeros Input",
            "input variable": [create_input_sequence(0, 0, 0, 0)],
        }
    ]
    scenarios.extend(all_zeros)

    # Scenario 5: All Ones Input
    all_ones = [
        {
            "scenario": "All Ones Input",
            "input variable": [create_input_sequence(1, 1, 1, 1)],
        }
    ]
    scenarios.extend(all_ones)

    # Scenario 6: Input Bit Toggling
    bit_toggling = [
        {
            "scenario": "Input Bit Toggling",
            "input variable": [
                create_input_sequence(0, 0, 0, 0),
                create_input_sequence(1, 0, 0, 0),
                create_input_sequence(0, 1, 0, 0),
                create_input_sequence(0, 0, 1, 0),
                create_input_sequence(0, 0, 0, 1),
            ],
        }
    ]
    scenarios.extend(bit_toggling)

    # Scenario 7: Rapid Input Changes
    rapid_changes = [
        {
            "scenario": "Rapid Input Changes",
            "input variable": [
                create_input_sequence(0, 0, 0, 0),
                create_input_sequence(1, 1, 1, 0),
                create_input_sequence(0, 1, 0, 1),
                create_input_sequence(1, 0, 1, 0),
                create_input_sequence(0, 0, 1, 1),
            ],
        }
    ]
    scenarios.extend(rapid_changes)

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
