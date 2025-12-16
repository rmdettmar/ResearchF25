import json
import random

from cocotb.binary import BinaryValue


def generate_walking_ones():
    patterns = []
    for i in range(100):
        val = 1 << i
        binary_val = BinaryValue(value=val, n_bits=100, bigEndian=True)
        patterns.append({"in": binary_val.binstr})
    return patterns


def generate_symmetric_pattern():
    # Create palindromic patterns
    pattern = ["0"] * 50 + ["0"] * 50
    for i in range(25):
        pattern[i] = pattern[99 - i] = "1"
    return [{"in": "".join(pattern)}]


def generate_boundary_pattern():
    # Set patterns at boundaries (bits 99:90 and 9:0)
    pattern = ["0"] * 100
    for i in range(90, 100):
        pattern[i] = "1"
    for i in range(0, 10):
        pattern[i] = "1"
    return [{"in": "".join(pattern)}]


def stimulus_gen():
    scenarios = []

    # All Zeros Test
    scenarios.append(
        {"scenario": "All Zeros Test", "input variable": [{"in": "0" * 100}]}
    )

    # All Ones Test
    scenarios.append(
        {"scenario": "All Ones Test", "input variable": [{"in": "1" * 100}]}
    )

    # Alternating Bits
    scenarios.append(
        {"scenario": "Alternating Bits", "input variable": [{"in": ("10" * 50)}]}
    )

    # Single Bit Set
    single_bit_patterns = [
        "1" + "0" * 99,  # MSB
        "0" * 49 + "1" + "0" * 50,  # Middle
        "0" * 99 + "1",  # LSB
    ]
    scenarios.append(
        {
            "scenario": "Single Bit Set",
            "input variable": [{"in": pattern} for pattern in single_bit_patterns],
        }
    )

    # Walking Ones
    scenarios.append(
        {"scenario": "Walking Ones", "input variable": generate_walking_ones()}
    )

    # Random Pattern
    random_pattern = "".join(random.choice(["0", "1"]) for _ in range(100))
    scenarios.append(
        {"scenario": "Random Pattern", "input variable": [{"in": random_pattern}]}
    )

    # Symmetric Pattern
    scenarios.append(
        {
            "scenario": "Symmetric Pattern",
            "input variable": generate_symmetric_pattern(),
        }
    )

    # Boundary Pattern
    scenarios.append(
        {"scenario": "Boundary Pattern", "input variable": generate_boundary_pattern()}
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
