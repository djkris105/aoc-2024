from typing import List, Tuple, Set


INPUT_FILE = 'input.txt'


def read_input() -> List[int]:
    data = []

    with open(INPUT_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            data.append([int(l) if l != '.' else 10000000 for l in line])

    return data


def iterate_trailhead(data: List[int]):
    h = len(data)
    w = len(data[0])

    for j in range(h):
        for i in range(w):
            if data[j][i] == 0:
                yield (i, j)


def find_all_trails(current: Tuple[int, int], reached: Set[Tuple[int, int]], data: List[int]) -> int:
    i, j = current
    trail_height = data[j][i]
    if trail_height == 9:
        reached.add(current)
        return 1

    w = len(data[0])
    h = len(data)

    tot = 0
    # go N
    if j > 0 and data[j - 1][i] == trail_height + 1:
        tot += find_all_trails((i, j - 1), reached, data)

    # go E
    if i < w - 1 and data[j][i + 1] == trail_height + 1:
        tot += find_all_trails((i + 1, j), reached, data)

    # go S
    if j < h - 1 and data[j + 1][i] == trail_height + 1:
        tot += find_all_trails((i, j + 1), reached, data)

    # go W
    if i > 0 and data[j][i - 1] == trail_height + 1:
        tot += find_all_trails((i - 1, j), reached, data)

    return tot


def solve_first(data: List[int]):
    acc = 0
    for trailhead in iterate_trailhead(data):
        reached = set()
        find_all_trails(trailhead, reached, data)

        # print(trailhead, len(reached))

        acc += len(reached)

    return acc


def solve_second(data: List[int]):
    acc = 0
    for trailhead in iterate_trailhead(data):
        distinct_trails = find_all_trails(trailhead, set(), data)
        acc += distinct_trails

    return acc


if __name__ == '__main__':
    data = read_input()
    print('first solution', solve_first(data))
    print('second solution', solve_second(data))
