import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers
        """
        self.ones_count = 0  # Count of consecutive ones
        self.prev_state = 0  # Previous state for output generation
        self.disc_out = 0  # Delayed disc output
        self.flag_out = 0  # Delayed flag output
        self.err_out = 0  # Delayed error output

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs according to FSM logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get input signals
            reset = int(BinaryValue(stimulus["reset"]).integer)
            in_bit = int(BinaryValue(stimulus["in"]).integer)

            # Store current state for output generation
            prev_count = self.ones_count

            # Handle reset
            if reset:
                self.ones_count = 0
            else:
                # Update ones count based on input
                if in_bit == 1:
                    self.ones_count += 1
                else:
                    self.ones_count = 0

            # Generate outputs based on previous state
            disc = 1 if prev_count == 5 and in_bit == 0 else 0
            flag = 1 if prev_count == 6 and in_bit == 0 else 0
            err = 1 if prev_count >= 7 else 0

            # Create output dictionary
            output = {
                "disc": format(disc, "b"),
                "flag": format(flag, "b"),
                "err": format(err, "b"),
            }
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
