import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize internal state registers
        self.prev_in = 0  # Previous input state
        self.out_reg = 0  # Output register

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract input signals
            reset = stimulus.get("reset", 0)
            in_val = stimulus.get("in", 0)

            # Handle reset
            if reset:
                self.out_reg = 0
                self.prev_in = in_val
            else:
                # Check for 1->0 transitions on each bit
                transitions = (self.prev_in & ~in_val) & 0xFFFFFFFF
                # Set output bits where transitions occurred
                self.out_reg = (self.out_reg | transitions) & 0xFFFFFFFF
                # Update previous input state
                self.prev_in = in_val

            # Append current output to results
            stimulus_outputs.append({"out": self.out_reg})

        output_dict = {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }

        return output_dict


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
