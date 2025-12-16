import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 7-bit global history register
        self.ghr = 0
        # Initialize 128-entry PHT with 2-bit counters set to 1 (weakly not taken)
        self.pht = [1] * 128

    def get_pht_index(self, pc: int, history: int) -> int:
        # XOR PC with history to get PHT index
        return pc ^ history

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            predict_valid = int(stimulus.get("predict_valid", "0"), 2)
            predict_pc = int(stimulus.get("predict_pc", "0"), 2)
            train_valid = int(stimulus.get("train_valid", "0"), 2)
            train_taken = int(stimulus.get("train_taken", "0"), 2)
            train_mispredicted = int(stimulus.get("train_mispredicted", "0"), 2)
            train_history = int(stimulus.get("train_history", "0"), 2)
            train_pc = int(stimulus.get("train_pc", "0"), 2)
            areset = int(stimulus.get("areset", "0"), 2)

            output = {}

            # Handle reset
            if areset:
                self.ghr = 0
                self.pht = [1] * 128
                output["predict_taken"] = "0"
                output["predict_history"] = format(0, "07b")
                stimulus_outputs.append(output)
                continue

            # Handle training
            if train_valid:
                # Get PHT index for training
                train_idx = self.get_pht_index(train_pc, train_history)

                # Update PHT entry
                if train_taken:
                    self.pht[train_idx] = min(3, self.pht[train_idx] + 1)
                else:
                    self.pht[train_idx] = max(0, self.pht[train_idx] - 1)

                # Update GHR if mispredicted
                if train_mispredicted:
                    self.ghr = ((train_history << 1) | train_taken) & 0x7F

            # Handle prediction
            if predict_valid and not (train_valid and train_mispredicted):
                # Get PHT index for prediction
                pred_idx = self.get_pht_index(predict_pc, self.ghr)

                # Make prediction
                pred_taken = self.pht[pred_idx] >= 2

                # Update GHR for prediction
                self.ghr = ((self.ghr << 1) | int(pred_taken)) & 0x7F

                # Set outputs
                output["predict_taken"] = "1" if pred_taken else "0"
                output["predict_history"] = format(self.ghr, "07b")
            else:
                output["predict_taken"] = "0"
                output["predict_history"] = format(self.ghr, "07b")

            stimulus_outputs.append(output)

        return {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }


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
