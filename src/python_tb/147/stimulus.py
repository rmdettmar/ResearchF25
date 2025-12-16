import json


def generate_byte_sequence(data_byte, include_stop=True):
    # Start bit (0) + 8 data bits (LSB first) + stop bit (1)
    sequence = "0"  # Start bit
    for i in range(8):
        sequence += str((data_byte >> i) & 1)
    if include_stop:
        sequence += "1"  # Stop bit
    return sequence


def stimulus_gen():
    scenarios = []

    # Scenario 1: Normal Operation Single Byte
    normal_seq = []
    # Idle period (3 cycles)
    for _ in range(3):
        normal_seq.append({"in": "1", "reset": "0"})
    # Send byte 0x55 (01010101)
    byte_seq = generate_byte_sequence(0x55)
    for bit in byte_seq:
        normal_seq.append({"in": bit, "reset": "0"})
    scenarios.append(
        {"scenario": "Normal Operation Single Byte", "input variable": normal_seq}
    )

    # Scenario 2: Multiple Consecutive Bytes
    multi_byte_seq = []
    for byte in [0x55, 0xAA, 0x33]:
        # Idle period (2 cycles)
        for _ in range(2):
            multi_byte_seq.append({"in": "1", "reset": "0"})
        # Send byte
        byte_seq = generate_byte_sequence(byte)
        for bit in byte_seq:
            multi_byte_seq.append({"in": bit, "reset": "0"})
    scenarios.append(
        {"scenario": "Multiple Consecutive Bytes", "input variable": multi_byte_seq}
    )

    # Scenario 3: Missing Stop Bit
    missing_stop_seq = []
    # Send byte without stop bit
    byte_seq = generate_byte_sequence(0xAA, include_stop=False)
    for bit in byte_seq:
        missing_stop_seq.append({"in": "0", "reset": "0"})
    # Add extended '0' period before recovery
    for _ in range(3):
        missing_stop_seq.append({"in": "0", "reset": "0"})
    # Recovery period
    for _ in range(2):
        missing_stop_seq.append({"in": "1", "reset": "0"})
    scenarios.append(
        {"scenario": "Missing Stop Bit", "input variable": missing_stop_seq}
    )

    # Scenario 4: Premature Stop Bit
    premature_stop_seq = []
    byte_seq = list(generate_byte_sequence(0x55))
    byte_seq[5] = "1"  # Insert premature '1' during data bits
    for bit in byte_seq:
        premature_stop_seq.append({"in": bit, "reset": "0"})
    scenarios.append(
        {"scenario": "Premature Stop Bit", "input variable": premature_stop_seq}
    )

    # Scenario 5: Reset During Reception
    reset_seq = []
    byte_seq = generate_byte_sequence(0xAA)
    for i, bit in enumerate(byte_seq):
        if i == 5:  # Assert reset during data reception
            reset_seq.append({"in": bit, "reset": "1"})
        else:
            reset_seq.append({"in": bit, "reset": "0"})
    scenarios.append(
        {"scenario": "Reset During Reception", "input variable": reset_seq}
    )

    # Scenario 6: Extended Idle Period
    idle_seq = []
    for _ in range(10):  # Extended idle period
        idle_seq.append({"in": "1", "reset": "0"})
    scenarios.append({"scenario": "Extended Idle Period", "input variable": idle_seq})

    # Scenario 7: False Start Bit
    false_start_seq = []
    false_start_seq.append({"in": "1", "reset": "0"})
    false_start_seq.append({"in": "0", "reset": "0"})
    for _ in range(3):  # Return to idle without data
        false_start_seq.append({"in": "1", "reset": "0"})
    scenarios.append({"scenario": "False Start Bit", "input variable": false_start_seq})

    # Scenario 8: Boundary Value Data
    boundary_seq = []
    # Test 0x00
    byte_seq = generate_byte_sequence(0x00)
    for bit in byte_seq:
        boundary_seq.append({"in": bit, "reset": "0"})
    # Idle period
    boundary_seq.append({"in": "1", "reset": "0"})
    # Test 0xFF
    byte_seq = generate_byte_sequence(0xFF)
    for bit in byte_seq:
        boundary_seq.append({"in": bit, "reset": "0"})
    scenarios.append(
        {"scenario": "Boundary Value Data", "input variable": boundary_seq}
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
