import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        STATE_A = 0  # Reset state
        STATE_B = 1  # f=1 state
        MONITOR_X = 2  # Monitoring x sequence
        MONITOR_Y = 3  # Monitoring y input
        G_HIGH = 4  # g permanently high
        G_LOW = 5  # g permanently low

    def __init__(self):
        self.current_state = self.State.STATE_A
        self.x_history = []
        self.y_counter = 0
        self.f = 0
        self.g = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            resetn = int(BinaryValue(stimulus["resetn"]).value)
            x = int(BinaryValue(stimulus["x"]).value)
            y = int(BinaryValue(stimulus["y"]).value)

            # Handle reset
            if not resetn:
                self.current_state = self.State.STATE_A
                self.x_history = []
                self.y_counter = 0
                self.f = 0
                self.g = 0
            else:
                # State machine transitions
                if self.current_state == self.State.STATE_A:
                    self.current_state = self.State.STATE_B
                    self.f = 1

                elif self.current_state == self.State.STATE_B:
                    self.f = 0
                    self.current_state = self.State.MONITOR_X
                    self.x_history = [x]

                elif self.current_state == self.State.MONITOR_X:
                    self.x_history.append(x)
                    if len(self.x_history) >= 3:
                        if self.x_history[-3:] == [1, 0, 1]:
                            self.current_state = self.State.MONITOR_Y
                            self.g = 1
                            self.y_counter = 0
                        if len(self.x_history) > 3:
                            self.x_history.pop(0)

                elif self.current_state == self.State.MONITOR_Y:
                    if y == 1:
                        self.current_state = self.State.G_HIGH
                    else:
                        self.y_counter += 1
                        if self.y_counter >= 2:
                            self.current_state = self.State.G_LOW
                            self.g = 0

                elif self.current_state == self.State.G_HIGH:
                    self.g = 1

                elif self.current_state == self.State.G_LOW:
                    self.g = 0

            stimulus_outputs.append({"f": str(self.f), "g": str(self.g)})

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
