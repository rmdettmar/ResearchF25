import json


def stimulus_gen():
    scenarios = []

    # Helper function to create a scenario dictionary
    def create_scenario(name, input_sequences):
        return {
            "scenario": name,
            "input variable": [{"in": seq} for seq in input_sequences],
        }

    # Scenario 1: Single Bit Detection
    single_bit = create_scenario(
        "Single Bit Detection", ["0001", "0010", "0100", "1000"]
    )
    scenarios.append(single_bit)

    # Scenario 2: Multiple Bits Active
    multiple_bits = create_scenario(
        "Multiple Bits Active", ["1100", "1110", "1111", "1010"]
    )
    scenarios.append(multiple_bits)

    # Scenario 3: Zero Input
    zero_input = create_scenario("Zero Input", ["0000"])
    scenarios.append(zero_input)

    # Scenario 4: Adjacent Bits
    adjacent_bits = create_scenario("Adjacent Bits", ["0011", "0110", "1100"])
    scenarios.append(adjacent_bits)

    # Scenario 5: Alternating Patterns
    alternating = create_scenario("Alternating Patterns", ["0101", "1010"])
    scenarios.append(alternating)

    # Scenario 6: Rapid Input Changes
    rapid_changes = create_scenario(
        "Rapid Input Changes", ["0000", "1111", "0000", "1010", "0101"]
    )
    scenarios.append(rapid_changes)

    # Scenario 7: Boundary Transitions
    boundary = create_scenario(
        "Boundary Transitions", ["0000", "1111", "1000", "0001", "0100"]
    )
    scenarios.append(boundary)

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
