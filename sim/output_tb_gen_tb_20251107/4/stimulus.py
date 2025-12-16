
import json
import random

def stimulus_gen():
    scenarios = [
        {
            "scenario": "AllZerosInput",
            "input variable": [{"in": "00000000000000000000000000000000"}]
        },
        {
            "scenario": "AllOnesInput",
            "input variable": [{"in": "11111111111111111111111111111111"}]
        },
        {
            "scenario": "AlternatingBitsPattern",
            "input variable": [{"in": "10101010101010101010101010101010"}]
        },
        {
            "scenario": "ByteBoundaryTest",
            "input variable": [{"in": "00000001000000100000001100000100"}]
        },
        {
            "scenario": "SingleByteSet",
            "input variable": [{"in": "00000000000000000000000011111111"}]
        },
        {
            "scenario": "SequentialBytesIncreasing",
            "input variable": [{"in": "00000001000000100000001100000100"}]
        },
        {
            "scenario": "SequentialBytesDecreasing",
            "input variable": [{"in": "00000100000000110000001000000001"}]
        },
        {
            "scenario": "RandomBits",
            "input variable": [{"in": "10100101101001011010010110100101"}]
        }
    ]
    return scenarios
if __name__ == "__main__":
    result = stimulus_gen()
    # Convert result to JSON string
    if isinstance(result, list):
        result = json.dumps(result, indent=4)
    elif not isinstance(result, str):
        result = json.dumps(result, indent=4)

    with open("stimulus.json", "w") as f:
        f.write(result)
