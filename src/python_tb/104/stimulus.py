import json

from cocotb.binary import BinaryValue


def gen_binary_str(value, width):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Basic Write Operation
    scenarios.append(
        {
            "scenario": "Basic Write Operation",
            "input variable": [
                {
                    "clk": "1",
                    "resetn": "1",
                    "byteena": "11",
                    "d": gen_binary_str(0xABCD, 16),
                }
            ],
        }
    )

    # Upper Byte Write Only
    scenarios.append(
        {
            "scenario": "Upper Byte Write Only",
            "input variable": [
                {
                    "clk": "1",
                    "resetn": "1",
                    "byteena": "10",
                    "d": gen_binary_str(0xFFFF, 16),
                }
            ],
        }
    )

    # Lower Byte Write Only
    scenarios.append(
        {
            "scenario": "Lower Byte Write Only",
            "input variable": [
                {
                    "clk": "1",
                    "resetn": "1",
                    "byteena": "01",
                    "d": gen_binary_str(0xFFFF, 16),
                }
            ],
        }
    )

    # No Byte Enable
    scenarios.append(
        {
            "scenario": "No Byte Enable",
            "input variable": [
                {
                    "clk": "1",
                    "resetn": "1",
                    "byteena": "00",
                    "d": gen_binary_str(0xFFFF, 16),
                }
            ],
        }
    )

    # Synchronous Reset
    scenarios.append(
        {
            "scenario": "Synchronous Reset",
            "input variable": [
                {
                    "clk": "1",
                    "resetn": "0",
                    "byteena": "11",
                    "d": gen_binary_str(0xFFFF, 16),
                },
                {
                    "clk": "1",
                    "resetn": "1",
                    "byteena": "11",
                    "d": gen_binary_str(0xFFFF, 16),
                },
            ],
        }
    )

    # Alternating Byte Enables
    scenarios.append(
        {
            "scenario": "Alternating Byte Enables",
            "input variable": [
                {
                    "clk": "1",
                    "resetn": "1",
                    "byteena": "10",
                    "d": gen_binary_str(0xA5A5, 16),
                },
                {
                    "clk": "1",
                    "resetn": "1",
                    "byteena": "01",
                    "d": gen_binary_str(0x5A5A, 16),
                },
            ],
        }
    )

    # Reset During Byte Enable
    scenarios.append(
        {
            "scenario": "Reset During Byte Enable",
            "input variable": [
                {
                    "clk": "1",
                    "resetn": "1",
                    "byteena": "10",
                    "d": gen_binary_str(0xAAAA, 16),
                },
                {
                    "clk": "1",
                    "resetn": "0",
                    "byteena": "01",
                    "d": gen_binary_str(0x5555, 16),
                },
                {
                    "clk": "1",
                    "resetn": "1",
                    "byteena": "11",
                    "d": gen_binary_str(0x0000, 16),
                },
            ],
        }
    )

    # Setup Time Verification
    scenarios.append(
        {
            "scenario": "Setup Time Verification",
            "input variable": [
                {
                    "clk": "1",
                    "resetn": "1",
                    "byteena": "11",
                    "d": gen_binary_str(0x1234, 16),
                },
                {
                    "clk": "1",
                    "resetn": "1",
                    "byteena": "11",
                    "d": gen_binary_str(0x5678, 16),
                },
                {
                    "clk": "1",
                    "resetn": "1",
                    "byteena": "11",
                    "d": gen_binary_str(0x9ABC, 16),
                },
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
