import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        IDLE = 0  # Waiting for start bit
        DATA = 1  # Receiving data bits
        STOP = 2  # Checking stop bit

    def __init__(self):
        """
        Initialize internal state registers
        """
        self.state = self.State.IDLE
        self.bit_counter = 0
        self.data_reg = 0
        self.done_reg = 0
        self.out_byte_reg = 0

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and update state
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to values
            reset = int(stimulus["reset"], 2)
            in_bit = int(stimulus["in"], 2)

            # Handle reset
            if reset:
                self.state = self.State.IDLE
                self.bit_counter = 0
                self.data_reg = 0
                self.done_reg = 0
                self.out_byte_reg = 0
            else:
                # FSM state transitions
                if self.state == self.State.IDLE:
                    if in_bit == 0:  # Start bit detected
                        self.state = self.State.DATA
                        self.bit_counter = 0
                        self.data_reg = 0
                        self.done_reg = 0

                elif self.state == self.State.DATA:
                    # Shift in data LSB first
                    self.data_reg = (self.data_reg >> 1) | (in_bit << 7)
                    self.bit_counter += 1

                    if self.bit_counter == 8:
                        self.state = self.State.STOP
                        self.out_byte_reg = self.data_reg

                elif self.state == self.State.STOP:
                    if in_bit == 1:  # Valid stop bit
                        self.done_reg = 1
                        self.state = self.State.IDLE
                    else:  # Invalid stop bit
                        self.done_reg = 0
                        # Stay in STOP state until we see a 1

            # Convert output values to binary strings
            out_byte = BinaryValue(value=self.out_byte_reg, n_bits=8)
            done = BinaryValue(value=self.done_reg, n_bits=1)

            stimulus_outputs.append({"out_byte": out_byte.binstr, "done": done.binstr})

            # Reset done signal after one cycle
            self.done_reg = 0

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
