import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        IDLE = 0
        DATA_BITS = 1
        STOP_BIT = 2
        WAIT_STOP = 3

    def __init__(self):
        """Initialize internal state registers"""
        self.state = self.State.IDLE
        self.data_reg = 0
        self.bit_count = 0
        self.done_reg = 0
        self.out_byte_reg = 0

    def load(self, stimulus_dict: Dict[str, any]):
        """Process input signals and update state"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            reset = BinaryValue(stimulus["reset"]).integer
            in_bit = BinaryValue(stimulus["in"]).integer

            # Reset logic
            if reset:
                self.state = self.State.IDLE
                self.data_reg = 0
                self.bit_count = 0
                self.done_reg = 0
                self.out_byte_reg = 0
            else:
                # FSM state transitions
                if self.state == self.State.IDLE:
                    if in_bit == 0:  # Start bit detected
                        self.state = self.State.DATA_BITS
                        self.bit_count = 0
                        self.data_reg = 0
                        self.done_reg = 0

                elif self.state == self.State.DATA_BITS:
                    self.data_reg |= in_bit << self.bit_count
                    self.bit_count += 1
                    if self.bit_count == 8:
                        self.state = self.State.STOP_BIT

                elif self.state == self.State.STOP_BIT:
                    if in_bit == 1:  # Valid stop bit
                        self.done_reg = 1
                        self.out_byte_reg = self.data_reg
                        self.state = self.State.IDLE
                    else:  # Invalid stop bit
                        self.state = self.State.WAIT_STOP
                        self.done_reg = 0

                elif self.state == self.State.WAIT_STOP:
                    if in_bit == 1:
                        self.state = self.State.IDLE

            # Prepare output dictionary for this stimulus
            out_byte_bv = BinaryValue(value=self.out_byte_reg, n_bits=8)
            done_bv = BinaryValue(value=self.done_reg, n_bits=1)

            stimulus_outputs.append(
                {"out_byte": out_byte_bv.binstr, "done": done_bv.binstr}
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
