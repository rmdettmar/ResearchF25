import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize FSM state and output registers
        """
        self.current_state = 0  # FSM state: 0-4
        self.start_shifting = 0  # Output signal

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process input signals and update FSM state
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            reset_bv = BinaryValue(stimulus["reset"])
            data_bv = BinaryValue(stimulus["data"])

            # Get integer values
            reset = reset_bv.integer
            data = data_bv.integer

            # Update FSM state
            if reset:
                self.current_state = 0
                self.start_shifting = 0
            else:
                if self.current_state == 0:
                    if data == 1:
                        self.current_state = 1
                elif self.current_state == 1:
                    if data == 1:
                        self.current_state = 2
                    else:
                        self.current_state = 0
                elif self.current_state == 2:
                    if data == 0:
                        self.current_state = 3
                    else:
                        self.current_state = 2
                elif self.current_state == 3:
                    if data == 1:
                        self.current_state = 4
                    else:
                        self.current_state = 0
                elif self.current_state == 4:
                    self.current_state = 4  # Stay in this state

            # Update output
            self.start_shifting = 1 if self.current_state == 4 else 0

            # Convert output to binary string
            out_bv = BinaryValue(value=self.start_shifting, n_bits=1)
            stimulus_outputs.append({"start_shifting": out_bv.binstr})

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
