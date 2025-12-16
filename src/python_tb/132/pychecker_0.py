import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state variables
        """
        self.shut_off_computer = BinaryValue("0")
        self.keep_driving = BinaryValue("0")

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and generate outputs
        """
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            cpu_overheated = BinaryValue(stimulus["cpu_overheated"])
            arrived = BinaryValue(stimulus["arrived"])
            gas_tank_empty = BinaryValue(stimulus["gas_tank_empty"])

            # Implement the logic for shut_off_computer
            self.shut_off_computer = BinaryValue(value=cpu_overheated.integer)

            # Implement the logic for keep_driving
            # keep_driving = ~arrived & ~gas_tank_empty
            self.keep_driving = BinaryValue(
                value=((not arrived.integer) and (not gas_tank_empty.integer))
            )

            # Add outputs to list
            output_list.append(
                {
                    "shut_off_computer": self.shut_off_computer.binstr,
                    "keep_driving": self.keep_driving.binstr,
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
