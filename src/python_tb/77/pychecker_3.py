import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize previous input register to 0
        self.prev_in = BinaryValue(value=0, n_bits=8)
        self.anyedge = BinaryValue(value=0, n_bits=8)

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            current_in = BinaryValue(value=int(stimulus["in"], 2), n_bits=8)

            # Compare each bit of current and previous input
            for i in range(8):
                # Extract bits using proper indexing
                curr_bit = int(current_in[i])
                prev_bit = int(self.prev_in[i])

                # Set output if there was an edge in previous cycle
                if curr_bit != prev_bit:
                    self.anyedge[i] = 1
                else:
                    self.anyedge[i] = 0

            # Store output for this stimulus
            stimulus_outputs.append({"anyedge": self.anyedge.binstr})

            # Update previous input for next cycle
            self.prev_in = current_in

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
