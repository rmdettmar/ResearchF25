import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class State(Enum):
    IDLE = 0
    COLLECTING_DELAY = 1
    COUNTING = 2
    DONE = 3


class GoldenDUT:
    def __init__(self):
        self.state = State.IDLE
        self.pattern_reg = 0
        self.delay_reg = 0
        self.delay_count = 0
        self.cycle_counter = 0
        self.remaining_time = 0
        self.counting = 0
        self.done = 0
        self.count = 0
        self.bits_collected = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(BinaryValue(stimulus["reset"]).value)
            data = int(BinaryValue(stimulus["data"]).value)
            ack = int(BinaryValue(stimulus["ack"]).value)

            if reset:
                self.state = State.IDLE
                self.pattern_reg = 0
                self.delay_reg = 0
                self.delay_count = 0
                self.cycle_counter = 0
                self.remaining_time = 0
                self.counting = 0
                self.done = 0
                self.count = 0
                self.bits_collected = 0
            else:
                if self.state == State.IDLE:
                    self.pattern_reg = ((self.pattern_reg << 1) | data) & 0xF
                    self.counting = 0
                    self.done = 0
                    if self.pattern_reg == 0b1101:
                        self.state = State.COLLECTING_DELAY
                        self.bits_collected = 0

                elif self.state == State.COLLECTING_DELAY:
                    self.delay_reg = (self.delay_reg << 1) | data
                    self.bits_collected += 1
                    if self.bits_collected == 4:
                        self.state = State.COUNTING
                        self.counting = 1
                        self.cycle_counter = 0
                        self.remaining_time = self.delay_reg
                        self.count = self.delay_reg

                elif self.state == State.COUNTING:
                    self.cycle_counter += 1
                    if self.cycle_counter >= 1000:
                        self.cycle_counter = 0
                        if self.remaining_time > 0:
                            self.remaining_time -= 1
                            self.count = self.remaining_time
                        else:
                            self.state = State.DONE
                            self.counting = 0
                            self.done = 1

                elif self.state == State.DONE:
                    if ack:
                        self.state = State.IDLE
                        self.pattern_reg = 0
                        self.done = 0

            # Prepare output dictionary for this stimulus
            output = {
                "count": format(self.count & 0xF, "04b"),
                "counting": format(self.counting & 0x1, "01b"),
                "done": format(self.done & 0x1, "01b"),
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
