import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers
        """
        self.prev_in = BinaryValue(value=0, n_bits=8)  # Previous input value
        self.anyedge = BinaryValue(value=0, n_bits=8)  # Output register

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process input stimulus and generate output
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            current_in = BinaryValue(value=stimulus["in"], n_bits=8)

            # Detect edges by XORing current and previous values
            # If bits are different, there was an edge
            edge_detect = current_in.integer ^ self.prev_in.integer

            # Update output register
            self.anyedge = BinaryValue(value=edge_detect, n_bits=8)

            # Store current input as previous for next cycle
            self.prev_in = current_in

            # Add current output to results
            stimulus_outputs.append({"anyedge": self.anyedge.binstr})

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
