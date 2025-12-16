import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers
        """
        self.shut_off_computer = 0
        self.keep_driving = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs according to RTL logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            cpu_overheated = BinaryValue(stimulus["cpu_overheated"]).integer
            arrived = BinaryValue(stimulus["arrived"]).integer
            gas_tank_empty = BinaryValue(stimulus["gas_tank_empty"]).integer

            # Implement the corrected logic for shut_off_computer
            self.shut_off_computer = 1 if cpu_overheated else 0

            # Implement the corrected logic for keep_driving
            self.keep_driving = 0 if arrived else (not gas_tank_empty)

            # Convert outputs to binary strings
            out_dict = {
                "shut_off_computer": BinaryValue(
                    value=self.shut_off_computer, n_bits=1
                ).binstr,
                "keep_driving": BinaryValue(value=self.keep_driving, n_bits=1).binstr,
            }
            stimulus_outputs.append(out_dict)

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
