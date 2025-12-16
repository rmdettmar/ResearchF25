import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize previous input state to 0
        self.prev_in = BinaryValue(value=0, n_bits=8)
        self.pedge = BinaryValue(value=0, n_bits=8)

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get current input and convert to BinaryValue
            current_in = BinaryValue(value=stimulus["in"], n_bits=8)

            # Initialize output
            out = 0

            # Check each bit for 0->1 transition
            for i in range(8):
                # Extract bits using proper indexing
                prev_bit = int(self.prev_in[i])
                curr_bit = int(current_in[i])

                # Set output bit if positive edge detected
                if prev_bit == 0 and curr_bit == 1:
                    out |= 1 << i

            # Convert output to BinaryValue
            self.pedge = BinaryValue(value=out, n_bits=8)

            # Store current input as previous for next cycle
            self.prev_in = current_in

            # Add output to results
            stimulus_outputs.append({"pedge": self.pedge.binstr})

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
