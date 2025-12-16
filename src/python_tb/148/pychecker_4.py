import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # FSM states
        self.STATE_IDLE = 0
        self.STATE_DATA = 1
        self.STATE_STOP = 2

        # Initialize state variables
        self.current_state = self.STATE_IDLE
        self.bit_counter = 0
        self.shift_reg = 0
        self.done_reg = 0
        self.out_byte_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals from binary strings to values
            reset = BinaryValue(stimulus["reset"]).integer
            in_bit = BinaryValue(stimulus["in"]).integer

            # Reset logic
            if reset:
                self.current_state = self.STATE_IDLE
                self.bit_counter = 0
                self.shift_reg = 0
                self.done_reg = 0
                self.out_byte_reg = 0
            else:
                # FSM state machine
                if self.current_state == self.STATE_IDLE:
                    self.done_reg = 0
                    if in_bit == 0:  # Start bit detected
                        self.current_state = self.STATE_DATA
                        self.bit_counter = 0
                        self.shift_reg = 0

                elif self.current_state == self.STATE_DATA:
                    self.shift_reg = (self.shift_reg >> 1) | (in_bit << 7)
                    self.bit_counter += 1

                    if self.bit_counter == 8:
                        self.current_state = self.STATE_STOP

                elif self.current_state == self.STATE_STOP:
                    if in_bit == 1:  # Valid stop bit
                        self.done_reg = 1
                        self.out_byte_reg = self.shift_reg
                    self.current_state = self.STATE_IDLE

            # Prepare output dictionary for this stimulus
            output = {
                "done": format(self.done_reg, "b"),
                "out_byte": format(self.out_byte_reg, "08b"),
            }
            stimulus_outputs.append(output)

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
