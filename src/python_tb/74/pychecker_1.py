import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 10-bit counter to 0
        self.counter = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to proper format
            load = int(stimulus["load"], 2)
            data = BinaryValue(stimulus["data"]).integer

            # Update counter based on load signal
            if load:
                # Load counter with input data
                self.counter = data & 0x3FF  # Ensure 10-bit value
            elif self.counter > 0:
                # Decrement counter if not zero
                self.counter -= 1

            # Generate tc output (1 when counter is 0)
            tc = 1 if self.counter == 0 else 0

            # Convert tc to binary string
            tc_bv = BinaryValue(value=tc, n_bits=1)
            stimulus_outputs.append({"tc": tc_bv.binstr})

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
