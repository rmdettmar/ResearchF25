import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the flip-flop state
        """
        self.out_reg = BinaryValue(value=0, n_bits=1)

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and update state on each clock edge
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get input signal
            in_signal = BinaryValue(stimulus["in"])

            # Calculate XOR of input and current output
            xor_result = (in_signal.integer ^ self.out_reg.integer) & 0x1

            # Update flip-flop state with XOR result
            self.out_reg = BinaryValue(value=xor_result, n_bits=1)

            # Add current output to results
            stimulus_outputs.append({"out": self.out_reg.binstr})

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
