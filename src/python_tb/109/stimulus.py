import json

from cocotb.binary import BinaryValue


def create_binary_string(value, width=100):
    binary_val = BinaryValue(value=value, n_bits=width, bigEndian=True)
    return binary_val.binstr


def walking_pattern(width, value):
    patterns = []
    for i in range(width):
        pattern = (1 << i) if value == 1 else ((1 << width) - 1) ^ (1 << i)
        patterns.append(create_binary_string(pattern, width))
    return patterns


def stimulus_gen():
    scenarios = []

    # Scenario 1: All Zeros Input
    scenarios.append(
        {"scenario": "All Zeros Input", "input variable": [{"in": "0" * 100}]}
    )

    # Scenario 2: All Ones Input
    scenarios.append(
        {"scenario": "All Ones Input", "input variable": [{"in": "1" * 100}]}
    )

    # Scenario 3: Alternating Bits
    alt_pattern = "".join(["10"] * 50)
    scenarios.append(
        {"scenario": "Alternating Bits", "input variable": [{"in": alt_pattern}]}
    )

    # Scenario 4: Left Edge Case
    left_edge = "1" + "0" * 98 + "1"  # Setting in[99] and in[0] to 1
    scenarios.append(
        {"scenario": "Left Edge Case", "input variable": [{"in": left_edge}]}
    )

    # Scenario 5: Right Edge Case
    right_edge = "0" * 98 + "11"  # Setting in[1] and in[0] to 1
    scenarios.append(
        {"scenario": "Right Edge Case", "input variable": [{"in": right_edge}]}
    )

    # Scenario 6: Walking One
    walk_one_seq = {
        "scenario": "Walking One",
        "input variable": [{"in": pattern} for pattern in walking_pattern(100, 1)],
    }
    scenarios.append(walk_one_seq)

    # Scenario 7: Walking Zero
    walk_zero_seq = {
        "scenario": "Walking Zero",
        "input variable": [{"in": pattern} for pattern in walking_pattern(100, 0)],
    }
    scenarios.append(walk_zero_seq)

    # Scenario 8: Random Patterns
    import random

    random.seed(42)  # For reproducibility
    random_patterns = []
    for _ in range(5):
        random_val = random.getrandbits(100)
        random_patterns.append({"in": create_binary_string(random_val)})
    scenarios.append({"scenario": "Random Patterns", "input variable": random_patterns})

    # Scenario 9: Wrap-around Verification
    wrap_patterns = [
        "1" + "0" * 98 + "1",  # in[99] and in[0] both 1
        "1" + "0" * 98 + "0",  # in[99]=1, in[0]=0
        "0" + "0" * 98 + "1",  # in[99]=0, in[0]=1
        "0" + "0" * 98 + "0",  # in[99] and in[0] both 0
    ]
    scenarios.append(
        {
            "scenario": "Wrap-around Verification",
            "input variable": [{"in": pattern} for pattern in wrap_patterns],
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
