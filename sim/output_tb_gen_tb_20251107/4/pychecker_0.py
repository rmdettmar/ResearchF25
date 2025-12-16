
import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        pass

    def load(self, stimulus_dict):
        input_bin = stimulus_dict['in']
        assert len(input_bin) == 32, "Input must be 32 bits."
        
        # Divide the input into 4 bytes and reverse the order
        byte0 = input_bin[0:8]
        byte1 = input_bin[8:16]
        byte2 = input_bin[16:24]
        byte3 = input_bin[24:32]
        
        # Reverse byte order
        reversed_bin = byte3 + byte2 + byte1 + byte0

        return {"out": reversed_bin}
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


