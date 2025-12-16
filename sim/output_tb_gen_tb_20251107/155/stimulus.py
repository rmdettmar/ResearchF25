
import json
import random
import random

def stimulus_gen():
    stim_list = []

    # Scenario: Normal walking left and right
    stim_list.append({
        "scenario": "NormalWalking",
        "input variable": [
            {
                "clock cycles": 20,
                "areset": ["0"] * 20,
                "bump_left": ["0"] * 10 + ["1"] * 10,
                "bump_right": ["1"] * 10 + ["0"] * 10,
                "ground": ["1"] * 20,
                "dig": ["0"] * 20
            }
        ]
    })

    # Scenario: Falling and splattering
    stim_list.append({
        "scenario": "FallingAndSplattering",
        "input variable": [
            {
                "clock cycles": 25,
                "areset": ["0"] * 25,
                "bump_left": ["0"] * 25,
                "bump_right": ["0"] * 25,
                "ground": ["1"] * 5 + ["0"] * 20,
                "dig": ["0"] * 25
            }
        ]
    })

    # Scenario: Digging and falling
    stim_list.append({
        "scenario": "DiggingAndFalling",
        "input variable": [
            {
                "clock cycles": 15,
                "areset": ["0"] * 15,
                "bump_left": ["0"] * 15,
                "bump_right": ["0"] * 15,
                "ground": ["1"] * 10 + ["0"] * 5,
                "dig": ["0"] * 5 + ["1"] * 5 + ["0"] * 5
            }
        ]
    })

    # Scenario: Simultaneous bumps
    stim_list.append({
        "scenario": "SimultaneousBumps",
        "input variable": [
            {
                "clock cycles": 10,
                "areset": ["0"] * 10,
                "bump_left": ["1"] * 10,
                "bump_right": ["1"] * 10,
                "ground": ["1"] * 10,
                "dig": ["0"] * 10
            }
        ]
    })

    # Randomized test scenarios
    for idx in range(10):
        clock_cycles = random.randint(15, 30)
        stim_list.append({
            "scenario": f"RandomScenario{idx}",
            "input variable": [
                {
                    "clock cycles": clock_cycles,
                    "areset": ["0"] * clock_cycles,
                    "bump_left": [random.choice("01") for _ in range(clock_cycles)],
                    "bump_right": [random.choice("01") for _ in range(clock_cycles)],
                    "ground": [random.choice("01") for _ in range(clock_cycles)],
                    "dig": [random.choice("01") for _ in range(clock_cycles)]
                }
            ]
        })

    return stim_list
if __name__ == "__main__":
    result = stimulus_gen()
    # Convert result to JSON string
    if isinstance(result, list):
        result = json.dumps(result, indent=4)
    elif not isinstance(result, str):
        result = json.dumps(result, indent=4)

    with open("stimulus.json", "w") as f:
        f.write(result)
