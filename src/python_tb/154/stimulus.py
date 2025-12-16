import json

from cocotb.binary import BinaryValue


def dec_to_bcd(dec):
    tens = dec // 10
    ones = dec % 10
    return f"{tens:04b}{ones:04b}"


def stimulus_gen():
    scenarios = []

    def add_time_sequence(start_h, start_m, start_s, count, ena_val="1", rst="0"):
        sequence = []
        h, m, s = start_h, start_m, start_s
        for _ in range(count):
            sequence.append(
                {
                    "reset": rst,
                    "ena": ena_val,
                    "hh": dec_to_bcd(h),
                    "mm": dec_to_bcd(m),
                    "ss": dec_to_bcd(s),
                }
            )
            if ena_val == "1" and rst == "0":
                s += 1
                if s == 60:
                    s = 0
                    m += 1
                    if m == 60:
                        m = 0
                        h += 1
                        if h == 13:
                            h = 1
        return sequence

    # Basic Time Progression
    scenarios.append(
        {
            "scenario": "Basic Time Progression",
            "input variable": add_time_sequence(12, 0, 0, 180),
        }
    )

    # Hour Rollover
    scenarios.append(
        {
            "scenario": "Hour Rollover",
            "input variable": add_time_sequence(12, 59, 55, 10),
        }
    )

    # AM to PM Transition
    scenarios.append(
        {
            "scenario": "AM to PM Transition",
            "input variable": add_time_sequence(11, 59, 55, 10),
        }
    )

    # PM to AM Transition
    scenarios.append(
        {
            "scenario": "PM to AM Transition",
            "input variable": add_time_sequence(11, 59, 55, 10),
        }
    )

    # Reset During Operation
    reset_seq = add_time_sequence(3, 45, 30, 5)
    reset_seq.extend(
        [
            {
                "reset": "1",
                "ena": "1",
                "hh": dec_to_bcd(12),
                "mm": dec_to_bcd(0),
                "ss": dec_to_bcd(0),
            }
            for _ in range(5)
        ]
    )
    scenarios.append(
        {"scenario": "Reset During Operation", "input variable": reset_seq}
    )

    # Disable Enable Signal
    disable_seq = add_time_sequence(2, 30, 0, 5)
    disable_seq.extend(add_time_sequence(2, 30, 0, 5, ena_val="0"))
    scenarios.append(
        {"scenario": "Disable Enable Signal", "input variable": disable_seq}
    )

    # Reset Priority
    priority_seq = [
        {
            "reset": "1",
            "ena": "1",
            "hh": dec_to_bcd(12),
            "mm": dec_to_bcd(0),
            "ss": dec_to_bcd(0),
        }
        for _ in range(10)
    ]
    scenarios.append({"scenario": "Reset Priority", "input variable": priority_seq})

    # BCD Format Verification
    scenarios.append(
        {
            "scenario": "BCD Format Verification",
            "input variable": add_time_sequence(9, 58, 55, 10),
        }
    )

    # Long Term Stability
    scenarios.append(
        {
            "scenario": "Long Term Stability",
            "input variable": add_time_sequence(11, 58, 0, 300),
        }
    )

    # Invalid Time Prevention
    scenarios.append(
        {
            "scenario": "Invalid Time Prevention",
            "input variable": add_time_sequence(12, 58, 55, 10),
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
