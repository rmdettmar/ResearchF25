import json


def stimulus_gen():
    scenarios = []

    # Helper function to convert integer to 8-bit binary string
    def to_bin(val, width=8):
        return format(val & ((1 << width) - 1), f"0{width}b")

    # Scenario 1: Single Bit Transition
    single_bit = {
        "scenario": "Single Bit Transition",
        "input variable": [
            {"clk": "1", "in": "00000000"},
            {"clk": "1", "in": "00000001"},
            {"clk": "1", "in": "00000001"},
        ],
    }
    scenarios.append(single_bit)

    # Scenario 2: Multiple Simultaneous Transitions
    multi_trans = {
        "scenario": "Multiple Simultaneous Transitions",
        "input variable": [
            {"clk": "1", "in": "00000000"},
            {"clk": "1", "in": "11111111"},
            {"clk": "1", "in": "11111111"},
        ],
    }
    scenarios.append(multi_trans)

    # Scenario 3: No Transition Detection
    no_trans = {
        "scenario": "No Transition Detection",
        "input variable": [
            {"clk": "1", "in": "11111111"},
            {"clk": "1", "in": "11111111"},
            {"clk": "1", "in": "00000000"},
        ],
    }
    scenarios.append(no_trans)

    # Scenario 4: Alternating Patterns
    alt_pattern = {
        "scenario": "Alternating Patterns",
        "input variable": [
            {"clk": "1", "in": "01010101"},
            {"clk": "1", "in": "10101010"},
            {"clk": "1", "in": "01010101"},
        ],
    }
    scenarios.append(alt_pattern)

    # Scenario 5: Walking Ones Pattern
    walking_ones = {
        "scenario": "Walking Ones Pattern",
        "input variable": [
            {"clk": "1", "in": "00000001"},
            {"clk": "1", "in": "00000010"},
            {"clk": "1", "in": "00000100"},
            {"clk": "1", "in": "00001000"},
            {"clk": "1", "in": "00010000"},
            {"clk": "1", "in": "00100000"},
            {"clk": "1", "in": "01000000"},
            {"clk": "1", "in": "10000000"},
        ],
    }
    scenarios.append(walking_ones)

    # Scenario 6: Back-to-Back Transitions
    back_to_back = {
        "scenario": "Back-to-Back Transitions",
        "input variable": [
            {"clk": "1", "in": "00000000"},
            {"clk": "1", "in": "11111111"},
            {"clk": "1", "in": "00000000"},
            {"clk": "1", "in": "11111111"},
        ],
    }
    scenarios.append(back_to_back)

    # Scenario 7: Clock Cycle Boundary
    clock_boundary = {
        "scenario": "Clock Cycle Boundary",
        "input variable": [
            {"clk": "1", "in": "00000000"},
            {"clk": "1", "in": "11111111"},
            {"clk": "1", "in": "11111111"},
            {"clk": "1", "in": "11111111"},
        ],
    }
    scenarios.append(clock_boundary)

    # Scenario 8: Reset Condition
    reset_condition = {
        "scenario": "Reset Condition",
        "input variable": [
            {"clk": "1", "in": "00000000"},
            {"clk": "1", "in": "00000000"},
            {"clk": "1", "in": "00000000"},
            {"clk": "1", "in": "11111111"},
        ],
    }
    scenarios.append(reset_condition)

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
