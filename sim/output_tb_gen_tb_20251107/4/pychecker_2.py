
import json
from typing import Dict, List, Union


from typing import Dict, List, Any

class GoldenDUT:
    def __init__(self):
        # Initialization not needed for combinational logic without state
        pass

    def load(self, stimulus_dict: Dict[str, Any]) -> List[Dict[str, str]]:
        # Extract the binary string representing the 32-bit input
        input_bin_str = stimulus_dict['in']
        assert len(input_bin_str) == 32, "Input must be 32 bits."

        # Split the input into bytes
        byte0 = input_bin_str[0:8]
        byte1 = input_bin_str[8:16]
        byte2 = input_bin_str[16:24]
        byte3 = input_bin_str[24:32]

        # Reverse the byte order
        reversed_bytes = byte3 + byte2 + byte1 + byte0

        return [{'out': reversed_bytes}]
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


