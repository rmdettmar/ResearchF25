
import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        '''
        Initialize all internal state registers to zero.
        Each internal register/state variable must align with the module header.
        Explicitly initialize these states according to the RTL specification.
        '''
        pass  # No internal state needed

    def load(self, stimulus_dict: Dict[str, any]):
        '''
        stimulus_dict: a dictionary formatted as shown above.
        Parse each input variable: Generate a Python dictionary that decodes a binary string into the corresponding RTL signal assignments
        Returns a dictionary of the outputs strictly aligned with the RTL module outputs name and updated states for verification.
        '''

        # Extract the input from the stimulus dictionary
        in_str = stimulus_dict["in"]
        assert len(in_str) == 32, "Input must be 32 bits."

        # Convert binary string to integer
        in_int = int(in_str, 2)

        # Reverse the byte order
        out_int = (
            ((in_int & 0x000000FF) << 24) |  # Least significant byte
            ((in_int & 0x0000FF00) << 8) |   # Second byte
            ((in_int & 0x00FF0000) >> 8) |   # Third byte
            ((in_int & 0xFF000000) >> 24)    # Most significant byte
        )

        # Convert the resulting integer back to a binary string, ensuring it's 32-bits
        out_str = f'{out_int:032b}'

        return {"out": out_str}
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


