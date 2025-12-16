import json


def stimulus_gen():
    scenarios = []

    # Helper function to create a stimulus dictionary
    def create_stimulus(name, input_list):
        return {"scenario": name, "input variable": input_list}

    # Scenario 1: Basic Shift Operation - Shift in 1010
    shift_seq = []
    for bit in ["1", "0", "1", "0"]:  # MSB first
        shift_seq.append({"clk": "1", "shift_ena": "1", "count_ena": "0", "data": bit})
    scenarios.append(create_stimulus("Basic Shift Operation", shift_seq))

    # Scenario 2: Basic Count Operation
    count_seq = []
    # First load 1111 via shift
    for _ in range(4):
        count_seq.append({"clk": "1", "shift_ena": "1", "count_ena": "0", "data": "1"})
    # Then count down 16 times
    for _ in range(16):
        count_seq.append({"clk": "1", "shift_ena": "0", "count_ena": "1", "data": "0"})
    scenarios.append(create_stimulus("Basic Count Operation", count_seq))

    # Scenario 3: Zero Value Counting
    zero_count_seq = []
    # First load 0000 via shift
    for _ in range(4):
        zero_count_seq.append(
            {"clk": "1", "shift_ena": "1", "count_ena": "0", "data": "0"}
        )
    # Try counting down from zero
    for _ in range(4):
        zero_count_seq.append(
            {"clk": "1", "shift_ena": "0", "count_ena": "1", "data": "0"}
        )
    scenarios.append(create_stimulus("Zero Value Counting", zero_count_seq))

    # Scenario 4: Maximum Value Loading
    max_val_seq = []
    for _ in range(4):
        max_val_seq.append(
            {"clk": "1", "shift_ena": "1", "count_ena": "0", "data": "1"}
        )
    scenarios.append(create_stimulus("Maximum Value Loading", max_val_seq))

    # Scenario 5: Control Signal Toggling
    toggle_seq = []
    for i in range(8):
        toggle_seq.append(
            {
                "clk": "1",
                "shift_ena": "1" if i % 2 == 0 else "0",
                "count_ena": "0" if i % 2 == 0 else "1",
                "data": "1",
            }
        )
    scenarios.append(create_stimulus("Control Signal Toggling", toggle_seq))

    # Scenario 6: Rapid Mode Switching
    rapid_switch_seq = []
    for i in range(8):
        rapid_switch_seq.append(
            {
                "clk": "1",
                "shift_ena": "1" if i % 2 == 0 else "0",
                "count_ena": "0" if i % 2 == 0 else "1",
                "data": "1" if i % 2 == 0 else "0",
            }
        )
    scenarios.append(create_stimulus("Rapid Mode Switching", rapid_switch_seq))

    # Scenario 7: Clock Edge Behavior
    clock_edge_seq = []
    for i in range(4):
        clock_edge_seq.append(
            {"clk": "0", "shift_ena": "1", "count_ena": "0", "data": "1"}
        )
        clock_edge_seq.append(
            {"clk": "1", "shift_ena": "1", "count_ena": "0", "data": "1"}
        )
    scenarios.append(create_stimulus("Clock Edge Behavior", clock_edge_seq))

    # Scenario 8: Initial Power-up State
    init_seq = []
    init_seq.append({"clk": "1", "shift_ena": "0", "count_ena": "0", "data": "0"})
    scenarios.append(create_stimulus("Initial Power-up State", init_seq))

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
