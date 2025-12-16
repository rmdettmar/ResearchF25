import json


def stimulus_gen():
    scenarios = []

    # Helper function to generate clock cycles with specific reset value
    def gen_clock_cycles(num_cycles, reset_val):
        return [
            {"clk": "1", "reset": reset_val},
            {"clk": "0", "reset": reset_val},
        ] * num_cycles

    # Scenario 1: Initial Reset Behavior
    sequence = []
    sequence.extend(gen_clock_cycles(2, "0"))  # Initial cycles
    sequence.extend(gen_clock_cycles(4, "1"))  # Reset active
    sequence.extend(gen_clock_cycles(6, "0"))  # Monitor after reset
    scenarios.append({"scenario": "Initial Reset Behavior", "input variable": sequence})

    # Scenario 2: Multiple Reset Pulses
    sequence = []
    sequence.extend(gen_clock_cycles(4, "1"))  # First reset
    sequence.extend(gen_clock_cycles(6, "0"))  # Gap
    sequence.extend(gen_clock_cycles(4, "1"))  # Second reset
    sequence.extend(gen_clock_cycles(4, "0"))  # Monitor
    scenarios.append({"scenario": "Multiple Reset Pulses", "input variable": sequence})

    # Scenario 3: Reset During Active Shift
    sequence = []
    sequence.extend(gen_clock_cycles(2, "1"))  # Initial reset
    sequence.extend(gen_clock_cycles(2, "0"))  # During shift
    sequence.extend(gen_clock_cycles(4, "1"))  # New reset
    sequence.extend(gen_clock_cycles(4, "0"))  # Monitor
    scenarios.append(
        {"scenario": "Reset During Active Shift", "input variable": sequence}
    )

    # Scenario 4: Long-term Stability
    sequence = []
    sequence.extend(gen_clock_cycles(4, "1"))  # Reset
    sequence.extend(gen_clock_cycles(20, "0"))  # Long monitoring period
    scenarios.append({"scenario": "Long-term Stability", "input variable": sequence})

    # Scenario 5: Reset Timing Verification
    sequence = []
    sequence.extend([{"clk": "0", "reset": "0"}])  # Start at clock low
    sequence.extend([{"clk": "1", "reset": "1"}])  # Reset at clock high
    sequence.extend(gen_clock_cycles(5, "0"))  # Monitor synchronous behavior
    scenarios.append(
        {"scenario": "Reset Timing Verification", "input variable": sequence}
    )

    # Scenario 6: Glitch Immunity
    sequence = []
    sequence.extend([{"clk": "0", "reset": "0"}])
    sequence.extend([{"clk": "0", "reset": "1"}])  # Glitch during clock low
    sequence.extend([{"clk": "0", "reset": "0"}])
    sequence.extend(gen_clock_cycles(4, "0"))  # Monitor no response
    scenarios.append({"scenario": "Glitch Immunity", "input variable": sequence})

    # Scenario 7: Power-on State
    sequence = []
    sequence.extend(gen_clock_cycles(10, "0"))  # Monitor initial state
    scenarios.append({"scenario": "Power-on State", "input variable": sequence})

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
