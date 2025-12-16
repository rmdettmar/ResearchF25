import json

from cocotb.binary import BinaryValue


def create_binary_sequence(value, bits=1):
    return BinaryValue(value=value, n_bits=bits, bigEndian=True).binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Pattern Detection
    sequence1 = {
        "scenario": "Basic Pattern Detection",
        "input variable": [
            {"reset": "1", "data": "0", "ack": "0"},  # Initial reset
            {"reset": "0", "data": "1", "ack": "0"},  # Send 1101
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},  # Send 0000 delay
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            *[
                {"reset": "0", "data": "0", "ack": "0"} for _ in range(998)
            ],  # Wait for count
            {"reset": "0", "data": "0", "ack": "1"},  # Acknowledge
        ],
    }
    scenarios.append(sequence1)

    # Scenario 2: Maximum Delay Count
    sequence2 = {
        "scenario": "Maximum Delay Count",
        "input variable": [
            {"reset": "0", "data": "1", "ack": "0"},  # Send 1101
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},  # Send 1111 delay
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},
            *[
                {"reset": "0", "data": "0", "ack": "0"} for _ in range(15998)
            ],  # Wait for count
            {"reset": "0", "data": "0", "ack": "1"},  # Acknowledge
        ],
    }
    scenarios.append(sequence2)

    # Scenario 3: Partial Pattern Reset
    sequence3 = {
        "scenario": "Partial Pattern Reset",
        "input variable": [
            {"reset": "0", "data": "1", "ack": "0"},  # Send 110
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "1", "data": "0", "ack": "0"},  # Reset
            {"reset": "0", "data": "0", "ack": "0"},  # Resume normal operation
        ],
    }
    scenarios.append(sequence3)

    # Scenario 4: Invalid Pattern Rejection
    sequence4 = {
        "scenario": "Invalid Pattern Rejection",
        "input variable": [
            {"reset": "0", "data": "1", "ack": "0"},  # Send 1100
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},  # Send 1111
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},
        ],
    }
    scenarios.append(sequence4)

    # Scenario 5: Missing Acknowledgment
    sequence5 = {
        "scenario": "Missing Acknowledgment",
        "input variable": [
            {"reset": "0", "data": "1", "ack": "0"},  # Send pattern and delay
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            *[
                {"reset": "0", "data": "0", "ack": "0"} for _ in range(1000)
            ],  # Wait without ack
        ],
    }
    scenarios.append(sequence5)

    # Scenario 6: Immediate Reset During Count
    sequence6 = {
        "scenario": "Immediate Reset During Count",
        "input variable": [
            {"reset": "0", "data": "1", "ack": "0"},  # Start counting sequence
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "1", "data": "0", "ack": "0"},  # Reset during count
            {"reset": "0", "data": "0", "ack": "0"},
        ],
    }
    scenarios.append(sequence6)

    # Scenario 7: Data Input During Count
    sequence7 = {
        "scenario": "Data Input During Count",
        "input variable": [
            {"reset": "0", "data": "1", "ack": "0"},  # First pattern
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},  # Delay bits
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},  # Send new pattern during count
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},
            *[{"reset": "0", "data": "0", "ack": "0"} for _ in range(996)],
            {"reset": "0", "data": "0", "ack": "1"},
        ],
    }
    scenarios.append(sequence7)

    # Scenario 8: Multiple Sequential Timers
    sequence8 = {
        "scenario": "Multiple Sequential Timers",
        "input variable": [
            # First timer (delay = 1)
            *[{"reset": "0", "data": bit, "ack": "0"} for bit in "11011000"],
            *[{"reset": "0", "data": "0", "ack": "0"} for _ in range(1998)],
            {"reset": "0", "data": "0", "ack": "1"},
            # Second timer (delay = 2)
            *[{"reset": "0", "data": bit, "ack": "0"} for bit in "11010100"],
            *[{"reset": "0", "data": "0", "ack": "0"} for _ in range(2998)],
            {"reset": "0", "data": "0", "ack": "1"},
            # Third timer (delay = 3)
            *[{"reset": "0", "data": bit, "ack": "0"} for bit in "11010110"],
            *[{"reset": "0", "data": "0", "ack": "0"} for _ in range(3998)],
            {"reset": "0", "data": "0", "ack": "1"},
        ],
    }
    scenarios.append(sequence8)

    # Scenario 9: Count Output Verification
    sequence9 = {
        "scenario": "Count Output Verification",
        "input variable": [
            *[
                {"reset": "0", "data": bit, "ack": "0"} for bit in "11010011"
            ],  # Pattern + delay=3
            *[
                {"reset": "0", "data": "0", "ack": "0"} for _ in range(3998)
            ],  # Wait for full count
            {"reset": "0", "data": "0", "ack": "1"},
        ],
    }
    scenarios.append(sequence9)

    # Scenario 10: Signal Timing Verification
    sequence10 = {
        "scenario": "Signal Timing Verification",
        "input variable": [
            {"reset": "1", "data": "0", "ack": "0"},  # Reset
            {"reset": "0", "data": "1", "ack": "0"},  # Pattern
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "1", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},  # Delay=0
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            {"reset": "0", "data": "0", "ack": "0"},
            *[{"reset": "0", "data": "0", "ack": "0"} for _ in range(998)],
            {"reset": "0", "data": "0", "ack": "1"},  # Acknowledge
        ],
    }
    scenarios.append(sequence10)

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
