import json

from cocotb.binary import BinaryValue


def get_mux_in_for_cd(c, d):
    if c == "0" and d == "0":
        return "1001"  # cd=00 row from K-map
    elif c == "0" and d == "1":
        return "0001"  # cd=01 row from K-map
    elif c == "1" and d == "1":
        return "1011"  # cd=11 row from K-map
    else:  # c == '1' and d == '0'
        return "1001"  # cd=10 row from K-map


def stimulus_gen():
    stimulus_list = []

    # Scenario 1: All Input Combinations for c=0
    scenario1 = {
        "scenario": "All Input Combinations for c=0",
        "input variable": [{"c": "0", "d": "0"}, {"c": "0", "d": "1"}],
    }
    stimulus_list.append(scenario1)

    # Scenario 2: All Input Combinations for c=1
    scenario2 = {
        "scenario": "All Input Combinations for c=1",
        "input variable": [{"c": "1", "d": "0"}, {"c": "1", "d": "1"}],
    }
    stimulus_list.append(scenario2)

    # Scenario 3: Boundary Transition cd=00->01
    scenario3 = {
        "scenario": "Boundary Transition cd=00->01",
        "input variable": [{"c": "0", "d": "0"}, {"c": "0", "d": "1"}],
    }
    stimulus_list.append(scenario3)

    # Scenario 4: Boundary Transition cd=10->11
    scenario4 = {
        "scenario": "Boundary Transition cd=10->11",
        "input variable": [{"c": "1", "d": "0"}, {"c": "1", "d": "1"}],
    }
    stimulus_list.append(scenario4)

    # Scenario 5: Static Input Verification
    scenario5 = {
        "scenario": "Static Input Verification",
        "input variable": [
            {"c": "0", "d": "0"},
            {"c": "0", "d": "0"},
            {"c": "0", "d": "0"},
            {"c": "1", "d": "1"},
            {"c": "1", "d": "1"},
            {"c": "1", "d": "1"},
        ],
    }
    stimulus_list.append(scenario5)

    # Scenario 6: Rapid Input Toggling
    scenario6 = {
        "scenario": "Rapid Input Toggling",
        "input variable": [
            {"c": "0", "d": "0"},
            {"c": "1", "d": "1"},
            {"c": "0", "d": "1"},
            {"c": "1", "d": "0"},
            {"c": "0", "d": "0"},
            {"c": "1", "d": "1"},
        ],
    }
    stimulus_list.append(scenario6)

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
