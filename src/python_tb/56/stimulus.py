import json


def stimulus_gen():
    scenarios = []

    # Helper function to generate clock cycles with data changes
    def gen_clock_cycles(num_cycles, data_pattern):
        sequence = []
        for i in range(num_cycles * 2):  # *2 for both edges
            sequence.append(
                {
                    "clk": "1" if i % 2 == 0 else "0",
                    "d": data_pattern[i % len(data_pattern)],
                }
            )
        return sequence

    # Scenario 1: Basic Rising Edge Operation
    scenarios.append(
        {
            "scenario": "Basic Rising Edge Operation",
            "input variable": gen_clock_cycles(
                4, ["0", "0", "1", "1", "0", "0", "1", "1"]
            ),
        }
    )

    # Scenario 2: Basic Falling Edge Operation
    scenarios.append(
        {
            "scenario": "Basic Falling Edge Operation",
            "input variable": gen_clock_cycles(
                4, ["1", "1", "0", "0", "1", "1", "0", "0"]
            ),
        }
    )

    # Scenario 3: Alternating Edge Response
    scenarios.append(
        {
            "scenario": "Alternating Edge Response",
            "input variable": gen_clock_cycles(
                4, ["0", "1", "0", "1", "0", "1", "0", "1"]
            ),
        }
    )

    # Scenario 4: Setup Time Verification
    setup_seq = []
    for i in range(8):
        setup_seq.append({"clk": "0", "d": "0"})
        setup_seq.append({"clk": "0", "d": "1"})  # Change data close to edge
        setup_seq.append({"clk": "1", "d": "1"})
    scenarios.append(
        {"scenario": "Setup Time Verification", "input variable": setup_seq}
    )

    # Scenario 5: Hold Time Verification
    hold_seq = []
    for i in range(8):
        hold_seq.append({"clk": "0", "d": "1"})
        hold_seq.append({"clk": "1", "d": "1"})
        hold_seq.append({"clk": "1", "d": "0"})  # Change data right after edge
    scenarios.append({"scenario": "Hold Time Verification", "input variable": hold_seq})

    # Scenario 6: Data Pattern Test
    scenarios.append(
        {
            "scenario": "Data Pattern Test",
            "input variable": gen_clock_cycles(
                8, ["1", "0", "1", "0", "1", "0", "1", "0"]
            ),
        }
    )

    # Scenario 7: Clock Glitch Immunity
    glitch_seq = []
    for i in range(10):
        glitch_seq.append({"clk": "0", "d": "1"})
        glitch_seq.append({"clk": "1", "d": "1"})  # Normal edge
        glitch_seq.append({"clk": "0", "d": "1"})  # Glitch
        glitch_seq.append({"clk": "1", "d": "1"})  # Glitch
        glitch_seq.append({"clk": "0", "d": "1"})  # Return to normal
    scenarios.append(
        {"scenario": "Clock Glitch Immunity", "input variable": glitch_seq}
    )

    # Scenario 8: Power-On State
    scenarios.append(
        {
            "scenario": "Power-On State",
            "input variable": [
                {"clk": "0", "d": "0"},
                {"clk": "0", "d": "0"},
                {"clk": "1", "d": "0"},
                {"clk": "1", "d": "0"},
            ],
        }
    )

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
