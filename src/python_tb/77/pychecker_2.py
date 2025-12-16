import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize previous input state and output register
        self.prev_in = 0
        self.anyedge = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            in_bv = BinaryValue(stimulus["in"])
            current_in = in_bv.integer

            # Detect edges by XORing current and previous inputs
            # If bits are different, there was an edge
            edges = current_in ^ self.prev_in

            # Update output register with detected edges
            self.anyedge = edges

            # Store current input as previous for next cycle
            self.prev_in = current_in

            # Convert output to 8-bit binary string
            out_bv = BinaryValue(value=self.anyedge, n_bits=8)
            stimulus_outputs.append({"anyedge": out_bv.binstr})

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
