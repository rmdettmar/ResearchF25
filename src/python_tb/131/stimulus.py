import json


def create_binary_sequence(a_val, b_val):
    return {"a": "1" if a_val else "0", "b": "1" if b_val else "0"}


def stimulus_gen():
    scenarios = []

    # Scenario 1: All Input Combinations
    input_seq1 = [
        create_binary_sequence(0, 0),
        create_binary_sequence(0, 1),
        create_binary_sequence(1, 0),
        create_binary_sequence(1, 1),
    ]
    scenarios.append(
        {"scenario": "All Input Combinations", "input variable": input_seq1}
    )

    # Scenario 2: No Carry Generation
    input_seq2 = [
        create_binary_sequence(0, 0),
        create_binary_sequence(0, 1),
        create_binary_sequence(1, 0),
    ]
    scenarios.append({"scenario": "No Carry Generation", "input variable": input_seq2})

    # Scenario 3: Carry Generation
    input_seq3 = [create_binary_sequence(1, 1)]
    scenarios.append({"scenario": "Carry Generation", "input variable": input_seq3})

    # Scenario 4: Input Transitions
    input_seq4 = [
        create_binary_sequence(0, 0),
        create_binary_sequence(0, 1),
        create_binary_sequence(1, 1),
        create_binary_sequence(1, 0),
        create_binary_sequence(0, 0),
    ]
    scenarios.append({"scenario": "Input Transitions", "input variable": input_seq4})

    # Scenario 5: Setup and Hold Time
    input_seq5 = [
        create_binary_sequence(0, 0),
        create_binary_sequence(1, 1),
        create_binary_sequence(0, 1),
        create_binary_sequence(1, 0),
    ]
    scenarios.append({"scenario": "Setup and Hold Time", "input variable": input_seq5})

    # Scenario 6: Output Propagation Delay
    input_seq6 = [
        create_binary_sequence(0, 0),
        create_binary_sequence(1, 1),
        create_binary_sequence(0, 1),
        create_binary_sequence(1, 0),
    ]
    scenarios.append(
        {"scenario": "Output Propagation Delay", "input variable": input_seq6}
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
