import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for this combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to boolean values
            mode = BinaryValue(stimulus["mode"]).integer
            too_cold = BinaryValue(stimulus["too_cold"]).integer
            too_hot = BinaryValue(stimulus["too_hot"]).integer
            fan_on = BinaryValue(stimulus["fan_on"]).integer

            # Calculate outputs based on control logic
            heater = 1 if (mode == 1 and too_cold == 1) else 0
            aircon = 1 if (mode == 0 and too_hot == 1) else 0
            fan = 1 if (heater == 1 or aircon == 1 or fan_on == 1) else 0

            # Create output dictionary with binary string values
            output = {
                "heater": BinaryValue(value=heater, n_bits=1).binstr,
                "aircon": BinaryValue(value=aircon, n_bits=1).binstr,
                "fan": BinaryValue(value=fan, n_bits=1).binstr,
            }
            stimulus_outputs.append(output)

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
