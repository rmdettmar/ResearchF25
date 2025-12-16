import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state to A (one-hot encoding)
        """
        self.state = 1  # State A=1, State B=0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs according to 2's complementer FSM
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            areset = BinaryValue(stimulus["areset"]).integer
            x = BinaryValue(stimulus["x"]).integer

            # Handle asynchronous reset
            if areset:
                self.state = 1  # Reset to state A
                z = 0
            else:
                # State transition and output logic
                if self.state == 1:  # State A
                    if x == 0:
                        z = 0
                        self.state = 1  # Stay in A
                    else:  # x == 1
                        z = 1
                        self.state = 0  # Go to B
                else:  # State B
                    self.state = 0  # Stay in B
                    z = 1 if x == 0 else 0

            # Format output as binary string
            z_bv = BinaryValue(value=z, n_bits=1)
            stimulus_outputs.append({"z": z_bv.binstr})

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
