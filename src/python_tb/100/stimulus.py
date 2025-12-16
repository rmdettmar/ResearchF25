import json

from cocotb.binary import BinaryValue


def get_binary_string(value, width=8):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: All Zeros Input
    scenarios.append(
        {"scenario": "All Zeros Input", "input variable": [{"in": "00000000"}]}
    )

    # Scenario 2: All Ones Input
    scenarios.append(
        {"scenario": "All Ones Input", "input variable": [{"in": "11111111"}]}
    )

    # Scenario 3: Single Bit Set
    single_bit_sequence = []
    for i in range(8):
        single_bit_sequence.append({"in": get_binary_string(1 << i)})
    scenarios.append(
        {"scenario": "Single Bit Set", "input variable": single_bit_sequence}
    )

    # Scenario 4: Alternating Bits
    scenarios.append(
        {
            "scenario": "Alternating Bits",
            "input variable": [{"in": "01010101"}, {"in": "10101010"}],  # 0x55  # 0xAA
        }
    )

    # Scenario 5: Random Data Pattern
    random_patterns = [
        {"in": "10110011"},  # 0xB3
        {"in": "11001010"},  # 0xCA
        {"in": "01101001"},  # 0x69
        {"in": "11110000"},  # 0xF0
    ]
    scenarios.append(
        {"scenario": "Random Data Pattern", "input variable": random_patterns}
    )

    # Scenario 6: Walking Ones
    walking_ones = []
    for i in range(8):
        walking_ones.append({"in": get_binary_string(1 << i)})
    scenarios.append({"scenario": "Walking Ones", "input variable": walking_ones})

    # Scenario 7: Adjacent Bit Pairs
    adjacent_pairs = [
        {"in": "00000011"},  # 0x03
        {"in": "00001100"},  # 0x0C
        {"in": "00110000"},  # 0x30
        {"in": "11000000"},  # 0xC0
    ]
    scenarios.append(
        {"scenario": "Adjacent Bit Pairs", "input variable": adjacent_pairs}
    )

    # Scenario 8: Quick Toggle
    quick_toggle = [
        {"in": "00000000"},
        {"in": "11111111"},
        {"in": "10101010"},
        {"in": "01010101"},
    ]
    scenarios.append({"scenario": "Quick Toggle", "input variable": quick_toggle})

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
