import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 32-bit register to 1 (default state)
        self.q_reg = 1

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to proper format
            reset = BinaryValue(stimulus["reset"]).integer

            if reset:
                # Synchronous reset to 32'h1
                self.q_reg = 1
            else:
                # Get the MSB (bit 31)
                msb = (self.q_reg >> 31) & 1

                # Create new value by shifting right
                new_value = self.q_reg >> 1

                # XOR with tap positions if MSB is 1
                if msb:
                    # Tap at bit 32 (MSB) is handled by the shift
                    # XOR with bit 22
                    new_value ^= 1 << 21
                    # XOR with bit 2
                    new_value ^= 1 << 1
                    # XOR with bit 1
                    new_value ^= 1 << 0

                # Update register
                self.q_reg = new_value & 0xFFFFFFFF

            # Format output as binary string
            q_bin = BinaryValue(value=self.q_reg, n_bits=32)
            stimulus_outputs.append({"q": q_bin.binstr})

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
