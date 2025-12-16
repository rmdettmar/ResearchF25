import json

from cocotb.binary import BinaryValue


def create_binary_string(value, width):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Basic Selection
    in_val = "0" * 1024
    in_val = in_val[:1020] + "1010"  # Set in[3:0] to 1010
    in_val = in_val[:1016] + "0101" + in_val[1020:]  # Set in[7:4] to 0101
    scenarios.append(
        {
            "scenario": "Basic Selection",
            "input variable": [
                {"in": in_val, "sel": create_binary_string(0, 8)},
                {"in": in_val, "sel": create_binary_string(1, 8)},
            ],
        }
    )

    # Maximum Selection
    in_val = "0" * 1024
    in_val = "1111" + in_val[4:]  # Set in[1023:1020] to 1111
    scenarios.append(
        {
            "scenario": "Maximum Selection",
            "input variable": [{"in": in_val, "sel": create_binary_string(255, 8)}],
        }
    )

    # Boundary Selection
    in_val = "0" * 1024
    in_val = "1100" + in_val[4:]  # Set in[1023:1020] to 1100
    in_val = "0011" + in_val[4:1020] + in_val[1020:]  # Set in[1019:1016] to 0011
    scenarios.append(
        {
            "scenario": "Boundary Selection",
            "input variable": [
                {"in": in_val, "sel": create_binary_string(254, 8)},
                {"in": in_val, "sel": create_binary_string(255, 8)},
            ],
        }
    )

    # Random Selection Pattern
    in_val = "0" * 1024
    for i in range(0, 1024, 4):
        in_val = in_val[:i] + create_binary_string(i // 4, 4) + in_val[i + 4 :]
    scenarios.append(
        {
            "scenario": "Random Selection Pattern",
            "input variable": [
                {"in": in_val, "sel": create_binary_string(42, 8)},
                {"in": in_val, "sel": create_binary_string(127, 8)},
                {"in": in_val, "sel": create_binary_string(200, 8)},
            ],
        }
    )

    # Input Pattern All Zeros
    scenarios.append(
        {
            "scenario": "Input Pattern All Zeros",
            "input variable": [
                {"in": "0" * 1024, "sel": create_binary_string(0, 8)},
                {"in": "0" * 1024, "sel": create_binary_string(128, 8)},
                {"in": "0" * 1024, "sel": create_binary_string(255, 8)},
            ],
        }
    )

    # Input Pattern All Ones
    scenarios.append(
        {
            "scenario": "Input Pattern All Ones",
            "input variable": [
                {"in": "1" * 1024, "sel": create_binary_string(0, 8)},
                {"in": "1" * 1024, "sel": create_binary_string(128, 8)},
                {"in": "1" * 1024, "sel": create_binary_string(255, 8)},
            ],
        }
    )

    # Alternating Bit Pattern
    alt_pattern = "".join(["1010" for _ in range(256)])
    scenarios.append(
        {
            "scenario": "Alternating Bit Pattern",
            "input variable": [
                {"in": alt_pattern, "sel": create_binary_string(0, 8)},
                {"in": alt_pattern, "sel": create_binary_string(64, 8)},
                {"in": alt_pattern, "sel": create_binary_string(128, 8)},
            ],
        }
    )

    # Rapid Selection Changes
    in_val = "0" * 1024
    for i in range(0, 1024, 4):
        in_val = in_val[:i] + create_binary_string(15 - i // 64, 4) + in_val[i + 4 :]
    scenarios.append(
        {
            "scenario": "Rapid Selection Changes",
            "input variable": [
                {"in": in_val, "sel": create_binary_string(0, 8)},
                {"in": in_val, "sel": create_binary_string(64, 8)},
                {"in": in_val, "sel": create_binary_string(128, 8)},
                {"in": in_val, "sel": create_binary_string(255, 8)},
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
