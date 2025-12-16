import json

from cocotb.binary import BinaryValue


def create_32bit_value(value):
    return BinaryValue(value=value, n_bits=32, bigEndian=True).binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Single Bit Transition
    single_trans = {
        "scenario": "Single Bit Transition",
        "input variable": [
            {"reset": "0", "in": create_32bit_value(0x00000002)},
            {"reset": "0", "in": create_32bit_value(0x00000000)},
        ],
    }
    scenarios.append(single_trans)

    # Scenario 2: Multiple Simultaneous Transitions
    multi_trans = {
        "scenario": "Multiple Simultaneous Transitions",
        "input variable": [
            {"reset": "0", "in": create_32bit_value(0x0000F000)},
            {"reset": "0", "in": create_32bit_value(0x00000000)},
        ],
    }
    scenarios.append(multi_trans)

    # Scenario 3: No Transition Detection
    no_trans = {
        "scenario": "No Transition Detection",
        "input variable": [
            {"reset": "0", "in": create_32bit_value(0x00000000)},
            {"reset": "0", "in": create_32bit_value(0x0000FFFF)},
            {"reset": "0", "in": create_32bit_value(0x0000FFFF)},
        ],
    }
    scenarios.append(no_trans)

    # Scenario 4: Reset Functionality
    reset_func = {
        "scenario": "Reset Functionality",
        "input variable": [
            {"reset": "0", "in": create_32bit_value(0xFFFFFFFF)},
            {"reset": "0", "in": create_32bit_value(0x00000000)},
            {"reset": "1", "in": create_32bit_value(0x00000000)},
        ],
    }
    scenarios.append(reset_func)

    # Scenario 5: Consecutive Transitions
    consec_trans = {
        "scenario": "Consecutive Transitions",
        "input variable": [
            {"reset": "0", "in": create_32bit_value(0x00000001)},
            {"reset": "0", "in": create_32bit_value(0x00000000)},
            {"reset": "0", "in": create_32bit_value(0x00000001)},
            {"reset": "0", "in": create_32bit_value(0x00000000)},
        ],
    }
    scenarios.append(consec_trans)

    # Scenario 6: All Bits Transition
    all_trans = {
        "scenario": "All Bits Transition",
        "input variable": [
            {"reset": "0", "in": create_32bit_value(0xFFFFFFFF)},
            {"reset": "0", "in": create_32bit_value(0x00000000)},
        ],
    }
    scenarios.append(all_trans)

    # Scenario 7: Reset Recovery
    reset_recovery = {
        "scenario": "Reset Recovery",
        "input variable": [
            {"reset": "1", "in": create_32bit_value(0xFFFFFFFF)},
            {"reset": "0", "in": create_32bit_value(0xFFFFFFFF)},
            {"reset": "0", "in": create_32bit_value(0x00000000)},
        ],
    }
    scenarios.append(reset_recovery)

    # Scenario 8: Long-term Stability
    stability = {
        "scenario": "Long-term Stability",
        "input variable": [
            {"reset": "0", "in": create_32bit_value(0xFFFFFFFF)},
            {"reset": "0", "in": create_32bit_value(0x00000000)},
            {"reset": "0", "in": create_32bit_value(0x00000000)},
            {"reset": "0", "in": create_32bit_value(0x00000000)},
            {"reset": "0", "in": create_32bit_value(0x00000000)},
        ],
    }
    scenarios.append(stability)

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
