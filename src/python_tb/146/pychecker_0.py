import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state registers to represent low water state
        """
        self.prev_sensors = 0  # Previous sensor state
        self.fr3 = 1  # Flow rate controls
        self.fr2 = 1
        self.fr1 = 1
        self.dfr = 1  # Supplemental flow

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to proper format
            reset = BinaryValue(stimulus["reset"]).integer
            sensors = BinaryValue(stimulus["s"]).integer

            if reset:
                # Reset to low water state
                self.fr3 = 1
                self.fr2 = 1
                self.fr1 = 1
                self.dfr = 1
                self.prev_sensors = 0
            else:
                # Determine if water level is rising
                rising = sensors > self.prev_sensors

                # Update flow rates based on sensor readings
                if sensors & 0b100:  # s[3] is high
                    self.fr3 = 0
                    self.fr2 = 0
                    self.fr1 = 0
                elif sensors & 0b010:  # s[2] is high
                    self.fr3 = 0
                    self.fr2 = 0
                    self.fr1 = 1
                elif sensors & 0b001:  # s[1] is high
                    self.fr3 = 0
                    self.fr2 = 1
                    self.fr1 = 1
                else:  # No sensors active
                    self.fr3 = 1
                    self.fr2 = 1
                    self.fr1 = 1

                # Set supplemental flow if level is rising
                self.dfr = 1 if rising else 0

                # Store current sensor state for next cycle
                self.prev_sensors = sensors

            # Create output dictionary for this stimulus
            output = {
                "fr3": format(self.fr3, "b"),
                "fr2": format(self.fr2, "b"),
                "fr1": format(self.fr1, "b"),
                "dfr": format(self.dfr, "b"),
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
