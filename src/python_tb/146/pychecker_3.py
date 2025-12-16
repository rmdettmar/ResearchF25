import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state registers
        self.prev_sensors = 0  # Previous sensor state
        self.fr3 = 0
        self.fr2 = 0
        self.fr1 = 0
        self.dfr = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            reset = BinaryValue(stimulus["reset"]).integer
            s = BinaryValue(stimulus["s"]).integer

            if reset:
                # Reset condition - low water level state
                self.fr3 = 1
                self.fr2 = 1
                self.fr1 = 1
                self.dfr = 1
                self.prev_sensors = 0
            else:
                # Check if water level is rising
                rising = s > self.prev_sensors

                # Update flow rates based on sensor readings
                if s & 0b100:  # Above s[3]
                    self.fr3 = 0
                    self.fr2 = 0
                    self.fr1 = 0
                elif s & 0b110 == 0b110:  # Between s[3] and s[2]
                    self.fr3 = 0
                    self.fr2 = 0
                    self.fr1 = 1
                elif s & 0b001:  # Between s[2] and s[1]
                    self.fr3 = 0
                    self.fr2 = 1
                    self.fr1 = 1
                else:  # Below s[1]
                    self.fr3 = 1
                    self.fr2 = 1
                    self.fr1 = 1

                # Set dfr if water level is rising
                self.dfr = 1 if rising else 0

                # Update previous sensor state
                self.prev_sensors = s

            # Create output dictionary for this stimulus
            output = {
                "fr3": bin(self.fr3)[2:],
                "fr2": bin(self.fr2)[2:],
                "fr1": bin(self.fr1)[2:],
                "dfr": bin(self.dfr)[2:],
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
