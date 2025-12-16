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
            # Convert input signals
            reset = stimulus["reset"]
            in_val = BinaryValue(stimulus["in"], n_bits=32).integer

            if reset:
                # Synchronous reset - clear all outputs
                self.out_reg = 0
            else:
                # Detect falling edges (1->0 transitions)
                falling_edges = (self.prev_in & ~in_val) & 0xFFFFFFFF
                # Update output - maintain previous 1s and add new falling edges
                self.out_reg = (self.out_reg | falling_edges) & 0xFFFFFFFF

            # Store current input for next cycle
            self.prev_in = in_val

            # Convert output to binary string format
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
