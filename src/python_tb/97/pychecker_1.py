import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the FSM state to 000
        """
        self.state = 0  # 3-bit state register

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Update FSM state and output based on inputs
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(BinaryValue(stimulus["reset"]).value)
            x = int(BinaryValue(stimulus["x"]).value)

            # Handle reset
            if reset:
                self.state = 0
            else:
                # State transition logic
                if self.state == 0b000:
                    self.state = 0b001 if x else 0b000
                elif self.state == 0b001:
                    self.state = 0b100 if x else 0b001
                elif self.state == 0b010:
                    self.state = 0b001 if x else 0b010
                elif self.state == 0b011:
                    self.state = 0b010 if x else 0b001
                elif self.state == 0b100:
                    self.state = 0b100 if x else 0b011

            # Output logic
            z = 1 if self.state in [0b011, 0b100] else 0

            # Format output as binary string
            z_bv = BinaryValue(value=z, n_bits=1)
            stimulus_outputs.append({"z": z_bv.binstr})

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
