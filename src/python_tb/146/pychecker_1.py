import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize internal state registers"""
        self.prev_sensors = 0  # Previous sensor state
        self.fr3 = 0
        self.fr2 = 0
        self.fr1 = 0
        self.dfr = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to proper format
            reset = int(stimulus["reset"], 2)
            sensors = int(stimulus["s"], 2)

            if reset:
                # Reset condition - low water level state
                self.fr3 = 1
                self.fr2 = 1
                self.fr1 = 1
                self.dfr = 1
                self.prev_sensors = 0
            else:
                # Determine flow rates based on sensor readings
                if sensors == 0b111:  # Above s[3]
                    self.fr3 = 0
                    self.fr2 = 0
                    self.fr1 = 0
                elif sensors == 0b011:  # Between s[3] and s[2]
                    self.fr3 = 0
                    self.fr2 = 0
                    self.fr1 = 1
                elif sensors == 0b001:  # Between s[2] and s[1]
                    self.fr3 = 0
                    self.fr2 = 1
                    self.fr1 = 1
                else:  # Below s[1]
                    self.fr3 = 1
                    self.fr2 = 1
                    self.fr1 = 1

                # Determine supplemental flow
                self.dfr = 1 if sensors > self.prev_sensors else 0
                self.prev_sensors = sensors

            # Format outputs as binary strings
            output_dict = {
                "fr3": format(self.fr3, "b"),
                "fr2": format(self.fr2, "b"),
                "fr1": format(self.fr1, "b"),
                "dfr": format(self.dfr, "b"),
            }
            stimulus_outputs.append(output_dict)

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
