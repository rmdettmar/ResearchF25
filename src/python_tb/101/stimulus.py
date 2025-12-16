import json

from cocotb.binary import BinaryValue


def get_binary_str(value, width):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    stimulus_list = []

    # Scenario 1: Basic State Transitions with Input 0
    scenario1 = {
        "scenario": "Basic State Transitions with Input 0",
        "input variable": [
            {"in": "0", "state": "00"},  # A->A
            {"in": "0", "state": "01"},  # B->C
            {"in": "0", "state": "10"},  # C->A
            {"in": "0", "state": "11"},  # D->C
        ],
    }
    stimulus_list.append(scenario1)

    # Scenario 2: Basic State Transitions with Input 1
    scenario2 = {
        "scenario": "Basic State Transitions with Input 1",
        "input variable": [
            {"in": "1", "state": "00"},  # A->B
            {"in": "1", "state": "01"},  # B->B
            {"in": "1", "state": "10"},  # C->D
            {"in": "1", "state": "11"},  # D->B
        ],
    }
    stimulus_list.append(scenario2)

    # Scenario 3: Output Verification
    scenario3 = {
        "scenario": "Output Verification",
        "input variable": [
            {"in": "0", "state": "00"},  # A: out=0
            {"in": "1", "state": "01"},  # B: out=0
            {"in": "0", "state": "10"},  # C: out=0
            {"in": "1", "state": "11"},  # D: out=1
        ],
    }
    stimulus_list.append(scenario3)

    # Scenario 4: State Encoding Boundary
    scenario4 = {
        "scenario": "State Encoding Boundary",
        "input variable": [
            {"in": "0", "state": "11"},  # D->C
            {"in": "1", "state": "11"},  # D->B
        ],
    }
    stimulus_list.append(scenario4)

    # Scenario 5: Input Toggle in Each State
    scenario5 = {
        "scenario": "Input Toggle in Each State",
        "input variable": [
            {"in": "0", "state": "00"},  # A with input=0
            {"in": "1", "state": "00"},  # A with input=1
            {"in": "0", "state": "01"},  # B with input=0
            {"in": "1", "state": "01"},  # B with input=1
            {"in": "0", "state": "10"},  # C with input=0
            {"in": "1", "state": "10"},  # C with input=1
            {"in": "0", "state": "11"},  # D with input=0
            {"in": "1", "state": "11"},  # D with input=1
        ],
    }
    stimulus_list.append(scenario5)

    # Scenario 6: Self-Loop Verification
    scenario6 = {
        "scenario": "Self-Loop Verification",
        "input variable": [
            {"in": "0", "state": "00"},  # A->A
            {"in": "0", "state": "00"},  # A->A again
            {"in": "1", "state": "01"},  # B->B
            {"in": "1", "state": "01"},  # B->B again
        ],
    }
    stimulus_list.append(scenario6)

    # Scenario 7: Complete State Coverage
    scenario7 = {
        "scenario": "Complete State Coverage",
        "input variable": [
            {"in": "0", "state": "00"},  # A, input=0
            {"in": "1", "state": "00"},  # A, input=1
            {"in": "0", "state": "01"},  # B, input=0
            {"in": "1", "state": "01"},  # B, input=1
            {"in": "0", "state": "10"},  # C, input=0
            {"in": "1", "state": "10"},  # C, input=1
            {"in": "0", "state": "11"},  # D, input=0
            {"in": "1", "state": "11"},  # D, input=1
        ],
    }
    stimulus_list.append(scenario7)

    return stimulus_list


if __name__ == "__main__":
    result = stimulus_gen()
    # 将结果转换为 JSON 字符串
    if isinstance(result, list):
        result = json.dumps(result, indent=4)
    elif not isinstance(result, str):
        result = json.dumps(result, indent=4)

    with open("stimulus.json", "w") as f:
        f.write(result)
