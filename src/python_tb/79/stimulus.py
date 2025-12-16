import json


def stimulus_gen():
    scenarios = []

    def gen_clock_cycle(a_val):
        # Generate one clock cycle worth of inputs
        return {"clk": "0", "a": a_val}, {"clk": "1", "a": a_val}

    # Scenario 1: Initial State Verification
    scenario1 = {
        "scenario": "Initial State Verification",
        "input variable": [{"clk": "0", "a": "1"}, {"clk": "1", "a": "1"}],
    }
    scenarios.append(scenario1)

    # Scenario 2: Stable Output with a=1
    scenario2 = {"scenario": "Stable Output with a=1", "input variable": []}
    for _ in range(4):  # Test for 4 clock cycles
        low, high = gen_clock_cycle("1")
        scenario2["input variable"].extend([low, high])
    scenarios.append(scenario2)

    # Scenario 3: Transition to Counting Mode
    scenario3 = {"scenario": "Transition to Counting Mode", "input variable": []}
    for _ in range(5):  # Test complete counting sequence
        low, high = gen_clock_cycle("0")
        scenario3["input variable"].extend([low, high])
    scenarios.append(scenario3)

    # Scenario 4: Counter Rollover
    scenario4 = {"scenario": "Counter Rollover", "input variable": []}
    for _ in range(8):  # Test through rollover and beyond
        low, high = gen_clock_cycle("0")
        scenario4["input variable"].extend([low, high])
    scenarios.append(scenario4)

    # Scenario 5: Mode Switch During Count
    scenario5 = {"scenario": "Mode Switch During Count", "input variable": []}
    for i in range(4):
        a_val = "0" if i < 2 else "1"
        low, high = gen_clock_cycle(a_val)
        scenario5["input variable"].extend([low, high])
    scenarios.append(scenario5)

    # Scenario 6: Clock Edge Sensitivity
    scenario6 = {
        "scenario": "Clock Edge Sensitivity",
        "input variable": [
            {"clk": "0", "a": "0"},
            {"clk": "1", "a": "0"},
            {"clk": "0", "a": "0"},
        ],
    }
    scenarios.append(scenario6)

    # Scenario 7: Multiple Mode Transitions
    scenario7 = {"scenario": "Multiple Mode Transitions", "input variable": []}
    for i in range(6):
        a_val = "1" if i % 2 == 0 else "0"
        low, high = gen_clock_cycle(a_val)
        scenario7["input variable"].extend([low, high])
    scenarios.append(scenario7)

    # Scenario 8: Long-term Stability
    scenario8 = {"scenario": "Long-term Stability", "input variable": []}
    for _ in range(10):  # Run for 10 complete cycles
        low, high = gen_clock_cycle("0")
        scenario8["input variable"].extend([low, high])
    scenarios.append(scenario8)

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
