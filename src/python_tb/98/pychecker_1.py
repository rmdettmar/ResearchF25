import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class State(Enum):
    STATE_A = 0  # Reset state
    STATE_B = 1  # Initial state after reset
    STATE_C = 2  # f=1 state
    STATE_X1 = 3  # Waiting for first 1 in x sequence
    STATE_X2 = 4  # Waiting for 0 in x sequence
    STATE_X3 = 5  # Waiting for second 1 in x sequence
    STATE_Y = 6  # Monitoring y input
    STATE_G1 = 7  # g=1 permanent
    STATE_G0 = 8  # g=0 permanent


class GoldenDUT:
    def __init__(self):
        self.state = State.STATE_A
        self.y_counter = 0
        self.f = 0
        self.g = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to appropriate format
            resetn = BinaryValue(stimulus["resetn"]).integer
            x = BinaryValue(stimulus["x"]).integer
            y = BinaryValue(stimulus["y"]).integer

            # Reset condition
            if not resetn:
                self.state = State.STATE_A
                self.y_counter = 0
                self.f = 0
                self.g = 0
            else:
                # State machine transitions
                if self.state == State.STATE_A:
                    self.state = State.STATE_B
                    self.f = 0

                elif self.state == State.STATE_B:
                    self.state = State.STATE_C
                    self.f = 1

                elif self.state == State.STATE_C:
                    self.state = State.STATE_X1
                    self.f = 0

                elif self.state == State.STATE_X1:
                    if x == 1:
                        self.state = State.STATE_X2

                elif self.state == State.STATE_X2:
                    if x == 0:
                        self.state = State.STATE_X3
                    else:
                        self.state = State.STATE_X1

                elif self.state == State.STATE_X3:
                    if x == 1:
                        self.state = State.STATE_Y
                        self.g = 1
                        self.y_counter = 0
                    else:
                        self.state = State.STATE_X1

                elif self.state == State.STATE_Y:
                    if y == 1:
                        self.state = State.STATE_G1
                    else:
                        self.y_counter += 1
                        if self.y_counter >= 2:
                            self.state = State.STATE_G0
                            self.g = 0

            outputs.append({"f": format(self.f, "b"), "g": format(self.g, "b")})

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
