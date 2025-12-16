import json


def stimulus_gen():
    scenarios = []

    # Scenario 1: All Zero Inputs
    scenarios.append(
        {
            "scenario": "All Zero Inputs",
            "input variable": [{"a": "0", "b": "0", "c": "0", "d": "0"}],
        }
    )

    # Scenario 2: First AND Gate Active
    scenarios.append(
        {
            "scenario": "First AND Gate Active",
            "input variable": [{"a": "1", "b": "1", "c": "0", "d": "0"}],
        }
    )

    # Scenario 3: Second AND Gate Active
    scenarios.append(
        {
            "scenario": "Second AND Gate Active",
            "input variable": [{"a": "0", "b": "0", "c": "1", "d": "1"}],
        }
    )

    # Scenario 4: Both AND Gates Active
    scenarios.append(
        {
            "scenario": "Both AND Gates Active",
            "input variable": [{"a": "1", "b": "1", "c": "1", "d": "1"}],
        }
    )

    # Scenario 5: Single Input Transitions
    scenarios.append(
        {
            "scenario": "Single Input Transitions",
            "input variable": [
                {"a": "0", "b": "0", "c": "0", "d": "0"},
                {"a": "1", "b": "0", "c": "0", "d": "0"},
                {"a": "0", "b": "1", "c": "0", "d": "0"},
                {"a": "0", "b": "0", "c": "1", "d": "0"},
                {"a": "0", "b": "0", "c": "0", "d": "1"},
            ],
        }
    )

    # Scenario 6: Partial AND Activation
    scenarios.append(
        {
            "scenario": "Partial AND Activation",
            "input variable": [
                {"a": "1", "b": "0", "c": "0", "d": "0"},
                {"a": "0", "b": "1", "c": "0", "d": "0"},
                {"a": "0", "b": "0", "c": "1", "d": "0"},
                {"a": "0", "b": "0", "c": "0", "d": "1"},
            ],
        }
    )

    # Scenario 7: Glitch Detection
    scenarios.append(
        {
            "scenario": "Glitch Detection",
            "input variable": [
                {"a": "0", "b": "0", "c": "0", "d": "0"},
                {"a": "1", "b": "1", "c": "0", "d": "0"},
                {"a": "0", "b": "0", "c": "1", "d": "1"},
                {"a": "1", "b": "1", "c": "1", "d": "1"},
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
