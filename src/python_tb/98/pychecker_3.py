import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        STATE_A = 0
        STATE_F = 1
        STATE_X1 = 2
        STATE_X0 = 3
        STATE_X2 = 4
        STATE_G = 5
        STATE_G_WAIT = 6
        STATE_G_PERM = 7
        STATE_G_OFF = 8

    def __init__(self):
        self.current_state = self.State.STATE_A
        self.f = 0
        self.g = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            resetn = int(BinaryValue(stimulus["resetn"]).value)
            x = int(BinaryValue(stimulus["x"]).value)
            y = int(BinaryValue(stimulus["y"]).value)

            # Handle reset
            if not resetn:
                self.current_state = self.State.STATE_A
                self.f = 0
                self.g = 0
            else:
                # State transitions
                if self.current_state == self.State.STATE_A:
                    self.current_state = self.State.STATE_F
                elif self.current_state == self.State.STATE_F:
                    self.current_state = self.State.STATE_X1
                elif self.current_state == self.State.STATE_X1:
                    if x == 1:
                        self.current_state = self.State.STATE_X0
                elif self.current_state == self.State.STATE_X0:
                    if x == 0:
                        self.current_state = self.State.STATE_X2
                    else:
                        self.current_state = self.State.STATE_X1
                elif self.current_state == self.State.STATE_X2:
                    if x == 1:
                        self.current_state = self.State.STATE_G
                    else:
                        self.current_state = self.State.STATE_X1
                elif self.current_state == self.State.STATE_G:
                    if y == 1:
                        self.current_state = self.State.STATE_G_PERM
                    else:
                        self.current_state = self.State.STATE_G_WAIT
                elif self.current_state == self.State.STATE_G_WAIT:
                    if y == 1:
                        self.current_state = self.State.STATE_G_PERM
                    else:
                        self.current_state = self.State.STATE_G_OFF

            # Output logic
            self.f = 1 if self.current_state == self.State.STATE_F else 0
            self.g = (
                1
                if self.current_state
                in [
                    self.State.STATE_G,
                    self.State.STATE_G_WAIT,
                    self.State.STATE_G_PERM,
                ]
                else 0
            )

            # Convert outputs to binary strings
            f_bin = BinaryValue(value=self.f, n_bits=1).binstr
            g_bin = BinaryValue(value=self.g, n_bits=1).binstr

            stimulus_outputs.append({"f": f_bin, "g": g_bin})

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
