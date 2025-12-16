import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """
        Initialize the internal state register q
        """
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Update the flip-flop state based on input stimulus
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get input d value
            d = int(stimulus["d"], 2)

            # Update state - D flip-flop copies d to q on clock edge
            self.q_reg = d

            # Append output to results
            stimulus_outputs.append({"q": format(self.q_reg, "b")})

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
