import json

from cocotb.binary import BinaryValue


def bin3(val):
    # Convert integer to 3-bit binary string
    return BinaryValue(value=val, n_bits=3).binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: All Zeros Input
    scenarios.append(
        {"scenario": "All Zeros Input", "input variable": [{"a": "000", "b": "000"}]}
    )

    # Scenario 2: All Ones Input
    scenarios.append(
        {"scenario": "All Ones Input", "input variable": [{"a": "111", "b": "111"}]}
    )

    # Scenario 3: Alternating Bits
    scenarios.append(
        {"scenario": "Alternating Bits", "input variable": [{"a": "101", "b": "010"}]}
    )

    # Scenario 4: Single Bit Set
    scenarios.append(
        {"scenario": "Single Bit Set", "input variable": [{"a": "001", "b": "100"}]}
    )

    # Scenario 5: Complementary Inputs
    scenarios.append(
        {
            "scenario": "Complementary Inputs",
            "input variable": [{"a": "110", "b": "001"}],
        }
    )

    # Scenario 6: Sequential Bit Patterns
    seq_patterns = []
    for a in range(8):  # 0 to 7 for 3 bits
        for b in range(8):
            seq_patterns.append({"a": bin3(a), "b": bin3(b)})
    scenarios.append(
        {"scenario": "Sequential Bit Patterns", "input variable": seq_patterns}
    )

    # Scenario 7: Output Bit Position Verification
    scenarios.append(
        {
            "scenario": "Output Bit Position Verification",
            "input variable": [
                {"a": "101", "b": "010"},
                {"a": "011", "b": "100"},
                {"a": "110", "b": "001"},
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
