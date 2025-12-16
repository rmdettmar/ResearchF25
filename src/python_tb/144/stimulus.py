import json


def stimulus_gen():
    scenarios = []

    # Helper function to create stimulus dictionary
    def create_stimulus(name, input_sequence):
        return {
            "scenario": name,
            "input variable": [
                {"clk": "1", "reset": "0", "in": bit} for bit in input_sequence
            ],
        }

    # Basic Flag Detection
    scenarios.append(
        create_stimulus(
            "Basic Flag Detection",
            "01111110" + "0000",  # Flag pattern + extra bits to verify timing
        )
    )

    # Bit Stuffing Detection
    scenarios.append(
        create_stimulus(
            "Bit Stuffing Detection", "0111110" + "000"  # Stuff pattern + extra bits
        )
    )

    # Error Condition
    scenarios.append(
        create_stimulus(
            "Error Condition", "01111111" + "000"  # Error pattern + extra bits
        )
    )

    # Reset Behavior
    reset_sequence = []
    for bit in "01111":
        reset_sequence.extend(
            [
                {"clk": "1", "reset": "0", "in": bit},
                {"clk": "1", "reset": "1", "in": bit},
                {"clk": "1", "reset": "0", "in": "0"},
            ]
        )
    scenarios.append({"scenario": "Reset Behavior", "input variable": reset_sequence})

    # Consecutive Flags
    scenarios.append(
        create_stimulus(
            "Consecutive Flags", "01111110" + "01111110" + "00"  # Two consecutive flags
        )
    )

    # Mixed Pattern Sequence
    scenarios.append(
        create_stimulus(
            "Mixed Pattern Sequence",
            "01111110" + "0111110" + "01111111" + "000",  # Flag + stuff + error
        )
    )

    # Partial Pattern Recovery
    scenarios.append(
        create_stimulus(
            "Partial Pattern Recovery",
            "01111" + "01111110" + "000",  # Partial + complete flag
        )
    )

    # Output Timing
    scenarios.append(
        create_stimulus(
            "Output Timing",
            "01111110"
            + "0111110"
            + "01111111"
            + "0000",  # All patterns with extra cycles
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
