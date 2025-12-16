import json


def stimulus_gen():
    scenarios = []

    # Helper function to create stimulus sequence
    def create_sequence(scenario_name, input_list):
        return {
            "scenario": scenario_name,
            "input variable": [
                {"clk": "1", "reset": reset, "data": data} for reset, data in input_list
            ],
        }

    # Scenario 1: Basic Sequence Detection
    scenarios.append(
        create_sequence(
            "Basic Sequence Detection",
            [
                ("0", "1"),
                ("0", "1"),
                ("0", "0"),
                ("0", "1"),
                ("0", "0"),
                ("0", "0"),
            ],  # Extra cycles to verify output stays high
        )
    )

    # Scenario 2: Overlapping Sequence
    scenarios.append(
        create_sequence(
            "Overlapping Sequence",
            [
                ("0", "1"),
                ("0", "1"),
                ("0", "0"),
                ("0", "1"),
                ("0", "1"),
                ("0", "1"),
                ("0", "0"),
                ("0", "1"),
            ],
        )
    )

    # Scenario 3: Partial Match Reset
    scenarios.append(
        create_sequence(
            "Partial Match Reset",
            [
                ("0", "1"),
                ("0", "1"),
                ("0", "0"),
                ("1", "0"),  # Reset during partial match
                ("0", "0"),
                ("0", "0"),
            ],  # Verify no detection
        )
    )

    # Scenario 4: Post-Detection Reset
    scenarios.append(
        create_sequence(
            "Post-Detection Reset",
            [
                ("0", "1"),
                ("0", "1"),
                ("0", "0"),
                ("0", "1"),  # Detect sequence
                ("0", "0"),
                ("1", "0"),
                ("0", "0"),
            ],  # Reset after detection
        )
    )

    # Scenario 5: Multiple Reset Cycles
    scenarios.append(
        create_sequence(
            "Multiple Reset Cycles",
            [
                ("1", "0"),
                ("0", "1"),
                ("1", "0"),
                ("0", "1"),
                ("1", "0"),
                ("0", "0"),
                ("0", "1"),
            ],
        )
    )

    # Scenario 6: False Pattern Testing
    scenarios.append(
        create_sequence(
            "False Pattern Testing",
            [
                ("0", "1"),
                ("0", "1"),
                ("0", "0"),
                ("0", "0"),  # Test '1100'
                ("0", "1"),
                ("0", "1"),
                ("0", "1"),
                ("0", "1"),  # Test '1111'
                ("0", "0"),
                ("0", "1"),
                ("0", "1"),
                ("0", "0"),
            ],  # Test '0110'
        )
    )

    # Scenario 7: Continuous Operation
    scenarios.append(
        create_sequence(
            "Continuous Operation",
            [
                ("0", "1"),
                ("0", "1"),
                ("0", "0"),
                ("0", "1"),  # Detect sequence
                ("0", "1"),
                ("0", "0"),
                ("0", "1"),
                ("0", "0"),  # Random bits after detection
                ("0", "1"),
                ("0", "0"),
            ],
        )
    )

    # Scenario 8: Quick Transition Testing
    scenarios.append(
        create_sequence(
            "Quick Transition Testing",
            [
                ("0", "1"),
                ("0", "1"),
                ("0", "0"),
                ("0", "1"),
                ("0", "0"),
                ("0", "1"),
                ("0", "0"),
                ("0", "1"),
            ],
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
