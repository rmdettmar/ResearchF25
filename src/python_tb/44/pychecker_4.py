import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state. For this combinational logic,
        no state storage is needed.
        """
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and generate outputs according to thermostat logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert string inputs to boolean
            mode = int(stimulus["mode"])
            too_cold = int(stimulus["too_cold"])
            too_hot = int(stimulus["too_hot"])
            fan_on = int(stimulus["fan_on"])

            # Compute outputs
            heater = 1 if (mode and too_cold) else 0
            aircon = 1 if (not mode and too_hot) else 0
            fan = 1 if (heater or aircon or fan_on) else 0

            # Create output dictionary for this stimulus
            output = {"heater": str(heater), "aircon": str(aircon), "fan": str(fan)}
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
