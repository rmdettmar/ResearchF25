import json


def stimulus_gen():
    # Create list to store all test scenarios
    test_scenarios = []

    # Scenario 1: Basic Output Verification
    test_scenarios.append(
        {"scenario": "Basic Output Verification", "input variable": [{}]}
    )

    # Scenario 2: Power-on State
    test_scenarios.append({"scenario": "Power-on State", "input variable": [{}]})

    # Scenario 3: Long-term Stability
    test_scenarios.append(
        {
            "scenario": "Long-term Stability",
            "input variable": [{}] * 1000,  # Monitor for 1000 cycles
        }
    )

    # Scenario 4: Clock Edge Behavior
    test_scenarios.append(
        {
            "scenario": "Clock Edge Behavior",
            "input variable": [{}] * 10,  # Monitor across multiple clock edges
        }
    )

    # Scenario 5: Reset Condition
    test_scenarios.append({"scenario": "Reset Condition", "input variable": [{}]})

    return test_scenarios


if __name__ == "__main__":
    result = stimulus_gen()
    # 将结果转换为 JSON 字符串
    if isinstance(result, list):
        result = json.dumps(result, indent=4)
    elif not isinstance(result, str):
        result = json.dumps(result, indent=4)

    with open("stimulus.json", "w") as f:
        f.write(result)
