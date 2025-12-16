import json

from cocotb.binary import BinaryValue


def stimulus_gen():
    scenarios = []

    # Helper function to format binary string
    def format_binary(value, width=8):
        binary = BinaryValue(value=value, n_bits=width)
        return binary.binstr

    # Scenario 1: All Zeros Pattern
    scenarios.append(
        {"scenario": "All Zeros Pattern", "input variable": [{"in": "00000000"}]}
    )

    # Scenario 2: All Ones Pattern
    scenarios.append(
        {"scenario": "All Ones Pattern", "input variable": [{"in": "11111111"}]}
    )

    # Scenario 3: Alternating Bits
    scenarios.append(
        {"scenario": "Alternating Bits", "input variable": [{"in": "10101010"}]}
    )

    # Scenario 4: Single Bit Set
    scenarios.append(
        {"scenario": "Single Bit Set", "input variable": [{"in": "10000000"}]}
    )

    # Scenario 5: Random Pattern
    scenarios.append(
        {"scenario": "Random Pattern", "input variable": [{"in": "10110101"}]}
    )

    # Scenario 6: Walking Ones
    walking_ones = []
    for i in range(8):
        walking_ones.append({"in": format_binary(1 << i)})
    scenarios.append({"scenario": "Walking Ones", "input variable": walking_ones})

    # Scenario 7: Palindrome Pattern
    scenarios.append(
        {"scenario": "Palindrome Pattern", "input variable": [{"in": "11000011"}]}
    )

    # Scenario 8: Rapid Input Changes
    rapid_changes = [
        {"in": "10101010"},
        {"in": "01010101"},
        {"in": "11110000"},
        {"in": "00001111"},
    ]
    scenarios.append(
        {"scenario": "Rapid Input Changes", "input variable": rapid_changes}
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
