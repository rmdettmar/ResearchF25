import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Define states
        self.STATE_A = 0
        self.STATE_B = 1
        # Initialize state to B (reset state)
        self.current_state = self.STATE_B

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            reset_bv = BinaryValue(stimulus["reset"])
            in_bv = BinaryValue(stimulus["in"])

            # Handle reset
            if reset_bv.integer == 1:
                self.current_state = self.STATE_B
            else:
                # State transition logic
                if self.current_state == self.STATE_B:
                    if in_bv.integer == 0:
                        self.current_state = self.STATE_A
                    # else stay in STATE_B
                else:  # current_state == STATE_A
                    if in_bv.integer == 0:
                        self.current_state = self.STATE_B
                    # else stay in STATE_A

            # Output logic (Moore machine)
            out = 1 if self.current_state == self.STATE_B else 0

            # Convert output to binary string
            out_bv = BinaryValue(value=out, n_bits=1)
            stimulus_outputs.append({"out": out_bv.binstr})

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
