import json


def stimulus_gen():
    scenarios = []

    # Helper function to create a sequence of input transitions
    def create_input_sequence(values, scenario_name, description):
        return {
            "scenario": scenario_name,
            "input variable": [{"in": value} for value in values],
        }

    # Scenario 1: Basic Input Value Verification
    basic_values = ["0" * 20, "1" * 20]  # Hold each value for 20 cycles
    scenarios.append(
        create_input_sequence(
            basic_values, "Basic Input Value Verification", "Static logic values test"
        )
    )

    # Scenario 2: Input Transition Testing
    transition_sequence = ["0", "1"] * 10  # Alternate between 0 and 1
    scenarios.append(
        create_input_sequence(
            transition_sequence,
            "Input Transition Testing",
            "Toggle input between 0 and 1",
        )
    )

    # Scenario 3: High Frequency Switching
    high_freq_sequence = ["0", "1"] * 50  # Rapid transitions
    scenarios.append(
        create_input_sequence(
            high_freq_sequence, "High Frequency Switching", "Rapid input transitions"
        )
    )

    # Scenario 4: Glitch Immunity
    glitch_sequence = ["0"] * 5 + ["1"] + ["0"] * 5 + ["1"] * 5 + ["0"] + ["1"] * 5
    scenarios.append(
        create_input_sequence(
            glitch_sequence, "Glitch Immunity", "Test response to input glitches"
        )
    )

    # Scenario 5: Setup/Hold Time Verification
    timing_sequence = ["0"] * 10 + ["1"] * 10 + ["0"] * 10 + ["1"] * 10
    scenarios.append(
        create_input_sequence(
            timing_sequence,
            "Setup/Hold Time Verification",
            "Verify timing requirements",
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
