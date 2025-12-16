import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize 3-bit counter register q
        """
        self.q = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Update counter based on input a
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            clk = BinaryValue(stimulus["clk"]).integer
            a = BinaryValue(stimulus["a"]).integer

            # Only update on positive clock edge
            if clk == 1:
                if a == 1:
                    # When a=1, increment until 4
                    if self.q < 4:
                        self.q += 1
                else:
                    # When a=0, increment and wrap around after 6
                    if self.q == 6:
                        self.q = 0
                    else:
                        self.q += 1

            # Convert output to 3-bit binary string
            q_bv = BinaryValue(value=self.q, n_bits=3)
            stimulus_outputs.append({"q": q_bv.binstr})

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
