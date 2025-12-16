import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state registers
        self.prev_in = 0  # Previous input state
        self.pedge = 0  # Output register

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary string to BinaryValue
            in_bv = BinaryValue(stimulus["in"])
            current_in = in_bv.integer

            # Detect rising edges by comparing with previous state
            # Edge occurs when previous bit was 0 and current bit is 1
            edge_detected = (current_in & ~self.prev_in) & 0xFF

            # Update output register with edge detection result
            self.pedge = edge_detected

            # Store current input as previous for next cycle
            self.prev_in = current_in

            # Convert output to binary string format
            out_bv = BinaryValue(value=self.pedge, n_bits=8)
            stimulus_outputs.append({"pedge": out_bv.binstr})

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
