import json


def stimulus_gen():
    scenarios = []

    # Helper function to convert to binary string
    def to_bin(val):
        return "1" if val else "0"

    # Scenario 1: Reset Verification
    reset_seq = {
        "scenario": "Reset Verification",
        "input variable": [
            {"areset": "0", "x": "1"},  # Get to state B
            {"areset": "1", "x": "1"},  # Assert reset
            {"areset": "0", "x": "0"},  # Normal operation
            {"areset": "1", "x": "0"},  # Reset again
        ],
    }
    scenarios.append(reset_seq)

    # Scenario 2: State A Transitions
    state_a_trans = {
        "scenario": "State A Transitions",
        "input variable": [
            {"areset": "0", "x": "0"},  # Stay in A
            {"areset": "0", "x": "0"},  # Stay in A
            {"areset": "0", "x": "1"},  # Move to B
            {"areset": "0", "x": "0"},  # Now in B
        ],
    }
    scenarios.append(state_a_trans)

    # Scenario 3: State B Self-Loops
    state_b_loops = {
        "scenario": "State B Self-Loops",
        "input variable": [
            {"areset": "0", "x": "1"},  # Get to B
            {"areset": "0", "x": "0"},  # Stay in B
            {"areset": "0", "x": "1"},  # Stay in B
            {"areset": "0", "x": "0"},  # Stay in B
        ],
    }
    scenarios.append(state_b_loops)

    # Scenario 4: Complete Sequence
    complete_seq = {
        "scenario": "Complete Sequence",
        "input variable": [
            {"areset": "0", "x": "0"},  # Start in A
            {"areset": "0", "x": "1"},  # Move to B
            {"areset": "0", "x": "1"},  # Stay in B
            {"areset": "0", "x": "0"},  # Stay in B
        ],
    }
    scenarios.append(complete_seq)

    # Scenario 5: Input Toggle
    input_toggle = {
        "scenario": "Input Toggle",
        "input variable": [
            {"areset": "0", "x": "0"},
            {"areset": "0", "x": "1"},
            {"areset": "0", "x": "0"},
            {"areset": "0", "x": "1"},
        ],
    }
    scenarios.append(input_toggle)

    # Scenario 6: Reset During Transition
    reset_transition = {
        "scenario": "Reset During Transition",
        "input variable": [
            {"areset": "0", "x": "1"},  # Start transition
            {"areset": "1", "x": "1"},  # Reset during transition
            {"areset": "0", "x": "0"},  # Back to normal
            {"areset": "0", "x": "1"},  # New transition
        ],
    }
    scenarios.append(reset_transition)

    # Scenario 7: Clock Edge Alignment
    clock_edge = {
        "scenario": "Clock Edge Alignment",
        "input variable": [
            {"areset": "0", "x": "0"},  # Stable input
            {"areset": "0", "x": "1"},  # Change near clock edge
            {"areset": "0", "x": "0"},  # Quick toggle
            {"areset": "0", "x": "1"},  # Another edge change
        ],
    }
    scenarios.append(clock_edge)

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
