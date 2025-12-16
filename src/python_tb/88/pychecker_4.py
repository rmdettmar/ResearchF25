import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers
        """
        self.counter = 0  # Counter to track cycles after reset
        self.shift_ena = 0  # Output signal

    def load(self, stimulus_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input stimulus and generate output
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            reset = BinaryValue(stimulus["reset"]).integer

            if reset:
                # On reset, start counter and enable shift
                self.counter = 0
                self.shift_ena = 1
            elif self.counter < 4:
                # Keep shift enabled and increment counter
                self.counter += 1
                self.shift_ena = 1
            else:
                # After 4 cycles, disable shift
                self.shift_ena = 0

            # Convert output to binary string
            shift_ena_bv = BinaryValue(value=self.shift_ena, n_bits=1)
            output = {"shift_ena": shift_ena_bv.binstr}
            stimulus_outputs.append(output)

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
