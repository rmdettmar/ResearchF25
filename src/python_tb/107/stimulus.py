import json

from cocotb.binary import BinaryValue


def gen_binary_str(value, width=512):
    binary_val = BinaryValue(value=value, n_bits=width, bigEndian=True)
    return binary_val.binstr


def alternate_pattern():
    pattern = 0
    for i in range(0, 512, 2):
        pattern |= 1 << i
    return gen_binary_str(pattern)


def stimulus_gen():
    scenarios = []

    # Basic Load Operation
    basic_load = {
        "scenario": "Basic Load Operation",
        "input variable": [
            {"clk": "0", "load": "1", "data": alternate_pattern()},
            {"clk": "1", "load": "1", "data": alternate_pattern()},
            {"clk": "0", "load": "0", "data": alternate_pattern()},
        ],
    }
    scenarios.append(basic_load)

    # Boundary Condition Verification
    boundary = {
        "scenario": "Boundary Condition Verification",
        "input variable": [
            {"clk": "0", "load": "1", "data": gen_binary_str(1)},
            {"clk": "1", "load": "1", "data": gen_binary_str(1)},
            {"clk": "0", "load": "0", "data": gen_binary_str(1)},
            {"clk": "1", "load": "0", "data": gen_binary_str(1)},
            {"clk": "0", "load": "1", "data": gen_binary_str(1 << 511)},
            {"clk": "1", "load": "1", "data": gen_binary_str(1 << 511)},
        ],
    }
    scenarios.append(boundary)

    # Single Cell Evolution
    single_cell = {
        "scenario": "Single Cell Evolution",
        "input variable": [
            {"clk": "0", "load": "1", "data": gen_binary_str(1 << 256)},
            {"clk": "1", "load": "1", "data": gen_binary_str(1 << 256)},
            {"clk": "0", "load": "0", "data": gen_binary_str(1 << 256)},
            {"clk": "1", "load": "0", "data": gen_binary_str(1 << 256)},
        ],
    }
    scenarios.append(single_cell)

    # All Ones Pattern
    all_ones = {
        "scenario": "All Ones Pattern",
        "input variable": [
            {"clk": "0", "load": "1", "data": gen_binary_str((1 << 512) - 1)},
            {"clk": "1", "load": "1", "data": gen_binary_str((1 << 512) - 1)},
            {"clk": "0", "load": "0", "data": gen_binary_str((1 << 512) - 1)},
        ],
    }
    scenarios.append(all_ones)

    # All Zeros Pattern
    all_zeros = {
        "scenario": "All Zeros Pattern",
        "input variable": [
            {"clk": "0", "load": "1", "data": gen_binary_str(0)},
            {"clk": "1", "load": "1", "data": gen_binary_str(0)},
            {"clk": "0", "load": "0", "data": gen_binary_str(0)},
        ],
    }
    scenarios.append(all_zeros)

    # Complex Pattern Evolution
    sierpinski = gen_binary_str(0x55AA55AA)
    complex_pattern = {
        "scenario": "Complex Pattern Evolution",
        "input variable": [
            {"clk": "0", "load": "1", "data": sierpinski},
            {"clk": "1", "load": "1", "data": sierpinski},
            {"clk": "0", "load": "0", "data": sierpinski},
            {"clk": "1", "load": "0", "data": sierpinski},
        ],
    }
    scenarios.append(complex_pattern)

    # Load During Evolution
    load_interrupt = {
        "scenario": "Load During Evolution",
        "input variable": [
            {"clk": "0", "load": "1", "data": gen_binary_str(0xAAAA)},
            {"clk": "1", "load": "0", "data": gen_binary_str(0xAAAA)},
            {"clk": "0", "load": "0", "data": gen_binary_str(0xAAAA)},
            {"clk": "1", "load": "1", "data": gen_binary_str(0x5555)},
        ],
    }
    scenarios.append(load_interrupt)

    # Multiple Load Operations
    multiple_loads = {
        "scenario": "Multiple Load Operations",
        "input variable": [
            {"clk": "0", "load": "1", "data": gen_binary_str(0xAAAA)},
            {"clk": "1", "load": "1", "data": gen_binary_str(0x5555)},
            {"clk": "0", "load": "1", "data": gen_binary_str(0xFFFF)},
        ],
    }
    scenarios.append(multiple_loads)

    # Edge Pattern Propagation
    edge_pattern = {
        "scenario": "Edge Pattern Propagation",
        "input variable": [
            {"clk": "0", "load": "1", "data": gen_binary_str(0x3)},
            {"clk": "1", "load": "1", "data": gen_binary_str(0x3)},
            {"clk": "0", "load": "0", "data": gen_binary_str(0x3)},
            {"clk": "1", "load": "0", "data": gen_binary_str(0x3)},
        ],
    }
    scenarios.append(edge_pattern)

    # Timing Verification
    timing = {
        "scenario": "Timing Verification",
        "input variable": [
            {"clk": "0", "load": "0", "data": gen_binary_str(0)},
            {"clk": "1", "load": "1", "data": gen_binary_str(0xAAAA)},
            {"clk": "0", "load": "1", "data": gen_binary_str(0xAAAA)},
            {"clk": "1", "load": "0", "data": gen_binary_str(0xAAAA)},
        ],
    }
    scenarios.append(timing)

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
