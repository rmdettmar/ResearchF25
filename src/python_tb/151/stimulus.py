import json


def stimulus_gen():
    scenarios = []

    # Helper function to create a sequence dictionary
    def create_sequence(name, input_list):
        return {"scenario": name, "input variable": input_list}

    # Scenario 1: Basic Pattern Detection
    basic_pattern = []
    for i in range(10):
        basic_pattern.append(
            {
                "reset": "0",
                "data": "1" if i in [4, 5, 6] else "0",
                "done_counting": "0",
                "ack": "0",
            }
        )
    scenarios.append(create_sequence("Basic Pattern Detection", basic_pattern))

    # Scenario 2: Partial Pattern Reset
    partial_pattern = []
    for i in range(8):
        partial_pattern.append(
            {
                "reset": "1" if i == 4 else "0",
                "data": "1" if i in [1, 2] else "0",
                "done_counting": "0",
                "ack": "0",
            }
        )
    scenarios.append(create_sequence("Partial Pattern Reset", partial_pattern))

    # Scenario 3: False Pattern Detection
    false_pattern = []
    for i in range(12):
        false_pattern.append(
            {
                "reset": "0",
                "data": "1" if i in [2, 3, 6, 7, 8, 9] else "0",
                "done_counting": "0",
                "ack": "0",
            }
        )
    scenarios.append(create_sequence("False Pattern Detection", false_pattern))

    # Scenario 4: Counting State Transition
    counting_state = []
    for i in range(15):
        counting_state.append(
            {
                "reset": "0",
                "data": "1" if i in [4, 5, 6] else "0",
                "done_counting": "1" if i == 14 else "0",
                "ack": "0",
            }
        )
    scenarios.append(create_sequence("Counting State Transition", counting_state))

    # Scenario 5: Completion Handshake
    completion = []
    for i in range(12):
        completion.append(
            {
                "reset": "0",
                "data": "0",
                "done_counting": "1",
                "ack": "1" if i == 10 else "0",
            }
        )
    scenarios.append(create_sequence("Completion Handshake", completion))

    # Scenario 6: Reset During Operation
    reset_op = []
    for i in range(10):
        reset_op.append(
            {
                "reset": "1" if i == 5 else "0",
                "data": "1" if i in [2, 3, 4] else "0",
                "done_counting": "0",
                "ack": "0",
            }
        )
    scenarios.append(create_sequence("Reset During Operation", reset_op))

    # Scenario 7: Multiple Timer Cycles
    multiple_cycles = []
    for i in range(20):
        multiple_cycles.append(
            {
                "reset": "0",
                "data": "1" if i in [2, 3, 4, 12, 13, 14] else "0",
                "done_counting": "1" if i in [8, 18] else "0",
                "ack": "1" if i in [9, 19] else "0",
            }
        )
    scenarios.append(create_sequence("Multiple Timer Cycles", multiple_cycles))

    # Scenario 8: Quick Acknowledgment
    quick_ack = []
    for i in range(15):
        quick_ack.append(
            {
                "reset": "0",
                "data": "1" if i in [2, 3, 4] else "0",
                "done_counting": "1" if i == 10 else "0",
                "ack": "1" if i == 11 else "0",
            }
        )
    scenarios.append(create_sequence("Quick Acknowledgment", quick_ack))

    # Scenario 9: Delayed Acknowledgment
    delayed_ack = []
    for i in range(20):
        delayed_ack.append(
            {
                "reset": "0",
                "data": "1" if i in [2, 3, 4] else "0",
                "done_counting": "1" if i >= 10 else "0",
                "ack": "1" if i == 18 else "0",
            }
        )
    scenarios.append(create_sequence("Delayed Acknowledgment", delayed_ack))

    # Scenario 10: Signal Timing Verification
    timing_verify = []
    for i in range(25):
        timing_verify.append(
            {
                "reset": "0",
                "data": "1" if i in [2, 3, 4] else "0",
                "done_counting": "1" if i in [15, 16, 17] else "0",
                "ack": "1" if i == 20 else "0",
            }
        )
    scenarios.append(create_sequence("Signal Timing Verification", timing_verify))

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
