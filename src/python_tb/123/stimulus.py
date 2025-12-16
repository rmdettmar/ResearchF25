import json


def stimulus_gen():
    # List to store all test scenarios
    scenarios = []

    # Basic Output Verification
    scenarios.append(
        {
            "scenario": "Basic Output Verification",
            "input variable": [{}] * 10,  # 10 cycles of monitoring
        }
    )

    # Power-on State
    scenarios.append(
        {
            "scenario": "Power-on State",
            "input variable": [{}] * 5,  # 5 cycles after power-on
        }
    )

    # Long-term Stability
    scenarios.append(
        {
            "scenario": "Long-term Stability",
            "input variable": [{}] * 1000,  # 1000 cycles of monitoring
        }
    )

    # Reset Behavior
    scenarios.append(
        {
            "scenario": "Reset Behavior",
            "input variable": [{}] * 20,  # 20 cycles during/after reset
        }
    )

    # Clock Edge Response
    scenarios.append(
        {
            "scenario": "Clock Edge Response",
            "input variable": [{}] * 50,  # 50 cycles across multiple clock edges
        }
    )

    # Output Load Variation
    scenarios.append(
        {
            "scenario": "Output Load Variation",
            "input variable": [{}] * 30,  # 30 cycles under different loads
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
