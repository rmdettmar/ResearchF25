import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers
        prev_in: Store previous input value for edge detection
        pedge: Store output edge detection results
        """
        self.prev_in = 0
        self.pedge = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process input stimuli and generate edge detection outputs
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get current input value
            in_bv = BinaryValue(stimulus["in"], n_bits=8)
            in_val = in_bv.integer

            # Initialize output value
            out_val = 0

            # Check each bit for 0->1 transition
            for i in range(8):
                prev_bit = (self.prev_in >> i) & 1
                curr_bit = (in_val >> i) & 1

                # Set output bit if positive edge detected
                if prev_bit == 0 and curr_bit == 1:
                    out_val |= 1 << i

            # Update previous input state
            self.prev_in = in_val

            # Create output dictionary
            out_bv = BinaryValue(value=out_val, n_bits=8)
            stimulus_outputs.append({"pedge": out_bv.binstr})

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
