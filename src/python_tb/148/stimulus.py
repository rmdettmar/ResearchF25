import json


def stimulus_gen():
    scenarios = []

    def create_byte_sequence(data_byte):
        # Convert integer to 8-bit binary string, reverse for LSB first
        data_bits = format(data_byte, "08b")[::-1]
        # Return complete sequence: start(0) + data + stop(1)
        return "0" + data_bits + "1"

    def create_idle_sequence(length):
        return "1" * length

    # Scenario 1: Basic Valid Byte Reception (0x55)
    scenarios.append(
        {
            "scenario": "Basic Valid Byte Reception",
            "input variable": [
                {"in": "1", "reset": "0"},  # Initial idle
                {"in": create_byte_sequence(0x55), "reset": "0"},  # Valid byte
            ],
        }
    )

    # Scenario 2: Multiple Consecutive Bytes
    multi_byte = (
        create_byte_sequence(0xAA)
        + create_byte_sequence(0x55)
        + create_byte_sequence(0xFF)
    )
    scenarios.append(
        {
            "scenario": "Multiple Consecutive Bytes",
            "input variable": [
                {"in": "1", "reset": "0"},  # Initial idle
                {"in": multi_byte, "reset": "0"},  # Three consecutive bytes
            ],
        }
    )

    # Scenario 3: Missing Stop Bit
    invalid_byte = (
        "0" + format(0x55, "08b")[::-1] + "0" + "1" * 5
    )  # Missing stop bit followed by idle
    scenarios.append(
        {
            "scenario": "Missing Stop Bit",
            "input variable": [
                {"in": "1", "reset": "0"},  # Initial idle
                {"in": invalid_byte, "reset": "0"},
            ],
        }
    )

    # Scenario 4: Idle Line Recovery
    recovery_sequence = (
        "0" + format(0x55, "08b")[::-1] + "0" + "1" * 5 + create_byte_sequence(0xAA)
    )
    scenarios.append(
        {
            "scenario": "Idle Line Recovery",
            "input variable": [
                {"in": "1", "reset": "0"},  # Initial idle
                {"in": recovery_sequence, "reset": "0"},
            ],
        }
    )

    # Scenario 5: Reset During Reception
    reset_sequence = "0" + format(0x55, "04b")[::-1]  # Half byte
    scenarios.append(
        {
            "scenario": "Reset During Reception",
            "input variable": [
                {"in": "1", "reset": "0"},  # Initial idle
                {"in": reset_sequence, "reset": "0"},  # Start reception
                {"in": "1", "reset": "1"},  # Assert reset
                {
                    "in": create_byte_sequence(0xAA),
                    "reset": "0",
                },  # New byte after reset
            ],
        }
    )

    # Scenario 6: Bit Ordering Verification
    scenarios.append(
        {
            "scenario": "Bit Ordering Verification",
            "input variable": [
                {"in": "1", "reset": "0"},  # Initial idle
                {"in": create_byte_sequence(0x80), "reset": "0"},  # Byte with MSB set
            ],
        }
    )

    # Scenario 7: Extended Idle Period
    scenarios.append(
        {
            "scenario": "Extended Idle Period",
            "input variable": [
                {"in": create_idle_sequence(10), "reset": "0"},  # Extended idle
                {"in": create_byte_sequence(0x55), "reset": "0"},  # Valid byte
            ],
        }
    )

    # Scenario 8: Premature Start Bit
    premature_start = (
        "0" + format(0x55, "04b")[::-1] + "0" + format(0x55, "04b")[::-1] + "1"
    )
    scenarios.append(
        {
            "scenario": "Premature Start Bit",
            "input variable": [
                {"in": "1", "reset": "0"},  # Initial idle
                {"in": premature_start, "reset": "0"},
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
