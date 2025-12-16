import json


def stimulus_gen():
    scenarios = []

    # Helper function to convert integer to binary string
    def to_bin(val):
        return "1" if val else "0"

    # Scenario 1: Basic Shift Operation
    basic_shift = {
        "scenario": "Basic Shift Operation",
        "input variable": [
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "0"},
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "0"},
        ],
    }
    scenarios.append(basic_shift)

    # Scenario 2: Synchronous Reset
    sync_reset = {
        "scenario": "Synchronous Reset",
        "input variable": [
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "0", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "1"},
        ],
    }
    scenarios.append(sync_reset)

    # Scenario 3: Consecutive Ones
    cons_ones = {
        "scenario": "Consecutive Ones",
        "input variable": [
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "1"},
        ],
    }
    scenarios.append(cons_ones)

    # Scenario 4: Consecutive Zeros
    cons_zeros = {
        "scenario": "Consecutive Zeros",
        "input variable": [
            {"clk": "0", "resetn": "1", "in": "0"},
            {"clk": "0", "resetn": "1", "in": "0"},
            {"clk": "0", "resetn": "1", "in": "0"},
            {"clk": "0", "resetn": "1", "in": "0"},
            {"clk": "0", "resetn": "1", "in": "0"},
            {"clk": "0", "resetn": "1", "in": "0"},
        ],
    }
    scenarios.append(cons_zeros)

    # Scenario 5: Reset Recovery
    reset_recovery = {
        "scenario": "Reset Recovery",
        "input variable": [
            {"clk": "0", "resetn": "0", "in": "0"},
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "0"},
        ],
    }
    scenarios.append(reset_recovery)

    # Scenario 6: Reset During Input Change
    reset_during_change = {
        "scenario": "Reset During Input Change",
        "input variable": [
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "0", "in": "0"},
            {"clk": "0", "resetn": "0", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "0"},
        ],
    }
    scenarios.append(reset_during_change)

    # Scenario 7: Setup Time Verification
    setup_time = {
        "scenario": "Setup Time Verification",
        "input variable": [
            {"clk": "0", "resetn": "1", "in": "0"},
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "0"},
            {"clk": "0", "resetn": "1", "in": "1"},
        ],
    }
    scenarios.append(setup_time)

    # Scenario 8: Hold Time Verification
    hold_time = {
        "scenario": "Hold Time Verification",
        "input variable": [
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "1"},
            {"clk": "0", "resetn": "1", "in": "0"},
            {"clk": "0", "resetn": "1", "in": "0"},
        ],
    }
    scenarios.append(hold_time)

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
