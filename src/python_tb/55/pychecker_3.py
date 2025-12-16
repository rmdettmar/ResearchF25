import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state to B (True) as per reset condition
        """
        self.state = True  # True represents state B, False represents state A

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs according to state machine logic
        """
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            areset = BinaryValue(stimulus["areset"]).integer
            in_val = BinaryValue(stimulus["in"]).integer

            # Handle asynchronous reset
            if areset:
                self.state = True  # Go to state B
            else:
                # State transition logic
                if self.state:  # Current state is B
                    self.state = (
                        in_val == 1
                    )  # Stay in B if input is 1, go to A if input is 0
                else:  # Current state is A
                    self.state = (
                        in_val == 0
                    )  # Go to B if input is 0, stay in A if input is 1

            # Output depends only on current state (Moore machine)
            out = "1" if self.state else "0"
            outputs.append({"out": out})

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
