import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state registers
        self.prev_in = 0  # Previous input state
        self.out_reg = 0  # Output register

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get current inputs
            reset = stimulus["reset"]
            current_in = int(BinaryValue(stimulus["in"]).value)

            if reset:
                # Synchronous reset - clear output register
                self.out_reg = 0
            else:
                # Check for 1->0 transitions
                transitions = (self.prev_in & ~current_in) & 0xFFFFFFFF
                # Set output bits where transitions occurred
                self.out_reg = (self.out_reg | transitions) & 0xFFFFFFFF

            # Store current input for next cycle
            self.prev_in = current_in

            # Format output as binary string
            out_bv = BinaryValue(value=self.out_reg, n_bits=32, bigEndian=False)
            stimulus_outputs.append({"out": out_bv.binstr})

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
