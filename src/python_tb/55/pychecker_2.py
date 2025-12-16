import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state to B (1) as per reset condition
        """
        self.state = 1  # 1 represents state B, 0 represents state A

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and update state according to Moore machine logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary string to BinaryValue
            areset = BinaryValue(stimulus["areset"]).integer
            in_val = BinaryValue(stimulus["in"]).integer

            # Handle asynchronous reset
            if areset:
                self.state = 1  # Reset to state B
            else:
                # State transition logic
                if self.state == 1:  # Current state is B
                    if in_val == 0:
                        self.state = 0  # Go to state A
                    # else stay in state B
                else:  # Current state is A
                    if in_val == 0:
                        self.state = 1  # Go to state B
                    # else stay in state A

            # Output is directly determined by state (Moore machine)
            out_val = BinaryValue(value=self.state, n_bits=1)
            stimulus_outputs.append({"out": out_val.binstr})

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
