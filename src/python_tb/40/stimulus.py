import json

from cocotb.binary import BinaryValue


def get_binary_string(value, width):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def create_prediction_sequence(taken_pattern, length):
    return [
        {
            "predict_valid": "1",
            "predict_taken": str(bit),
            "train_mispredicted": "0",
            "train_taken": "0",
            "train_history": "0" * 32,
            "areset": "0",
        }
        for bit in taken_pattern[:length]
    ]


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Prediction Shift
    basic_pred = {
        "scenario": "Basic Prediction Shift",
        "input variable": create_prediction_sequence([1, 0, 1, 0, 1], 5),
    }
    scenarios.append(basic_pred)

    # Scenario 2: Misprediction Recovery
    mispred = {
        "scenario": "Misprediction Recovery",
        "input variable": [
            {
                "predict_valid": "0",
                "predict_taken": "0",
                "train_mispredicted": "1",
                "train_taken": "1",
                "train_history": get_binary_string(0xAAAAAAAA, 32),
                "areset": "0",
            }
        ],
    }
    scenarios.append(mispred)

    # Scenario 3: Asynchronous Reset
    reset = {
        "scenario": "Asynchronous Reset",
        "input variable": [
            {
                "predict_valid": "1",
                "predict_taken": "1",
                "train_mispredicted": "0",
                "train_taken": "0",
                "train_history": "0" * 32,
                "areset": "1",
            },
            {
                "predict_valid": "0",
                "predict_taken": "0",
                "train_mispredicted": "0",
                "train_taken": "0",
                "train_history": "0" * 32,
                "areset": "0",
            },
        ],
    }
    scenarios.append(reset)

    # Scenario 4: Concurrent Predict and Train
    concurrent = {
        "scenario": "Concurrent Predict and Train",
        "input variable": [
            {
                "predict_valid": "1",
                "predict_taken": "1",
                "train_mispredicted": "1",
                "train_taken": "0",
                "train_history": get_binary_string(0x55555555, 32),
                "areset": "0",
            }
        ],
    }
    scenarios.append(concurrent)

    # Scenario 5: Multiple Consecutive Predictions
    multi_pred = {
        "scenario": "Multiple Consecutive Predictions",
        "input variable": create_prediction_sequence([1] * 33, 33),
    }
    scenarios.append(multi_pred)

    # Scenario 6: Edge Case History Values
    edge_cases = {
        "scenario": "Edge Case History Values",
        "input variable": [
            {
                "predict_valid": "0",
                "predict_taken": "0",
                "train_mispredicted": "1",
                "train_taken": "1",
                "train_history": "1" * 32,
                "areset": "0",
            },
            {
                "predict_valid": "0",
                "predict_taken": "0",
                "train_mispredicted": "1",
                "train_taken": "0",
                "train_history": "0" * 32,
                "areset": "0",
            },
        ],
    }
    scenarios.append(edge_cases)

    # Scenario 7: Rapid Toggle
    rapid_toggle = {
        "scenario": "Rapid Toggle",
        "input variable": [
            {
                "predict_valid": "1",
                "predict_taken": "1",
                "train_mispredicted": "0",
                "train_taken": "0",
                "train_history": "0" * 32,
                "areset": "0",
            },
            {
                "predict_valid": "0",
                "predict_taken": "0",
                "train_mispredicted": "1",
                "train_taken": "1",
                "train_history": get_binary_string(0x12345678, 32),
                "areset": "0",
            },
        ]
        * 3,
    }
    scenarios.append(rapid_toggle)

    # Scenario 8: Reset Recovery
    reset_recovery = {
        "scenario": "Reset Recovery",
        "input variable": [
            {
                "predict_valid": "0",
                "predict_taken": "0",
                "train_mispredicted": "0",
                "train_taken": "0",
                "train_history": "0" * 32,
                "areset": "1",
            },
            {
                "predict_valid": "1",
                "predict_taken": "1",
                "train_mispredicted": "0",
                "train_taken": "0",
                "train_history": "0" * 32,
                "areset": "0",
            },
        ],
    }
    scenarios.append(reset_recovery)

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
