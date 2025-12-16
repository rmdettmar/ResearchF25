import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state to B (1) due to async reset
        self.current_state = 1  # 1 for state B, 0 for state A

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            areset_bv = BinaryValue(stimulus["areset"])
            in_bv = BinaryValue(stimulus["in"])

            # Handle async reset
            if areset_bv.integer == 1:
                self.current_state = 1  # Reset to state B
            else:
                # State transition logic
                if self.current_state == 0:  # Current state A
                    if in_bv.integer == 0:
                        self.current_state = 1  # Go to B
                    else:
                        self.current_state = 0  # Stay in A
                else:  # Current state B
                    if in_bv.integer == 0:
                        self.current_state = 0  # Go to A
                    else:
                        self.current_state = 1  # Stay in B

            # Output depends only on current state
            out_val = BinaryValue(value=self.current_state, n_bits=1)
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
