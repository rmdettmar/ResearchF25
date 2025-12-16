import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        IDLE = 0
        DATA = 1
        STOP = 2

    def __init__(self):
        """Initialize internal state registers"""
        self.current_state = self.State.IDLE
        self.bit_count = 0
        self.done = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """Process inputs and update state"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            reset = BinaryValue(stimulus["reset"]).integer
            in_bit = BinaryValue(stimulus["in"]).integer

            # Process reset
            if reset:
                self.current_state = self.State.IDLE
                self.bit_count = 0
                self.done = 0
            else:
                # FSM state transitions
                if self.current_state == self.State.IDLE:
                    self.done = 0
                    if in_bit == 0:  # Start bit detected
                        self.current_state = self.State.DATA
                        self.bit_count = 0

                elif self.current_state == self.State.DATA:
                    self.bit_count += 1
                    if self.bit_count >= 8:
                        self.current_state = self.State.STOP

                elif self.current_state == self.State.STOP:
                    if in_bit == 1:  # Valid stop bit
                        self.done = 1
                    self.current_state = self.State.IDLE

            # Append output to results
            stimulus_outputs.append({"done": format(self.done, "01b")})

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
