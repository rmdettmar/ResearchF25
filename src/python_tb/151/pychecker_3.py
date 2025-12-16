import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        DETECT = 0  # Detecting pattern 1101
        SHIFT = 1  # Shifting in 4 bits
        COUNT = 2  # Waiting for done_counting
        DONE = 3  # Waiting for ack

    def __init__(self):
        self.current_state = self.State.DETECT
        self.pattern_reg = 0  # Stores last 4 bits
        self.shift_count = 0  # Count shifts during SHIFT state
        self.shift_ena = 0
        self.counting = 0
        self.done = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to appropriate types
            reset = int(stimulus["reset"], 2)
            data = int(stimulus["data"], 2)
            done_counting = int(stimulus["done_counting"], 2)
            ack = int(stimulus["ack"], 2)

            # Handle reset
            if reset:
                self.current_state = self.State.DETECT
                self.pattern_reg = 0
                self.shift_count = 0
                self.shift_ena = 0
                self.counting = 0
                self.done = 0
            else:
                # State machine logic
                if self.current_state == self.State.DETECT:
                    self.shift_ena = 0
                    self.counting = 0
                    self.done = 0
                    # Shift in new bit and check pattern
                    self.pattern_reg = ((self.pattern_reg << 1) | data) & 0xF
                    if self.pattern_reg == 0b1101:
                        self.current_state = self.State.SHIFT
                        self.shift_count = 0
                        self.shift_ena = 1

                elif self.current_state == self.State.SHIFT:
                    if self.shift_count < 3:
                        self.shift_count += 1
                        self.shift_ena = 1
                    else:
                        self.shift_ena = 0
                        self.current_state = self.State.COUNT
                        self.counting = 1

                elif self.current_state == self.State.COUNT:
                    if done_counting:
                        self.counting = 0
                        self.current_state = self.State.DONE
                        self.done = 1

                elif self.current_state == self.State.DONE:
                    if ack:
                        self.done = 0
                        self.current_state = self.State.DETECT
                        self.pattern_reg = 0

            # Create output dictionary for this cycle
            outputs = {
                "shift_ena": format(self.shift_ena, "b"),
                "counting": format(self.counting, "b"),
                "done": format(self.done, "b"),
            }
            output_list.append(outputs)

        return {"scenario": stimulus_dict["scenario"], "output variable": output_list}


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
