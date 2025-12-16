import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state to OFF (False)
        """
        self.state = False  # False=OFF, True=ON

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs according to Moore machine spec
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            areset_bv = BinaryValue(stimulus["areset"])
            j_bv = BinaryValue(stimulus["j"])
            k_bv = BinaryValue(stimulus["k"])

            # Handle asynchronous reset
            if areset_bv.integer == 1:
                self.state = False
            else:
                # State transitions
                if not self.state:  # OFF state
                    if j_bv.integer == 1:
                        self.state = True
                else:  # ON state
                    if k_bv.integer == 1:
                        self.state = False

            # Output depends only on current state
            out = 1 if self.state else 0
            out_bv = BinaryValue(value=out, n_bits=1)
            stimulus_outputs.append({"out": out_bv.binstr})

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
