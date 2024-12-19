from typing import List, Dict
from collections import defaultdict


INPUT_FILE = "input.txt"
INPUT_TYPE = List[int]
MEMORY = defaultdict[int, Dict[int, int]]   # value -> level -> count


def read_input() -> INPUT_TYPE:
    with open(INPUT_FILE, 'r') as f:
        line = f.readline().strip()
        return [int(x) for x in line.split(" ")]


def apply_rule_one(i: int, data: INPUT_TYPE):
    data[i] = 1


def apply_rule_two(i: int, data: INPUT_TYPE):
    str_i = str(data[i])
    half_point = int(len(str_i) / 2)
    left_half = int(str_i[:half_point])    # precondition: even number of digits
    right_half = int(str_i[half_point:])
    data[i] = left_half
    data.append(right_half)


def apply_rule_three(i: int, data: INPUT_TYPE):
    data[i] = data[i] * 2024


def check_rule_one(i: int, data:INPUT_TYPE):
    return data[i] == 0


def check_rule_two(i: int, data: INPUT_TYPE):
    return len(str(data[i])) % 2 == 0


def compute_rule_one():
    return 1


def compute_rule_two(value: int):
    str_i = str(value)
    half_point = int(len(str_i) / 2)
    left_half = int(str_i[:half_point])    # precondition: even number of digits
    right_half = int(str_i[half_point:])
    return left_half, right_half


def compute_rule_three(value: int):
    return value * 2024


def blink(data: INPUT_TYPE):
    i = 0
    while i < len(data):
        if check_rule_one(i, data):
            apply_rule_one(i, data)
        elif check_rule_two(i, data):
            apply_rule_two(i, data)
            i += 1
        else:
            apply_rule_three(i, data)

        i += 1


def solve_first(data: INPUT_TYPE, blink_count: int):
    data = data.copy()

    for i in range(blink_count): 
        print('blink', i)
        blink(data)

    return len(data)


def solve_recursive_tree(x: int, blink: int, memory: MEMORY) -> int:

    if blink == 1:
        if check_rule_two(0, [x]):
            return 2
        return 1

    # check in memory if computation has been done
    if blink in memory[x]:
        return memory[x][blink]
    
    # compute left and right side of the computation
    result_left = 0
    result_right = 0

    if check_rule_one(0, [x]):
        result_left = solve_recursive_tree(compute_rule_one(), blink - 1, memory)
    elif check_rule_two(0, [x]):
        left_node, right_node = compute_rule_two(x)

        result_left = solve_recursive_tree(left_node, blink - 1, memory)
        result_right = solve_recursive_tree(right_node, blink - 1, memory)
    else:
        result_left = solve_recursive_tree(compute_rule_three(x), blink - 1, memory)

    result = result_left + result_right
    memory[x][blink] = result

    return result


def solve_second(data: INPUT_TYPE, blink: int):
    data = data.copy()
    
    memory: MEMORY = defaultdict(dict)
    total = 0

    for i in data:
        total += solve_recursive_tree(i, blink, memory)

    print('memory size', len(memory))

    return total


if __name__ == '__main__':
    data = read_input()
    print('First solution', solve_first(data, 25))
    print('Second solution', solve_second(data, 75))