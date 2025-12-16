
import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        a = stimulus_dict['a']  # binary string
        b = stimulus_dict['b']  # binary string
        c = stimulus_dict['c']  # binary string
        
        # For each input set, compute the output
        outputs = []
        for i in range(len(a)):
            a_bit = int(a[i])
            b_bit = int(b[i])
            c_bit = int(c[i])
            
            # Assume AND logic for demo purposes
            out_bit = a_bit & b_bit & c_bit
            
            outputs.append({'out': str(out_bit)})
        
        return outputs
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


