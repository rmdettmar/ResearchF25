import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 7-bit branch history register
        self.history_reg = 0
        # Initialize 128-entry PHT with 2-bit saturating counters
        self.pht = [2] * 128  # All entries start at 2 (weakly taken)

    def _get_pht_index(self, pc: int, history: int) -> int:
        # XOR PC with history to get PHT index
        return pc ^ history

    def _update_counter(self, index: int, taken: bool):
        # Update 2-bit saturating counter
        if taken:
            self.pht[index] = min(3, self.pht[index] + 1)
        else:
            self.pht[index] = max(0, self.pht[index] - 1)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to proper format
            areset = int(stimulus["areset"], 2)
            predict_valid = int(stimulus["predict_valid"], 2)
            predict_pc = int(stimulus["predict_pc"], 2)
            train_valid = int(stimulus["train_valid"], 2)
            train_taken = int(stimulus["train_taken"], 2)
            train_mispredicted = int(stimulus["train_mispredicted"], 2)
            train_history = int(stimulus["train_history"], 2)
            train_pc = int(stimulus["train_pc"], 2)

            # Handle reset
            if areset:
                self.history_reg = 0
                self.pht = [2] * 128
                predict_taken = 0
                predict_history = 0
            else:
                # Handle training (takes precedence)
                if train_valid:
                    train_idx = self._get_pht_index(train_pc, train_history)
                    self._update_counter(train_idx, train_taken == 1)
                    if train_mispredicted:
                        # Restore history on misprediction
                        self.history_reg = train_history

                # Handle prediction
                if predict_valid:
                    predict_history = self.history_reg
                    pred_idx = self._get_pht_index(predict_pc, predict_history)
                    predict_taken = 1 if self.pht[pred_idx] >= 2 else 0

                    # Update history with prediction unless training happened
                    if not train_valid:
                        self.history_reg = (
                            (self.history_reg << 1) | predict_taken
                        ) & 0x7F
                else:
                    predict_taken = 0
                    predict_history = self.history_reg

            # Format outputs as binary strings
            output_dict = {
                "predict_taken": format(predict_taken, "01b"),
                "predict_history": format(predict_history, "07b"),
            }
            stimulus_outputs.append(output_dict)

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
