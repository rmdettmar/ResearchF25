import json

from cocotb.binary import BinaryValue


def create_binary_sequence(value, width=10):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Load and Countdown
    sequence = []
    sequence.append({"load": "1", "data": create_binary_sequence(0x010)})  # Load 16
    sequence.extend(
        [{"load": "0", "data": create_binary_sequence(0x010)} for _ in range(16)]
    )
    scenarios.append(
        {"scenario": "Basic Load and Countdown", "input variable": sequence}
    )

    # Scenario 2: Zero Load Value
    sequence = []
    sequence.append({"load": "1", "data": create_binary_sequence(0x000)})  # Load 0
    sequence.extend(
        [{"load": "0", "data": create_binary_sequence(0x000)} for _ in range(5)]
    )
    scenarios.append({"scenario": "Zero Load Value", "input variable": sequence})

    # Scenario 3: Maximum Count Value
    sequence = []
    sequence.append({"load": "1", "data": create_binary_sequence(0x3FF)})  # Load 1023
    sequence.extend(
        [{"load": "0", "data": create_binary_sequence(0x3FF)} for _ in range(1024)]
    )
    scenarios.append({"scenario": "Maximum Count Value", "input variable": sequence})

    # Scenario 4: Mid-Count Load
    sequence = []
    sequence.append({"load": "1", "data": create_binary_sequence(0x020)})  # Load 32
    sequence.extend(
        [{"load": "0", "data": create_binary_sequence(0x020)} for _ in range(16)]
    )
    sequence.append({"load": "1", "data": create_binary_sequence(0x010)})  # Load 16
    sequence.extend(
        [{"load": "0", "data": create_binary_sequence(0x010)} for _ in range(16)]
    )
    scenarios.append({"scenario": "Mid-Count Load", "input variable": sequence})

    # Scenario 5: Multiple Sequential Loads
    sequence = []
    sequence.append({"load": "1", "data": create_binary_sequence(0x005)})
    sequence.append({"load": "1", "data": create_binary_sequence(0x003)})
    sequence.append({"load": "1", "data": create_binary_sequence(0x008)})
    sequence.extend(
        [{"load": "0", "data": create_binary_sequence(0x008)} for _ in range(8)]
    )
    scenarios.append(
        {"scenario": "Multiple Sequential Loads", "input variable": sequence}
    )

    # Scenario 6: Hold at Zero
    sequence = []
    sequence.append({"load": "1", "data": create_binary_sequence(0x002)})  # Load 2
    sequence.extend(
        [{"load": "0", "data": create_binary_sequence(0x002)} for _ in range(3)]
    )  # Count down
    sequence.extend(
        [{"load": "0", "data": create_binary_sequence(0x000)} for _ in range(10)]
    )  # Hold at zero
    scenarios.append({"scenario": "Hold at Zero", "input variable": sequence})

    # Scenario 7: Continuous Operation
    sequence = []
    # First sequence: 5
    sequence.append({"load": "1", "data": create_binary_sequence(0x005)})
    sequence.extend(
        [{"load": "0", "data": create_binary_sequence(0x005)} for _ in range(5)]
    )
    # Second sequence: 3
    sequence.append({"load": "1", "data": create_binary_sequence(0x003)})
    sequence.extend(
        [{"load": "0", "data": create_binary_sequence(0x003)} for _ in range(3)]
    )
    # Third sequence: 4
    sequence.append({"load": "1", "data": create_binary_sequence(0x004)})
    sequence.extend(
        [{"load": "0", "data": create_binary_sequence(0x004)} for _ in range(4)]
    )
    scenarios.append({"scenario": "Continuous Operation", "input variable": sequence})

    # Scenario 8: Load Signal Timing
    sequence = []
    sequence.append({"load": "1", "data": create_binary_sequence(0x004)})
    sequence.append({"load": "0", "data": create_binary_sequence(0x004)})
    sequence.append({"load": "1", "data": create_binary_sequence(0x003)})
    sequence.append({"load": "0", "data": create_binary_sequence(0x003)})
    scenarios.append({"scenario": "Load Signal Timing", "input variable": sequence})

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
