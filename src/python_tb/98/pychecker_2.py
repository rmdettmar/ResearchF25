import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        A = 0  # Reset state
        B = 1  # f=1 state
        C = 2  # Monitor x
        D = 3  # Monitor y
        E = 4  # g=1 permanent
        F = 5  # g=0 permanent

    def __init__(self):
        self.current_state = self.State.A
        self.x_history = [0, 0, 0]  # Store last 3 x values
        self.y_counter = 0  # Counter for y monitoring
        self.f = 0
        self.g = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            resetn = int(BinaryValue(stimulus["resetn"]).value)
            x = int(BinaryValue(stimulus["x"]).value)
            y = int(BinaryValue(stimulus["y"]).value)

            # State machine logic
            if not resetn:
                self.current_state = self.State.A
                self.x_history = [0, 0, 0]
                self.y_counter = 0
                self.f = 0
                self.g = 0
            else:
                if self.current_state == self.State.A:
                    self.current_state = self.State.B
                    self.f = 1

                elif self.current_state == self.State.B:
                    self.current_state = self.State.C
                    self.f = 0
                    self.x_history = [0, 0, 0]

                elif self.current_state == self.State.C:
                    # Update x history
                    self.x_history = [x] + self.x_history[:-1]
                    if self.x_history == [1, 0, 1]:
                        self.current_state = self.State.D
                        self.g = 1
                        self.y_counter = 0

                elif self.current_state == self.State.D:
                    if y == 1:
                        self.current_state = self.State.E
                    else:
                        self.y_counter += 1
                        if self.y_counter >= 2:
                            self.current_state = self.State.F
                            self.g = 0

                elif self.current_state == self.State.E:
                    self.g = 1

                elif self.current_state == self.State.F:
                    self.g = 0

            stimulus_outputs.append(
                {"f": format(self.f, "b"), "g": format(self.g, "b")}
            )

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
