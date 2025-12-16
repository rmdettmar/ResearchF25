import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers
        """
        self.counter = 0  # Counter to track cycles after reset
        self.shift_ena = 0  # Output signal
        self.state = "IDLE"  # FSM state

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process input signals and update state
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            reset = BinaryValue(stimulus["reset"]).integer

            # State machine logic
            if reset:
                self.counter = 0
                self.shift_ena = 1
                self.state = "COUNTING"
            elif self.state == "COUNTING":
                if self.counter < 3:
                    self.counter += 1
                    self.shift_ena = 1
                else:
                    self.counter = 0
                    self.shift_ena = 0
                    self.state = "IDLE"
            else:  # IDLE state
                self.shift_ena = 0

            # Convert output to binary string format
            shift_ena_bv = BinaryValue(value=self.shift_ena, n_bits=1)
            stimulus_outputs.append({"shift_ena": shift_ena_bv.binstr})

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
