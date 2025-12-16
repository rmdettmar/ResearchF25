import json

from cocotb.binary import BinaryValue


def create_binary_signal(value, width=1):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Initial Reset State
    scenarios.append(
        {
            "scenario": "Initial Reset State",
            "input variable": [
                {"areset": "1", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
            ],
        }
    )

    # Scenario 2: Left to Right Transition
    scenarios.append(
        {
            "scenario": "Left to Right Transition",
            "input variable": [
                {"areset": "1", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "1", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
            ],
        }
    )

    # Scenario 3: Right to Left Transition
    scenarios.append(
        {
            "scenario": "Right to Left Transition",
            "input variable": [
                {"areset": "1", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "1", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "1"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
            ],
        }
    )

    # Scenario 4: Simultaneous Bumps
    scenarios.append(
        {
            "scenario": "Simultaneous Bumps",
            "input variable": [
                {"areset": "1", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "1", "bump_right": "1"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
            ],
        }
    )

    # Scenario 5: No Direction Change
    scenarios.append(
        {
            "scenario": "No Direction Change",
            "input variable": [
                {"areset": "1", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
            ],
        }
    )

    # Scenario 6: Reset During Walk
    scenarios.append(
        {
            "scenario": "Reset During Walk",
            "input variable": [
                {"areset": "1", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "1", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
                {"areset": "1", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
            ],
        }
    )

    # Scenario 7: Multiple Direction Changes
    scenarios.append(
        {
            "scenario": "Multiple Direction Changes",
            "input variable": [
                {"areset": "1", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "1", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "1"},
                {"areset": "0", "bump_left": "1", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "1"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
            ],
        }
    )

    # Scenario 8: Glitch Immunity
    scenarios.append(
        {
            "scenario": "Glitch Immunity",
            "input variable": [
                {"areset": "1", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "1", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "1", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
                {"areset": "0", "bump_left": "0", "bump_right": "0"},
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
