import json

from cocotb.binary import BinaryValue


def stimulus_gen():
    scenarios = []

    # Helper function to create a stimulus dictionary
    def create_stimulus(scenario_name, input_value):
        return {
            "scenario": scenario_name,
            "input variable": [{"in": BinaryValue(value=input_value, n_bits=4).binstr}],
        }

    # Scenario 1: All Zeros Input
    scenarios.append(create_stimulus("All Zeros Input", 0b0000))

    # Scenario 2: All Ones Input
    scenarios.append(create_stimulus("All Ones Input", 0b1111))

    # Scenario 3: Alternating Bits
    scenarios.append(create_stimulus("Alternating Bits", 0b1010))

    # Scenario 4: Single One
    scenarios.append(create_stimulus("Single One", 0b0001))

    # Scenario 5: Adjacent Ones
    scenarios.append(create_stimulus("Adjacent Ones", 0b0011))

    # Scenario 6: Separated Ones
    scenarios.append(create_stimulus("Separated Ones", 0b1001))

    # Scenario 7: Boundary Transition
    scenarios.append(create_stimulus("Boundary Transition", 0b1100))

    # Scenario 8: Rapid Input Changes
    scenarios.append(create_stimulus("Rapid Input Changes", 0b0101))

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
