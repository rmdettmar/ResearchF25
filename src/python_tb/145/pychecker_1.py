import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # State encoding
        self.SEARCH = 0
        self.READ_DELAY = 1
        self.COUNTING = 2
        self.WAIT_ACK = 3

        # Initialize state registers
        self.current_state = self.SEARCH
        self.shift_reg = 0
        self.delay_reg = 0
        self.counter = 0
        self.bits_received = 0
        self.remaining_time = 0

        # Output registers
        self.counting = 0
        self.done = 0
        self.count = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(BinaryValue(stimulus["reset"]).value)
            data = int(BinaryValue(stimulus["data"]).value)
            ack = int(BinaryValue(stimulus["ack"]).value)

            if reset:
                self.current_state = self.SEARCH
                self.shift_reg = 0
                self.delay_reg = 0
                self.counter = 0
                self.bits_received = 0
                self.counting = 0
                self.done = 0
                self.count = 0
            else:
                if self.current_state == self.SEARCH:
                    self.shift_reg = ((self.shift_reg << 1) | data) & 0xF
                    if self.shift_reg == 0b1101:
                        self.current_state = self.READ_DELAY
                        self.bits_received = 0
                        self.shift_reg = 0

                elif self.current_state == self.READ_DELAY:
                    self.shift_reg = (self.shift_reg << 1) | data
                    self.bits_received += 1
                    if self.bits_received == 4:
                        self.delay_reg = self.shift_reg
                        self.current_state = self.COUNTING
                        self.counter = (self.delay_reg + 1) * 1000
                        self.counting = 1
                        self.remaining_time = self.delay_reg

                elif self.current_state == self.COUNTING:
                    if self.counter > 0:
                        self.counter -= 1
                        if self.counter % 1000 == 0:
                            self.remaining_time = (self.counter // 1000) - 1
                    if self.counter == 0:
                        self.current_state = self.WAIT_ACK
                        self.counting = 0
                        self.done = 1

                elif self.current_state == self.WAIT_ACK:
                    if ack:
                        self.current_state = self.SEARCH
                        self.done = 0
                        self.shift_reg = 0

            # Prepare outputs
            output_dict = {
                "counting": BinaryValue(value=self.counting, n_bits=1).binstr,
                "done": BinaryValue(value=self.done, n_bits=1).binstr,
                "count": BinaryValue(
                    value=self.remaining_time if self.counting else 0, n_bits=4
                ).binstr,
            }
            stimulus_outputs.append(output_dict)

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
