import json
from typing import Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 7-bit branch history register
        self.branch_history = 0
        # Initialize 128-entry PHT with 2-bit saturating counters
        self.pht = [0] * 128  # Each entry is 2 bits (0-3)

    def get_pht_index(self, pc: int, history: int) -> int:
        # XOR PC with history to get PHT index
        return pc ^ history

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            predict_valid = int(BinaryValue(stimulus.get("predict_valid", "0")).integer)
            predict_pc = int(BinaryValue(stimulus.get("predict_pc", "0")).integer)
            train_valid = int(BinaryValue(stimulus.get("train_valid", "0")).integer)
            train_taken = int(BinaryValue(stimulus.get("train_taken", "0")).integer)
            train_mispredicted = int(
                BinaryValue(stimulus.get("train_mispredicted", "0")).integer
            )
            train_history = int(BinaryValue(stimulus.get("train_history", "0")).integer)
            train_pc = int(BinaryValue(stimulus.get("train_pc", "0")).integer)
            areset = int(BinaryValue(stimulus.get("areset", "0")).integer)

            output = {}

            if areset:
                self.branch_history = 0
                self.pht = [0] * 128
                predict_taken = 0
                predict_history = 0
            else:
                # Handle training first (takes precedence)
                if train_valid:
                    train_idx = self.get_pht_index(train_pc, train_history)
                    # Update PHT entry
                    if train_taken:
                        self.pht[train_idx] = min(3, self.pht[train_idx] + 1)
                    else:
                        self.pht[train_idx] = max(0, self.pht[train_idx] - 1)

                    # Restore history on misprediction
                    if train_mispredicted:
                        self.branch_history = train_history

                # Handle prediction
                if predict_valid and not (train_valid and train_mispredicted):
                    predict_idx = self.get_pht_index(predict_pc, self.branch_history)
                    predict_taken = 1 if self.pht[predict_idx] >= 2 else 0
                    predict_history = self.branch_history
                    # Update history with prediction
                    self.branch_history = (
                        (self.branch_history << 1) | predict_taken
                    ) & 0x7F
                else:
                    predict_taken = 0
                    predict_history = self.branch_history

            # Convert outputs to BinaryValue format
            output["predict_taken"] = BinaryValue(value=predict_taken, n_bits=1).binstr
            output["predict_history"] = BinaryValue(
                value=predict_history, n_bits=7
            ).binstr
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
