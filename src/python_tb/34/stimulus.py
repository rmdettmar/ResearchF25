import json


def to_8bit_binary(num):
    # Convert integer to 8-bit binary string, handling negative numbers
    if num < 0:
        num = (abs(num) ^ 0xFF) + 1  # 2's complement
    return format(num & 0xFF, "08b")


def stimulus_gen():
    scenarios = []

    # Basic Addition
    scenarios.append(
        {
            "scenario": "Basic Addition",
            "input variable": [{"a": "00000101", "b": "00000011"}],
        }
    )

    # Negative Number Addition
    scenarios.append(
        {
            "scenario": "Negative Number Addition",
            "input variable": [{"a": "11111100", "b": "11111101"}],
        }
    )

    # Mixed Sign Addition
    scenarios.append(
        {
            "scenario": "Mixed Sign Addition",
            "input variable": [{"a": "00000101", "b": "11111101"}],
        }
    )

    # Positive Overflow
    scenarios.append(
        {
            "scenario": "Positive Overflow",
            "input variable": [{"a": "01100100", "b": "00110010"}],
        }
    )

    # Negative Overflow
    scenarios.append(
        {
            "scenario": "Negative Overflow",
            "input variable": [{"a": "10011100", "b": "11001110"}],
        }
    )

    # Maximum Positive Values
    scenarios.append(
        {
            "scenario": "Maximum Positive Values",
            "input variable": [{"a": "01111111", "b": "00000001"}],
        }
    )

    # Maximum Negative Values
    scenarios.append(
        {
            "scenario": "Maximum Negative Values",
            "input variable": [{"a": "10000000", "b": "11111111"}],
        }
    )

    # Zero Addition
    scenarios.append(
        {
            "scenario": "Zero Addition",
            "input variable": [{"a": "00000000", "b": "00000000"}],
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
