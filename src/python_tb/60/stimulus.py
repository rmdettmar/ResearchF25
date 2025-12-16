import json


def create_stimulus_sequence(reset_val, cycles):
    return {"clk": "1", "reset": reset_val}


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Counting Operation
    basic_count = {
        "scenario": "Basic Counting Operation",
        "input variable": [{"clk": "1", "reset": "0"} for _ in range(1000)],
    }
    scenarios.append(basic_count)

    # Scenario 2: Synchronous Reset
    sync_reset = {
        "scenario": "Synchronous Reset",
        "input variable": [{"clk": "1", "reset": "0"} for _ in range(5)]
        + [{"clk": "1", "reset": "1"}]
        + [{"clk": "1", "reset": "0"} for _ in range(5)],
    }
    scenarios.append(sync_reset)

    # Scenario 3: Reset During Active Count
    reset_mid_count = {
        "scenario": "Reset During Active Count",
        "input variable": [{"clk": "1", "reset": "0"} for _ in range(500)]
        + [{"clk": "1", "reset": "1"}]
        + [{"clk": "1", "reset": "0"} for _ in range(10)],
    }
    scenarios.append(reset_mid_count)

    # Scenario 4: Maximum Value Rollover
    max_rollover = {
        "scenario": "Maximum Value Rollover",
        "input variable": [{"clk": "1", "reset": "0"} for _ in range(1005)],
    }
    scenarios.append(max_rollover)

    # Scenario 5: Multiple Period Verification
    multi_period = {
        "scenario": "Multiple Period Verification",
        "input variable": [{"clk": "1", "reset": "0"} for _ in range(3000)],
    }
    scenarios.append(multi_period)

    # Scenario 6: Reset at Boundary Condition
    reset_at_max = {
        "scenario": "Reset at Boundary Condition",
        "input variable": [{"clk": "1", "reset": "0"} for _ in range(999)]
        + [{"clk": "1", "reset": "1"}]
        + [{"clk": "1", "reset": "0"} for _ in range(10)],
    }
    scenarios.append(reset_at_max)

    # Scenario 7: Initial Power-up State
    power_up = {
        "scenario": "Initial Power-up State",
        "input variable": [{"clk": "1", "reset": "0"} for _ in range(10)],
    }
    scenarios.append(power_up)

    # Scenario 8: Rapid Reset Toggling
    rapid_reset = {"scenario": "Rapid Reset Toggling", "input variable": []}
    for _ in range(5):
        rapid_reset["input variable"].extend(
            [
                {"clk": "1", "reset": "1"},
                {"clk": "1", "reset": "0"},
                {"clk": "1", "reset": "0"},
            ]
        )
    scenarios.append(rapid_reset)

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
