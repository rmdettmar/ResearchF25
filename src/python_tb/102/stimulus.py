import json


def stimulus_gen():
    # List to store all test scenarios
    scenarios = []

    # Helper function to create binary strings
    def create_binary_str(value):
        return "1" if value else "0"

    # Scenario 1: All Zero Inputs
    scenarios.append(
        {
            "scenario": "All Zero Inputs",
            "input variable": [{"x": "0", "y": "0"} for _ in range(5)],
        }
    )

    # Scenario 2: Single High Input X
    scenarios.append(
        {
            "scenario": "Single High Input X",
            "input variable": [{"x": "1", "y": "0"} for _ in range(2)],
        }
    )

    # Scenario 3: Single High Input Y
    scenarios.append(
        {
            "scenario": "Single High Input Y",
            "input variable": [{"x": "0", "y": "1"} for _ in range(2)],
        }
    )

    # Scenario 4: Both Inputs High
    scenarios.append(
        {
            "scenario": "Both Inputs High",
            "input variable": [{"x": "1", "y": "1"} for _ in range(2)],
        }
    )

    # Scenario 5: Input Transitions
    scenarios.append(
        {
            "scenario": "Input Transitions",
            "input variable": [
                {"x": "0", "y": "0"},
                {"x": "0", "y": "1"},
                {"x": "1", "y": "1"},
                {"x": "0", "y": "1"},
                {"x": "1", "y": "0"},
            ],
        }
    )

    # Scenario 6: Glitch Detection
    scenarios.append(
        {
            "scenario": "Glitch Detection",
            "input variable": [
                {"x": "0", "y": "0"},
                {"x": "1", "y": "0"},
                {"x": "0", "y": "1"},
                {"x": "1", "y": "1"},
                {"x": "0", "y": "0"},
            ],
        }
    )

    # Scenario 7: Setup and Hold Times
    scenarios.append(
        {
            "scenario": "Setup and Hold Times",
            "input variable": [
                {"x": "0", "y": "0"},
                {"x": "1", "y": "0"},
                {"x": "0", "y": "1"},
                {"x": "1", "y": "1"},
                {"x": "0", "y": "0"},
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
