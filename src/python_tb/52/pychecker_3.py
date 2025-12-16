import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 4-bit counter register to 0
        self.q = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue objects
            reset_bv = BinaryValue(stimulus["reset"])
            slowena_bv = BinaryValue(stimulus["slowena"])

            # Extract values
            reset = reset_bv.integer
            slowena = slowena_bv.integer

            # Update counter based on inputs
            if reset:
                self.q = 0
            elif slowena:
                # Increment counter if slowena is high
                if self.q == 9:
                    self.q = 0
                else:
                    self.q = self.q + 1

            # Convert output to BinaryValue with 4 bits
            q_bv = BinaryValue(value=self.q, n_bits=4)

            # Add current output to results
            stimulus_outputs.append({"q": q_bv.binstr})

        # Return results in specified format
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
