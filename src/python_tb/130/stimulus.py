import json
import random

from cocotb.binary import BinaryValue


def gen_walking_ones(width):
    patterns = []
    for i in range(width):
        val = 1 << i
        bin_val = BinaryValue(value=val, n_bits=width)
        patterns.append(bin_val.binstr)
    return patterns


def gen_random_patterns(width, count):
    patterns = []
    for _ in range(count):
        val = random.getrandbits(width)
        bin_val = BinaryValue(value=val, n_bits=width)
        patterns.append(bin_val.binstr)
    return patterns


def stimulus_gen():
    width = 100
    scenarios = []

    # Scenario 1: All Zeros
    all_zeros = {"scenario": "All Zeros Input", "input variable": [{"in": "0" * width}]}
    scenarios.append(all_zeros)

    # Scenario 2: All Ones
    all_ones = {"scenario": "All Ones Input", "input variable": [{"in": "1" * width}]}
    scenarios.append(all_ones)

    # Scenario 3: Single One Input
    single_one = {
        "scenario": "Single One Input",
        "input variable": [{"in": pat} for pat in gen_walking_ones(width)],
    }
    scenarios.append(single_one)

    # Scenario 4: Single Zero Input
    single_zero_patterns = []
    for i in range(width):
        pattern = list("1" * width)
        pattern[i] = "0"
        single_zero_patterns.append({"in": "".join(pattern)})
    single_zero = {
        "scenario": "Single Zero Input",
        "input variable": single_zero_patterns,
    }
    scenarios.append(single_zero)

    # Scenario 5: Alternating Pattern
    alt_pattern = {
        "scenario": "Alternating Pattern",
        "input variable": [{"in": "".join(["10" * 50])}],
    }
    scenarios.append(alt_pattern)

    # Scenario 6: Random Input Patterns
    random_patterns = {
        "scenario": "Random Input Patterns",
        "input variable": [{"in": pat} for pat in gen_random_patterns(width, 1000)],
    }
    scenarios.append(random_patterns)

    # Scenario 7: Walking Ones Pattern
    walking_ones = {
        "scenario": "Walking Ones Pattern",
        "input variable": [{"in": pat} for pat in gen_walking_ones(width)],
    }
    scenarios.append(walking_ones)

    # Scenario 8: Input Transition Time
    transition_patterns = [
        {"in": "0" * width},
        {"in": "1" * width},
        {"in": "0" * width},
        {"in": "1" * (width // 2) + "0" * (width // 2)},
        {"in": "0" * (width // 2) + "1" * (width // 2)},
    ]
    transition_time = {
        "scenario": "Input Transition Time",
        "input variable": transition_patterns,
    }
    scenarios.append(transition_time)

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
