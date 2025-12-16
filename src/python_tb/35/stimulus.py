import json

from cocotb.binary import BinaryValue


def create_state_vector(hot_bit):
    state = ["0"] * 10
    if 0 <= hot_bit < 10:
        state[hot_bit] = "1"
    return "".join(state)


def stimulus_gen():
    scenarios = []

    # Pattern Detection 1101
    pattern_detect = {
        "scenario": "Pattern Detection 1101",
        "input variable": [
            {
                "d": "1",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(0),
            },
            {
                "d": "1",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(1),
            },
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(2),
            },
            {
                "d": "1",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(3),
            },
        ],
    }
    scenarios.append(pattern_detect)

    # Reset Pattern Detection
    reset_pattern = {
        "scenario": "Reset Pattern Detection",
        "input variable": [
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(1),
            },
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(2),
            },
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(3),
            },
        ],
    }
    scenarios.append(reset_pattern)

    # Shift Enable Sequence
    shift_sequence = {
        "scenario": "Shift Enable Sequence",
        "input variable": [
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(4),
            },
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(5),
            },
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(6),
            },
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(7),
            },
        ],
    }
    scenarios.append(shift_sequence)

    # Counting State Operation
    counting_op = {
        "scenario": "Counting State Operation",
        "input variable": [
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(8),
            },
            {
                "d": "0",
                "done_counting": "1",
                "ack": "0",
                "state": create_state_vector(8),
            },
        ],
    }
    scenarios.append(counting_op)

    # Wait State Handshaking
    wait_state = {
        "scenario": "Wait State Handshaking",
        "input variable": [
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(9),
            },
            {
                "d": "0",
                "done_counting": "0",
                "ack": "1",
                "state": create_state_vector(9),
            },
        ],
    }
    scenarios.append(wait_state)

    # Invalid State Combinations
    invalid_states = {
        "scenario": "Invalid State Combinations",
        "input variable": [
            {"d": "0", "done_counting": "0", "ack": "0", "state": "1100000000"},
            {"d": "0", "done_counting": "0", "ack": "0", "state": "0000000000"},
        ],
    }
    scenarios.append(invalid_states)

    # Fast Pattern Input
    fast_pattern = {
        "scenario": "Fast Pattern Input",
        "input variable": [
            {
                "d": "1",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(0),
            },
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(0),
            },
            {
                "d": "1",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(0),
            },
        ],
    }
    scenarios.append(fast_pattern)

    # Multiple Cycle Operation
    multiple_cycle = {
        "scenario": "Multiple Cycle Operation",
        "input variable": [
            {
                "d": "1",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(0),
            },
            {
                "d": "1",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(1),
            },
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(2),
            },
            {
                "d": "1",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(3),
            },
            {
                "d": "0",
                "done_counting": "1",
                "ack": "0",
                "state": create_state_vector(8),
            },
            {
                "d": "0",
                "done_counting": "0",
                "ack": "1",
                "state": create_state_vector(9),
            },
        ],
    }
    scenarios.append(multiple_cycle)

    # Output Signal Timing
    output_timing = {
        "scenario": "Output Signal Timing",
        "input variable": [
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(4),
            },
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(8),
            },
            {
                "d": "0",
                "done_counting": "0",
                "ack": "0",
                "state": create_state_vector(9),
            },
        ],
    }
    scenarios.append(output_timing)

    # Concurrent Signal Changes
    concurrent_signals = {
        "scenario": "Concurrent Signal Changes",
        "input variable": [
            {
                "d": "1",
                "done_counting": "1",
                "ack": "1",
                "state": create_state_vector(8),
            },
            {
                "d": "0",
                "done_counting": "1",
                "ack": "1",
                "state": create_state_vector(9),
            },
        ],
    }
    scenarios.append(concurrent_signals)

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
