import json

from cocotb.binary import BinaryValue


def get_binary_str(value, width):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Basic Prediction Operation
    basic_pred = {
        "scenario": "Basic Prediction Operation",
        "input variable": [
            {
                "predict_valid": "1",
                "predict_pc": get_binary_str(0, 7),
                "train_valid": "0",
                "train_taken": "0",
                "train_mispredicted": "0",
                "train_history": get_binary_str(0, 7),
                "train_pc": get_binary_str(0, 7),
                "areset": "0",
            },
            {
                "predict_valid": "1",
                "predict_pc": get_binary_str(64, 7),
                "train_valid": "0",
                "train_taken": "0",
                "train_mispredicted": "0",
                "train_history": get_binary_str(0, 7),
                "train_pc": get_binary_str(0, 7),
                "areset": "0",
            },
        ],
    }
    scenarios.append(basic_pred)

    # Basic Training Operation
    basic_train = {
        "scenario": "Basic Training Operation",
        "input variable": [
            {
                "predict_valid": "0",
                "predict_pc": get_binary_str(0, 7),
                "train_valid": "1",
                "train_taken": "1",
                "train_mispredicted": "0",
                "train_history": get_binary_str(0, 7),
                "train_pc": get_binary_str(32, 7),
                "areset": "0",
            },
            {
                "predict_valid": "0",
                "predict_pc": get_binary_str(0, 7),
                "train_valid": "1",
                "train_taken": "0",
                "train_mispredicted": "0",
                "train_history": get_binary_str(1, 7),
                "train_pc": get_binary_str(32, 7),
                "areset": "0",
            },
        ],
    }
    scenarios.append(basic_train)

    # Asynchronous Reset
    async_reset = {
        "scenario": "Asynchronous Reset",
        "input variable": [
            {
                "predict_valid": "0",
                "predict_pc": get_binary_str(0, 7),
                "train_valid": "0",
                "train_taken": "0",
                "train_mispredicted": "0",
                "train_history": get_binary_str(0, 7),
                "train_pc": get_binary_str(0, 7),
                "areset": "1",
            },
            {
                "predict_valid": "0",
                "predict_pc": get_binary_str(0, 7),
                "train_valid": "0",
                "train_taken": "0",
                "train_mispredicted": "0",
                "train_history": get_binary_str(0, 7),
                "train_pc": get_binary_str(0, 7),
                "areset": "0",
            },
        ],
    }
    scenarios.append(async_reset)

    # History Register Recovery
    history_recovery = {
        "scenario": "History Register Recovery",
        "input variable": [
            {
                "predict_valid": "0",
                "predict_pc": get_binary_str(0, 7),
                "train_valid": "1",
                "train_taken": "1",
                "train_mispredicted": "1",
                "train_history": get_binary_str(42, 7),
                "train_pc": get_binary_str(16, 7),
                "areset": "0",
            }
        ],
    }
    scenarios.append(history_recovery)

    # Concurrent Predict-Train
    concurrent_ops = {
        "scenario": "Concurrent Predict-Train",
        "input variable": [
            {
                "predict_valid": "1",
                "predict_pc": get_binary_str(16, 7),
                "train_valid": "1",
                "train_taken": "1",
                "train_mispredicted": "0",
                "train_history": get_binary_str(21, 7),
                "train_pc": get_binary_str(16, 7),
                "areset": "0",
            }
        ],
    }
    scenarios.append(concurrent_ops)

    # PHT Saturation Behavior
    pht_saturation = {
        "scenario": "PHT Saturation Behavior",
        "input variable": [
            {
                "predict_valid": "0",
                "predict_pc": get_binary_str(0, 7),
                "train_valid": "1",
                "train_taken": "1",
                "train_mispredicted": "0",
                "train_history": get_binary_str(0, 7),
                "train_pc": get_binary_str(8, 7),
                "areset": "0",
            },
            {
                "predict_valid": "0",
                "predict_pc": get_binary_str(0, 7),
                "train_valid": "1",
                "train_taken": "1",
                "train_mispredicted": "0",
                "train_history": get_binary_str(0, 7),
                "train_pc": get_binary_str(8, 7),
                "areset": "0",
            },
        ],
    }
    scenarios.append(pht_saturation)

    # Index Hashing Verification
    index_hash = {
        "scenario": "Index Hashing Verification",
        "input variable": [
            {
                "predict_valid": "1",
                "predict_pc": get_binary_str(85, 7),
                "train_valid": "0",
                "train_taken": "0",
                "train_mispredicted": "0",
                "train_history": get_binary_str(42, 7),
                "train_pc": get_binary_str(0, 7),
                "areset": "0",
            }
        ],
    }
    scenarios.append(index_hash)

    # Branch Pattern Learning
    pattern_learning = {
        "scenario": "Branch Pattern Learning",
        "input variable": [
            {
                "predict_valid": "0",
                "predict_pc": get_binary_str(0, 7),
                "train_valid": "1",
                "train_taken": "1",
                "train_mispredicted": "0",
                "train_history": get_binary_str(21, 7),
                "train_pc": get_binary_str(42, 7),
                "areset": "0",
            },
            {
                "predict_valid": "1",
                "predict_pc": get_binary_str(42, 7),
                "train_valid": "0",
                "train_taken": "0",
                "train_mispredicted": "0",
                "train_history": get_binary_str(21, 7),
                "train_pc": get_binary_str(0, 7),
                "areset": "0",
            },
        ],
    }
    scenarios.append(pattern_learning)

    # Multiple Mispredictions
    multiple_mispred = {
        "scenario": "Multiple Mispredictions",
        "input variable": [
            {
                "predict_valid": "0",
                "predict_pc": get_binary_str(0, 7),
                "train_valid": "1",
                "train_taken": "0",
                "train_mispredicted": "1",
                "train_history": get_binary_str(10, 7),
                "train_pc": get_binary_str(20, 7),
                "areset": "0",
            },
            {
                "predict_valid": "0",
                "predict_pc": get_binary_str(0, 7),
                "train_valid": "1",
                "train_taken": "1",
                "train_mispredicted": "1",
                "train_history": get_binary_str(11, 7),
                "train_pc": get_binary_str(21, 7),
                "areset": "0",
            },
        ],
    }
    scenarios.append(multiple_mispred)

    # Boundary Conditions
    boundary = {
        "scenario": "Boundary Conditions",
        "input variable": [
            {
                "predict_valid": "1",
                "predict_pc": get_binary_str(127, 7),
                "train_valid": "0",
                "train_taken": "0",
                "train_mispredicted": "0",
                "train_history": get_binary_str(127, 7),
                "train_pc": get_binary_str(0, 7),
                "areset": "0",
            }
        ],
    }
    scenarios.append(boundary)

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
