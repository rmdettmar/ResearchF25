import json

from cocotb.binary import BinaryValue


def generate_walking_ones():
    patterns = []
    for i in range(8):
        val = BinaryValue(value=(1 << i), n_bits=8)
        patterns.append({"in": val.binstr})
    return patterns


def generate_multiple_bits():
    test_values = [0x03, 0x0F, 0xFF]
    patterns = []
    for val in test_values:
        binary_val = BinaryValue(value=val, n_bits=8)
        patterns.append({"in": binary_val.binstr})
    return patterns


def generate_alternating():
    test_values = [0x55, 0xAA]
    patterns = []
    for val in test_values:
        binary_val = BinaryValue(value=val, n_bits=8)
        patterns.append({"in": binary_val.binstr})
    return patterns


def generate_random_patterns():
    import random

    patterns = []
    for _ in range(5):
        val = random.randint(0, 255)
        binary_val = BinaryValue(value=val, n_bits=8)
        patterns.append({"in": binary_val.binstr})
    return patterns


def stimulus_gen():
    scenarios = [
        {"scenario": "Single Bit Test", "input variable": generate_walking_ones()},
        {"scenario": "Multiple Bits Test", "input variable": generate_multiple_bits()},
        {"scenario": "Zero Input Test", "input variable": [{"in": "00000000"}]},
        {
            "scenario": "Alternating Pattern Test",
            "input variable": generate_alternating(),
        },
        {"scenario": "Walking Ones Test", "input variable": generate_walking_ones()},
        {
            "scenario": "Random Pattern Test",
            "input variable": generate_random_patterns(),
        },
        {
            "scenario": "Boundary Value Test",
            "input variable": [{"in": "11111111"}, {"in": "10000000"}],
        },
    ]
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
