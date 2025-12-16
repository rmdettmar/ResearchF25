import json

from cocotb.binary import BinaryValue


def create_5bit_bin(value):
    binary_val = BinaryValue(value=value, n_bits=5)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: All Zeros Input
    scenarios.append(
        {
            "scenario": "All Zeros Input",
            "input variable": [
                {
                    "a": "00000",
                    "b": "00000",
                    "c": "00000",
                    "d": "00000",
                    "e": "00000",
                    "f": "00000",
                }
            ],
        }
    )

    # Scenario 2: All Ones Input
    scenarios.append(
        {
            "scenario": "All Ones Input",
            "input variable": [
                {
                    "a": "11111",
                    "b": "11111",
                    "c": "11111",
                    "d": "11111",
                    "e": "11111",
                    "f": "11111",
                }
            ],
        }
    )

    # Scenario 3: Alternating Patterns
    scenarios.append(
        {
            "scenario": "Alternating Patterns",
            "input variable": [
                {
                    "a": "10101",
                    "b": "01010",
                    "c": "10101",
                    "d": "01010",
                    "e": "10101",
                    "f": "01010",
                }
            ],
        }
    )

    # Scenario 4: Walking Ones
    walking_ones = []
    for i in range(30):
        pos = i // 5
        val = 1 << (4 - (i % 5))
        inputs = {
            "a": "00000",
            "b": "00000",
            "c": "00000",
            "d": "00000",
            "e": "00000",
            "f": "00000",
        }
        if pos == 0:
            inputs["a"] = create_5bit_bin(val)
        elif pos == 1:
            inputs["b"] = create_5bit_bin(val)
        elif pos == 2:
            inputs["c"] = create_5bit_bin(val)
        elif pos == 3:
            inputs["d"] = create_5bit_bin(val)
        elif pos == 4:
            inputs["e"] = create_5bit_bin(val)
        else:
            inputs["f"] = create_5bit_bin(val)
        walking_ones.append(inputs)
    scenarios.append({"scenario": "Walking Ones", "input variable": walking_ones})

    # Scenario 5: Boundary Pattern
    scenarios.append(
        {
            "scenario": "Boundary Pattern",
            "input variable": [
                {
                    "a": "11111",
                    "b": "01111",
                    "c": "00111",
                    "d": "00011",
                    "e": "00001",
                    "f": "00000",
                }
            ],
        }
    )

    # Scenario 6: Random Values
    import random

    random.seed(42)  # For reproducibility
    scenarios.append(
        {
            "scenario": "Random Values",
            "input variable": [
                {
                    "a": create_5bit_bin(random.randint(0, 31)),
                    "b": create_5bit_bin(random.randint(0, 31)),
                    "c": create_5bit_bin(random.randint(0, 31)),
                    "d": create_5bit_bin(random.randint(0, 31)),
                    "e": create_5bit_bin(random.randint(0, 31)),
                    "f": create_5bit_bin(random.randint(0, 31)),
                }
            ],
        }
    )

    # Scenario 7: LSB Padding Verification
    scenarios.append(
        {
            "scenario": "LSB Padding Verification",
            "input variable": [
                {
                    "a": "10101",
                    "b": "11001",
                    "c": "00110",
                    "d": "11100",
                    "e": "01011",
                    "f": "10010",
                }
            ],
        }
    )

    # Scenario 8: Cross-boundary Splitting
    scenarios.append(
        {
            "scenario": "Cross-boundary Splitting",
            "input variable": [
                {
                    "a": "11000",
                    "b": "00111",
                    "c": "11000",
                    "d": "00111",
                    "e": "11000",
                    "f": "00111",
                }
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
