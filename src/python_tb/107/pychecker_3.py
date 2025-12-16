import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize 512-bit internal state register
        """
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs according to Rule 90
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            load = int(stimulus["load"], 2)
            data = int(stimulus["data"], 2)

            if load:
                # Load new data into register
                self.q_reg = data
            else:
                # Apply Rule 90: next_state[i] = q[i-1] XOR q[i+1]
                next_state = 0
                for i in range(512):
                    # Get left neighbor (0 for i=0)
                    left = (self.q_reg >> (i - 1)) & 1 if i > 0 else 0
                    # Get right neighbor (0 for i=511)
                    right = (self.q_reg >> (i + 1)) & 1 if i < 511 else 0
                    # XOR operation
                    next_bit = left ^ right
                    # Set bit in next state
                    next_state |= next_bit << i
                self.q_reg = next_state

            # Convert result to binary string
            result_bv = BinaryValue(value=self.q_reg, n_bits=512, bigEndian=False)
            stimulus_outputs.append({"q": result_bv.binstr})

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
