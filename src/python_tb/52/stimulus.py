import json


def stimulus_gen():
    scenarios = []

    # Helper function to convert integer to binary string
    def to_bin(val, width=1):
        return format(val, f"0{width}b")

    # Scenario 1: Basic Counting Operation
    basic_count = {
        "scenario": "Basic Counting Operation",
        "input variable": [{"slowena": "1", "reset": "0"} for _ in range(10)],
    }
    scenarios.append(basic_count)

    # Scenario 2: Synchronous Reset
    sync_reset = {
        "scenario": "Synchronous Reset",
        "input variable": [
            {"slowena": "1", "reset": "0"},
            {"slowena": "1", "reset": "0"},
            {"slowena": "1", "reset": "0"},
            {"slowena": "1", "reset": "1"},  # Assert reset
            {"slowena": "1", "reset": "0"},
            {"slowena": "1", "reset": "0"},
        ],
    }
    scenarios.append(sync_reset)

    # Scenario 3: Counter Pause
    counter_pause = {
        "scenario": "Counter Pause",
        "input variable": [
            {"slowena": "1", "reset": "0"},
            {"slowena": "1", "reset": "0"},
            {"slowena": "0", "reset": "0"},  # Pause
            {"slowena": "0", "reset": "0"},  # Still paused
            {"slowena": "1", "reset": "0"},  # Resume
            {"slowena": "1", "reset": "0"},
        ],
    }
    scenarios.append(counter_pause)

    # Scenario 4: Rollover Verification
    rollover = {
        "scenario": "Rollover Verification",
        "input variable": [
            {"slowena": "1", "reset": "0"} for _ in range(11)
        ],  # Count through 9 and verify rollover to 0
    }
    scenarios.append(rollover)

    # Scenario 5: Reset Priority
    reset_priority = {
        "scenario": "Reset Priority",
        "input variable": [
            {"slowena": "1", "reset": "0"},
            {"slowena": "1", "reset": "0"},
            {"slowena": "1", "reset": "1"},  # Both active
            {"slowena": "1", "reset": "0"},
            {"slowena": "1", "reset": "0"},
        ],
    }
    scenarios.append(reset_priority)

    # Scenario 6: Boundary Value Testing
    boundary = {
        "scenario": "Boundary Value Testing",
        "input variable": [
            {"slowena": "1", "reset": "0"} for _ in range(12)
        ],  # Run through multiple cycles to verify range
    }
    scenarios.append(boundary)

    # Scenario 7: Initial Power-up State
    powerup = {
        "scenario": "Initial Power-up State",
        "input variable": [
            {"slowena": "0", "reset": "0"},
            {"slowena": "0", "reset": "0"},
            {"slowena": "0", "reset": "0"},
        ],
    }
    scenarios.append(powerup)

    # Scenario 8: Multiple Reset Cycles
    multiple_reset = {
        "scenario": "Multiple Reset Cycles",
        "input variable": [
            {"slowena": "1", "reset": "0"},
            {"slowena": "1", "reset": "1"},
            {"slowena": "1", "reset": "0"},
            {"slowena": "1", "reset": "0"},
            {"slowena": "1", "reset": "1"},
            {"slowena": "1", "reset": "0"},
        ],
    }
    scenarios.append(multiple_reset)

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
