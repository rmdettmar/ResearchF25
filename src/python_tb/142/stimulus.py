import json


def stimulus_gen():
    scenarios = []

    # Helper function to create stimulus sequence
    def create_stimulus(name, input_list):
        return {"scenario": name, "input variable": input_list}

    # Scenario 1: Initial Power-up State
    scenarios.append(
        create_stimulus(
            "Initial Power-up State",
            [{"clk": "0", "a": "0", "b": "0"}, {"clk": "1", "a": "0", "b": "0"}],
        )
    )

    # Scenario 2: State Transition with a=0, b=0
    scenarios.append(
        create_stimulus(
            "State Transition with a=0, b=0",
            [
                {"clk": "0", "a": "0", "b": "0"},
                {"clk": "1", "a": "0", "b": "0"},
                {"clk": "0", "a": "0", "b": "0"},
                {"clk": "1", "a": "0", "b": "0"},
                {"clk": "0", "a": "0", "b": "0"},
            ],
        )
    )

    # Scenario 3: Input Pattern Sequence
    scenarios.append(
        create_stimulus(
            "Input Pattern Sequence",
            [
                {"clk": "0", "a": "0", "b": "1"},
                {"clk": "1", "a": "0", "b": "1"},
                {"clk": "0", "a": "1", "b": "0"},
                {"clk": "1", "a": "1", "b": "0"},
            ],
        )
    )

    # Scenario 4: Consecutive Same Inputs
    scenarios.append(
        create_stimulus(
            "Consecutive Same Inputs",
            [
                {"clk": "0", "a": "1", "b": "1"},
                {"clk": "1", "a": "1", "b": "1"},
                {"clk": "0", "a": "1", "b": "1"},
                {"clk": "1", "a": "1", "b": "1"},
            ],
        )
    )

    # Scenario 5: State Toggle Check
    scenarios.append(
        create_stimulus(
            "State Toggle Check",
            [
                {"clk": "0", "a": "0", "b": "0"},
                {"clk": "1", "a": "0", "b": "0"},
                {"clk": "0", "a": "1", "b": "1"},
                {"clk": "1", "a": "1", "b": "1"},
            ],
        )
    )

    # Scenario 6: Output Hold
    scenarios.append(
        create_stimulus(
            "Output Hold",
            [
                {"clk": "1", "a": "1", "b": "1"},
                {"clk": "0", "a": "0", "b": "0"},
                {"clk": "0", "a": "1", "b": "1"},
            ],
        )
    )

    # Scenario 7: All Input Combinations
    scenarios.append(
        create_stimulus(
            "All Input Combinations",
            [
                {"clk": "0", "a": "0", "b": "0"},
                {"clk": "1", "a": "0", "b": "0"},
                {"clk": "0", "a": "0", "b": "1"},
                {"clk": "1", "a": "0", "b": "1"},
                {"clk": "0", "a": "1", "b": "0"},
                {"clk": "1", "a": "1", "b": "0"},
                {"clk": "0", "a": "1", "b": "1"},
                {"clk": "1", "a": "1", "b": "1"},
            ],
        )
    )

    # Scenario 8: Clock Edge Sensitivity
    scenarios.append(
        create_stimulus(
            "Clock Edge Sensitivity",
            [
                {"clk": "0", "a": "1", "b": "1"},
                {"clk": "1", "a": "1", "b": "1"},
                {"clk": "0", "a": "0", "b": "0"},
                {"clk": "1", "a": "0", "b": "0"},
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
