from typing import List, Tuple, Set, Dict
from collections import defaultdict


INPUT_FILE = "input.txt"


Coord = Tuple[int, int]


def read_input() -> List[str]:
    data = []

    with open(INPUT_FILE, 'r') as f:
        for line in f: 
            line = line.strip()
            if len(line) == 0:
                continue

            data.append(line)

    return data


def draw_state(data: List[str], antinode_positions: Set[Coord]):
    data = data.copy()
    for x, y in antinode_positions:
        data[y] = data[y][0:x] + '#' + data[y][x+1:]

    for row in data:
        print(row)


def is_oob(data: List[str], coord: Coord) -> bool:
    h = len(data)
    w = len(data[0])

    if coord[0] < 0 or coord[1] < 0:
        return True
    
    if coord[0] >= w or coord[1] >= h:
        return True
    
    return False


def get_antinodes(data: List[str], antenna: str, antennas_dict: defaultdict[str, set[Coord]]) -> Set[Coord]:
    result = []

    same_freq_antennas = antennas_dict[antenna]

    for first in same_freq_antennas:
        for second in same_freq_antennas:
            if first == second:
                continue

            f_x, f_y = first
            s_x, s_y = second

            anti_X = 2 * f_x - s_x
            anti_Y = 2 * f_y - s_y

            anti_coords = (anti_X, anti_Y)

            if is_oob(data, anti_coords):
                continue

            result.append(anti_coords)

    return result


def get_antinodes_harmonics(data: List[str], antenna: str, antennas_dict: defaultdict[str, set[Coord]]) -> Set[Coord]:
    result = []

    same_freq_antennas = antennas_dict[antenna]

    for first in same_freq_antennas:
        for second in same_freq_antennas:
            if first == second:
                continue

            f_x, f_y = first
            s_x, s_y = second

            delta_X = f_x - s_x
            delta_Y = f_y - s_y

            result.append((f_x, f_y))

            while True:

                anti_coords = (f_x + delta_X, f_y + delta_Y)

                if is_oob(data, anti_coords):
                    break

                result.append(anti_coords)

                # keep adding directional vector to the last registered point
                f_x = anti_coords[0]
                f_y = anti_coords[1]

    return result


def solve_first(data: List[str]):
    # make an initial scan to extract all antennas positions
    antennas: defaultdict[str, set[Coord]] = defaultdict(set)

    for j in range(len(data)):
        for i in range(len(data[j])):
            v = data[j][i]
            if v == '.':
                continue

            antennas[v].add((i, j))

    antinode_set = set()
    for antenna in antennas:
        antenna_antinode_positions = get_antinodes(data, antenna, antennas)
        draw_state(data, antenna_antinode_positions)

        for antinode in antenna_antinode_positions:
            antinode_set.add(antinode)

    return len(antinode_set)


def solve_second(data: List[str]):
    # make an initial scan to extract all antennas positions
    antennas: defaultdict[str, set[Coord]] = defaultdict(set)

    for j in range(len(data)):
        for i in range(len(data[j])):
            v = data[j][i]
            if v == '.':
                continue

            antennas[v].add((i, j))

    antinode_set = set()
    for antenna in antennas:
        antenna_antinode_positions = get_antinodes_harmonics(data, antenna, antennas)
        # print('Harmonics for ', antenna)
        # draw_state(data, antenna_antinode_positions)
        # print('=============================')

        for antinode in antenna_antinode_positions:
            antinode_set.add(antinode)

    # draw_state(data, antinode_set)

    return len(antinode_set)


if __name__ == '__main__':
    data = read_input()
    # print('first solution:', solve_first(data))
    print('second solution:', solve_second(data))