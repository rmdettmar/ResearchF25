import json

from cocotb.binary import BinaryValue


def gen_basic_sampling():
    return [
        {"clk": "0", "d": "0"},
        {"clk": "1", "d": "0"},
        {"clk": "0", "d": "1"},
        {"clk": "1", "d": "1"},
        {"clk": "0", "d": "0"},
        {"clk": "1", "d": "0"},
    ]


def gen_setup_time():
    return [
        {"clk": "0", "d": "0"},
        {"clk": "0", "d": "1"},
        {"clk": "1", "d": "1"},
        {"clk": "0", "d": "0"},
    ]


def gen_hold_time():
    return [
        {"clk": "0", "d": "1"},
        {"clk": "1", "d": "1"},
        {"clk": "1", "d": "0"},
        {"clk": "0", "d": "0"},
    ]


def gen_rapid_toggle():
    return [
        {"clk": "0", "d": "0"},
        {"clk": "0", "d": "1"},
        {"clk": "0", "d": "0"},
        {"clk": "1", "d": "0"},
        {"clk": "1", "d": "1"},
        {"clk": "1", "d": "0"},
    ]


def gen_clock_variation():
    return [
        {"clk": "0", "d": "1"},
        {"clk": "1", "d": "1"},
        {"clk": "0", "d": "0"},
        {"clk": "1", "d": "0"},
    ]


def gen_power_on():
    return [{"clk": "0", "d": "0"}, {"clk": "0", "d": "0"}, {"clk": "1", "d": "0"}]


def gen_glitch_immunity():
    return [
        {"clk": "0", "d": "0"},
        {"clk": "0", "d": "1"},
        {"clk": "0", "d": "0"},
        {"clk": "1", "d": "0"},
    ]


def stimulus_gen():
    scenarios = [
        {"scenario": "Basic Data Sampling", "input variable": gen_basic_sampling()},
        {"scenario": "Setup Time Verification", "input variable": gen_setup_time()},
        {"scenario": "Hold Time Verification", "input variable": gen_hold_time()},
        {"scenario": "Rapid Data Toggle", "input variable": gen_rapid_toggle()},
        {"scenario": "Clock Period Variation", "input variable": gen_clock_variation()},
        {"scenario": "Power-On State", "input variable": gen_power_on()},
        {"scenario": "Glitch Immunity", "input variable": gen_glitch_immunity()},
    ]
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
