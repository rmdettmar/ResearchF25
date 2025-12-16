import json


def stimulus_gen():
    scenarios = []

    # Helper function to create a stimulus sequence
    def create_sequence(scenario_name, clock_seq, a_seq):
        return {
            "scenario": scenario_name,
            "input variable": [{"clock": c, "a": a} for c, a in zip(clock_seq, a_seq)],
        }

    # Scenario 1: Basic Signal Following
    scenarios.append(
        create_sequence(
            "Basic Signal Following",
            ["0", "1", "1", "0", "0", "1", "1"],
            ["0", "1", "0", "0", "1", "1", "0"],
        )
    )

    # Scenario 2: Transition Detection
    scenarios.append(
        create_sequence(
            "Transition Detection",
            ["1", "1", "1", "1", "0", "0"],
            ["1", "1", "0", "0", "0", "0"],
        )
    )

    # Scenario 3: No Detection on Clock Low
    scenarios.append(
        create_sequence(
            "No Detection on Clock Low",
            ["0", "0", "0", "0", "0", "0"],
            ["1", "1", "0", "0", "1", "0"],
        )
    )

    # Scenario 4: Multiple Transitions
    scenarios.append(
        create_sequence(
            "Multiple Transitions",
            ["1", "1", "0", "1", "1", "0", "1", "1"],
            ["1", "0", "0", "1", "0", "0", "1", "0"],
        )
    )

    # Scenario 5: Reset Condition
    scenarios.append(
        create_sequence(
            "Reset Condition", ["0", "0", "1", "1", "1"], ["0", "0", "0", "0", "0"]
        )
    )

    # Scenario 6: Output Persistence
    scenarios.append(
        create_sequence(
            "Output Persistence",
            ["1", "1", "0", "0", "0", "1"],
            ["1", "0", "0", "1", "1", "0"],
        )
    )

    # Scenario 7: Glitch Immunity
    scenarios.append(
        create_sequence(
            "Glitch Immunity",
            ["1", "1", "1", "1", "1", "1"],
            ["0", "1", "0", "1", "0", "1"],
        )
    )

    # Scenario 8: Clock Edge Timing
    scenarios.append(
        create_sequence(
            "Clock Edge Timing",
            ["0", "1", "1", "0", "1", "1"],
            ["0", "1", "0", "1", "1", "0"],
        )
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
