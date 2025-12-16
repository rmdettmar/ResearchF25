import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state register to OFF state (0)
        """
        self.state = 0  # OFF=0, ON=1

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and update state according to Moore machine logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            reset = BinaryValue(stimulus["reset"]).integer
            j = BinaryValue(stimulus["j"]).integer
            k = BinaryValue(stimulus["k"]).integer

            # Update state based on inputs
            if reset:
                self.state = 0  # Reset to OFF state
            else:
                if self.state == 0:  # OFF state
                    if j == 1:
                        self.state = 1  # Transition to ON
                else:  # ON state
                    if k == 1:
                        self.state = 0  # Transition to OFF

            # Output depends only on current state
            out = self.state

            # Convert output to BinaryValue for consistent format
            out_bv = BinaryValue(value=out, n_bits=1)
            stimulus_outputs.append({"out": out_bv.binstr})

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
