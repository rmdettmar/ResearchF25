
import json
from typing import Dict, List, Union

class GoldenDUT:
    def __init__(self):
        pass

    def load(self, stimulus_dict):
        input_str = stimulus_dict['in']  # 32-bit input
        assert len(input_str) == 32, 'Input must be 32 bits long.'

        # Rearrange the input bytes as specified
        byte0 = input_str[0:8]
        byte1 = input_str[8:16]
        byte2 = input_str[16:24]
        byte3 = input_str[24:32]

        # Form the output by rearranging the bytes
        output_str = byte3 + byte2 + byte1 + byte0

        # Return the output as a dictionary
        return {'out': output_str}
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


