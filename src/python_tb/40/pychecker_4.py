import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 32-bit history register to 0
        self.history_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals from binary strings
            areset = int(stimulus["areset"], 2)
            predict_valid = int(stimulus["predict_valid"], 2)
            predict_taken = int(stimulus["predict_taken"], 2)
            train_mispredicted = int(stimulus["train_mispredicted"], 2)
            train_taken = int(stimulus["train_taken"], 2)
            train_history = int(stimulus["train_history"], 2)

            # Handle asynchronous reset
            if areset:
                self.history_reg = 0
            else:
                if train_mispredicted:
                    # Misprediction: load train_history concatenated with train_taken
                    self.history_reg = ((train_history << 1) | train_taken) & 0xFFFFFFFF
                elif predict_valid:
                    # Prediction: shift in predict_taken from LSB
                    self.history_reg = (
                        (self.history_reg << 1) | predict_taken
                    ) & 0xFFFFFFFF

            # Convert output to 32-bit binary string
            predict_history = BinaryValue(value=self.history_reg, n_bits=32)
            stimulus_outputs.append({"predict_history": predict_history.binstr})

        output_dict = {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }

        return output_dict


def check_output(stimulus_list):

    dut = GoldenDUT()
    tb_outputs = []

    for stimulus in stimulus_list:

        tb_outputs.append(dut.load(stimulus))

    return tb_outputs


if __name__ == "__main__":

    with open("stimulus.json", "r") as f:
        stimulus_data = json.load(f)

    if isinstance(stimulus_data, dict):
        stimulus_list = stimulus_data.get("input variable", [])
    else:
        stimulus_list = stimulus_data

    outputs = check_output(stimulus_list)

    print(json.dumps(outputs, indent=2))
