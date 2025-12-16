import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        IDLE = 0  # Looking for pattern
        CAPTURE_DELAY = 1  # Capturing delay value
        COUNTING = 2  # Counting down
        DONE = 3  # Waiting for ack

    def __init__(self):
        self.state = self.State.IDLE
        self.pattern_reg = 0
        self.pattern_count = 0
        self.delay_reg = 0
        self.delay_count = 0
        self.counter = 0
        self.time_remaining = 0
        self.counting = 0
        self.done = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to proper format
            reset = int(stimulus["reset"], 2)
            data = int(stimulus["data"], 2)
            ack = int(stimulus["ack"], 2)

            # Reset logic
            if reset:
                self.state = self.State.IDLE
                self.pattern_reg = 0
                self.pattern_count = 0
                self.delay_reg = 0
                self.delay_count = 0
                self.counter = 0
                self.time_remaining = 0
                self.counting = 0
                self.done = 0
            else:
                # State machine logic
                if self.state == self.State.IDLE:
                    self.pattern_reg = ((self.pattern_reg << 1) | data) & 0xF
                    if self.pattern_reg == 0b1101:
                        self.state = self.State.CAPTURE_DELAY
                        self.delay_count = 0

                elif self.state == self.State.CAPTURE_DELAY:
                    self.delay_reg = (self.delay_reg << 1) | data
                    self.delay_count += 1
                    if self.delay_count == 4:
                        self.state = self.State.COUNTING
                        self.counter = (self.delay_reg + 1) * 1000
                        self.time_remaining = self.delay_reg
                        self.counting = 1

                elif self.state == self.State.COUNTING:
                    self.counter -= 1
                    if self.counter % 1000 == 0 and self.counter > 0:
                        self.time_remaining -= 1
                    if self.counter == 0:
                        self.state = self.State.DONE
                        self.counting = 0
                        self.done = 1

                elif self.state == self.State.DONE:
                    if ack:
                        self.state = self.State.IDLE
                        self.pattern_reg = 0
                        self.done = 0

            # Prepare outputs
            count_bv = BinaryValue(value=self.time_remaining, n_bits=4)
            counting_bv = BinaryValue(value=self.counting, n_bits=1)
            done_bv = BinaryValue(value=self.done, n_bits=1)

            output_dict = {
                "count": count_bv.binstr,
                "counting": counting_bv.binstr,
                "done": done_bv.binstr,
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
