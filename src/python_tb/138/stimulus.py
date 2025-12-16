import json


def stimulus_gen():
    scenarios = []

    # Helper function to format binary values
    def format_inputs(a, b, cin):
        return {"a": f"{a:01b}", "b": f"{b:01b}", "cin": f"{cin:01b}"}

    # Scenario 1: Basic Addition Cases
    basic_cases = {
        "scenario": "Basic Addition Cases",
        "input variable": [
            format_inputs(0, 0, 0),
            format_inputs(0, 0, 1),
            format_inputs(0, 1, 0),
            format_inputs(0, 1, 1),
            format_inputs(1, 0, 0),
            format_inputs(1, 0, 1),
            format_inputs(1, 1, 0),
            format_inputs(1, 1, 1),
        ],
    }
    scenarios.append(basic_cases)

    # Scenario 2: Single Bit Transitions
    single_trans = {
        "scenario": "Single Bit Transitions",
        "input variable": [
            format_inputs(0, 0, 0),
            format_inputs(1, 0, 0),
            format_inputs(1, 1, 0),
            format_inputs(1, 1, 1),
        ],
    }
    scenarios.append(single_trans)

    # Scenario 3: Multiple Bit Transitions
    multi_trans = {
        "scenario": "Multiple Bit Transitions",
        "input variable": [
            format_inputs(0, 0, 0),
            format_inputs(1, 1, 1),
            format_inputs(0, 1, 0),
            format_inputs(1, 0, 1),
        ],
    }
    scenarios.append(multi_trans)

    # Scenario 4: Carry Propagation
    carry_prop = {
        "scenario": "Carry Propagation",
        "input variable": [
            format_inputs(0, 1, 1),
            format_inputs(1, 1, 0),
            format_inputs(1, 1, 1),
            format_inputs(1, 0, 1),
        ],
    }
    scenarios.append(carry_prop)

    # Scenario 5: Setup Time Verification
    setup_time = {
        "scenario": "Setup Time Verification",
        "input variable": [
            format_inputs(0, 0, 0),
            format_inputs(1, 0, 0),
            format_inputs(0, 1, 0),
            format_inputs(0, 0, 1),
        ],
    }
    scenarios.append(setup_time)

    # Scenario 6: Hold Time Verification
    hold_time = {
        "scenario": "Hold Time Verification",
        "input variable": [
            format_inputs(1, 1, 1),
            format_inputs(1, 1, 1),
            format_inputs(1, 1, 1),
            format_inputs(0, 0, 0),
        ],
    }
    scenarios.append(hold_time)

    # Scenario 7: Input Signal Stability
    stability = {
        "scenario": "Input Signal Stability",
        "input variable": [
            format_inputs(1, 0, 1),
            format_inputs(1, 0, 1),
            format_inputs(1, 0, 1),
            format_inputs(1, 0, 1),
        ],
    }
    scenarios.append(stability)

    # Scenario 8: Maximum Frequency Operation
    max_freq = {
        "scenario": "Maximum Frequency Operation",
        "input variable": [
            format_inputs(0, 0, 0),
            format_inputs(1, 1, 1),
            format_inputs(0, 0, 0),
            format_inputs(1, 1, 1),
        ],
    }
    scenarios.append(max_freq)

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
