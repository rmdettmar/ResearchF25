import json


def stimulus_gen():
    # Helper function to convert integer to binary string with specified width
    def int_to_bin(value, width=4):
        return format(value, f"0{width}b")

    scenarios = []

    # Scenario 1: All Zeros Input
    scenarios.append(
        {"scenario": "All Zeros Input", "input variable": [{"in": "0000"}]}
    )

    # Scenario 2: All Ones Input
    scenarios.append({"scenario": "All Ones Input", "input variable": [{"in": "1111"}]})

    # Scenario 3: Single One Input
    single_one_patterns = ["0001", "0010", "0100", "1000"]
    scenarios.append(
        {
            "scenario": "Single One Input",
            "input variable": [{"in": pattern} for pattern in single_one_patterns],
        }
    )

    # Scenario 4: Three Ones Input
    three_ones_patterns = ["1110", "1101", "1011", "0111"]
    scenarios.append(
        {
            "scenario": "Three Ones Input",
            "input variable": [{"in": pattern} for pattern in three_ones_patterns],
        }
    )

    # Scenario 5: Alternating Patterns
    alternating_patterns = ["0101", "1010"]
    scenarios.append(
        {
            "scenario": "Alternating Patterns",
            "input variable": [{"in": pattern} for pattern in alternating_patterns],
        }
    )

    # Scenario 6: Random Combinations
    import random

    random_patterns = [int_to_bin(random.randint(0, 15)) for _ in range(4)]
    scenarios.append(
        {
            "scenario": "Random Combinations",
            "input variable": [{"in": pattern} for pattern in random_patterns],
        }
    )

    # Scenario 7: Input Transitions
    transition_patterns = ["0000", "1111", "0101", "1010", "1100", "0011"]
    scenarios.append(
        {
            "scenario": "Input Transitions",
            "input variable": [{"in": pattern} for pattern in transition_patterns],
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
