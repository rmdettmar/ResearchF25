import json


def stimulus_gen():
    scenarios = []

    # Helper function to create a sequence dictionary
    def create_sequence(name, signals):
        return {"scenario": name, "input variable": signals}

    # Scenario 1: Normal Data Capture
    normal_signals = [
        {"clk": "0", "d": "0", "ar": "0"},
        {"clk": "1", "d": "0", "ar": "0"},
        {"clk": "0", "d": "1", "ar": "0"},
        {"clk": "1", "d": "1", "ar": "0"},
        {"clk": "0", "d": "0", "ar": "0"},
        {"clk": "1", "d": "0", "ar": "0"},
    ]
    scenarios.append(create_sequence("Normal Data Capture", normal_signals))

    # Scenario 2: Asynchronous Reset Assertion
    reset_signals = [
        {"clk": "0", "d": "1", "ar": "0"},
        {"clk": "0", "d": "1", "ar": "1"},
        {"clk": "1", "d": "1", "ar": "1"},
        {"clk": "0", "d": "1", "ar": "1"},
    ]
    scenarios.append(create_sequence("Asynchronous Reset Assertion", reset_signals))

    # Scenario 3: Reset Recovery
    recovery_signals = [
        {"clk": "0", "d": "1", "ar": "1"},
        {"clk": "0", "d": "1", "ar": "0"},
        {"clk": "1", "d": "1", "ar": "0"},
        {"clk": "0", "d": "1", "ar": "0"},
    ]
    scenarios.append(create_sequence("Reset Recovery", recovery_signals))

    # Scenario 4: Setup Time Verification
    setup_signals = [
        {"clk": "0", "d": "0", "ar": "0"},
        {"clk": "0", "d": "1", "ar": "0"},
        {"clk": "1", "d": "1", "ar": "0"},
        {"clk": "0", "d": "1", "ar": "0"},
    ]
    scenarios.append(create_sequence("Setup Time Verification", setup_signals))

    # Scenario 5: Hold Time Verification
    hold_signals = [
        {"clk": "0", "d": "1", "ar": "0"},
        {"clk": "1", "d": "1", "ar": "0"},
        {"clk": "1", "d": "0", "ar": "0"},
        {"clk": "0", "d": "0", "ar": "0"},
    ]
    scenarios.append(create_sequence("Hold Time Verification", hold_signals))

    # Scenario 6: Clock Edge Sensitivity
    edge_signals = [
        {"clk": "0", "d": "1", "ar": "0"},
        {"clk": "1", "d": "1", "ar": "0"},
        {"clk": "0", "d": "0", "ar": "0"},
        {"clk": "1", "d": "0", "ar": "0"},
    ]
    scenarios.append(create_sequence("Clock Edge Sensitivity", edge_signals))

    # Scenario 7: Reset During Clock Edge
    reset_edge_signals = [
        {"clk": "0", "d": "1", "ar": "0"},
        {"clk": "1", "d": "1", "ar": "1"},
        {"clk": "0", "d": "1", "ar": "1"},
        {"clk": "1", "d": "1", "ar": "1"},
    ]
    scenarios.append(create_sequence("Reset During Clock Edge", reset_edge_signals))

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
