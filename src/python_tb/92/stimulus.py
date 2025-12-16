import json

from cocotb.binary import BinaryValue


def create_binary_sequence(value, width):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = [
        {
            "scenario": "Reset Verification",
            "input variable": [
                {"resetn": "0", "r": "000"},
                {"resetn": "0", "r": "000"},
                {"resetn": "1", "r": "000"},
            ],
        },
        {
            "scenario": "No Requests",
            "input variable": [
                {"resetn": "1", "r": "000"},
                {"resetn": "1", "r": "000"},
                {"resetn": "1", "r": "000"},
            ],
        },
        {
            "scenario": "Single Request Priority",
            "input variable": [
                {"resetn": "1", "r": "100"},  # r1
                {"resetn": "1", "r": "010"},  # r2
                {"resetn": "1", "r": "001"},  # r3
            ],
        },
        {
            "scenario": "Multiple Request Priority",
            "input variable": [
                {"resetn": "1", "r": "110"},  # r1=r2=1
                {"resetn": "1", "r": "101"},  # r1=r3=1
                {"resetn": "1", "r": "011"},  # r2=r3=1
                {"resetn": "1", "r": "111"},  # r1=r2=r3=1
            ],
        },
        {
            "scenario": "Grant Persistence",
            "input variable": [
                {"resetn": "1", "r": "100"},  # Set r1
                {"resetn": "1", "r": "100"},  # Keep r1
                {"resetn": "1", "r": "100"},  # Keep r1
                {"resetn": "1", "r": "000"},  # Release r1
            ],
        },
        {
            "scenario": "State A to B Transition",
            "input variable": [
                {"resetn": "1", "r": "000"},  # Initial state A
                {"resetn": "1", "r": "100"},  # Set r1
                {"resetn": "1", "r": "100"},  # Verify state B
            ],
        },
        {
            "scenario": "State A to C Transition",
            "input variable": [
                {"resetn": "1", "r": "000"},  # Initial state A
                {"resetn": "1", "r": "010"},  # Set r2
                {"resetn": "1", "r": "010"},  # Verify state C
            ],
        },
        {
            "scenario": "Return to State A",
            "input variable": [
                {"resetn": "1", "r": "100"},  # Go to state B
                {"resetn": "1", "r": "000"},  # Return to A
                {"resetn": "1", "r": "010"},  # Go to state C
                {"resetn": "1", "r": "000"},  # Return to A
            ],
        },
        {
            "scenario": "Reset During Operation",
            "input variable": [
                {"resetn": "1", "r": "100"},  # Go to state B
                {"resetn": "0", "r": "100"},  # Assert reset
                {"resetn": "1", "r": "000"},  # Verify state A
            ],
        },
        {
            "scenario": "Request Change During Grant",
            "input variable": [
                {"resetn": "1", "r": "100"},  # Go to state B
                {"resetn": "1", "r": "110"},  # Add r2 request
                {"resetn": "1", "r": "111"},  # Add r3 request
                {"resetn": "1", "r": "100"},  # Verify g1 persistence
            ],
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
