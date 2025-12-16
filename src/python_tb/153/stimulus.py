import json


def stimulus_gen():
    scenarios = []

    # Helper function to create input dictionary
    def create_inputs(areset="0", bump_left="0", bump_right="0", ground="1", dig="0"):
        return {
            "areset": areset,
            "bump_left": bump_left,
            "bump_right": bump_right,
            "ground": ground,
            "dig": dig,
        }

    # Scenario 1: Basic Walking Direction Change
    scenarios.append(
        {
            "scenario": "Basic Walking Direction Change",
            "input variable": [
                create_inputs(),  # Initial state
                create_inputs(bump_left="1"),  # Bump left
                create_inputs(),  # Walking right
                create_inputs(bump_right="1"),  # Bump right
                create_inputs(),  # Walking left
            ],
        }
    )

    # Scenario 2: Falling Behavior
    scenarios.append(
        {
            "scenario": "Falling Behavior",
            "input variable": [
                create_inputs(),  # Initial walking
                create_inputs(ground="0"),  # Ground disappears
                create_inputs(ground="0"),  # Still falling
                create_inputs(),  # Ground returns
                create_inputs(),  # Continue walking
            ],
        }
    )

    # Scenario 3: Digging Operation
    scenarios.append(
        {
            "scenario": "Digging Operation",
            "input variable": [
                create_inputs(),  # Initial walking
                create_inputs(dig="1"),  # Start digging
                create_inputs(dig="1"),  # Continue digging
                create_inputs(dig="1", ground="0"),  # Ground disappears
                create_inputs(ground="0"),  # Falling
                create_inputs(),  # Resume walking
            ],
        }
    )

    # Scenario 4: Priority Testing
    scenarios.append(
        {
            "scenario": "Priority Testing",
            "input variable": [
                create_inputs(),  # Initial state
                create_inputs(
                    ground="0", dig="1", bump_left="1"
                ),  # Multiple conditions
                create_inputs(ground="0"),  # Should be falling
                create_inputs(dig="1"),  # Should start digging
                create_inputs(bump_left="1"),  # Should change direction
            ],
        }
    )

    # Scenario 5: Asynchronous Reset
    scenarios.append(
        {
            "scenario": "Asynchronous Reset",
            "input variable": [
                create_inputs(),  # Initial state
                create_inputs(dig="1"),  # Digging
                create_inputs(areset="1"),  # Reset while digging
                create_inputs(ground="0"),  # Falling
                create_inputs(areset="1"),  # Reset while falling
            ],
        }
    )

    # Scenario 6: Bump While Falling
    scenarios.append(
        {
            "scenario": "Bump While Falling",
            "input variable": [
                create_inputs(),  # Initial walking
                create_inputs(ground="0"),  # Start falling
                create_inputs(ground="0", bump_left="1"),  # Bump while falling
                create_inputs(),  # Ground returns
                create_inputs(),  # Should maintain original direction
            ],
        }
    )

    # Scenario 7: Invalid Dig Commands
    scenarios.append(
        {
            "scenario": "Invalid Dig Commands",
            "input variable": [
                create_inputs(ground="0"),  # Falling
                create_inputs(ground="0", dig="1"),  # Try to dig while falling
                create_inputs(),  # Ground returns
                create_inputs(ground="0", dig="1"),  # Try to dig with no ground
                create_inputs(),  # Normal walking
            ],
        }
    )

    # Scenario 8: Simultaneous Bumps
    scenarios.append(
        {
            "scenario": "Simultaneous Bumps",
            "input variable": [
                create_inputs(),  # Initial walking
                create_inputs(bump_left="1", bump_right="1"),  # Both bumps
                create_inputs(),  # Changed direction
                create_inputs(bump_left="1", bump_right="1"),  # Both bumps again
                create_inputs(),  # Changed direction again
            ],
        }
    )

    # Scenario 9: Ground Edge Conditions
    scenarios.append(
        {
            "scenario": "Ground Edge Conditions",
            "input variable": [
                create_inputs(),  # Initial walking
                create_inputs(ground="0", bump_left="1"),  # Ground disappears and bump
                create_inputs(ground="0"),  # Still falling
                create_inputs(),  # Ground returns
                create_inputs(),  # Continue walking
            ],
        }
    )

    # Scenario 10: State Persistence
    scenarios.append(
        {
            "scenario": "State Persistence",
            "input variable": [
                create_inputs(),  # Initial walking
                create_inputs(ground="0"),  # Start falling
                create_inputs(ground="0"),  # Continue falling
                create_inputs(),  # Ground returns
                create_inputs(dig="1"),  # Start digging
                create_inputs(dig="1", ground="0"),  # Ground disappears while digging
                create_inputs(),  # Ground returns
                create_inputs(),  # Should maintain original direction
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
