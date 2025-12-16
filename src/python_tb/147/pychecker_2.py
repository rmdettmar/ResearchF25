import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        IDLE = 0  # Waiting for start bit
        DATA = 1  # Receiving data bits
        STOP = 2  # Checking stop bit
        ERROR = 3  # Error state, waiting for 1

    def __init__(self):
        """Initialize FSM state and counters"""
        self.current_state = self.State.IDLE
        self.bit_counter = 0
        self.done_reg = 0

    def load(self, stimulus_dict: Dict[str, any]):
        """Process input signals and update FSM state"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals
            reset = int(stimulus["reset"], 2)
            in_bit = int(stimulus["in"], 2)

            # Handle reset
            if reset:
                self.current_state = self.State.IDLE
                self.bit_counter = 0
                self.done_reg = 0
            else:
                # FSM state transitions
                if self.current_state == self.State.IDLE:
                    if in_bit == 0:  # Start bit detected
                        self.current_state = self.State.DATA
                        self.bit_counter = 0
                        self.done_reg = 0

                elif self.current_state == self.State.DATA:
                    self.bit_counter += 1
                    if self.bit_counter == 8:  # All data bits received
                        self.current_state = self.State.STOP
                        self.bit_counter = 0

                elif self.current_state == self.State.STOP:
                    if in_bit == 1:  # Valid stop bit
                        self.done_reg = 1
                        self.current_state = self.State.IDLE
                    else:  # Invalid stop bit
                        self.current_state = self.State.ERROR

                elif self.current_state == self.State.ERROR:
                    if in_bit == 1:  # Found a 1, can look for next start bit
                        self.current_state = self.State.IDLE
                    self.done_reg = 0

            # Convert output to binary string
            done_bv = BinaryValue(value=self.done_reg, n_bits=1)
            stimulus_outputs.append({"done": done_bv.binstr})

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
