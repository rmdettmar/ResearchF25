import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """Initialize internal state registers"""
        self.prev_in = 0  # Previous input value
        self.out_reg = 0  # Output register

    def load(self, stimulus_dict: Dict[str, any]):
        """Process input stimulus and generate output"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract input signals
            reset = stimulus["reset"]
            in_val = stimulus["in"]

            if reset:
                # Synchronous reset
                self.out_reg = 0
            else:
                # Detect falling edges (1->0 transitions)
                falling_edges = (self.prev_in & ~in_val) & 0xFFFFFFFF
                # Set output bits where falling edges detected
                self.out_reg = (self.out_reg | falling_edges) & 0xFFFFFFFF

            # Store current input for next cycle
            self.prev_in = in_val
            # Append current output to results
            stimulus_outputs.append(self.out_reg)

        return {
            "scenario": stimulus_dict["scenario"],
            "output variable": [{"out": out_val} for out_val in stimulus_outputs],
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
