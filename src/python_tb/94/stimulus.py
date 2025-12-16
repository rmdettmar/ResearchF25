import json

from cocotb.binary import BinaryValue


def create_byte(bit3_value, other_bits=0):
    # Helper function to create 8-bit byte with specific bit3 value
    value = other_bits | (bit3_value << 3)
    binary_val = BinaryValue(value=value, n_bits=8)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Message Detection
    basic_msg = {
        "scenario": "Basic Message Detection",
        "input variable": [
            {"in": create_byte(1, 0xF), "reset": "0"},  # First byte with in[3]=1
            {"in": create_byte(0, 0x5), "reset": "0"},  # Second byte
            {"in": create_byte(0, 0x7), "reset": "0"},  # Third byte
            {"in": create_byte(0, 0x0), "reset": "0"},  # Extra cycle to check done
        ],
    }
    scenarios.append(basic_msg)

    # Scenario 2: Multiple Valid Messages
    multiple_msgs = {
        "scenario": "Multiple Valid Messages",
        "input variable": [
            {"in": create_byte(1, 0x1), "reset": "0"},
            {"in": create_byte(0, 0x2), "reset": "0"},
            {"in": create_byte(0, 0x3), "reset": "0"},
            {"in": create_byte(1, 0x4), "reset": "0"},
            {"in": create_byte(0, 0x5), "reset": "0"},
            {"in": create_byte(0, 0x6), "reset": "0"},
        ],
    }
    scenarios.append(multiple_msgs)

    # Scenario 3: Invalid Byte Stream Sync
    sync_msg = {
        "scenario": "Invalid Byte Stream Sync",
        "input variable": [
            {"in": create_byte(0, 0x1), "reset": "0"},
            {"in": create_byte(0, 0x2), "reset": "0"},
            {"in": create_byte(1, 0x3), "reset": "0"},
            {"in": create_byte(0, 0x4), "reset": "0"},
            {"in": create_byte(0, 0x5), "reset": "0"},
        ],
    }
    scenarios.append(sync_msg)

    # Scenario 4: Reset During Message
    reset_msg = {
        "scenario": "Reset During Message",
        "input variable": [
            {"in": create_byte(1, 0x1), "reset": "0"},
            {"in": create_byte(0, 0x2), "reset": "1"},
            {"in": create_byte(1, 0x3), "reset": "0"},
            {"in": create_byte(0, 0x4), "reset": "0"},
            {"in": create_byte(0, 0x5), "reset": "0"},
        ],
    }
    scenarios.append(reset_msg)

    # Scenario 5: False Message Start
    false_start = {
        "scenario": "False Message Start",
        "input variable": [
            {"in": create_byte(1, 0x1), "reset": "0"},
            {"in": create_byte(1, 0x2), "reset": "0"},
            {"in": create_byte(0, 0x3), "reset": "0"},
            {"in": create_byte(0, 0x4), "reset": "0"},
        ],
    }
    scenarios.append(false_start)

    # Scenario 6: Continuous Reset Toggle
    reset_toggle = {
        "scenario": "Continuous Reset Toggle",
        "input variable": [
            {"in": create_byte(1, 0x1), "reset": "0"},
            {"in": create_byte(0, 0x2), "reset": "1"},
            {"in": create_byte(0, 0x3), "reset": "0"},
            {"in": create_byte(1, 0x4), "reset": "1"},
            {"in": create_byte(0, 0x5), "reset": "0"},
        ],
    }
    scenarios.append(reset_toggle)

    # Scenario 7: All Bytes with in[3]=1
    all_bit3 = {
        "scenario": "All Bytes with in[3]=1",
        "input variable": [
            {"in": create_byte(1, 0x1), "reset": "0"},
            {"in": create_byte(1, 0x2), "reset": "0"},
            {"in": create_byte(1, 0x3), "reset": "0"},
            {"in": create_byte(1, 0x4), "reset": "0"},
        ],
    }
    scenarios.append(all_bit3)

    # Scenario 8: Done Signal Timing
    done_timing = {
        "scenario": "Done Signal Timing",
        "input variable": [
            {"in": create_byte(1, 0x1), "reset": "0"},
            {"in": create_byte(0, 0x2), "reset": "0"},
            {"in": create_byte(0, 0x3), "reset": "0"},
            {"in": create_byte(0, 0x0), "reset": "0"},
            {"in": create_byte(1, 0x4), "reset": "0"},
        ],
    }
    scenarios.append(done_timing)

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
