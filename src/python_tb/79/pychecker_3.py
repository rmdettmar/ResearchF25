import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers
        """
        self.q_reg = BinaryValue("xxx", n_bits=3)  # Initialize q as unknown
        self.prev_a = 0  # Previous value of input a

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process input stimulus and generate outputs
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            clk = int(stimulus["clk"])
            a = int(stimulus["a"])

            # Only update on positive clock edge
            if clk == 1:
                if a == 1:
                    # When a is 1, q should be 4
                    self.q_reg = BinaryValue(value=4, n_bits=3)
                elif self.prev_a == 1 and a == 0:
                    # On 1->0 transition of a, start counting from 4
                    self.q_reg = BinaryValue(value=4, n_bits=3)
                elif a == 0:
                    # When a is 0, increment q
                    if self.q_reg.binstr != "xxx":
                        next_val = (self.q_reg.integer + 1) % 8
                        self.q_reg = BinaryValue(value=next_val, n_bits=3)

                self.prev_a = a

            # Add current output to results
            stimulus_outputs.append({"q": self.q_reg.binstr})

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
