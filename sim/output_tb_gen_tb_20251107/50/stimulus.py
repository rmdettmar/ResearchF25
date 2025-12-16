
import json
import random

def stimulus_gen():
    scenarios = [
        {
            "scenario": "AllZeroInputs",
            "input variable": [{"a": "0", "b": "0", "c": "0"}]
        },
        {
            "scenario": "AllOneInputs",
            "input variable": [{"a": "1", "b": "1", "c": "1"}]
        },
        {
            "scenario": "SingleOneInputAtA",
            "input variable": [{"a": "1", "b": "0", "c": "0"}]
        },
        {
            "scenario": "SingleOneInputAtB",
            "input variable": [{"a": "0", "b": "1", "c": "0"}]
        },
        {
            "scenario": "SingleOneInputAtC",
            "input variable": [{"a": "0", "b": "0", "c": "1"}]
        },
        {
            "scenario": "ABEqualHigh",
            "input variable": [{"a": "1", "b": "1", "c": "0"}]
        },
        {
            "scenario": "BCEqualHigh",
            "input variable": [{"a": "0", "b": "1", "c": "1"}]
        },
        {
            "scenario": "AlternatingBitPattern",
            "input variable": [{"a": "1", "b": "0", "c": "1"}]
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
