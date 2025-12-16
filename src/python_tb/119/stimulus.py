import json

from cocotb.binary import BinaryValue


def stimulus_gen():
    scenarios = []

    # Helper function to create stimulus dictionary
    def create_stimulus(scenario_name, input_value):
        binary_val = BinaryValue(value=input_value, n_bits=8)
        return {
            "scenario": scenario_name,
            "input variable": [{"in": binary_val.binstr}],
        }

    # Scenario 1: Positive Number Extension (0x5A)
    scenarios.append(create_stimulus("Positive Number Extension", 0x5A))

    # Scenario 2: Negative Number Extension (0xDA)
    scenarios.append(create_stimulus("Negative Number Extension", 0xDA))

    # Scenario 3: Maximum Positive Value (0x7F)
    scenarios.append(create_stimulus("Maximum Positive Value", 0x7F))

    # Scenario 4: Maximum Negative Value (0x80)
    scenarios.append(create_stimulus("Maximum Negative Value", 0x80))

    # Scenario 5: Zero Value Extension
    scenarios.append(create_stimulus("Zero Value Extension", 0x00))

    # Scenario 6: All Ones Value
    scenarios.append(create_stimulus("All Ones Value", 0xFF))

    # Scenario 7: Alternating Bits
    # First test with MSB=1
    scenarios.append(create_stimulus("Alternating Bits", 0xAA))

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
