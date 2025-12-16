import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize the 4-bit counter register to 0
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract reset signal
            reset = int(BinaryValue(stimulus["reset"]).value)

            if reset:
                # Synchronous reset - set counter to 0
                self.q_reg = 0
            else:
                # Increment counter if less than 9, wrap to 0 if at 9
                self.q_reg = 0 if self.q_reg == 9 else self.q_reg + 1

            # Convert current count to 4-bit BinaryValue for output
            q_bv = BinaryValue(value=self.q_reg, n_bits=4, bigEndian=False)

            # Append the current output state
            stimulus_outputs.append({"q": q_bv.binstr})

        # Return the output dictionary
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
