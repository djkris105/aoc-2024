from typing import List, Tuple, Dict, Set
from enum import Enum
from collections import defaultdict


INPUT_FILE = "input.txt"
COORD = Tuple[int, int]
REGION_MAP = Dict[COORD, int]
REGION_TO_COORD = Dict[int, Set[COORD]]


class Dir(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


ALL_DIRS = [Dir.N, Dir.E, Dir.S, Dir.W]


def read_input() -> List[str]:
    data = []

    with open(INPUT_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue

            data.append(line)
    return data


def move_coord(c: COORD, d: Dir) -> COORD:
    x, y = c
    if d == Dir.N:
        return (x, y - 1)
    if d == Dir.E:
        return (x + 1, y)
    if d == Dir.S:
        return (x, y + 1)
    if d == Dir.W:
        return (x - 1, y)

    raise Exception("Unhandled direction", d)


def are_coord_safe(c: COORD, data: List[str]):
    w, h = len(data[0]), len(data)
    x, y = c
    if y < 0 or y >= h or x < 0 or x >= w:
        return False
    return True


def is_adjacent_same_region(fruit: str, fruit_pos: COORD, dir: Dir, data: List[str]):
    w, h = len(data[0]), len(data)

    x, y = fruit_pos
    x, y = move_coord(fruit_pos, dir)

    if y < 0 or y >= h or x < 0 or x >= w:
        return False
    
    return data[y][x] == fruit


def dfs_region(fruit: str, pos: COORD, data: List[str], visited: Set[COORD]):
    visited.add(pos)

    for d in ALL_DIRS:
        adj = move_coord(pos, d)
        if not are_coord_safe(adj, data):
            continue

        if adj in visited:
            continue
        
        if fruit != data[adj[1]][adj[0]]:
            continue

        dfs_region(fruit, adj, data, visited)


def find_region(pos: COORD, data: List[str]) -> Set[COORD]:
    x, y = pos
    fruit = data[y][x]

    result: Set[COORD] = { pos }
    dfs_region(fruit, pos, data, result)

    return result


def compute_perimeter(region_to_coords: REGION_TO_COORD, region_id: int) -> int:
    region_coords = region_to_coords[region_id]
    perimeter = 0

    for c in region_coords:
        perimeter += sum(1 if move_coord(c, d) not in region_coords else 0 for d in ALL_DIRS)

    return perimeter


def get_bounding_box(region_coords: Set[COORD]) -> Tuple[COORD, COORD]:
    leftmost, rightmost, topmost, bottomost = 1000000, 0, 1000000, 0

    for x, y in region_coords:
        if x < leftmost: 
            leftmost = x
        if x > rightmost:
            rightmost = x
        if y < topmost:
            topmost = y
        if y > bottomost:
            bottomost = y

    return (leftmost, topmost), (rightmost, bottomost)


def get_vertical_projection(column: int, starting_row: int, ending_row: int, region_coords: Set[COORD]) -> List[int]:
    result = []

    for x in range(starting_row, ending_row):
        result.append(1 if (column, x) in region_coords else 0)

    return result


def get_horizontal_projection(row: int, starting_col: int, ending_col: int, region_coords: Set[COORD]) -> List[int]:
    result = []

    for x in range(starting_col, ending_col):
        result.append(1 if (x, row) in region_coords else 0)

    return result


def count_sides(first_projection: List[int], second_projection: List[int]) -> int:
    counting = False
    counting_side = 0
    count = 0

    for i in range(len(first_projection)):
        if first_projection[i] + second_projection[i] == 1: # we have a side
            # check that the side is from the same side
            if counting and (counting_side == first_projection[i] or (counting_side == 2 and second_projection[i] == 1)):
                continue

            count += 1
            counting = True
            counting_side = 1 if first_projection[i] == 1 else 2
        else:
            counting = False

    return count

def compute_sides(region_to_coords: REGION_TO_COORD, region_id: int) -> int:
    region_coords = region_to_coords[region_id]
    bbox_top_left, bbox_bottom_right = get_bounding_box(region_coords)
    bbox_width = bbox_bottom_right[0] - bbox_top_left[0] + 1
    bbox_height = bbox_bottom_right[1] - bbox_top_left[1] + 1

    sides = 0
    # get all sides going N-S 
    for i in range(bbox_top_left[0], bbox_top_left[0] + bbox_width + 1):
        proj_a = get_vertical_projection(i - 1, bbox_top_left[1], bbox_bottom_right[1] + 1, region_coords)
        proj_b = get_vertical_projection(i, bbox_top_left[1], bbox_bottom_right[1] + 1, region_coords)
        sides += count_sides(proj_a, proj_b)

    # get all sides going E-W
    for j in range(bbox_top_left[1], bbox_top_left[1] + bbox_height + 1):
        proj_a = get_horizontal_projection(j - 1, bbox_top_left[0], bbox_bottom_right[0] + 1, region_coords)
        proj_b = get_horizontal_projection(j, bbox_top_left[0], bbox_bottom_right[0] + 1, region_coords)
        sides += count_sides(proj_a, proj_b)

    return sides


def compute_area(region_to_coords: REGION_TO_COORD, region_id: int) -> int:
    return len(region_to_coords[region_id])


def solve_first(data: List[str]) -> int:

    next_region_id = 0
    region_map: REGION_MAP = dict()
    region_to_coords: REGION_TO_COORD = dict()

    # find all regions
    for j, row in enumerate(data):
        for i, _ in enumerate(row):
            pos = (i, j)

            if pos in region_map:
                continue

            region = find_region(pos, data)
            region_to_coords[next_region_id] = region
            for coord in region:
                region_map[coord] = next_region_id
            next_region_id += 1

    # compute perimeter and area
    price = 0 
    for r in range(next_region_id):
        price += compute_area(region_to_coords, r) * compute_perimeter(region_to_coords, r)
    return price


def solve_second(data: List[str]) -> int:

    next_region_id = 0
    region_map: REGION_MAP = dict()
    region_to_coords: REGION_TO_COORD = dict()

    # find all regions
    for j, row in enumerate(data):
        for i, _ in enumerate(row):
            pos = (i, j)

            if pos in region_map:
                continue

            region = find_region(pos, data)
            region_to_coords[next_region_id] = region
            for coord in region:
                region_map[coord] = next_region_id
            next_region_id += 1

    # compute perimeter and area
    price = 0 
    for r in range(next_region_id):
        area = compute_area(region_to_coords, r)
        sides = compute_sides(region_to_coords, r)

        # print(r, area, sides)

        price += area * sides
    return price


if __name__ == "__main__":
    data = read_input()
    print("First solution", solve_first(data))
    print("Second solution", solve_second(data))