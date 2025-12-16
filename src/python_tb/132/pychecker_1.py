import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize outputs
        self.shut_off_computer = 0
        self.keep_driving = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            cpu_overheated = BinaryValue(stimulus["cpu_overheated"]).integer
            arrived = BinaryValue(stimulus["arrived"]).integer
            gas_tank_empty = BinaryValue(stimulus["gas_tank_empty"]).integer

            # Logic for shut_off_computer
            self.shut_off_computer = 1 if cpu_overheated else 0

            # Logic for keep_driving
            self.keep_driving = 0 if arrived else (not gas_tank_empty)

            # Convert outputs to binary strings
            shut_off_computer_bv = BinaryValue(value=self.shut_off_computer, n_bits=1)
            keep_driving_bv = BinaryValue(value=self.keep_driving, n_bits=1)

            # Add outputs to list
            output_list.append(
                {
                    "shut_off_computer": shut_off_computer_bv.binstr,
                    "keep_driving": keep_driving_bv.binstr,
                }
            )

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
