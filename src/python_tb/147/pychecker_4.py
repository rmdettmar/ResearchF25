import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        IDLE = 0
        START_BIT = 1
        DATA_BITS = 2
        STOP_BIT = 3

    def __init__(self):
        """
        Initialize FSM state and counters
        """
        self.current_state = self.State.IDLE
        self.bit_counter = 0
        self.done_reg = 0

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Update FSM state based on inputs
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            reset = BinaryValue(stimulus["reset"]).integer
            in_bit = BinaryValue(stimulus["in"]).integer

            # Handle reset
            if reset:
                self.current_state = self.State.IDLE
                self.bit_counter = 0
                self.done_reg = 0
            else:
                # FSM state transitions
                if self.current_state == self.State.IDLE:
                    if in_bit == 0:  # Start bit detected
                        self.current_state = self.State.START_BIT
                    self.done_reg = 0

                elif self.current_state == self.State.START_BIT:
                    self.current_state = self.State.DATA_BITS
                    self.bit_counter = 0
                    self.done_reg = 0

                elif self.current_state == self.State.DATA_BITS:
                    if self.bit_counter < 7:
                        self.bit_counter += 1
                        self.done_reg = 0
                    else:
                        self.current_state = self.State.STOP_BIT
                        self.done_reg = 0

                elif self.current_state == self.State.STOP_BIT:
                    if in_bit == 1:  # Valid stop bit
                        self.current_state = self.State.IDLE
                        self.done_reg = 1
                    self.bit_counter = 0

            stimulus_outputs.append({"done": format(self.done_reg, "01b")})

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
