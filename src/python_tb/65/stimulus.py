import json


def stimulus_gen():
    scenarios = []

    # Helper function to format input dictionary
    def create_input_dict(a, b, c, d, e):
        return {"a": str(a), "b": str(b), "c": str(c), "d": str(d), "e": str(e)}

    # Scenario 1: All Zeros Input
    scenarios.append(
        {
            "scenario": "All Zeros Input",
            "input variable": [create_input_dict("0", "0", "0", "0", "0")],
        }
    )

    # Scenario 2: All Ones Input
    scenarios.append(
        {
            "scenario": "All Ones Input",
            "input variable": [create_input_dict("1", "1", "1", "1", "1")],
        }
    )

    # Scenario 3: Single One Input
    scenarios.append(
        {
            "scenario": "Single One Input",
            "input variable": [create_input_dict("1", "0", "0", "0", "0")],
        }
    )

    # Scenario 4: Alternating Pattern
    scenarios.append(
        {
            "scenario": "Alternating Pattern",
            "input variable": [create_input_dict("1", "0", "1", "0", "1")],
        }
    )

    # Scenario 5: Self-Comparison Check
    scenarios.append(
        {
            "scenario": "Self-Comparison Check",
            "input variable": [
                create_input_dict("0", "1", "0", "1", "0"),
                create_input_dict("1", "0", "1", "0", "1"),
            ],
        }
    )

    # Scenario 6: Diagonal Symmetry
    scenarios.append(
        {
            "scenario": "Diagonal Symmetry",
            "input variable": [
                create_input_dict("1", "0", "1", "0", "1"),
                create_input_dict("0", "1", "0", "1", "0"),
            ],
        }
    )

    # Scenario 7: Rapid Input Transitions
    scenarios.append(
        {
            "scenario": "Rapid Input Transitions",
            "input variable": [
                create_input_dict("0", "0", "0", "0", "0"),
                create_input_dict("1", "1", "1", "1", "1"),
                create_input_dict("0", "0", "0", "0", "0"),
                create_input_dict("1", "1", "1", "1", "1"),
            ],
        }
    )

    # Scenario 8: Walking Ones Pattern
    scenarios.append(
        {
            "scenario": "Walking Ones Pattern",
            "input variable": [
                create_input_dict("1", "0", "0", "0", "0"),
                create_input_dict("0", "1", "0", "0", "0"),
                create_input_dict("0", "0", "1", "0", "0"),
                create_input_dict("0", "0", "0", "1", "0"),
                create_input_dict("0", "0", "0", "0", "1"),
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
