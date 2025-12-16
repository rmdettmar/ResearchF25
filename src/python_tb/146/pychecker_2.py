import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers
        """
        self.prev_sensors = 0  # Previous sensor state
        self.fr3_reg = 0
        self.fr2_reg = 0
        self.fr1_reg = 0
        self.dfr_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            reset = BinaryValue(stimulus["reset"]).integer
            sensors = BinaryValue(stimulus["s"]).integer

            if reset:
                # Reset condition - all flow rates on (low water level)
                self.fr3_reg = 1
                self.fr2_reg = 1
                self.fr1_reg = 1
                self.dfr_reg = 1
                self.prev_sensors = 0
            else:
                # Check if water level is rising
                rising = sensors > self.prev_sensors

                # Update flow rates based on sensor readings
                if sensors & 0b100:  # Above s[3]
                    self.fr3_reg = 0
                    self.fr2_reg = 0
                    self.fr1_reg = 0
                    self.dfr_reg = 0
                elif sensors & 0b010:  # Between s[3] and s[2]
                    self.fr3_reg = 0
                    self.fr2_reg = 0
                    self.fr1_reg = 1
                    self.dfr_reg = rising
                elif sensors & 0b001:  # Between s[2] and s[1]
                    self.fr3_reg = 0
                    self.fr2_reg = 1
                    self.fr1_reg = 1
                    self.dfr_reg = rising
                else:  # Below s[1]
                    self.fr3_reg = 1
                    self.fr2_reg = 1
                    self.fr1_reg = 1
                    self.dfr_reg = 1

                # Update previous sensor state
                self.prev_sensors = sensors

            # Prepare output dictionary
            output = {
                "fr3": BinaryValue(value=self.fr3_reg, n_bits=1).binstr,
                "fr2": BinaryValue(value=self.fr2_reg, n_bits=1).binstr,
                "fr1": BinaryValue(value=self.fr1_reg, n_bits=1).binstr,
                "dfr": BinaryValue(value=self.dfr_reg, n_bits=1).binstr,
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
