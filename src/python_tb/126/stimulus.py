import json

from cocotb.binary import BinaryValue


def stimulus_gen():
    scenarios = []

    # Helper function to create binary strings
    def bin_str(value, width=1):
        return BinaryValue(value=value, n_bits=width).binstr

    # Scenario 1: Initial State Verification
    scenarios.append(
        {
            "scenario": "Initial State Verification",
            "input variable": [
                {"clk": "0", "in": "0"},
                {"clk": "1", "in": "0"},
                {"clk": "0", "in": "0"},
            ],
        }
    )

    # Scenario 2: Basic Input Toggle
    scenarios.append(
        {
            "scenario": "Basic Input Toggle",
            "input variable": [
                {"clk": "0", "in": "0"},
                {"clk": "1", "in": "0"},
                {"clk": "0", "in": "1"},
                {"clk": "1", "in": "1"},
                {"clk": "0", "in": "0"},
                {"clk": "1", "in": "0"},
            ],
        }
    )

    # Scenario 3: Consecutive Same Input
    scenarios.append(
        {
            "scenario": "Consecutive Same Input",
            "input variable": [
                {"clk": "0", "in": "1"},
                {"clk": "1", "in": "1"},
                {"clk": "0", "in": "1"},
                {"clk": "1", "in": "1"},
                {"clk": "0", "in": "1"},
                {"clk": "1", "in": "1"},
            ],
        }
    )

    # Scenario 4: Input Change at Clock Edge
    scenarios.append(
        {
            "scenario": "Input Change at Clock Edge",
            "input variable": [
                {"clk": "0", "in": "0"},
                {"clk": "1", "in": "1"},
                {"clk": "0", "in": "1"},
                {"clk": "1", "in": "0"},
            ],
        }
    )

    # Scenario 5: Rapid Input Transitions
    scenarios.append(
        {
            "scenario": "Rapid Input Transitions",
            "input variable": [
                {"clk": "0", "in": "0"},
                {"clk": "1", "in": "1"},
                {"clk": "0", "in": "0"},
                {"clk": "1", "in": "1"},
                {"clk": "0", "in": "0"},
                {"clk": "1", "in": "1"},
            ],
        }
    )

    # Scenario 6: Long-term Stability
    scenarios.append(
        {
            "scenario": "Long-term Stability",
            "input variable": [
                {"clk": "0", "in": "1"},
                {"clk": "1", "in": "1"},
                {"clk": "0", "in": "1"},
                {"clk": "1", "in": "1"},
                {"clk": "0", "in": "1"},
                {"clk": "1", "in": "1"},
                {"clk": "0", "in": "1"},
                {"clk": "1", "in": "1"},
            ],
        }
    )

    # Scenario 7: Clock Glitch Immunity
    scenarios.append(
        {
            "scenario": "Clock Glitch Immunity",
            "input variable": [
                {"clk": "0", "in": "1"},
                {"clk": "1", "in": "1"},
                {"clk": "0", "in": "1"},
                {"clk": "1", "in": "1"},
                {"clk": "0", "in": "1"},
            ],
        }
    )

    # Scenario 8: Input Pattern Sequences
    scenarios.append(
        {
            "scenario": "Input Pattern Sequences",
            "input variable": [
                {"clk": "0", "in": "0"},
                {"clk": "1", "in": "1"},
                {"clk": "0", "in": "1"},
                {"clk": "1", "in": "0"},
                {"clk": "0", "in": "0"},
                {"clk": "1", "in": "1"},
            ],
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
