import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 128-entry PHT with 2-bit saturating counters (00)
        self.pht = [0] * 128
        # Initialize 7-bit global history register
        self.history = 0

    def get_pht_index(self, pc: int, history: int) -> int:
        # XOR pc[6:0] with history[6:0] to get PHT index
        return pc ^ history

    def update_counter(self, counter: int, taken: bool) -> int:
        # Update 2-bit saturating counter
        if taken:
            return min(3, counter + 1)
        else:
            return max(0, counter - 1)

    def load(self, stimulus_dict: Dict[str, Any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
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

            if areset:
                self.pht = [0] * 128
                self.history = 0
                predict_taken = 0
                predict_history = self.history
            else:
                # Handle training with higher priority
                if train_valid:
                    train_idx = self.get_pht_index(train_pc, train_history)
                    self.pht[train_idx] = self.update_counter(
                        self.pht[train_idx], train_taken
                    )
                    if train_mispredicted:
                        self.history = train_history

                # Handle prediction
                if predict_valid and not (train_valid and train_mispredicted):
                    pred_idx = self.get_pht_index(predict_pc, self.history)
                    predict_taken = 1 if self.pht[pred_idx] >= 2 else 0
                    predict_history = self.history
                    # Update history with prediction
                    self.history = ((self.history << 1) | predict_taken) & 0x7F
                else:
                    predict_taken = 0
                    predict_history = self.history

            # Format outputs as binary strings
            output_dict = {
                "predict_taken": format(predict_taken, "b"),
                "predict_history": format(predict_history, "07b"),
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
