
import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        pass  # No internal state needed for this combinational operation

    def load(self, stimulus_dict):
        input_str = stimulus_dict['in']  # 32-bit input
        assert len(input_str) == 32, "Input must be 32 bits long."

        # Split input into bytes and reverse the order
        bytes_list = [input_str[i:i+8] for i in range(0, 32, 8)]
        reversed_bytes_list = list(reversed(bytes_list))

        # Join the reversed bytes to form the output
        output_str = ''.join(reversed_bytes_list)

        # Return the output as a dictionary
        return {"out": output_str}
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


