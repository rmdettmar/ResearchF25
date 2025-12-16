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
        Process inputs and generate outputs according to state machine rules
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            reset_bv = BinaryValue(stimulus["reset"])
            j_bv = BinaryValue(stimulus["j"])
            k_bv = BinaryValue(stimulus["k"])

            # Get integer values
            reset = reset_bv.integer
            j = j_bv.integer
            k = k_bv.integer

            # Update state based on inputs
            if reset:
                self.state = 0  # Reset to OFF state
            else:
                if self.state == 0:  # Currently in OFF state
                    if j == 1:
                        self.state = 1  # Transition to ON
                else:  # Currently in ON state
                    if k == 1:
                        self.state = 0  # Transition to OFF

            # Create output dictionary
            # Convert output to binary string format
            out_bv = BinaryValue(value=self.state, n_bits=1)
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
