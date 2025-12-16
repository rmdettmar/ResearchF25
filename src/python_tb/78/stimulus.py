import json


def stimulus_gen():
    scenarios = []

    # Helper function to create stimulus dictionary for a scenario
    def create_scenario(name, reset_sequence):
        return {
            "scenario": name,
            "input variable": [{"reset": str(val)} for val in reset_sequence],
        }

    # Scenario 1: Normal Counting Sequence (15 cycles)
    scenarios.append(
        create_scenario("Normal Counting Sequence", ["0"] * 15)
    )  # Let it count through 1->10->1->5

    # Scenario 2: Synchronous Reset at different values
    scenarios.append(
        create_scenario("Synchronous Reset", ["0", "0", "0", "1", "0", "0", "1", "0"])
    )  # Reset at count=4 and count=7

    # Scenario 3: Power-on State
    scenarios.append(
        create_scenario("Power-on State", ["0"] * 5)
    )  # Check initial value without reset

    # Scenario 4: Boundary Value Transition
    scenarios.append(
        create_scenario("Boundary Value Transition", ["0"] * 12)
    )  # Let it count from 8->9->10->1->2

    # Scenario 5: Reset at Boundary
    scenarios.append(
        create_scenario(
            "Reset at Boundary", ["0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0"]
        )
    )  # Reset when count=10

    # Scenario 6: Multiple Reset Cycles
    scenarios.append(
        create_scenario("Multiple Reset Cycles", ["1", "1", "1", "1", "0", "0", "0"])
    )  # Hold reset for 4 cycles

    # Scenario 7: Long-term Stability
    scenarios.append(
        create_scenario("Long-term Stability", ["0"] * 30)
    )  # Run for 3 complete cycles (1-10)

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
