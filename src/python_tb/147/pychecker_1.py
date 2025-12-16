import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # FSM states
        self.STATE_IDLE = 0
        self.STATE_DATA = 1
        self.STATE_STOP = 2
        self.STATE_ERROR = 3

        # Initialize state variables
        self.current_state = self.STATE_IDLE
        self.bit_counter = 0
        self.done_reg = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to values
            reset = int(stimulus["reset"], 2)
            in_bit = int(stimulus["in"], 2)

            # Handle reset
            if reset:
                self.current_state = self.STATE_IDLE
                self.bit_counter = 0
                self.done_reg = 0
            else:
                # FSM state transitions
                if self.current_state == self.STATE_IDLE:
                    if in_bit == 0:  # Start bit detected
                        self.current_state = self.STATE_DATA
                        self.bit_counter = 0
                        self.done_reg = 0

                elif self.current_state == self.STATE_DATA:
                    self.bit_counter += 1
                    if self.bit_counter == 8:  # Received all data bits
                        self.current_state = self.STATE_STOP
                        self.bit_counter = 0

                elif self.current_state == self.STATE_STOP:
                    if in_bit == 1:  # Valid stop bit
                        self.done_reg = 1
                        self.current_state = self.STATE_IDLE
                    else:  # Invalid stop bit
                        self.current_state = self.STATE_ERROR
                        self.done_reg = 0

                elif self.current_state == self.STATE_ERROR:
                    if in_bit == 1:  # Found stop bit
                        self.current_state = self.STATE_IDLE

            # Append output for this stimulus
            stimulus_outputs.append({"done": format(self.done_reg, "b")})

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
