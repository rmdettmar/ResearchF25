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

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Update state based on input stimulus
        """
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(BinaryValue(stimulus["reset"]).value)

            # Synchronous reset logic
            if reset:
                self.counter = 0
                self.shift_ena = 1
            else:
                if self.counter < 4:
                    self.counter += 1
                    self.shift_ena = 1
                else:
                    self.shift_ena = 0

            # Convert output to binary string format
            shift_ena_bv = BinaryValue(value=self.shift_ena, n_bits=1)
            outputs.append({"shift_ena": shift_ena_bv.binstr})

        return {"scenario": stimulus_dict["scenario"], "output variable": outputs}


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
