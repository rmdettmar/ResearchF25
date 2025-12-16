import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        A = 0
        B = 1
        C = 2
        D = 3
        E = 4
        F = 5

    def __init__(self):
        """
        Initialize state register to state A (reset state)
        """
        self.current_state = self.State.A

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and generate outputs according to FSM specification
        """
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs from binary strings to values
            reset = BinaryValue(stimulus["reset"]).integer
            w = BinaryValue(stimulus["w"]).integer

            # Update state based on reset and input
            if reset:
                self.current_state = self.State.A
            else:
                if self.current_state == self.State.A:
                    self.current_state = self.State.B if w else self.State.A
                elif self.current_state == self.State.B:
                    self.current_state = self.State.C if w else self.State.D
                elif self.current_state == self.State.C:
                    self.current_state = self.State.E if w else self.State.D
                elif self.current_state == self.State.D:
                    self.current_state = self.State.F if w else self.State.A
                elif self.current_state == self.State.E:
                    self.current_state = self.State.E if w else self.State.D
                elif self.current_state == self.State.F:
                    self.current_state = self.State.C if w else self.State.D

            # Generate output z (1 in states E and F, 0 otherwise)
            z = "1" if self.current_state in [self.State.E, self.State.F] else "0"
            outputs.append({"z": z})

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
