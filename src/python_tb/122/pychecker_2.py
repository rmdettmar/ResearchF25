import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state to OFF (0)
        """
        self.state = 0  # 0=OFF, 1=ON

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and update state according to Moore machine rules
        """
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            areset = BinaryValue(stimulus["areset"]).integer
            j = BinaryValue(stimulus["j"]).integer
            k = BinaryValue(stimulus["k"]).integer

            # Check asynchronous reset first
            if areset:
                self.state = 0  # Reset to OFF state
            else:
                # State transition logic
                if self.state == 0:  # OFF state
                    if j == 1:
                        self.state = 1  # Transition to ON
                else:  # ON state
                    if k == 1:
                        self.state = 0  # Transition to OFF

            # Output is directly based on state (Moore machine)
            out = 1 if self.state == 1 else 0

            # Convert output to binary string format
            out_bv = BinaryValue(value=out, n_bits=1)
            outputs.append({"out": out_bv.binstr})

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
