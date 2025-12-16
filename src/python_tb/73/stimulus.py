import json

from cocotb.binary import BinaryValue


def create_binary_value(value, width):
    return BinaryValue(value=value, n_bits=width, bigEndian=True).binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Valid Selection Range
    scenario1 = {"scenario": "Valid Selection Range", "input variable": []}
    for sel in range(6):
        scenario1["input variable"].append(
            {
                "sel": create_binary_value(sel, 3),
                "data0": create_binary_value(0x1, 4),
                "data1": create_binary_value(0x2, 4),
                "data2": create_binary_value(0x4, 4),
                "data3": create_binary_value(0x8, 4),
                "data4": create_binary_value(0xC, 4),
                "data5": create_binary_value(0xF, 4),
            }
        )
    scenarios.append(scenario1)

    # Scenario 2: Invalid Selection Values
    scenario2 = {"scenario": "Invalid Selection Values", "input variable": []}
    for sel in [6, 7]:
        scenario2["input variable"].append(
            {
                "sel": create_binary_value(sel, 3),
                "data0": create_binary_value(0xF, 4),
                "data1": create_binary_value(0xF, 4),
                "data2": create_binary_value(0xF, 4),
                "data3": create_binary_value(0xF, 4),
                "data4": create_binary_value(0xF, 4),
                "data5": create_binary_value(0xF, 4),
            }
        )
    scenarios.append(scenario2)

    # Scenario 3: All Zeros Data Path
    scenario3 = {"scenario": "All Zeros Data Path", "input variable": []}
    for sel in range(8):
        scenario3["input variable"].append(
            {
                "sel": create_binary_value(sel, 3),
                "data0": create_binary_value(0x0, 4),
                "data1": create_binary_value(0x0, 4),
                "data2": create_binary_value(0x0, 4),
                "data3": create_binary_value(0x0, 4),
                "data4": create_binary_value(0x0, 4),
                "data5": create_binary_value(0x0, 4),
            }
        )
    scenarios.append(scenario3)

    # Scenario 4: All Ones Data Path
    scenario4 = {"scenario": "All Ones Data Path", "input variable": []}
    for sel in range(8):
        scenario4["input variable"].append(
            {
                "sel": create_binary_value(sel, 3),
                "data0": create_binary_value(0xF, 4),
                "data1": create_binary_value(0xF, 4),
                "data2": create_binary_value(0xF, 4),
                "data3": create_binary_value(0xF, 4),
                "data4": create_binary_value(0xF, 4),
                "data5": create_binary_value(0xF, 4),
            }
        )
    scenarios.append(scenario4)

    # Scenario 5: Alternating Patterns
    scenario5 = {"scenario": "Alternating Patterns", "input variable": []}
    for sel in range(6):
        scenario5["input variable"].append(
            {
                "sel": create_binary_value(sel, 3),
                "data0": create_binary_value(0x5, 4),
                "data1": create_binary_value(0xA, 4),
                "data2": create_binary_value(0x5, 4),
                "data3": create_binary_value(0xA, 4),
                "data4": create_binary_value(0x5, 4),
                "data5": create_binary_value(0xA, 4),
            }
        )
    scenarios.append(scenario5)

    # Scenario 6: Rapid Selection Changes
    scenario6 = {"scenario": "Rapid Selection Changes", "input variable": []}
    sel_sequence = [0, 5, 1, 4, 2, 3]
    for sel in sel_sequence:
        scenario6["input variable"].append(
            {
                "sel": create_binary_value(sel, 3),
                "data0": create_binary_value(0x1, 4),
                "data1": create_binary_value(0x2, 4),
                "data2": create_binary_value(0x3, 4),
                "data3": create_binary_value(0x4, 4),
                "data4": create_binary_value(0x5, 4),
                "data5": create_binary_value(0x6, 4),
            }
        )
    scenarios.append(scenario6)

    # Scenario 7: Unique Input Patterns
    scenario7 = {"scenario": "Unique Input Patterns", "input variable": []}
    for sel in range(6):
        scenario7["input variable"].append(
            {
                "sel": create_binary_value(sel, 3),
                "data0": create_binary_value(0x3, 4),
                "data1": create_binary_value(0x6, 4),
                "data2": create_binary_value(0x9, 4),
                "data3": create_binary_value(0xC, 4),
                "data4": create_binary_value(0xE, 4),
                "data5": create_binary_value(0xB, 4),
            }
        )
    scenarios.append(scenario7)

    # Scenario 8: Boundary Transitions
    scenario8 = {"scenario": "Boundary Transitions", "input variable": []}
    for sel in [5, 6, 5, 6]:
        scenario8["input variable"].append(
            {
                "sel": create_binary_value(sel, 3),
                "data0": create_binary_value(0x7, 4),
                "data1": create_binary_value(0x7, 4),
                "data2": create_binary_value(0x7, 4),
                "data3": create_binary_value(0x7, 4),
                "data4": create_binary_value(0x7, 4),
                "data5": create_binary_value(0x7, 4),
            }
        )
    scenarios.append(scenario8)

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
