import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        SEARCH = 0
        SHIFT_DELAY = 1
        COUNTING = 2
        DONE = 3

    def __init__(self):
        self.state = self.State.SEARCH
        self.pattern_reg = 0  # Stores last 4 bits for pattern detection
        self.delay_reg = 0  # Stores delay value
        self.counter = 0  # Main counter
        self.bit_count = 0  # Counts bits received in SHIFT_DELAY
        self.remaining = 0  # Remaining time for count output
        self.counting = 0  # counting output
        self.done = 0  # done output
        self.count = 0  # count output

    def load(self, stimulus_dict: Dict[str, Any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(BinaryValue(stimulus["reset"]).value)
            data = int(BinaryValue(stimulus["data"]).value)
            ack = int(BinaryValue(stimulus["ack"]).value)

            if reset:
                self.state = self.State.SEARCH
                self.pattern_reg = 0
                self.delay_reg = 0
                self.counter = 0
                self.bit_count = 0
                self.remaining = 0
                self.counting = 0
                self.done = 0
                self.count = 0
            else:
                if self.state == self.State.SEARCH:
                    self.pattern_reg = ((self.pattern_reg << 1) | data) & 0xF
                    if self.pattern_reg == 0b1101:
                        self.state = self.State.SHIFT_DELAY
                        self.bit_count = 0

                elif self.state == self.State.SHIFT_DELAY:
                    self.delay_reg = (self.delay_reg << 1) | data
                    self.bit_count += 1
                    if self.bit_count == 4:
                        self.state = self.State.COUNTING
                        self.counter = (self.delay_reg + 1) * 1000
                        self.remaining = self.delay_reg
                        self.counting = 1

                elif self.state == self.State.COUNTING:
                    self.counter -= 1
                    if self.counter % 1000 == 0 and self.counter > 0:
                        self.remaining -= 1
                    if self.counter == 0:
                        self.state = self.State.DONE
                        self.counting = 0
                        self.done = 1

                elif self.state == self.State.DONE:
                    if ack:
                        self.state = self.State.SEARCH
                        self.pattern_reg = 0
                        self.done = 0
                        self.remaining = 0

            # Prepare outputs
            output_dict = {
                "count": format(self.remaining, "04b"),
                "counting": format(self.counting, "01b"),
                "done": format(self.done, "01b"),
            }
            outputs.append(output_dict)

        return {"scenario": stimulus_dict["scenario"], "output variable": outputs}


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
