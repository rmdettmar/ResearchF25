import json
import random

from cocotb.binary import BinaryValue


def gen_walking_ones(width, n_bits):
    patterns = []
    for i in range(n_bits - width + 1):
        val = ((1 << width) - 1) << i
        binary_val = BinaryValue(value=val, n_bits=n_bits)
        patterns.append(binary_val.binstr)
    return patterns


def gen_random_with_density(n_bits, density):
    num_ones = int(n_bits * density)
    positions = random.sample(range(n_bits), num_ones)
    val = sum(1 << pos for pos in positions)
    binary_val = BinaryValue(value=val, n_bits=n_bits)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []
    n_bits = 255

    # Scenario 1: All Zeros
    all_zeros = {
        "scenario": "All Zeros Input",
        "input variable": [{"in": "0" * n_bits}],
    }
    scenarios.append(all_zeros)

    # Scenario 2: All Ones
    all_ones = {"scenario": "All Ones Input", "input variable": [{"in": "1" * n_bits}]}
    scenarios.append(all_ones)

    # Scenario 3: Single Bit Set
    single_bit_patterns = []
    for pos in [0, 127, 254]:
        val = 1 << pos
        binary_val = BinaryValue(value=val, n_bits=n_bits)
        single_bit_patterns.append({"in": binary_val.binstr})
    scenarios.append(
        {"scenario": "Single Bit Set", "input variable": single_bit_patterns}
    )

    # Scenario 4: Alternating Pattern
    alt_val = int("0b" + "10" * (n_bits // 2) + ("1" if n_bits % 2 else ""), 2)
    binary_val = BinaryValue(value=alt_val, n_bits=n_bits)
    alternating = {
        "scenario": "Alternating Pattern",
        "input variable": [{"in": binary_val.binstr}],
    }
    scenarios.append(alternating)

    # Scenario 5: Random Distribution
    random_patterns = []
    for _ in range(3):
        val = random.getrandbits(n_bits)
        binary_val = BinaryValue(value=val, n_bits=n_bits)
        random_patterns.append({"in": binary_val.binstr})
    scenarios.append(
        {"scenario": "Random Distribution", "input variable": random_patterns}
    )

    # Scenario 6: Walking Ones
    walking_patterns = []
    for width in [8, 16, 32]:
        patterns = gen_walking_ones(width, n_bits)
        walking_patterns.extend([{"in": pattern} for pattern in patterns[:2]])
    scenarios.append({"scenario": "Walking Ones", "input variable": walking_patterns})

    # Scenario 7: Sparse Pattern (10% density)
    sparse = {
        "scenario": "Sparse Pattern",
        "input variable": [{"in": gen_random_with_density(n_bits, 0.1)}],
    }
    scenarios.append(sparse)

    # Scenario 8: Dense Pattern (90% density)
    dense = {
        "scenario": "Dense Pattern",
        "input variable": [{"in": gen_random_with_density(n_bits, 0.9)}],
    }
    scenarios.append(dense)

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
