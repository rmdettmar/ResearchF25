import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state variables
        self.pattern_reg = 0  # Shift register for pattern detection
        self.delay_reg = 0  # Store delay value
        self.cycle_counter = 0  # Count cycles during delay
        self.pattern_bits = 0  # Count bits received after pattern
        self.counting = 0  # Counting state
        self.done = 0  # Done state
        self.state = "SEARCH"  # Current state
        self.remaining = 0  # Remaining time

    def load(self, stimulus_dict: Dict[str, any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(stimulus["reset"], 2)
            data = int(stimulus["data"], 2)
            ack = int(stimulus["ack"], 2)

            if reset:
                self.pattern_reg = 0
                self.delay_reg = 0
                self.cycle_counter = 0
                self.pattern_bits = 0
                self.counting = 0
                self.done = 0
                self.state = "SEARCH"
                self.remaining = 0
            else:
                if self.state == "SEARCH":
                    self.pattern_reg = ((self.pattern_reg << 1) | data) & 0xF
                    if self.pattern_reg == 0b1101:
                        self.state = "DELAY"
                        self.pattern_bits = 0

                elif self.state == "DELAY":
                    self.delay_reg = (self.delay_reg << 1) | data
                    self.pattern_bits += 1
                    if self.pattern_bits == 4:
                        self.state = "COUNT"
                        self.counting = 1
                        self.cycle_counter = (self.delay_reg + 1) * 1000
                        self.remaining = self.delay_reg

                elif self.state == "COUNT":
                    if self.cycle_counter > 0:
                        self.cycle_counter -= 1
                        if self.cycle_counter % 1000 == 0:
                            self.remaining = (self.cycle_counter // 1000) - 1
                    if self.cycle_counter == 0:
                        self.state = "DONE"
                        self.counting = 0
                        self.done = 1

                elif self.state == "DONE":
                    if ack:
                        self.state = "SEARCH"
                        self.pattern_reg = 0
                        self.delay_reg = 0
                        self.done = 0
                        self.remaining = 0

            # Prepare outputs
            output_dict = {
                "count": format(self.remaining & 0xF, "04b"),
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
