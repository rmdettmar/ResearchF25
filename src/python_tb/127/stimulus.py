import json

from cocotb.binary import BinaryValue


def int_to_bin(value, width):
    binary_val = BinaryValue(value=value, n_bits=width, bigEndian=True)
    return binary_val.binstr


def create_stimulus(areset, load, ena, data):
    return {
        "areset": int_to_bin(areset, 1),
        "load": int_to_bin(load, 1),
        "ena": int_to_bin(ena, 1),
        "data": int_to_bin(data, 4),
    }


def stimulus_gen():
    stimulus_list = []

    # Scenario 1: Asynchronous Reset Verification
    scenario1 = {
        "scenario": "Asynchronous Reset Verification",
        "input variable": [
            create_stimulus(0, 1, 0, 0xF),  # Load 1111
            create_stimulus(1, 1, 0, 0xF),  # Assert reset during load
            create_stimulus(1, 0, 1, 0x0),  # Assert reset during shift
            create_stimulus(0, 0, 0, 0x0),  # Release reset
        ],
    }

    # Scenario 2: Load Operation
    scenario2 = {
        "scenario": "Load Operation",
        "input variable": [
            create_stimulus(0, 1, 0, 0x5),  # Load 0101
            create_stimulus(0, 1, 0, 0xA),  # Load 1010
            create_stimulus(0, 1, 0, 0xF),  # Load 1111
            create_stimulus(0, 1, 0, 0x0),  # Load 0000
        ],
    }

    # Scenario 3: Right Shift Operation
    scenario3 = {
        "scenario": "Right Shift Operation",
        "input variable": [
            create_stimulus(0, 1, 0, 0xF),  # Load 1111
            create_stimulus(0, 0, 1, 0x0),  # Shift 1
            create_stimulus(0, 0, 1, 0x0),  # Shift 2
            create_stimulus(0, 0, 1, 0x0),  # Shift 3
            create_stimulus(0, 0, 1, 0x0),  # Shift 4
        ],
    }

    # Scenario 4: Priority Verification
    scenario4 = {
        "scenario": "Priority Verification",
        "input variable": [
            create_stimulus(0, 1, 1, 0x5),  # Load with both load and ena
            create_stimulus(0, 1, 1, 0xA),  # Verify load priority
            create_stimulus(0, 1, 1, 0xF),  # Another verification
        ],
    }

    # Scenario 5: No Operation
    scenario5 = {
        "scenario": "No Operation",
        "input variable": [
            create_stimulus(0, 1, 0, 0xA),  # Load initial value
            create_stimulus(0, 0, 0, 0x0),  # Hold
            create_stimulus(0, 0, 0, 0x0),  # Hold
            create_stimulus(0, 0, 0, 0x0),  # Hold
        ],
    }

    # Scenario 6: Sequential Operations
    scenario6 = {
        "scenario": "Sequential Operations",
        "input variable": [
            create_stimulus(0, 1, 0, 0xF),  # Load
            create_stimulus(0, 0, 1, 0x0),  # Shift
            create_stimulus(0, 0, 0, 0x0),  # Hold
            create_stimulus(0, 0, 1, 0x0),  # Shift
        ],
    }

    # Scenario 7: Control Signal Timing
    scenario7 = {
        "scenario": "Control Signal Timing",
        "input variable": [
            create_stimulus(0, 0, 0, 0x0),  # Idle
            create_stimulus(0, 1, 0, 0x5),  # Load setup
            create_stimulus(0, 1, 0, 0x5),  # Load hold
            create_stimulus(0, 0, 1, 0x0),  # Shift setup
        ],
    }

    # Scenario 8: Reset Recovery
    scenario8 = {
        "scenario": "Reset Recovery",
        "input variable": [
            create_stimulus(1, 0, 0, 0x0),  # Assert reset
            create_stimulus(0, 0, 0, 0x0),  # Deassert reset
            create_stimulus(0, 1, 0, 0x5),  # Immediate load
            create_stimulus(0, 0, 1, 0x0),  # Immediate shift
        ],
    }

    stimulus_list = [
        scenario1,
        scenario2,
        scenario3,
        scenario4,
        scenario5,
        scenario6,
        scenario7,
        scenario8,
    ]

    return stimulus_list


if __name__ == "__main__":
    result = stimulus_gen()
    # 将结果转换为 JSON 字符串
    if isinstance(result, list):
        result = json.dumps(result, indent=4)
    elif not isinstance(result, str):
        result = json.dumps(result, indent=4)

    with open("stimulus.json", "w") as f:
        f.write(result)
