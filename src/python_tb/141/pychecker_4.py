import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state register for one-hot encoding:
        State A = 01
        State B = 10
        Reset state is A
        """
        self.state = 0b01  # Initialize to state A

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs according to 2's complementer FSM
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            areset = BinaryValue(stimulus["areset"]).integer
            x = BinaryValue(stimulus["x"]).integer

            # Handle reset
            if areset:
                self.state = 0b01  # Reset to state A
                z = 0
            else:
                # Determine output based on current state and input
                if self.state == 0b01:  # State A
                    z = 1 if x else 0
                    # State transition
                    if x:
                        self.state = 0b10  # Go to state B
                else:  # State B
                    z = 0 if x else 1
                    # Stay in state B

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
