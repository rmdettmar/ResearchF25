import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state register.
        State B is represented as 1, State A as 0
        """
        self.current_state = 1  # Reset state is B

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs according to Moore state machine spec
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals from binary strings
            reset = BinaryValue(stimulus["reset"]).integer
            in_signal = BinaryValue(stimulus["in"]).integer

            # Update state
            if reset:
                self.current_state = 1  # Go to state B
            else:
                if self.current_state == 1:  # Current state is B
                    self.current_state = 0 if in_signal == 0 else 1
                else:  # Current state is A
                    self.current_state = 1 if in_signal == 0 else 0

            # Output is 1 in state B, 0 in state A
            out = BinaryValue(value=self.current_state, n_bits=1)

            # Add output to results
            stimulus_outputs.append({"out": out.binstr})

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
