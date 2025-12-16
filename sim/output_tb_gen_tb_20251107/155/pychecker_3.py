
import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        '''
        Initialize all internal state registers to zero.
        '''
        self.state = 'WALK_LEFT'  # Initial state is walking left
        self.fall_counter = 0     # Counter for falling cycles
        self.ground = 1           # Assume initially on ground
        self.walk_left = 0
        self.walk_right = 0
        self.aaah = 0
        self.digging = 0

    def load(self, clk, stimulus_dict: Dict[str, str]):
        '''
        Update FSM states and outputs based on inputs and clock.
        '''
        # Convert inputs from binary strings to integers
        areset = int(stimulus_dict['areset'], 2)
        bump_left = int(stimulus_dict['bump_left'], 2)
        bump_right = int(stimulus_dict['bump_right'], 2)
        ground = int(stimulus_dict['ground'], 2)
        dig = int(stimulus_dict['dig'], 2)

        # Asynchronous reset
        if areset == 1:
            self.state = 'WALK_LEFT'
            self.fall_counter = 0
            self.walk_left = 1
            self.walk_right = 0
            self.aaah = 0
            self.digging = 0
            return {'walk_left': '1', 'walk_right': '0', 'aaah': '0', 'digging': '0'}

        if clk == 1:  # On rising edge of clock
            if self.state == 'FALLING':
                self.fall_counter += 1
                if ground == 1:
                    if self.fall_counter > 20:
                        # Lemming splatters
                        self.state = 'SPLATTERED'
                        self.walk_left = 0
                        self.walk_right = 0
                        self.aaah = 0
                        self.digging = 0
                    else:
                        # Resume walking
                        self.state = 'WALK_LEFT' if self.walk_left else 'WALK_RIGHT'
                        self.fall_counter = 0
                else:
                    self.aaah = 1
            elif self.state == 'DIGGING':
                if ground == 0:
                    self.state = 'FALLING'
                    self.aaah = 1
                else:
                    self.digging = 1
            else:  # Walking states
                if ground == 0:
                    self.state = 'FALLING'
                    self.aaah = 1
                elif dig == 1:
                    self.state = 'DIGGING'
                    self.digging = 1
                elif (bump_left == 1 and self.state == 'WALK_LEFT') or (bump_right == 1 and self.state == 'WALK_RIGHT'):
                    # Switch directions
                    if self.state == 'WALK_LEFT':
                        self.state = 'WALK_RIGHT'
                        self.walk_left = 0
                        self.walk_right = 1
                    else:
                        self.state = 'WALK_LEFT'
                        self.walk_right = 0
                        self.walk_left = 1

        # Output logic
        self.walk_left = 1 if self.state == 'WALK_LEFT' else 0
        self.walk_right = 1 if self.state == 'WALK_RIGHT' else 0
        self.aaah = 1 if self.state == 'FALLING' else 0
        self.digging = 1 if self.state == 'DIGGING' else 0

        return {
            'walk_left': str(self.walk_left),
            'walk_right': str(self.walk_right),
            'aaah': str(self.aaah),
            'digging': str(self.digging)
        }
def check_output(stimulus_list_scenario):

    
    tb_outputs = []


    for stimulus_list in stimulus_list_scenario["input variable"]:
        dut = GoldenDUT()


        clock_cycles = stimulus_list['clock cycles']
        clk = 1
        input_vars_list = {k: v for k, v in stimulus_list.items() if k != "clock cycles"}
        output_vars_list = {'clock cycles':clock_cycles}
        for k,v in input_vars_list.items():
            if len(v) < clock_cycles:
                v.extend([v[-1]] * (clock_cycles - len(v)))
                
        

        for i in range(clock_cycles):
            input_vars = {k:v[i] for k,v in input_vars_list.items()}

            output_vars = dut.load(clk,input_vars)
            for k,v in output_vars.items():
                if k not in output_vars_list:
                    output_vars_list[k] = []
                output_vars_list[k].append(v)
            


        tb_outputs.append(output_vars_list)

    return tb_outputs

if __name__ == "__main__":
    stimulus_file_name = "stimulus.json"
    with open(stimulus_file_name, "r") as f:
        stimulus_data = json.load(f)


    if isinstance(stimulus_data, dict):
        stimulus_list_scenarios = stimulus_data.get("input variable", [])
    else:
        stimulus_list_scenarios = stimulus_data

    outputs=[]
    for stimulus_list_scenario in stimulus_list_scenarios:
        outputs.append( check_output(stimulus_list_scenario))
    with open(stimulus_file_name, "w") as f:
        json.dump(stimulus_list_scenarios, f, indent=4)

    print(json.dumps(outputs, indent=2))





