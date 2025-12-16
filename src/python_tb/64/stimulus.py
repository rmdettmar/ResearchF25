import json


def stimulus_gen():
    scenarios = []

    # Helper function to create a scenario dictionary
    def create_scenario(name, input_sequence):
        return {
            "scenario": name,
            "input variable": [{"in": val} for val in input_sequence],
        }

    # Scenario 1: All Zeros Input
    scenarios.append(create_scenario("All Zeros Input", ["000"]))

    # Scenario 2: All Ones Input
    scenarios.append(create_scenario("All Ones Input", ["111"]))

    # Scenario 3: Single One Patterns
    scenarios.append(create_scenario("Single One Patterns", ["001", "010", "100"]))

    # Scenario 4: Double One Patterns
    scenarios.append(create_scenario("Double One Patterns", ["011", "101", "110"]))

    # Scenario 5: Sequential Pattern
    scenarios.append(
        create_scenario(
            "Sequential Pattern",
            ["000", "001", "010", "011", "100", "101", "110", "111"],
        )
    )

    # Scenario 6: Random Transitions
    random_sequence = ["000", "111", "010", "101", "001", "110", "100", "011"]
    scenarios.append(create_scenario("Random Transitions", random_sequence))

    # Scenario 7: Rapid Input Changes
    rapid_sequence = ["000", "111", "000", "111", "000", "111"]
    scenarios.append(create_scenario("Rapid Input Changes", rapid_sequence))

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
