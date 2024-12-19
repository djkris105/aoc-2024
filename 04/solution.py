from typing import List
from enum import Enum
from itertools import repeat


class Dir(Enum):
    N = 0
    S = 1
    W = 2
    E = 3
    NW = 4
    NE = 5
    SW = 6
    SE = 7


INPUT_FILE = 'input.txt'
ALL_DIRS = [Dir.N, Dir.S, Dir.W, Dir.E, Dir.NW, Dir.NE, Dir.SW, Dir.SE]


def read_input() -> List[str]:
    data = []

    with open(INPUT_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) <= 0:
                continue

            data.append(line)

    return data


def first_solution(data: List[str], text: str) -> int:
    h = len(data)
    w = len(data[0])

    result = 0
    for y in range(h):
        for x in range(w):
            for d in ALL_DIRS:
                substr = get_slice(data, y, x, d, len(text))
                if substr == text or reversed(text) == substr:
                    result += 1

    return result


def second_solution(data: List[str], text: str) -> int:
    h = len(data)
    w = len(data[0])
    result = 0

    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if data[y][x] != 'A':
                continue

            to_right = get_slice(data, y - 1, x - 1, Dir.SE, 3)
            to_left = get_slice(data, y - 1, x + 1, Dir.SW, 3)

            if to_right != text and to_right[::-1] != text:
                continue
            if to_left != text and to_left[::-1] != text:
                continue

            result += 1

    return result


def get_slice(data: List[str], start_row: int, start_col: int, dir: Dir, text_size: int) -> str:
    end_row = start_row
    end_col = start_col
    
    if dir == Dir.N or dir == Dir.NW or dir == Dir.NE:
        end_row = start_row - text_size 
    elif dir == Dir.S or dir == Dir.SW or dir == Dir.SE:
        end_row = start_row + text_size

    if dir == Dir.W or dir == Dir.NW or dir == Dir.SW:
        end_col = start_col - text_size
    elif dir == Dir.E or dir == Dir.NE or dir == Dir.SE:
        end_col = start_col + text_size

    if end_row < -1 or end_col < -1 or end_row > len(data) or end_col > len(data[0]):
        return ''

    acc = ''
    it_row = range(start_row, end_row, 1 if end_row > start_row else -1) if start_row != end_row else repeat(start_row, text_size)
    it_col = range(start_col, end_col, 1 if end_col > start_col else -1) if start_col != end_col else repeat(start_col, text_size)
    for (y, x) in zip(it_row, it_col):
        acc += data[y][x]
            
    # print(dir.name, '\t', f'row:[{start_row}, {end_row}]', '\t', f'col:[{start_col},{end_col}]', '\t', acc)

    return acc


if __name__ == '__main__':
    data = read_input()
    print(first_solution(data, 'XMAS'))
    print(second_solution(data, 'MAS'))