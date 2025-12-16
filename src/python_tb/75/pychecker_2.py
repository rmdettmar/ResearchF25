import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # State encoding
        self.IDLE = 0
        self.GOT_1 = 1
        self.GOT_11 = 2
        self.GOT_110 = 3
        self.FOUND = 4

        # Initialize state register
        self.current_state = self.IDLE
        self.start_shifting = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert string inputs to BinaryValue
            reset = BinaryValue(stimulus["reset"]).integer
            data = BinaryValue(stimulus["data"]).integer

            # State transition logic
            if reset:
                next_state = self.IDLE
            else:
                if self.current_state == self.IDLE:
                    next_state = self.GOT_1 if data == 1 else self.IDLE
                elif self.current_state == self.GOT_1:
                    next_state = self.GOT_11 if data == 1 else self.IDLE
                elif self.current_state == self.GOT_11:
                    next_state = self.GOT_110 if data == 0 else self.GOT_11
                elif self.current_state == self.GOT_110:
                    next_state = self.FOUND if data == 1 else self.IDLE
                else:  # FOUND state
                    next_state = self.FOUND

            # Update state
            self.current_state = next_state

            # Output logic
            self.start_shifting = 1 if self.current_state == self.FOUND else 0

            # Convert output to BinaryValue string format
            out_bv = BinaryValue(value=self.start_shifting, n_bits=1)
            stimulus_outputs.append({"start_shifting": out_bv.binstr})

        output_dict = {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }

        return output_dict


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
