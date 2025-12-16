import json

from cocotb.binary import BinaryValue


def stimulus_gen():
    scenarios = []

    # Scenario 1: All Zeros Input
    scenarios.append(
        {
            "scenario": "All Zeros Input",
            "input variable": [
                {
                    "p1a": "0",
                    "p1b": "0",
                    "p1c": "0",
                    "p1d": "0",
                    "p2a": "0",
                    "p2b": "0",
                    "p2c": "0",
                    "p2d": "0",
                }
            ],
        }
    )

    # Scenario 2: All Ones Input
    scenarios.append(
        {
            "scenario": "All Ones Input",
            "input variable": [
                {
                    "p1a": "1",
                    "p1b": "1",
                    "p1c": "1",
                    "p1d": "1",
                    "p2a": "1",
                    "p2b": "1",
                    "p2c": "1",
                    "p2d": "1",
                }
            ],
        }
    )

    # Scenario 3: Mixed Inputs Gate 1
    scenarios.append(
        {
            "scenario": "Mixed Inputs Gate 1",
            "input variable": [
                {
                    "p1a": "0",
                    "p1b": "1",
                    "p1c": "1",
                    "p1d": "1",
                    "p2a": "1",
                    "p2b": "1",
                    "p2c": "1",
                    "p2d": "1",
                },
                {
                    "p1a": "1",
                    "p1b": "0",
                    "p1c": "1",
                    "p1d": "1",
                    "p2a": "1",
                    "p2b": "1",
                    "p2c": "1",
                    "p2d": "1",
                },
                {
                    "p1a": "1",
                    "p1b": "1",
                    "p1c": "0",
                    "p1d": "1",
                    "p2a": "1",
                    "p2b": "1",
                    "p2c": "1",
                    "p2d": "1",
                },
                {
                    "p1a": "1",
                    "p1b": "1",
                    "p1c": "1",
                    "p1d": "0",
                    "p2a": "1",
                    "p2b": "1",
                    "p2c": "1",
                    "p2d": "1",
                },
            ],
        }
    )

    # Scenario 4: Mixed Inputs Gate 2
    scenarios.append(
        {
            "scenario": "Mixed Inputs Gate 2",
            "input variable": [
                {
                    "p1a": "1",
                    "p1b": "1",
                    "p1c": "1",
                    "p1d": "1",
                    "p2a": "0",
                    "p2b": "1",
                    "p2c": "1",
                    "p2d": "1",
                },
                {
                    "p1a": "1",
                    "p1b": "1",
                    "p1c": "1",
                    "p1d": "1",
                    "p2a": "1",
                    "p2b": "0",
                    "p2c": "1",
                    "p2d": "1",
                },
                {
                    "p1a": "1",
                    "p1b": "1",
                    "p1c": "1",
                    "p1d": "1",
                    "p2a": "1",
                    "p2b": "1",
                    "p2c": "0",
                    "p2d": "1",
                },
                {
                    "p1a": "1",
                    "p1b": "1",
                    "p1c": "1",
                    "p1d": "1",
                    "p2a": "1",
                    "p2b": "1",
                    "p2c": "1",
                    "p2d": "0",
                },
            ],
        }
    )

    # Scenario 5: Independent Gate Operation
    scenarios.append(
        {
            "scenario": "Independent Gate Operation",
            "input variable": [
                {
                    "p1a": "1",
                    "p1b": "1",
                    "p1c": "1",
                    "p1d": "1",
                    "p2a": "0",
                    "p2b": "0",
                    "p2c": "0",
                    "p2d": "0",
                },
                {
                    "p1a": "0",
                    "p1b": "0",
                    "p1c": "0",
                    "p1d": "0",
                    "p2a": "1",
                    "p2b": "1",
                    "p2c": "1",
                    "p2d": "1",
                },
            ],
        }
    )

    # Scenario 6: Single Input Toggle
    scenarios.append(
        {
            "scenario": "Single Input Toggle",
            "input variable": [
                {
                    "p1a": "1",
                    "p1b": "0",
                    "p1c": "0",
                    "p1d": "0",
                    "p2a": "0",
                    "p2b": "0",
                    "p2c": "0",
                    "p2d": "0",
                },
                {
                    "p1a": "0",
                    "p1b": "1",
                    "p1c": "0",
                    "p1d": "0",
                    "p2a": "0",
                    "p2b": "0",
                    "p2c": "0",
                    "p2d": "0",
                },
                {
                    "p1a": "0",
                    "p1b": "0",
                    "p1c": "0",
                    "p1d": "0",
                    "p2a": "1",
                    "p2b": "0",
                    "p2c": "0",
                    "p2d": "0",
                },
                {
                    "p1a": "0",
                    "p1b": "0",
                    "p1c": "0",
                    "p1d": "0",
                    "p2a": "0",
                    "p2b": "1",
                    "p2c": "0",
                    "p2d": "0",
                },
            ],
        }
    )

    # Scenario 7: Transition Response
    scenarios.append(
        {
            "scenario": "Transition Response",
            "input variable": [
                {
                    "p1a": "0",
                    "p1b": "0",
                    "p1c": "0",
                    "p1d": "0",
                    "p2a": "0",
                    "p2b": "0",
                    "p2c": "0",
                    "p2d": "0",
                },
                {
                    "p1a": "1",
                    "p1b": "1",
                    "p1c": "1",
                    "p1d": "1",
                    "p2a": "1",
                    "p2b": "1",
                    "p2c": "1",
                    "p2d": "1",
                },
                {
                    "p1a": "0",
                    "p1b": "0",
                    "p1c": "0",
                    "p1d": "0",
                    "p2a": "0",
                    "p2b": "0",
                    "p2c": "0",
                    "p2d": "0",
                },
            ],
        }
    )

    # Scenario 8: Complementary Operation
    scenarios.append(
        {
            "scenario": "Complementary Operation",
            "input variable": [
                {
                    "p1a": "1",
                    "p1b": "1",
                    "p1c": "1",
                    "p1d": "1",
                    "p2a": "0",
                    "p2b": "0",
                    "p2c": "0",
                    "p2d": "0",
                },
                {
                    "p1a": "0",
                    "p1b": "0",
                    "p1c": "0",
                    "p1d": "0",
                    "p2a": "1",
                    "p2b": "1",
                    "p2c": "1",
                    "p2d": "1",
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
