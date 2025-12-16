import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        A = 0  # Idle state
        B = 1  # Grant to r1
        C = 2  # Grant to r2
        D = 3  # Grant to r3

    def __init__(self):
        """Initialize internal state registers"""
        self.current_state = self.State.A
        self.g = 0  # Output grants

    def load(self, stimulus_dict: Dict[str, Any]):
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to integers
            resetn = int(stimulus["resetn"], 2)
            r = int(stimulus["r"], 2)

            # Extract individual request signals
            r1 = (r >> 0) & 1
            r2 = (r >> 1) & 1
            r3 = (r >> 2) & 1

            # Handle reset
            if not resetn:
                self.current_state = self.State.A
            else:
                # State transitions
                if self.current_state == self.State.A:
                    if r1:
                        self.current_state = self.State.B
                    elif r2:
                        self.current_state = self.State.C
                    elif r3:
                        self.current_state = self.State.D
                elif self.current_state == self.State.B:
                    if not r1:
                        self.current_state = self.State.A
                elif self.current_state == self.State.C:
                    if not r2:
                        self.current_state = self.State.A
                elif self.current_state == self.State.D:
                    if not r3:
                        self.current_state = self.State.A

            # Generate outputs based on current state
            if self.current_state == self.State.B:
                self.g = 0b001  # g1 = 1
            elif self.current_state == self.State.C:
                self.g = 0b010  # g2 = 1
            elif self.current_state == self.State.D:
                self.g = 0b100  # g3 = 1
            else:  # State A
                self.g = 0b000  # all grants off

            # Format output as binary string
            g_bv = BinaryValue(value=self.g, n_bits=3)
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
