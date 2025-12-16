import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize the flip-flops to 0
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            reset_bv = BinaryValue(stimulus["reset"])
            d_bv = BinaryValue(stimulus["d"])

            # Process reset condition
            if reset_bv.integer == 1:
                self.q_reg = 0x34  # Reset to 0x34 as specified
            else:
                # On negative edge, capture input d
                self.q_reg = d_bv.integer & 0xFF  # Ensure 8-bit value

            # Create output dictionary entry
            stimulus_outputs.append({"q": format(self.q_reg, "08b")})

        # Return formatted output dictionary
        output_dict = {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }

        return output_dict


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
