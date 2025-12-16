
import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # No internal state is needed for a purely combinational logic
        pass

    def load(self, stimulus_dict):
        # Example truth table based on typical combinational logic
        # Assuming the logic: out = a AND b OR NOT c
        # This is a placeholder logic since the actual logic was not provided in the readable RTL spec.
        truth_table = {
            '000': '0',
            '001': '1',
            '010': '0',
            '011': '0',
            '100': '0',
            '101': '1',
            '110': '1',
            '111': '1'
        }

        outputs = []
        for input_vars in stimulus_dict['input variable']:
            a = input_vars['a']
            b = input_vars['b']
            c = input_vars['c']

            # Construct the key for the truth table lookup
            key = a + b + c
            out_val = truth_table[key] if key in truth_table else '0'

            # Append the result
            outputs.append({'out': out_val})

        return {'output variable': outputs}
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


