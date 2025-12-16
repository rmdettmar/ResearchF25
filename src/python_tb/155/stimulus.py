import json


def stimulus_gen():
    scenarios = []

    def gen_sequence(scenario_name, input_list):
        return {"scenario": scenario_name, "input variable": input_list}

    # Scenario 1: Basic Walking Direction
    basic_walking = [
        {"areset": "1", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
        {"areset": "0", "bump_left": "1", "bump_right": "0", "ground": "1", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
    ]
    scenarios.append(gen_sequence("Basic Walking Direction", basic_walking))

    # Scenario 2: Falling Behavior
    falling = [
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "0", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "0", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
    ]
    scenarios.append(gen_sequence("Falling Behavior", falling))

    # Scenario 3: Bump While Falling
    bump_falling = [
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "0", "clk": "0"},
        {"areset": "0", "bump_left": "1", "bump_right": "0", "ground": "0", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "1", "ground": "0", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
    ]
    scenarios.append(gen_sequence("Bump While Falling", bump_falling))

    # Scenario 4: Simultaneous Bumps
    simultaneous = [
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
        {"areset": "0", "bump_left": "1", "bump_right": "1", "ground": "1", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
    ]
    scenarios.append(gen_sequence("Simultaneous Bumps", simultaneous))

    # Scenario 5: Asynchronous Reset
    async_reset = [
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
        {"areset": "1", "bump_left": "0", "bump_right": "0", "ground": "0", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
    ]
    scenarios.append(gen_sequence("Asynchronous Reset", async_reset))

    # Scenario 6: Ground Edge Transitions
    ground_edge = [
        {"areset": "0", "bump_left": "1", "bump_right": "0", "ground": "1", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "0", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "1", "ground": "1", "clk": "0"},
    ]
    scenarios.append(gen_sequence("Ground Edge Transitions", ground_edge))

    # Scenario 7: Rapid State Changes
    rapid_changes = [
        {"areset": "0", "bump_left": "1", "bump_right": "0", "ground": "1", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "1", "ground": "0", "clk": "0"},
        {"areset": "0", "bump_left": "1", "bump_right": "0", "ground": "1", "clk": "0"},
    ]
    scenarios.append(gen_sequence("Rapid State Changes", rapid_changes))

    # Scenario 8: Long-term Walking
    long_walking = [
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
        {"areset": "0", "bump_left": "0", "bump_right": "0", "ground": "1", "clk": "0"},
    ]
    scenarios.append(gen_sequence("Long-term Walking", long_walking))

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
