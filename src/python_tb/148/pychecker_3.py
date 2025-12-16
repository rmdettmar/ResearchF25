import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # FSM states
        self.IDLE = 0
        self.RECEIVING = 1
        self.STOP_BIT = 2

        # Initialize state registers
        self.state = self.IDLE
        self.bit_counter = 0
        self.data_reg = 0
        self.done_reg = 0
        self.out_byte_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to proper format
            reset = int(BinaryValue(stimulus["reset"]).integer)
            in_bit = int(BinaryValue(stimulus["in"]).integer)

            # Process reset
            if reset:
                self.state = self.IDLE
                self.bit_counter = 0
                self.data_reg = 0
                self.done_reg = 0
                self.out_byte_reg = 0
            else:
                # FSM state machine
                if self.state == self.IDLE:
                    self.done_reg = 0
                    if in_bit == 0:  # Start bit detected
                        self.state = self.RECEIVING
                        self.bit_counter = 0
                        self.data_reg = 0

                elif self.state == self.RECEIVING:
                    self.data_reg = self.data_reg | (in_bit << self.bit_counter)
                    self.bit_counter += 1
                    if self.bit_counter == 8:
                        self.state = self.STOP_BIT

                elif self.state == self.STOP_BIT:
                    if in_bit == 1:  # Valid stop bit
                        self.done_reg = 1
                        self.out_byte_reg = self.data_reg
                        self.state = self.IDLE
                    else:  # Invalid stop bit
                        self.done_reg = 0
                        if in_bit == 0:  # New start bit
                            self.state = self.RECEIVING
                            self.bit_counter = 0
                            self.data_reg = 0

            # Prepare output dictionary
            output = {
                "done": str(self.done_reg),
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
