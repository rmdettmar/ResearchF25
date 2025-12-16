import json


def stimulus_gen():
    scenarios = []

    # Helper function to create binary strings
    def bin_str(val):
        return "1" if val else "0"

    # Scenario 1: Hold State Verification
    hold_state = {
        "scenario": "Hold State Verification",
        "input variable": [
            {"j": "0", "k": "0", "clk": "0"},
            {"j": "0", "k": "0", "clk": "1"},
            {"j": "0", "k": "0", "clk": "0"},
            {"j": "0", "k": "0", "clk": "1"},
        ],
    }
    scenarios.append(hold_state)

    # Scenario 2: Reset Operation
    reset_op = {
        "scenario": "Reset Operation",
        "input variable": [
            {"j": "0", "k": "1", "clk": "0"},
            {"j": "0", "k": "1", "clk": "1"},
            {"j": "0", "k": "1", "clk": "0"},
            {"j": "0", "k": "1", "clk": "1"},
        ],
    }
    scenarios.append(reset_op)

    # Scenario 3: Set Operation
    set_op = {
        "scenario": "Set Operation",
        "input variable": [
            {"j": "1", "k": "0", "clk": "0"},
            {"j": "1", "k": "0", "clk": "1"},
            {"j": "1", "k": "0", "clk": "0"},
            {"j": "1", "k": "0", "clk": "1"},
        ],
    }
    scenarios.append(set_op)

    # Scenario 4: Toggle Operation
    toggle_op = {
        "scenario": "Toggle Operation",
        "input variable": [
            {"j": "1", "k": "1", "clk": "0"},
            {"j": "1", "k": "1", "clk": "1"},
            {"j": "1", "k": "1", "clk": "0"},
            {"j": "1", "k": "1", "clk": "1"},
        ],
    }
    scenarios.append(toggle_op)

    # Scenario 5: Input Transitions
    input_trans = {
        "scenario": "Input Transitions",
        "input variable": [
            {"j": "0", "k": "0", "clk": "0"},
            {"j": "1", "k": "0", "clk": "0"},
            {"j": "1", "k": "0", "clk": "1"},
            {"j": "0", "k": "1", "clk": "0"},
            {"j": "0", "k": "1", "clk": "1"},
        ],
    }
    scenarios.append(input_trans)

    # Scenario 6: Rapid Input Changes
    rapid_changes = {
        "scenario": "Rapid Input Changes",
        "input variable": [
            {"j": "0", "k": "0", "clk": "0"},
            {"j": "1", "k": "1", "clk": "0"},
            {"j": "0", "k": "1", "clk": "0"},
            {"j": "1", "k": "0", "clk": "0"},
            {"j": "1", "k": "1", "clk": "1"},
        ],
    }
    scenarios.append(rapid_changes)

    # Scenario 7: Sequential State Changes
    seq_changes = {
        "scenario": "Sequential State Changes",
        "input variable": [
            {"j": "0", "k": "0", "clk": "0"},
            {"j": "0", "k": "0", "clk": "1"},
            {"j": "0", "k": "1", "clk": "0"},
            {"j": "0", "k": "1", "clk": "1"},
            {"j": "1", "k": "0", "clk": "0"},
            {"j": "1", "k": "0", "clk": "1"},
            {"j": "1", "k": "1", "clk": "0"},
            {"j": "1", "k": "1", "clk": "1"},
        ],
    }
    scenarios.append(seq_changes)

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
