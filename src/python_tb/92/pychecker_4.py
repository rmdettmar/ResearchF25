import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Define state encodings
        self.STATE_A = 0
        self.STATE_B = 1
        self.STATE_C = 2
        self.STATE_D = 3

        # Initialize internal state register
        self.current_state = self.STATE_A

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            resetn = BinaryValue(stimulus["resetn"]).integer
            r = BinaryValue(stimulus["r"]).integer

            # Extract individual request signals
            r1 = (r >> 0) & 1
            r2 = (r >> 1) & 1
            r3 = (r >> 2) & 1

            # Handle reset
            if not resetn:
                self.current_state = self.STATE_A
            else:
                # State transitions
                if self.current_state == self.STATE_A:
                    if r1:
                        self.current_state = self.STATE_B
                    elif r2:
                        self.current_state = self.STATE_C
                    elif r3:
                        self.current_state = self.STATE_D
                elif self.current_state == self.STATE_B:
                    if not r1:
                        self.current_state = self.STATE_A
                elif self.current_state == self.STATE_C:
                    if not r2:
                        self.current_state = self.STATE_A
                elif self.current_state == self.STATE_D:
                    if not r3:
                        self.current_state = self.STATE_A

            # Generate outputs based on current state
            g = 0
            if self.current_state == self.STATE_B:
                g |= 0b001  # g1 = 1
            elif self.current_state == self.STATE_C:
                g |= 0b010  # g2 = 1
            elif self.current_state == self.STATE_D:
                g |= 0b100  # g3 = 1

            # Convert output to BinaryValue and append to results
            g_bv = BinaryValue(value=g, n_bits=3, bigEndian=False)
            stimulus_outputs.append({"g": g_bv.binstr})

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
