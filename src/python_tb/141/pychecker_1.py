import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state registers
        Using one-hot encoding:
        State A = 2'b01 (reset state)
        State B = 2'b10
        """
        self.state = 0b01  # Reset state (State A)

    def load(self, stimulus_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process inputs and produce outputs according to 2's complementer FSM
        """
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get input values
            areset = BinaryValue(stimulus["areset"]).integer
            x = BinaryValue(stimulus["x"]).integer

            # Handle reset
            if areset:
                self.state = 0b01  # Go to state A
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

            # Add output to results
            outputs.append({"z": BinaryValue(value=z, n_bits=1).binstr})

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
