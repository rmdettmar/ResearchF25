import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state register to OFF state
        """
        self.state = False  # False = OFF, True = ON

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and update state according to Moore machine logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            reset = BinaryValue(stimulus["reset"]).integer
            j = BinaryValue(stimulus["j"]).integer
            k = BinaryValue(stimulus["k"]).integer

            # Update state based on inputs
            if reset:
                self.state = False  # Reset to OFF state
            else:
                if not self.state:  # OFF state
                    if j:
                        self.state = True  # Transition to ON
                else:  # ON state
                    if k:
                        self.state = False  # Transition to OFF

            # Output matches state (Moore machine)
            out = 1 if self.state else 0
            stimulus_outputs.append({"out": BinaryValue(value=out, n_bits=1).binstr})

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
