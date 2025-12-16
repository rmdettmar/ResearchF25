import json

from cocotb.binary import BinaryValue


def bin_str(value, width):
    return BinaryValue(value=value, n_bits=width, bigEndian=True).binstr


def stimulus_gen():
    scenarios = []

    # Basic Addition
    scenarios.append(
        {
            "scenario": "Basic Addition",
            "input variable": [{"do_sub": "0", "a": bin_str(3, 8), "b": bin_str(2, 8)}],
        }
    )

    # Basic Subtraction
    scenarios.append(
        {
            "scenario": "Basic Subtraction",
            "input variable": [{"do_sub": "1", "a": bin_str(5, 8), "b": bin_str(3, 8)}],
        }
    )

    # Zero Result Addition
    scenarios.append(
        {
            "scenario": "Zero Result Addition",
            "input variable": [{"do_sub": "0", "a": bin_str(0, 8), "b": bin_str(0, 8)}],
        }
    )

    # Zero Result Subtraction
    scenarios.append(
        {
            "scenario": "Zero Result Subtraction",
            "input variable": [{"do_sub": "1", "a": bin_str(5, 8), "b": bin_str(5, 8)}],
        }
    )

    # Addition Overflow
    scenarios.append(
        {
            "scenario": "Addition Overflow",
            "input variable": [
                {"do_sub": "0", "a": bin_str(255, 8), "b": bin_str(1, 8)}
            ],
        }
    )

    # Subtraction Underflow
    scenarios.append(
        {
            "scenario": "Subtraction Underflow",
            "input variable": [{"do_sub": "1", "a": bin_str(0, 8), "b": bin_str(1, 8)}],
        }
    )

    # Maximum Value Operations
    scenarios.append(
        {
            "scenario": "Maximum Value Operations",
            "input variable": [
                {"do_sub": "0", "a": bin_str(255, 8), "b": bin_str(255, 8)},
                {"do_sub": "1", "a": bin_str(255, 8), "b": bin_str(255, 8)},
            ],
        }
    )

    # Rapid Operation Switching
    scenarios.append(
        {
            "scenario": "Rapid Operation Switching",
            "input variable": [
                {"do_sub": "0", "a": bin_str(10, 8), "b": bin_str(5, 8)},
                {"do_sub": "1", "a": bin_str(10, 8), "b": bin_str(5, 8)},
                {"do_sub": "0", "a": bin_str(15, 8), "b": bin_str(7, 8)},
                {"do_sub": "1", "a": bin_str(15, 8), "b": bin_str(7, 8)},
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
