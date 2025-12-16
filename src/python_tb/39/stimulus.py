import json

from cocotb.binary import BinaryValue


def convert_to_bin(value, width):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Addition (2 + 3 = 5)
    scenarios.append(
        {
            "scenario": "Basic Addition",
            "input variable": [{"x": convert_to_bin(2, 4), "y": convert_to_bin(3, 4)}],
        }
    )

    # Scenario 2: Overflow Detection (15 + 1 = 16)
    scenarios.append(
        {
            "scenario": "Overflow Detection",
            "input variable": [{"x": convert_to_bin(15, 4), "y": convert_to_bin(1, 4)}],
        }
    )

    # Scenario 3: Maximum Value Addition (15 + 15 = 30)
    scenarios.append(
        {
            "scenario": "Maximum Value Addition",
            "input variable": [
                {"x": convert_to_bin(15, 4), "y": convert_to_bin(15, 4)}
            ],
        }
    )

    # Scenario 4: Zero Addition (0 + 5 = 5)
    scenarios.append(
        {
            "scenario": "Zero Addition",
            "input variable": [{"x": convert_to_bin(0, 4), "y": convert_to_bin(5, 4)}],
        }
    )

    # Scenario 5: Double Zero (0 + 0 = 0)
    scenarios.append(
        {
            "scenario": "Double Zero",
            "input variable": [{"x": convert_to_bin(0, 4), "y": convert_to_bin(0, 4)}],
        }
    )

    # Scenario 6: Carry Propagation (8 + 8 = 16)
    scenarios.append(
        {
            "scenario": "Carry Propagation",
            "input variable": [{"x": convert_to_bin(8, 4), "y": convert_to_bin(8, 4)}],
        }
    )

    # Scenario 7: Alternating Bits (5 + 10 = 15)
    scenarios.append(
        {
            "scenario": "Alternating Bits",
            "input variable": [{"x": convert_to_bin(5, 4), "y": convert_to_bin(10, 4)}],
        }
    )

    # Scenario 8: Random Combinations
    scenarios.append(
        {
            "scenario": "Random Combinations",
            "input variable": [
                {"x": convert_to_bin(7, 4), "y": convert_to_bin(6, 4)},
                {"x": convert_to_bin(12, 4), "y": convert_to_bin(4, 4)},
                {"x": convert_to_bin(3, 4), "y": convert_to_bin(9, 4)},
            ],
        }
    )

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
