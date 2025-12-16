import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state variables for the 2's complementer
        Using one-hot encoding: state_A = 1, state_B = 0 initially
        """
        self.state_A = 1  # Initial state is A
        self.state_B = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs according to the 2's complementer FSM
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            areset = BinaryValue(stimulus["areset"]).integer
            x = BinaryValue(stimulus["x"]).integer

            # Handle asynchronous reset
            if areset:
                self.state_A = 1
                self.state_B = 0
                z = 0
            else:
                # State transitions
                if self.state_A:
                    if x:
                        self.state_A = 0
                        self.state_B = 1
                    # else stay in state A

                # Output logic (Mealy machine)
                if self.state_A:
                    z = 1 if x else 0
                else:  # state B
                    z = 0 if x else 1

            # Convert output to binary string
            z_bv = BinaryValue(value=z, n_bits=1)
            stimulus_outputs.append({"z": z_bv.binstr})

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
