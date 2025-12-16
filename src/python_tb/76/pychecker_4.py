import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 8-bit output register
        self.q_reg = BinaryValue(value=0, n_bits=8)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            d = BinaryValue(stimulus["d"])
            reset = BinaryValue(stimulus["reset"]).integer

            # Update state on positive clock edge
            if reset:
                # Synchronous reset - set output to 0
                self.q_reg = BinaryValue(value=0, n_bits=8)
            else:
                # Normal operation - update with input d
                self.q_reg = d

            # Add current output to results
            stimulus_outputs.append({"q": self.q_reg.binstr})

        # Return output dictionary
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
