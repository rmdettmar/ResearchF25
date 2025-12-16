
import json
import random
def stimulus_gen():
    scenarios = []
    
    # Helper function to generate binary sequences
    def gen_binary_seq(value, cycles):
        return [format(value, '01b') for _ in range(cycles)]
    
    # Scenario 1: InitialZeroInput - 12 clock cycles with a=0
    scenarios.append({
        "scenario": "InitialZeroInput",
        "input variable": [{
            "clock cycles": 12,
            "a": gen_binary_seq(0, 12)
        }]
    })
    
    # Scenario 2: InitialOneInput - 12 clock cycles with a=1
    scenarios.append({
        "scenario": "InitialOneInput",
        "input variable": [{
            "clock cycles": 12,
            "a": gen_binary_seq(1, 12)
        }]
    })
    
    # Scenario 3: ZeroToOneTransition - 16 clock cycles
    zero_to_one = gen_binary_seq(0, 8) + gen_binary_seq(1, 8)
    scenarios.append({
        "scenario": "ZeroToOneTransition",
        "input variable": [{
            "clock cycles": 16,
            "a": zero_to_one
        }]
    })
    
    # Scenario 4: OneToZeroTransition - 16 clock cycles
    one_to_zero = gen_binary_seq(1, 8) + gen_binary_seq(0, 8)
    scenarios.append({
        "scenario": "OneToZeroTransition",
        "input variable": [{
            "clock cycles": 16,
            "a": one_to_zero
        }]
    })
    
    # Scenario 5: AlternatingPattern - 20 clock cycles
    alternating = []
    for _ in range(5):  # 5 groups of 4 cycles each
        alternating.extend(gen_binary_seq(0, 4))
        alternating.extend(gen_binary_seq(1, 4))
    scenarios.append({
        "scenario": "AlternatingPattern",
        "input variable": [{
            "clock cycles": 20,
            "a": alternating[:20]
        }]
    })
    
    return scenarios
if __name__ == "__main__":
    result = stimulus_gen()
    # 将结果转换为 JSON 字符串
    if isinstance(result, list):
        result = json.dumps(result, indent=4)
    elif not isinstance(result, str):
        result = json.dumps(result, indent=4)

    with open("stimulus.json", "w") as f:
        f.write(result)
