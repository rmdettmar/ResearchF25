import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state to 0
        self.state = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            a_bv = BinaryValue(stimulus["a"])
            b_bv = BinaryValue(stimulus["b"])

            # Convert to integers
            a = a_bv.integer
            b = b_bv.integer

            # Determine output q based on current state and inputs
            q = 0
            if self.state == 0:
                if (a == 0 and b == 1) or (a == 1 and b == 0):
                    q = 1
                elif a == 1 and b == 1:
                    q = 0
            else:  # state == 1
                if (a == 0 and b == 0) or (a == 1 and b == 1):
                    q = 1
                else:
                    q = 0

            # Determine next state
            if a == 0 and b == 0:
                next_state = 0
            elif a == 1 and b == 1:
                next_state = self.state ^ 1  # Toggle state
            else:
                next_state = self.state

            # Update state
            self.state = next_state

            # Format outputs as dictionary
            output = {"q": format(q, "b"), "state": format(self.state, "b")}
            stimulus_outputs.append(output)

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
