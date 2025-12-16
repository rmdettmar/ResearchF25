import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize the flip-flop state to 0
        self.ff_state = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        # Process each stimulus in sequence
        for stimulus in stimulus_dict["input variable"]:
            # Get input signal
            in_sig = BinaryValue(stimulus["in"]).integer

            # Calculate new state (XOR of input and current state)
            new_state = in_sig ^ self.ff_state

            # Update flip-flop state
            self.ff_state = new_state

            # Convert output to binary string format
            out_bv = BinaryValue(value=self.ff_state, n_bits=1)
            stimulus_outputs.append({"out": out_bv.binstr})

        # Return output dictionary
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
