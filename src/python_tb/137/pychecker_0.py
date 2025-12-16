import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state to B (True)
        self.state_B = True  # True for state B, False for state A

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert binary strings to boolean
            reset = bool(BinaryValue(stimulus["reset"]).integer)
            in_signal = bool(BinaryValue(stimulus["in"]).integer)

            # Update state
            if reset:
                self.state_B = True  # Reset to state B
            else:
                if self.state_B:  # Current state is B
                    if not in_signal:  # in=0
                        self.state_B = False  # Go to state A
                    # else stay in B
                else:  # Current state is A
                    if in_signal:  # in=1
                        self.state_B = False  # Stay in A
                    else:  # in=0
                        self.state_B = True  # Go to B

            # Output based on current state
            out = "1" if self.state_B else "0"
            stimulus_outputs.append({"out": out})

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
