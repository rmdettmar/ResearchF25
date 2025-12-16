import json


def stimulus_gen():
    scenarios = []

    def create_sequence(areset_val, train_valid_val, train_taken_val):
        return {
            "areset": areset_val,
            "train_valid": train_valid_val,
            "train_taken": train_taken_val,
        }

    # Scenario 1: Basic Increment Operation
    increment_seq = []
    for _ in range(5):  # Multiple cycles to reach and verify saturation
        increment_seq.append(create_sequence("0", "1", "1"))
    scenarios.append(
        {"scenario": "Basic Increment Operation", "input variable": increment_seq}
    )

    # Scenario 2: Basic Decrement Operation
    decrement_seq = []
    for _ in range(5):  # Multiple cycles to reach and verify minimum
        decrement_seq.append(create_sequence("0", "1", "0"))
    scenarios.append(
        {"scenario": "Basic Decrement Operation", "input variable": decrement_seq}
    )

    # Scenario 3: Saturation at Maximum
    max_sat_seq = []
    for _ in range(3):  # Try incrementing when already at maximum
        max_sat_seq.append(create_sequence("0", "1", "1"))
    scenarios.append(
        {"scenario": "Saturation at Maximum", "input variable": max_sat_seq}
    )

    # Scenario 4: Saturation at Minimum
    min_sat_seq = []
    for _ in range(3):  # Try decrementing when already at minimum
        min_sat_seq.append(create_sequence("0", "1", "0"))
    scenarios.append(
        {"scenario": "Saturation at Minimum", "input variable": min_sat_seq}
    )

    # Scenario 5: Training Disabled
    disabled_seq = []
    for taken in ["0", "1", "0", "1"]:  # Varying train_taken with training disabled
        disabled_seq.append(create_sequence("0", "0", taken))
    scenarios.append({"scenario": "Training Disabled", "input variable": disabled_seq})

    # Scenario 6: Asynchronous Reset
    reset_seq = []
    reset_seq.append(create_sequence("0", "1", "1"))  # First increment
    reset_seq.append(create_sequence("1", "1", "1"))  # Assert reset
    reset_seq.append(create_sequence("0", "1", "1"))  # Resume normal operation
    scenarios.append({"scenario": "Asynchronous Reset", "input variable": reset_seq})

    # Scenario 7: Alternating Training Patterns
    alt_seq = []
    for _ in range(3):
        alt_seq.append(create_sequence("0", "1", "1"))  # Increment
        alt_seq.append(create_sequence("0", "1", "0"))  # Decrement
    scenarios.append(
        {"scenario": "Alternating Training Patterns", "input variable": alt_seq}
    )

    # Scenario 8: Reset During Training
    reset_train_seq = []
    reset_train_seq.append(create_sequence("0", "1", "1"))  # Start training
    reset_train_seq.append(
        create_sequence("1", "1", "1")
    )  # Assert reset during training
    reset_train_seq.append(create_sequence("0", "1", "1"))  # Resume training
    scenarios.append(
        {"scenario": "Reset During Training", "input variable": reset_train_seq}
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
