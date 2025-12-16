import json

from cocotb.binary import BinaryValue


def get_binary_string(value, width):
    binary_val = BinaryValue(value=value, n_bits=width, bigEndian=True)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Synchronous Load Operation
    load_sequence = {
        "scenario": "Synchronous Load Operation",
        "input variable": [
            {"load": "1", "ena": "00", "data": "1" * 100},
            {"load": "0", "ena": "00", "data": "0" * 100},
        ],
    }
    scenarios.append(load_sequence)

    # Scenario 2: Right Rotation
    right_rot = {
        "scenario": "Right Rotation",
        "input variable": [{"load": "1", "ena": "00", "data": "1" + "0" * 99}],
    }
    for _ in range(101):  # Extra cycle to verify wrap-around
        right_rot["input variable"].append(
            {"load": "0", "ena": "01", "data": "0" * 100}
        )
    scenarios.append(right_rot)

    # Scenario 3: Left Rotation
    left_rot = {
        "scenario": "Left Rotation",
        "input variable": [{"load": "1", "ena": "00", "data": "1" + "0" * 99}],
    }
    for _ in range(101):
        left_rot["input variable"].append({"load": "0", "ena": "10", "data": "0" * 100})
    scenarios.append(left_rot)

    # Scenario 4: No Rotation
    no_rot = {
        "scenario": "No Rotation",
        "input variable": [{"load": "1", "ena": "00", "data": "1010" + "0" * 96}],
    }
    for i in range(10):
        no_rot["input variable"].append(
            {"load": "0", "ena": "00" if i % 2 == 0 else "11", "data": "0" * 100}
        )
    scenarios.append(no_rot)

    # Scenario 5: Load During Rotation
    load_during_rot = {
        "scenario": "Load During Rotation",
        "input variable": [{"load": "1", "ena": "00", "data": "1" + "0" * 99}],
    }
    for i in range(5):
        load_during_rot["input variable"].append(
            {"load": "0", "ena": "01", "data": "0" * 100}
        )
    load_during_rot["input variable"].append(
        {"load": "1", "ena": "01", "data": "1" * 100}
    )
    scenarios.append(load_during_rot)

    # Scenario 6: Alternating Directions
    alt_dir = {
        "scenario": "Alternating Directions",
        "input variable": [{"load": "1", "ena": "00", "data": "1010" + "0" * 96}],
    }
    for i in range(20):
        alt_dir["input variable"].append(
            {"load": "0", "ena": "10" if i % 2 == 0 else "01", "data": "0" * 100}
        )
    scenarios.append(alt_dir)

    # Scenario 7: Complex Data Pattern
    complex_pattern = {
        "scenario": "Complex Data Pattern",
        "input variable": [{"load": "1", "ena": "00", "data": ("10" * 50)}],
    }
    for i in range(10):
        complex_pattern["input variable"].append(
            {"load": "0", "ena": "10", "data": "0" * 100}
        )
    for i in range(10):
        complex_pattern["input variable"].append(
            {"load": "0", "ena": "01", "data": "0" * 100}
        )
    scenarios.append(complex_pattern)

    # Scenario 8: Rapid Enable Changes
    rapid_changes = {
        "scenario": "Rapid Enable Changes",
        "input variable": [{"load": "1", "ena": "00", "data": "1" * 100}],
    }
    ena_sequence = ["00", "01", "10", "11"]
    for i in range(20):
        rapid_changes["input variable"].append(
            {"load": "0", "ena": ena_sequence[i % 4], "data": "0" * 100}
        )
    scenarios.append(rapid_changes)

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
