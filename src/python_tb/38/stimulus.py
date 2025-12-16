import json

from cocotb.binary import BinaryValue


def get_binary_str(value, width=16):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = [
        {
            "scenario": "Valid Left Arrow Detection",
            "input variable": [{"scancode": get_binary_str(0xE06B)}],
        },
        {
            "scenario": "Valid Down Arrow Detection",
            "input variable": [{"scancode": get_binary_str(0xE072)}],
        },
        {
            "scenario": "Valid Right Arrow Detection",
            "input variable": [{"scancode": get_binary_str(0xE074)}],
        },
        {
            "scenario": "Valid Up Arrow Detection",
            "input variable": [{"scancode": get_binary_str(0xE075)}],
        },
        {
            "scenario": "Invalid Scancode Handling",
            "input variable": [
                {"scancode": get_binary_str(0x0000)},
                {"scancode": get_binary_str(0xFFFF)},
                {"scancode": get_binary_str(0xE076)},
            ],
        },
        {
            "scenario": "Rapid Key Transitions",
            "input variable": [
                {"scancode": get_binary_str(0xE06B)},
                {"scancode": get_binary_str(0xE072)},
                {"scancode": get_binary_str(0xE074)},
                {"scancode": get_binary_str(0xE075)},
            ],
        },
        {
            "scenario": "Similar Scancode Patterns",
            "input variable": [
                {"scancode": get_binary_str(0xE06A)},
                {"scancode": get_binary_str(0xE073)},
                {"scancode": get_binary_str(0xE06C)},
                {"scancode": get_binary_str(0xE076)},
            ],
        },
        {
            "scenario": "Initial State Verification",
            "input variable": [{"scancode": get_binary_str(0x0000)}],
        },
    ]
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
