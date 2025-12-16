import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # No internal state needed for this combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        # Process each set of inputs
        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            mode = BinaryValue(stimulus["mode"]).integer
            too_cold = BinaryValue(stimulus["too_cold"]).integer
            too_hot = BinaryValue(stimulus["too_hot"]).integer
            fan_on = BinaryValue(stimulus["fan_on"]).integer

            # Calculate outputs based on mode and conditions
            if mode:  # Heating mode
                heater = 1 if too_cold else 0
                aircon = 0
                fan = 1 if (heater or fan_on) else 0
            else:  # Cooling mode
                heater = 0
                aircon = 1 if too_hot else 0
                fan = 1 if (aircon or fan_on) else 0

            # Create output dictionary for this stimulus
            output = {
                "heater": BinaryValue(value=heater, n_bits=1).binstr,
                "aircon": BinaryValue(value=aircon, n_bits=1).binstr,
                "fan": BinaryValue(value=fan, n_bits=1).binstr,
            }
            stimulus_outputs.append(output)

        # Return formatted output dictionary
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
