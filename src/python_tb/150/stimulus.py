import json


def generate_walking_sequence(direction, cycles):
    if direction == "left":
        return {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "0"}
    return {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "0"}


def generate_falling_sequence(cycles):
    return {"bump_left": "0", "bump_right": "0", "ground": "0", "dig": "0"}


def generate_digging_sequence():
    return {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "1"}


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Walking Direction Changes
    scenario1 = {
        "scenario": "Basic Walking Direction Changes",
        "input variable": [
            {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "0"},
            {"bump_left": "1", "bump_right": "0", "ground": "1", "dig": "0"},
            {"bump_left": "0", "bump_right": "1", "ground": "1", "dig": "0"},
        ],
    }
    scenarios.append(scenario1)

    # Scenario 2: Falling Behavior
    scenario2 = {
        "scenario": "Falling Behavior",
        "input variable": [
            {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "0"},
            {"bump_left": "0", "bump_right": "0", "ground": "0", "dig": "0"},
            {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "0"},
        ],
    }
    scenarios.append(scenario2)

    # Scenario 3: Digging Operation
    scenario3 = {
        "scenario": "Digging Operation",
        "input variable": [
            {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "1"},
            {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "1"},
            {"bump_left": "0", "bump_right": "0", "ground": "0", "dig": "1"},
            {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "0"},
        ],
    }
    scenarios.append(scenario3)

    # Scenario 4: Splatter Condition
    falling_sequence = [
        {"bump_left": "0", "bump_right": "0", "ground": "0", "dig": "0"}
        for _ in range(21)
    ]
    falling_sequence.append(
        {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "0"}
    )
    scenario4 = {"scenario": "Splatter Condition", "input variable": falling_sequence}
    scenarios.append(scenario4)

    # Scenario 5: Priority Handling
    scenario5 = {
        "scenario": "Priority Handling",
        "input variable": [
            {"bump_left": "1", "bump_right": "0", "ground": "0", "dig": "1"},
            {"bump_left": "0", "bump_right": "1", "ground": "0", "dig": "1"},
            {"bump_left": "1", "bump_right": "1", "ground": "0", "dig": "1"},
        ],
    }
    scenarios.append(scenario5)

    # Scenario 6: Bump During Special States
    scenario6 = {
        "scenario": "Bump During Special States",
        "input variable": [
            {"bump_left": "0", "bump_right": "0", "ground": "0", "dig": "0"},
            {"bump_left": "1", "bump_right": "0", "ground": "0", "dig": "0"},
            {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "1"},
            {"bump_left": "1", "bump_right": "0", "ground": "1", "dig": "1"},
        ],
    }
    scenarios.append(scenario6)

    # Scenario 7: Asynchronous Reset
    scenario7 = {
        "scenario": "Asynchronous Reset",
        "input variable": [
            {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "0"},
            {"bump_left": "0", "bump_right": "0", "ground": "0", "dig": "0"},
            {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "1"},
        ],
    }
    scenarios.append(scenario7)

    # Scenario 8: Edge Case Transitions
    scenario8 = {
        "scenario": "Edge Case Transitions",
        "input variable": [
            {"bump_left": "1", "bump_right": "0", "ground": "1", "dig": "0"},
            {"bump_left": "0", "bump_right": "0", "ground": "0", "dig": "1"},
            {"bump_left": "1", "bump_right": "1", "ground": "1", "dig": "0"},
        ],
    }
    scenarios.append(scenario8)

    # Scenario 9: Fall Counter Boundary
    twenty_cycles = [
        {"bump_left": "0", "bump_right": "0", "ground": "0", "dig": "0"}
        for _ in range(20)
    ]
    twenty_cycles.append(
        {"bump_left": "0", "bump_right": "0", "ground": "1", "dig": "0"}
    )
    scenario9 = {"scenario": "Fall Counter Boundary", "input variable": twenty_cycles}
    scenarios.append(scenario9)

    # Scenario 10: Invalid Operation Handling
    scenario10 = {
        "scenario": "Invalid Operation Handling",
        "input variable": [
            {"bump_left": "0", "bump_right": "0", "ground": "0", "dig": "1"},
            {"bump_left": "0", "bump_right": "0", "ground": "0", "dig": "1"},
            {"bump_left": "1", "bump_right": "0", "ground": "0", "dig": "0"},
        ],
    }
    scenarios.append(scenario10)

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
