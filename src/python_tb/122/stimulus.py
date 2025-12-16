import json


def stimulus_gen():
    scenarios = []

    # Helper function to create a stimulus sequence
    def create_sequence(scenario_name, input_list):
        return {"scenario": scenario_name, "input variable": input_list}

    # Scenario 1: Basic State Transitions
    basic_transitions = [
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},  # Initial state
        {"clk": "0", "j": "1", "k": "0", "areset": "0"},  # OFF->ON
        {"clk": "1", "j": "1", "k": "0", "areset": "0"},
        {"clk": "0", "j": "0", "k": "1", "areset": "0"},  # ON->OFF
        {"clk": "1", "j": "0", "k": "1", "areset": "0"},
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},  # OFF->OFF
        {"clk": "1", "j": "0", "k": "0", "areset": "0"},
    ]
    scenarios.append(create_sequence("Basic State Transitions", basic_transitions))

    # Scenario 2: Asynchronous Reset During OFF
    reset_off = [
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},
        {"clk": "1", "j": "0", "k": "0", "areset": "0"},
        {"clk": "0", "j": "0", "k": "0", "areset": "1"},
        {"clk": "1", "j": "0", "k": "0", "areset": "1"},
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},
    ]
    scenarios.append(create_sequence("Asynchronous Reset During OFF", reset_off))

    # Scenario 3: Asynchronous Reset During ON
    reset_on = [
        {"clk": "0", "j": "1", "k": "0", "areset": "0"},  # Go to ON state
        {"clk": "1", "j": "1", "k": "0", "areset": "0"},
        {"clk": "0", "j": "0", "k": "0", "areset": "1"},  # Assert reset
        {"clk": "1", "j": "0", "k": "0", "areset": "1"},
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},  # Release reset
    ]
    scenarios.append(create_sequence("Asynchronous Reset During ON", reset_on))

    # Scenario 4: Input Changes at Clock Edge
    clock_edge = [
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},
        {"clk": "1", "j": "1", "k": "0", "areset": "0"},  # Change j at clock edge
        {"clk": "0", "j": "1", "k": "0", "areset": "0"},
        {"clk": "1", "j": "0", "k": "1", "areset": "0"},  # Change k at clock edge
    ]
    scenarios.append(create_sequence("Input Changes at Clock Edge", clock_edge))

    # Scenario 5: Simultaneous J/K Changes
    simultaneous = [
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},
        {"clk": "1", "j": "1", "k": "1", "areset": "0"},  # Both change
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},
        {"clk": "1", "j": "1", "k": "1", "areset": "0"},
    ]
    scenarios.append(create_sequence("Simultaneous J/K Changes", simultaneous))

    # Scenario 6: Reset Release Timing
    reset_timing = [
        {"clk": "0", "j": "0", "k": "0", "areset": "1"},
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},  # Release before clock edge
        {"clk": "1", "j": "0", "k": "0", "areset": "0"},
        {"clk": "0", "j": "0", "k": "0", "areset": "1"},
        {"clk": "1", "j": "0", "k": "0", "areset": "0"},  # Release at clock edge
    ]
    scenarios.append(create_sequence("Reset Release Timing", reset_timing))

    # Scenario 7: Input Glitch Immunity
    glitch = [
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},
        {"clk": "0", "j": "1", "k": "0", "areset": "0"},  # Glitch on j
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},
        {"clk": "1", "j": "0", "k": "0", "areset": "0"},
    ]
    scenarios.append(create_sequence("Input Glitch Immunity", glitch))

    # Scenario 8: Power-On State
    power_on = [
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},  # Initial state
        {"clk": "1", "j": "0", "k": "0", "areset": "0"},
        {"clk": "0", "j": "0", "k": "0", "areset": "0"},
        {"clk": "1", "j": "0", "k": "0", "areset": "0"},
    ]
    scenarios.append(create_sequence("Power-On State", power_on))

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
