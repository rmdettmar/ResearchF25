
import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        '''
        Initialize all internal state registers to **zero**. It is very important and you must do this. No matter what the initial value is in the RTL specification.
        Each internal register/state variable must align with the module header.
        Explicitly initialize these states according to the RTL specification.
        '''
        self.walking_left = 0
        self.walking_right = 0
        self.falling = 0
        self.digging = 0
        self.splattered = 0
        self.fall_counter = 0
        self.state = 'WALK_LEFT'  # Initial state

    def load(self, clk, stimulus_dict):
        '''
        clk: the clock signal, 1 for high, 0 for low
        Parse each input variable and use it to perform RTL state updates.
        Returns a dictionary of the outputs aligned with the RTL module outputs and updated states for verification.
        '''
        # Convert inputs
        areset = int(stimulus_dict['areset'], 2)
        bump_left = int(stimulus_dict['bump_left'], 2)
        bump_right = int(stimulus_dict['bump_right'], 2)
        ground = int(stimulus_dict['ground'], 2)
        dig = int(stimulus_dict['dig'], 2)

        if areset:
            # Reset the state to initial
            self.state = 'WALK_LEFT'
            self.falling = 0
            self.digging = 0
            self.splattered = 0
            self.fall_counter = 0
        elif clk == 1:  # Rising edge
            if self.splattered:
                # Lemming is splattered, do nothing
                pass
            else:
                if not ground:
                    # If no ground, fall
                    if not self.falling:
                        self.falling = 1
                        self.fall_counter = 0
                    self.fall_counter += 1
                    if self.fall_counter > 20:
                        # More than 20 cycles falling
                        self.splattered = 1
                else:
                    # On ground
                    if self.falling:
                        # If was falling, now back on ground
                        self.falling = 0
                        self.fall_counter = 0
                    if dig and not self.digging:
                        # Start digging
                        self.digging = 1
                    elif self.digging:
                        # Continue digging
                        if not ground:
                            # End of dig
                            self.digging = 0
                    else:
                        # Normal walking and switching
                        if bump_left or bump_right:
                            # Switch directions
                            self.state = 'WALK_LEFT' if self.state == 'WALK_RIGHT' else 'WALK_RIGHT'

            # Output logic
            self.walking_left = 1 if self.state == 'WALK_LEFT' and not self.falling and not self.splattered and not self.digging else 0
            self.walking_right = 1 if self.state == 'WALK_RIGHT' and not self.falling and not self.splattered and not self.digging else 0
            self.aaah = 1 if self.falling and not self.splattered else 0
            self.digging = 1 if self.digging and not self.falling and not self.splattered else 0

        # Return outputs
        return {
            'walk_left': str(self.walking_left),
            'walk_right': str(self.walking_right),
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





