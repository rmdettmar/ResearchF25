import json


def stimulus_gen():
    scenarios = []

    # Helper function to convert input combinations to dictionary format
    def create_input_dict(a, b, c, d):
        return {"a": f"{a}", "b": f"{b}", "c": f"{c}", "d": f"{d}"}

    # Scenario 1: All Zero Inputs
    scenarios.append(
        {
            "scenario": "All Zero Inputs",
            "input variable": [create_input_dict("0", "0", "0", "0")],
        }
    )

    # Scenario 2: Single Input High
    single_high = {
        "scenario": "Single Input High",
        "input variable": [
            create_input_dict("1", "0", "0", "0"),
            create_input_dict("0", "1", "0", "0"),
            create_input_dict("0", "0", "1", "0"),
            create_input_dict("0", "0", "0", "1"),
        ],
    }
    scenarios.append(single_high)

    # Scenario 3: Two Inputs High
    two_high = {
        "scenario": "Two Inputs High",
        "input variable": [
            create_input_dict("1", "1", "0", "0"),
            create_input_dict("1", "0", "1", "0"),
            create_input_dict("1", "0", "0", "1"),
            create_input_dict("0", "1", "1", "0"),
            create_input_dict("0", "1", "0", "1"),
            create_input_dict("0", "0", "1", "1"),
        ],
    }
    scenarios.append(two_high)

    # Scenario 4: Three Inputs High
    three_high = {
        "scenario": "Three Inputs High",
        "input variable": [
            create_input_dict("1", "1", "1", "0"),
            create_input_dict("1", "1", "0", "1"),
            create_input_dict("1", "0", "1", "1"),
            create_input_dict("0", "1", "1", "1"),
        ],
    }
    scenarios.append(three_high)

    # Scenario 5: All Inputs High
    scenarios.append(
        {
            "scenario": "All Inputs High",
            "input variable": [create_input_dict("1", "1", "1", "1")],
        }
    )

    # Scenario 6: Input Transitions
    transitions = {
        "scenario": "Input Transitions",
        "input variable": [
            create_input_dict("0", "0", "0", "0"),
            create_input_dict("1", "1", "0", "0"),
            create_input_dict("1", "1", "1", "0"),
            create_input_dict("1", "1", "1", "1"),
            create_input_dict("0", "0", "0", "0"),
        ],
    }
    scenarios.append(transitions)

    # Scenario 7: Propagation Delay
    prop_delay = {
        "scenario": "Propagation Delay",
        "input variable": [
            create_input_dict("0", "0", "0", "0"),
            create_input_dict("1", "1", "1", "0"),
            create_input_dict("0", "0", "0", "0"),
            create_input_dict("1", "1", "0", "1"),
        ],
    }
    scenarios.append(prop_delay)

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
