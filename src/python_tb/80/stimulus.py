import json

from cocotb.binary import BinaryValue


def stimulus_gen():
    scenarios = []

    def create_sequence(scenario_name, reset_seq, clk_seq=None):
        sequence = {"scenario": scenario_name, "input variable": []}
        for reset_val in reset_seq:
            sequence["input variable"].append({"clk": "1", "reset": reset_val})
            sequence["input variable"].append({"clk": "0", "reset": reset_val})
        return sequence

    # Reset Verification
    scenarios.append(create_sequence("Reset Verification", ["1", "1", "0"]))

    # Single State Transition
    scenarios.append(create_sequence("Single State Transition", ["1", "0", "0"]))

    # Maximum Length Sequence
    max_seq = ["1"] + ["0"] * 62  # 31 cycles * 2 (for clock)
    scenarios.append(create_sequence("Maximum Length Sequence", max_seq))

    # Mid-sequence Reset
    mid_reset = ["0"] * 20 + ["1"] + ["0"] * 10
    scenarios.append(create_sequence("Mid-sequence Reset", mid_reset))

    # Tap Position Verification
    scenarios.append(
        create_sequence("Tap Position Verification", ["1", "0", "0", "0", "0"])
    )

    # All-zeros Prevention
    scenarios.append(create_sequence("All-zeros Prevention", ["0"] * 40))  # 20 cycles

    # Sequence Repetition
    scenarios.append(
        create_sequence("Sequence Repetition", ["0"] * 124)
    )  # 62 cycles (2 full sequences)

    # Clock Edge Sensitivity
    clock_edge = ["1", "0"] * 5  # 5 clock cycles
    scenarios.append(create_sequence("Clock Edge Sensitivity", ["0"] * 10))

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
