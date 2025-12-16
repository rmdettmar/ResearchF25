import json


def create_repeating_pattern(value, count):
    return [{"in": value} for _ in range(count)]


def create_alternating_pattern(count):
    pattern = []
    for i in range(count):
        pattern.append({"in": "1" if i % 2 else "0"})
    return pattern


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Signal Propagation
    scenarios.append(
        {
            "scenario": "Basic Signal Propagation",
            "input variable": create_alternating_pattern(10),
        }
    )

    # Scenario 2: Static Value Hold
    static_test = create_repeating_pattern("0", 10) + create_repeating_pattern("1", 10)
    scenarios.append({"scenario": "Static Value Hold", "input variable": static_test})

    # Scenario 3: Rapid Transitions
    rapid_test = create_alternating_pattern(20)
    scenarios.append({"scenario": "Rapid Transitions", "input variable": rapid_test})

    # Scenario 4: Power-On State
    scenarios.append(
        {
            "scenario": "Power-On State",
            "input variable": create_repeating_pattern("0", 5),
        }
    )

    # Scenario 5: Timing Verification
    timing_test = [{"in": "0"}, {"in": "1"}, {"in": "0"}, {"in": "1"}, {"in": "0"}]
    scenarios.append({"scenario": "Timing Verification", "input variable": timing_test})

    # Scenario 6: Glitch Immunity
    glitch_test = [{"in": "0"}, {"in": "1"}, {"in": "0"}, {"in": "1"}, {"in": "0"}]
    scenarios.append({"scenario": "Glitch Immunity", "input variable": glitch_test})

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
