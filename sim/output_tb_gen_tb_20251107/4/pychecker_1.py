
import json
from typing import Dict, List, Union


class GoldenDUT:

    def __init__(self):
        pass  # No internal state is required for this purely combinational logic

    def load(self, stimulus_dict: Dict[str, any]) -> List[Dict[str, str]]:
        # Extract the input binary string
        in_str = stimulus_dict['in']
        assert len(in_str) == 32, "Input must be 32 bits."

        # Reverse the byte order
        # in[31:24], in[23:16], in[15:8], in[7:0]
        out = (
            in_str[24:32] +  # in[7:0]
            in_str[16:24] +  # in[15:8]
            in_str[8:16] +   # in[23:16]
            in_str[0:8]     # in[31:24]
        )

        # Return the output in the expected format
        return {"out": out}
def check_output(stimulus):

    dut = GoldenDUT()


        

    return dut.load(stimulus)

if __name__ == "__main__":

    with open("stimulus.json", "r") as f:
        stimulus_data = json.load(f)

    stimulus_list = []
    for stimulus in stimulus_data:
        stimulus_list.append(stimulus['input variable'])

    tb_outputs = []
    for stimulus in stimulus_list:
        scenario_outputs=[]
        for cycle in stimulus:

            outputs = check_output(cycle)
            scenario_outputs.append(outputs)
        tb_outputs.append(scenario_outputs)


    

    print(json.dumps(tb_outputs, indent=2))


