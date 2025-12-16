import json


def stimulus_gen():
    scenarios = []

    # Helper function to create reset sequences
    def create_reset_sequence(cycles, reset_value):
        return [{"reset": "1" if reset_value else "0"} for _ in range(cycles)]

    # Scenario 1: Synchronous Reset Verification
    scenarios.append(
        {
            "scenario": "Synchronous Reset Verification",
            "input variable": [
                {"reset": "1"},  # Assert reset
                {"reset": "0"},  # De-assert reset and observe
            ],
        }
    )

    # Scenario 2: Basic LFSR Operation
    basic_op = {
        "scenario": "Basic LFSR Operation",
        "input variable": [{"reset": "1"}]  # Initial reset
        + [{"reset": "0"} for _ in range(100)],
    }  # Run for 100 cycles
    scenarios.append(basic_op)

    # Scenario 3: Mid-sequence Reset
    mid_seq_reset = {
        "scenario": "Mid-sequence Reset",
        "input variable": [{"reset": "1"}]  # Initial reset
        + [{"reset": "0"} for _ in range(50)]  # Run for 50 cycles
        + [{"reset": "1"}]  # Assert reset
        + [{"reset": "0"} for _ in range(50)],
    }  # Run for 50 more cycles
    scenarios.append(mid_seq_reset)

    # Scenario 4: Full Sequence Period
    # Note: Using a shorter sequence for practical testing
    full_seq = {
        "scenario": "Full Sequence Period",
        "input variable": [{"reset": "1"}]  # Initial reset
        + [{"reset": "0"} for _ in range(1000)],
    }  # Run for 1000 cycles
    scenarios.append(full_seq)

    # Scenario 5: Reset During Active Operation
    reset_during_op = {
        "scenario": "Reset During Active Operation",
        "input variable": [{"reset": "1"}]  # Initial reset
        + [{"reset": "0"} for _ in range(10)]  # Run for 10 cycles
        + [{"reset": "1"}]  # Sudden reset
        + [{"reset": "0"} for _ in range(5)],
    }  # Continue operation
    scenarios.append(reset_during_op)

    # Scenario 6: Back-to-Back Reset
    back_to_back = {
        "scenario": "Back-to-Back Reset",
        "input variable": [{"reset": "1"} for _ in range(5)]  # Multiple resets
        + [{"reset": "0"} for _ in range(5)],
    }  # Continue operation
    scenarios.append(back_to_back)

    # Scenario 7: Feedback Path Verification
    feedback_verify = {
        "scenario": "Feedback Path Verification",
        "input variable": [{"reset": "1"}]  # Initial reset
        + [{"reset": "0"} for _ in range(32)],
    }  # Run for 32 cycles
    scenarios.append(feedback_verify)

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
