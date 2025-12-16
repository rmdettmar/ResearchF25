import json


def stimulus_gen():
    scenarios = []

    # Helper function to create a stimulus dictionary
    def create_stimulus(name, inputs):
        return {"scenario": name, "input variable": inputs}

    # Scenario 1: Normal Computer Operation
    scenarios.append(
        create_stimulus(
            "Normal Computer Operation",
            [{"cpu_overheated": "0", "arrived": "0", "gas_tank_empty": "0"}],
        )
    )

    # Scenario 2: CPU Overheating Protection
    scenarios.append(
        create_stimulus(
            "CPU Overheating Protection",
            [{"cpu_overheated": "1", "arrived": "0", "gas_tank_empty": "0"}],
        )
    )

    # Scenario 3: Normal Driving Condition
    scenarios.append(
        create_stimulus(
            "Normal Driving Condition",
            [{"cpu_overheated": "0", "arrived": "0", "gas_tank_empty": "0"}],
        )
    )

    # Scenario 4: Empty Gas Tank
    scenarios.append(
        create_stimulus(
            "Empty Gas Tank",
            [
                {"cpu_overheated": "0", "arrived": "0", "gas_tank_empty": "1"},
                {"cpu_overheated": "0", "arrived": "1", "gas_tank_empty": "1"},
            ],
        )
    )

    # Scenario 5: Destination Arrived
    scenarios.append(
        create_stimulus(
            "Destination Arrived",
            [
                {"cpu_overheated": "0", "arrived": "1", "gas_tank_empty": "0"},
                {"cpu_overheated": "0", "arrived": "1", "gas_tank_empty": "1"},
            ],
        )
    )

    # Scenario 6: Input Transitions
    scenarios.append(
        create_stimulus(
            "Input Transitions",
            [
                {"cpu_overheated": "0", "arrived": "0", "gas_tank_empty": "0"},
                {"cpu_overheated": "1", "arrived": "0", "gas_tank_empty": "0"},
                {"cpu_overheated": "0", "arrived": "1", "gas_tank_empty": "0"},
            ],
        )
    )

    # Scenario 7: Simultaneous Input Changes
    scenarios.append(
        create_stimulus(
            "Simultaneous Input Changes",
            [
                {"cpu_overheated": "0", "arrived": "0", "gas_tank_empty": "0"},
                {"cpu_overheated": "1", "arrived": "1", "gas_tank_empty": "1"},
            ],
        )
    )

    # Scenario 8: Default Output Values
    scenarios.append(
        create_stimulus(
            "Default Output Values",
            [{"cpu_overheated": "0", "arrived": "0", "gas_tank_empty": "0"}],
        )
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
