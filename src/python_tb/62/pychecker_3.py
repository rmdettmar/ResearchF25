import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state to S0 (one-hot encoding)
        self.current_state = 0b0000000001

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input to BinaryValue
            input_signal = BinaryValue(stimulus["in"])
            in_val = input_signal.integer

            # Calculate next state based on current state and input
            next_state = 0
            if self.current_state & 0b0000000001:  # S0
                next_state = 0b0000000010 if in_val else 0b0000000001
            elif self.current_state & 0b0000000010:  # S1
                next_state = 0b0000000100 if in_val else 0b0000000001
            elif self.current_state & 0b0000000100:  # S2
                next_state = 0b0000001000 if in_val else 0b0000000001
            elif self.current_state & 0b0000001000:  # S3
                next_state = 0b0000010000 if in_val else 0b0000000001
            elif self.current_state & 0b0000010000:  # S4
                next_state = 0b0000100000 if in_val else 0b0000000001
            elif self.current_state & 0b0000100000:  # S5
                next_state = 0b0001000000 if in_val else 0b0100000000
            elif self.current_state & 0b0001000000:  # S6
                next_state = 0b0010000000 if in_val else 0b1000000000
            elif self.current_state & 0b0010000000:  # S7
                next_state = 0b0010000000 if in_val else 0b0000000001
            elif self.current_state & 0b0100000000:  # S8
                next_state = 0b0000000010 if in_val else 0b0000000001
            elif self.current_state & 0b1000000000:  # S9
                next_state = 0b0000000010 if in_val else 0b0000000001

            # Calculate outputs based on current state
            out1 = 1 if (self.current_state & 0b1100000000) else 0
            out2 = 1 if (self.current_state & 0b1010000000) else 0

            # Update current state
            self.current_state = next_state

            # Add outputs to results
            output_dict = {
                "out1": str(out1),
                "out2": str(out2),
                "next_state": format(next_state, "010b"),
            }
            stimulus_outputs.append(output_dict)

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
