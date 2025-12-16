
import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        pass  # Combinational logic, no state needed

    def load(self, stimulus_dict):
        # Derived truth table based on the Karnaugh map
        _TRUTH_TABLE = {
            '000': '0',  # a=0, b=0, c=0
            '001': '0',  # a=0, b=0, c=1
            '011': '0',  # a=0, b=1, c=1
            '010': '0',  # a=0, b=1, c=0
            '110': '0',  # a=1, b=1, c=0
            '111': '1',  # a=1, b=1, c=1
            '101': '0',  # a=1, b=0, c=1
            '100': '0',  # a=1, b=0, c=0
        }

        # Assuming 'a', 'b', 'c' are given in stimulus_dict as strings
        a = stimulus_dict['a']
        b = stimulus_dict['b']
        c = stimulus_dict['c']

        outputs = []
        for a_bit, b_bit, c_bit in zip(a, b, c):
            key = a_bit + b_bit + c_bit
            out = _TRUTH_TABLE[key]
            outputs.append({'out': out})

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


