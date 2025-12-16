import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # State encoding
        self.STATE_A = 0b00
        self.STATE_B = 0b01
        self.STATE_C = 0b10
        self.STATE_D = 0b11

        # Initialize state register
        self.state = self.STATE_A

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            resetn = BinaryValue(stimulus["resetn"]).integer
            r = BinaryValue(stimulus["r"]).integer

            # Extract individual requests
            r1 = (r >> 2) & 1
            r2 = (r >> 1) & 1
            r3 = r & 1

            # State update logic
            if not resetn:
                self.state = self.STATE_A
            else:
                if self.state == self.STATE_A:
                    if r1:
                        self.state = self.STATE_B
                    elif r2:
                        self.state = self.STATE_C
                    elif r3:
                        self.state = self.STATE_D
                elif self.state == self.STATE_B:
                    if not r1:
                        self.state = self.STATE_A
                elif self.state == self.STATE_C:
                    if not r2:
                        self.state = self.STATE_A
                elif self.state == self.STATE_D:
                    if not r3:
                        self.state = self.STATE_A

            # Generate outputs
            g = 0
            if self.state == self.STATE_B:
                g |= 1 << 2  # g[1]
            elif self.state == self.STATE_C:
                g |= 1 << 1  # g[2]
            elif self.state == self.STATE_D:
                g |= 1  # g[3]

            # Convert output to 3-bit BinaryValue
            g_bv = BinaryValue(value=g, n_bits=3)
            stimulus_outputs.append({"g": g_bv.binstr})

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
