import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers
        This is a combinational logic module, so no state storage needed
        """
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs according to RTL specification
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to BinaryValue objects
            cpu_overheated = BinaryValue(stimulus["cpu_overheated"]).integer
            arrived = BinaryValue(stimulus["arrived"]).integer
            gas_tank_empty = BinaryValue(stimulus["gas_tank_empty"]).integer

            # Implement the corrected logic
            shut_off_computer = 1 if cpu_overheated else 0
            keep_driving = 1 if (not arrived and not gas_tank_empty) else 0

            # Convert outputs to binary strings
            out_shut_off = BinaryValue(value=shut_off_computer, n_bits=1).binstr
            out_keep_driving = BinaryValue(value=keep_driving, n_bits=1).binstr

            # Add outputs to results
            stimulus_outputs.append(
                {"shut_off_computer": out_shut_off, "keep_driving": out_keep_driving}
            )

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
