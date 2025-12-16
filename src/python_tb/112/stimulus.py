import json

from cocotb.binary import BinaryValue


def gen_16bit_str(value):
    return BinaryValue(value=value, n_bits=16).binstr


def gen_4bit_str(value):
    return BinaryValue(value=value, n_bits=4).binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Valid Selection Testing
    valid_sel = {"scenario": "Valid Selection Testing", "input variable": []}
    for sel in range(9):
        inputs = {
            "a": gen_16bit_str(0x1111),
            "b": gen_16bit_str(0x2222),
            "c": gen_16bit_str(0x3333),
            "d": gen_16bit_str(0x4444),
            "e": gen_16bit_str(0x5555),
            "f": gen_16bit_str(0x6666),
            "g": gen_16bit_str(0x7777),
            "h": gen_16bit_str(0x8888),
            "i": gen_16bit_str(0x9999),
            "sel": gen_4bit_str(sel),
        }
        valid_sel["input variable"].append(inputs)
    scenarios.append(valid_sel)

    # Scenario 2: Invalid Selection Testing
    invalid_sel = {"scenario": "Invalid Selection Testing", "input variable": []}
    for sel in range(9, 16):
        inputs = {
            "a": gen_16bit_str(0x0000),
            "b": gen_16bit_str(0x0000),
            "c": gen_16bit_str(0x0000),
            "d": gen_16bit_str(0x0000),
            "e": gen_16bit_str(0x0000),
            "f": gen_16bit_str(0x0000),
            "g": gen_16bit_str(0x0000),
            "h": gen_16bit_str(0x0000),
            "i": gen_16bit_str(0x0000),
            "sel": gen_4bit_str(sel),
        }
        invalid_sel["input variable"].append(inputs)
    scenarios.append(invalid_sel)

    # Scenario 3: Alternating Bit Patterns
    alt_patterns = {"scenario": "Alternating Bit Patterns", "input variable": []}
    for sel in range(9):
        inputs = {
            "a": gen_16bit_str(0x5555),
            "b": gen_16bit_str(0xAAAA),
            "c": gen_16bit_str(0x5555),
            "d": gen_16bit_str(0xAAAA),
            "e": gen_16bit_str(0x5555),
            "f": gen_16bit_str(0xAAAA),
            "g": gen_16bit_str(0x5555),
            "h": gen_16bit_str(0xAAAA),
            "i": gen_16bit_str(0x5555),
            "sel": gen_4bit_str(sel),
        }
        alt_patterns["input variable"].append(inputs)
    scenarios.append(alt_patterns)

    # Scenario 4: Boundary Value Testing
    boundary = {
        "scenario": "Boundary Value Testing",
        "input variable": [
            {
                "a": gen_16bit_str(0xFFFF),
                "b": gen_16bit_str(0xFFFF),
                "c": gen_16bit_str(0xFFFF),
                "d": gen_16bit_str(0xFFFF),
                "e": gen_16bit_str(0xFFFF),
                "f": gen_16bit_str(0xFFFF),
                "g": gen_16bit_str(0xFFFF),
                "h": gen_16bit_str(0xFFFF),
                "i": gen_16bit_str(0xFFFF),
                "sel": gen_4bit_str(8),
            },
            {
                "a": gen_16bit_str(0xFFFF),
                "b": gen_16bit_str(0xFFFF),
                "c": gen_16bit_str(0xFFFF),
                "d": gen_16bit_str(0xFFFF),
                "e": gen_16bit_str(0xFFFF),
                "f": gen_16bit_str(0xFFFF),
                "g": gen_16bit_str(0xFFFF),
                "h": gen_16bit_str(0xFFFF),
                "i": gen_16bit_str(0xFFFF),
                "sel": gen_4bit_str(9),
            },
        ],
    }
    scenarios.append(boundary)

    # Scenario 5: All-Zeros Input
    zeros = {"scenario": "All-Zeros Input", "input variable": []}
    for sel in range(16):
        inputs = {
            "a": gen_16bit_str(0x0000),
            "b": gen_16bit_str(0x0000),
            "c": gen_16bit_str(0x0000),
            "d": gen_16bit_str(0x0000),
            "e": gen_16bit_str(0x0000),
            "f": gen_16bit_str(0x0000),
            "g": gen_16bit_str(0x0000),
            "h": gen_16bit_str(0x0000),
            "i": gen_16bit_str(0x0000),
            "sel": gen_4bit_str(sel),
        }
        zeros["input variable"].append(inputs)
    scenarios.append(zeros)

    # Scenario 6: All-Ones Input
    ones = {"scenario": "All-Ones Input", "input variable": []}
    for sel in range(16):
        inputs = {
            "a": gen_16bit_str(0xFFFF),
            "b": gen_16bit_str(0xFFFF),
            "c": gen_16bit_str(0xFFFF),
            "d": gen_16bit_str(0xFFFF),
            "e": gen_16bit_str(0xFFFF),
            "f": gen_16bit_str(0xFFFF),
            "g": gen_16bit_str(0xFFFF),
            "h": gen_16bit_str(0xFFFF),
            "i": gen_16bit_str(0xFFFF),
            "sel": gen_4bit_str(sel),
        }
        ones["input variable"].append(inputs)
    scenarios.append(ones)

    # Scenario 7: Walking Ones
    walking = {"scenario": "Walking Ones", "input variable": []}
    for bit in range(16):
        inputs = {
            "a": gen_16bit_str(1 << bit),
            "b": gen_16bit_str(1 << ((bit + 1) % 16)),
            "c": gen_16bit_str(1 << ((bit + 2) % 16)),
            "d": gen_16bit_str(1 << ((bit + 3) % 16)),
            "e": gen_16bit_str(1 << ((bit + 4) % 16)),
            "f": gen_16bit_str(1 << ((bit + 5) % 16)),
            "g": gen_16bit_str(1 << ((bit + 6) % 16)),
            "h": gen_16bit_str(1 << ((bit + 7) % 16)),
            "i": gen_16bit_str(1 << ((bit + 8) % 16)),
            "sel": gen_4bit_str(bit % 9),
        }
        walking["input variable"].append(inputs)
    scenarios.append(walking)

    # Scenario 8: Rapid Selection Changes
    rapid = {"scenario": "Rapid Selection Changes", "input variable": []}
    test_data = 0xA5A5
    for sel in range(16):
        inputs = {
            "a": gen_16bit_str(test_data),
            "b": gen_16bit_str(test_data),
            "c": gen_16bit_str(test_data),
            "d": gen_16bit_str(test_data),
            "e": gen_16bit_str(test_data),
            "f": gen_16bit_str(test_data),
            "g": gen_16bit_str(test_data),
            "h": gen_16bit_str(test_data),
            "i": gen_16bit_str(test_data),
            "sel": gen_4bit_str(sel),
        }
        rapid["input variable"].append(inputs)
    scenarios.append(rapid)

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
