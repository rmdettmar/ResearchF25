import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize counter to 1 (not 0)
        self.q_reg = 1

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert reset from binary string to integer
            reset_bv = BinaryValue(stimulus["reset"])
            reset = reset_bv.integer

            if reset:
                # Synchronous reset - set counter to 1
                self.q_reg = 1
            else:
                # Normal counting operation
                if self.q_reg == 10:
                    # Wrap around to 1 after reaching 10
                    self.q_reg = 1
                else:
                    # Increment counter
                    self.q_reg = self.q_reg + 1

            # Convert current count to 4-bit BinaryValue for output
            q_bv = BinaryValue(value=self.q_reg, n_bits=4)
            stimulus_outputs.append({"q": q_bv.binstr})

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
