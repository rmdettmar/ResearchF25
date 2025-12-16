import json

from cocotb.binary import BinaryValue


def create_empty_grid():
    return "0" * 256


def create_full_grid():
    return "1" * 256


def set_cell(grid, row, col, value):
    index = row * 16 + col
    return grid[:index] + str(value) + grid[index + 1 :]


def create_block_pattern():
    grid = create_empty_grid()
    grid = set_cell(grid, 7, 7, 1)
    grid = set_cell(grid, 7, 8, 1)
    grid = set_cell(grid, 8, 7, 1)
    grid = set_cell(grid, 8, 8, 1)
    return grid


def create_blinker_pattern():
    grid = create_empty_grid()
    grid = set_cell(grid, 7, 7, 1)
    grid = set_cell(grid, 7, 8, 1)
    grid = set_cell(grid, 7, 9, 1)
    return grid


def create_glider_pattern():
    grid = create_empty_grid()
    grid = set_cell(grid, 1, 1, 1)
    grid = set_cell(grid, 2, 2, 1)
    grid = set_cell(grid, 2, 3, 1)
    grid = set_cell(grid, 1, 3, 1)
    grid = set_cell(grid, 0, 3, 1)
    return grid


def stimulus_gen():
    scenarios = []

    # Scenario 1: Initial State Loading
    alternating_pattern = "".join(["10"] * 128)
    scenarios.append(
        {
            "scenario": "Initial State Loading",
            "input variable": [
                {"clk": "0", "load": "1", "data": alternating_pattern},
                {"clk": "1", "load": "1", "data": alternating_pattern},
                {"clk": "0", "load": "0", "data": alternating_pattern},
            ],
        }
    )

    # Scenario 2: Single Cell Evolution
    single_cell = create_empty_grid()
    single_cell = set_cell(single_cell, 8, 8, 1)
    scenarios.append(
        {
            "scenario": "Single Cell Evolution",
            "input variable": [
                {"clk": "0", "load": "1", "data": single_cell},
                {"clk": "1", "load": "1", "data": single_cell},
                {"clk": "0", "load": "0", "data": single_cell},
                {"clk": "1", "load": "0", "data": single_cell},
            ],
        }
    )

    # Scenario 3: Stable Pattern
    block_pattern = create_block_pattern()
    scenarios.append(
        {
            "scenario": "Stable Pattern",
            "input variable": [
                {"clk": "0", "load": "1", "data": block_pattern},
                {"clk": "1", "load": "1", "data": block_pattern},
                {"clk": "0", "load": "0", "data": block_pattern},
                {"clk": "1", "load": "0", "data": block_pattern},
            ],
        }
    )

    # Scenario 4: Oscillating Pattern
    blinker_pattern = create_blinker_pattern()
    scenarios.append(
        {
            "scenario": "Oscillating Pattern",
            "input variable": [
                {"clk": "0", "load": "1", "data": blinker_pattern},
                {"clk": "1", "load": "1", "data": blinker_pattern},
                {"clk": "0", "load": "0", "data": blinker_pattern},
                {"clk": "1", "load": "0", "data": blinker_pattern},
            ],
        }
    )

    # Scenario 5: Edge Wrapping
    edge_pattern = create_empty_grid()
    edge_pattern = set_cell(edge_pattern, 0, 0, 1)
    edge_pattern = set_cell(edge_pattern, 0, 15, 1)
    edge_pattern = set_cell(edge_pattern, 15, 0, 1)
    edge_pattern = set_cell(edge_pattern, 15, 15, 1)
    scenarios.append(
        {
            "scenario": "Edge Wrapping",
            "input variable": [
                {"clk": "0", "load": "1", "data": edge_pattern},
                {"clk": "1", "load": "1", "data": edge_pattern},
                {"clk": "0", "load": "0", "data": edge_pattern},
            ],
        }
    )

    # Scenario 6: Overpopulation Rule
    dense_pattern = create_empty_grid()
    for i in range(4):
        for j in range(4):
            dense_pattern = set_cell(dense_pattern, i + 6, j + 6, 1)
    scenarios.append(
        {
            "scenario": "Overpopulation Rule",
            "input variable": [
                {"clk": "0", "load": "1", "data": dense_pattern},
                {"clk": "1", "load": "1", "data": dense_pattern},
                {"clk": "0", "load": "0", "data": dense_pattern},
            ],
        }
    )

    # Scenario 7: Multiple Load Operations
    scenarios.append(
        {
            "scenario": "Multiple Load Operations",
            "input variable": [
                {"clk": "0", "load": "1", "data": block_pattern},
                {"clk": "1", "load": "1", "data": block_pattern},
                {"clk": "0", "load": "0", "data": block_pattern},
                {"clk": "1", "load": "1", "data": blinker_pattern},
                {"clk": "0", "load": "1", "data": blinker_pattern},
            ],
        }
    )

    # Scenario 8: All Cells Dead
    dead_grid = create_empty_grid()
    scenarios.append(
        {
            "scenario": "All Cells Dead",
            "input variable": [
                {"clk": "0", "load": "1", "data": dead_grid},
                {"clk": "1", "load": "1", "data": dead_grid},
                {"clk": "0", "load": "0", "data": dead_grid},
            ],
        }
    )

    # Scenario 9: All Cells Alive
    alive_grid = create_full_grid()
    scenarios.append(
        {
            "scenario": "All Cells Alive",
            "input variable": [
                {"clk": "0", "load": "1", "data": alive_grid},
                {"clk": "1", "load": "1", "data": alive_grid},
                {"clk": "0", "load": "0", "data": alive_grid},
            ],
        }
    )

    # Scenario 10: Glider Pattern
    glider_pattern = create_glider_pattern()
    scenarios.append(
        {
            "scenario": "Glider Pattern",
            "input variable": [
                {"clk": "0", "load": "1", "data": glider_pattern},
                {"clk": "1", "load": "1", "data": glider_pattern},
                {"clk": "0", "load": "0", "data": glider_pattern},
                {"clk": "1", "load": "0", "data": glider_pattern},
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
