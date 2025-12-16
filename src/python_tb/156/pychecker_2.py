import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize 16-bit counter (4 BCD digits)
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []
        ena_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(stimulus["reset"], 2)

            if reset:
                self.q_reg = 0
            else:
                # Extract current digits
                digit0 = self.q_reg & 0xF
                digit1 = (self.q_reg >> 4) & 0xF
                digit2 = (self.q_reg >> 8) & 0xF
                digit3 = (self.q_reg >> 12) & 0xF

                # Calculate enables
                ena1 = 1 if digit0 == 9 else 0
                ena2 = 1 if digit1 == 9 and ena1 else 0
                ena3 = 1 if digit2 == 9 and ena2 else 0

                # Update digits
                digit0 = (digit0 + 1) % 10
                if ena1:
                    digit1 = (digit1 + 1) % 10
                if ena2:
                    digit2 = (digit2 + 1) % 10
                if ena3:
                    digit3 = (digit3 + 1) % 10

                # Combine digits back into q_reg
                self.q_reg = (digit3 << 12) | (digit2 << 8) | (digit1 << 4) | digit0

            # Format output
            q_str = format(self.q_reg, "016b")
            ena_str = format((ena3 << 2) | (ena2 << 1) | ena1, "03b")

            stimulus_outputs.append({"q": q_str})
            ena_outputs.append({"ena": ena_str})

        output_dict = {
            "scenario": stimulus_dict["scenario"],
            "output variable": [
                {**q_out, **e_out}
                for q_out, e_out in zip(stimulus_outputs, ena_outputs)
            ],
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
