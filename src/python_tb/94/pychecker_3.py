import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """
        Initialize state variables:
        - byte_count: tracks position in 3-byte message (0-2)
        - done_reg: output register for done signal
        """
        self.byte_count = 0
        self.done_reg = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract input signals
            in_byte = int(stimulus["in"], 2)
            reset = int(stimulus["reset"], 2)

            # Handle reset
            if reset:
                self.byte_count = 0
                self.done_reg = 0
            else:
                # Check if this is potentially byte 1 (in[3] = 1)
                is_byte1 = (in_byte >> 3) & 1

                if self.byte_count == 0:
                    # Looking for start of message
                    if is_byte1:
                        self.byte_count = 1
                    self.done_reg = 0
                elif self.byte_count == 1:
                    # Received byte 2
                    self.byte_count = 2
                    self.done_reg = 0
                elif self.byte_count == 2:
                    # Received byte 3, complete message
                    self.byte_count = 0
                    self.done_reg = 1
                    if (
                        is_byte1
                    ):  # If byte 3 has in[3]=1, it's also byte 1 of next message
                        self.byte_count = 1

            # Add current output to results
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
