import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        STATE_A = 0
        STATE_B = 1

    def __init__(self):
        """
        Initialize internal state registers.
        Reset state is B.
        """
        self.current_state = self.State.STATE_B

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and update state machine.
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            reset_bv = BinaryValue(stimulus["reset"])
            in_bv = BinaryValue(stimulus["in"])

            reset = reset_bv.integer
            in_val = in_bv.integer

            # Handle reset first
            if reset:
                self.current_state = self.State.STATE_B
            else:
                # State transition logic
                if self.current_state == self.State.STATE_B:
                    if in_val == 0:
                        self.current_state = self.State.STATE_A
                else:  # State A
                    if in_val == 0:
                        self.current_state = self.State.STATE_B

            # Output logic - Moore machine output only depends on current state
            out = 1 if self.current_state == self.State.STATE_B else 0

            # Convert output to BinaryValue and then to binary string
            out_bv = BinaryValue(value=out, n_bits=1)
            stimulus_outputs.append({"out": out_bv.binstr})

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
