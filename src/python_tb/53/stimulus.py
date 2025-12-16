import json


def stimulus_gen():
    scenarios = []

    # Scenario 1: All Input Combinations
    scenarios.append(
        {
            "scenario": "All Input Combinations",
            "input variable": [
                {"in1": "0", "in2": "0"},
                {"in1": "0", "in2": "1"},
                {"in1": "1", "in2": "0"},
                {"in1": "1", "in2": "1"},
            ],
        }
    )

    # Scenario 2: Input Transitions
    scenarios.append(
        {
            "scenario": "Input Transitions",
            "input variable": [
                {"in1": "0", "in2": "0"},
                {"in1": "0", "in2": "1"},
                {"in1": "1", "in2": "1"},
                {"in1": "1", "in2": "0"},
                {"in1": "0", "in2": "0"},
            ],
        }
    )

    # Scenario 3: Setup and Hold Times
    scenarios.append(
        {
            "scenario": "Setup and Hold Times",
            "input variable": [
                {"in1": "0", "in2": "0"},
                {"in1": "1", "in2": "0"},
                {"in1": "1", "in2": "0"},
                {"in1": "1", "in2": "1"},
            ],
        }
    )

    # Scenario 4: Propagation Delay
    scenarios.append(
        {
            "scenario": "Propagation Delay",
            "input variable": [
                {"in1": "0", "in2": "0"},
                {"in1": "1", "in2": "0"},
                {"in1": "0", "in2": "0"},
                {"in1": "1", "in2": "1"},
            ],
        }
    )

    # Scenario 5: Simultaneous Input Changes
    scenarios.append(
        {
            "scenario": "Simultaneous Input Changes",
            "input variable": [
                {"in1": "0", "in2": "0"},
                {"in1": "1", "in2": "1"},
                {"in1": "0", "in2": "0"},
                {"in1": "1", "in2": "0"},
            ],
        }
    )

    # Scenario 6: Input Signal Stability
    scenarios.append(
        {
            "scenario": "Input Signal Stability",
            "input variable": [
                {"in1": "1", "in2": "0"},
                {"in1": "1", "in2": "0"},
                {"in1": "1", "in2": "0"},
                {"in1": "1", "in2": "0"},
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
