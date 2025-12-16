import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 7-bit branch history register
        self.bhr = 0
        # Initialize 128-entry PHT with 2-bit counters (01 = weakly not taken)
        self.pht = [1 for _ in range(128)]

    def _get_pht_index(self, pc: int, history: int) -> int:
        # XOR PC with history to get PHT index
        return pc ^ history

    def _is_taken(self, counter: int) -> bool:
        # Counter >= 2 means taken
        return counter >= 2

    def _update_counter(self, counter: int, taken: bool) -> int:
        # Update 2-bit saturating counter
        if taken:
            return min(3, counter + 1)
        else:
            return max(0, counter - 1)

    def load(self, stimulus_dict: Dict[str, any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs from binary strings to integers
            predict_valid = BinaryValue(stimulus["predict_valid"]).integer
            predict_pc = BinaryValue(stimulus["predict_pc"]).integer
            train_valid = BinaryValue(stimulus["train_valid"]).integer
            train_taken = BinaryValue(stimulus["train_taken"]).integer
            train_mispredicted = BinaryValue(stimulus["train_mispredicted"]).integer
            train_history = BinaryValue(stimulus["train_history"]).integer
            train_pc = BinaryValue(stimulus["train_pc"]).integer
            areset = BinaryValue(stimulus["areset"]).integer

            # Handle reset
            if areset:
                self.bhr = 0
                self.pht = [1 for _ in range(128)]
                predict_taken = 0
                predict_history = 0
            else:
                # Handle training
                if train_valid:
                    train_idx = self._get_pht_index(train_pc, train_history)
                    self.pht[train_idx] = self._update_counter(
                        self.pht[train_idx], train_taken
                    )

                    # Update BHR on misprediction
                    if train_mispredicted:
                        self.bhr = ((train_history << 1) | train_taken) & 0x7F

                # Handle prediction if no misprediction training
                if predict_valid and not (train_valid and train_mispredicted):
                    predict_history = self.bhr
                    predict_idx = self._get_pht_index(predict_pc, predict_history)
                    predict_taken = int(self._is_taken(self.pht[predict_idx]))
                    # Update BHR for prediction
                    self.bhr = ((self.bhr << 1) | predict_taken) & 0x7F
                else:
                    predict_taken = 0
                    predict_history = self.bhr

            # Convert outputs to binary strings
            output_dict = {
                "predict_taken": BinaryValue(value=predict_taken, n_bits=1).binstr,
                "predict_history": BinaryValue(value=predict_history, n_bits=7).binstr,
            }
            outputs.append(output_dict)

        return {"scenario": stimulus_dict["scenario"], "output variable": outputs}


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
