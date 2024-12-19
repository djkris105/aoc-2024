from typing import List, Union, Literal, Tuple


INPUT_FILE = "input.txt"


DISK_MAP = List[Union[Literal['.'], int]]
DISK_DESCRIPTION = List[Tuple[Union[Literal['.'], int], int]]


def read_input() -> str:
    with open(INPUT_FILE, 'r') as f:
        return f.readline().strip()


def input_to_representation(disk_map: str) -> DISK_MAP:
    disk = []
    curr_id = 0

    # even characters are file blocks, odd characters are free space blocks
    for i, c in enumerate(disk_map):
        block_count = int(c)

        if i % 2 == 0:
            if block_count == 0:
                curr_id += 1
                continue

            for _ in range(block_count):
                disk.append(curr_id)
            curr_id += 1
        else:
            if block_count == 0:
                continue

            for _ in range(block_count):
                disk.append('.')

    return disk


def compute_checksum(disk_representation: DISK_MAP):
    acc = 0

    for i, c in enumerate(disk_representation):
        if c == '.':
            continue

        file_id = c
        acc += i * file_id

    return acc


def solve_first(disk_map: str):
    disk = input_to_representation(disk_map)

    free_position = disk.index('.')
    def find_free_position():
        for i in range(free_position, len(disk)):
            if disk[i] == '.':
                return i
        return -1

    for i in range(len(disk) - 1, -1, -1):
        block = disk[i]
        if block == '.':
            continue

        disk[free_position] = block
        disk[i] = '.'

        free_position = find_free_position()
        if free_position == -1 or free_position >= i - 1:
            break

    return compute_checksum(disk)


def find_start_of_chunk(i: int, disk: DISK_MAP) -> int:
    file_id = disk[i]
    ptr = i 
    while disk[ptr - 1] == file_id and ptr >= 0:
        ptr -= 1
    return ptr


def find_end_of_chunk(i: int, disk: DISK_MAP) -> int:
    file_id = disk[i]
    ptr = i
    while disk[ptr + 1] == file_id and ptr < len(disk):
        ptr += 1
    return ptr + 1


def find_free_chunk(size: int, stop_at: int, disk: DISK_MAP) -> int:
    for i in range(stop_at):
        if disk[i] != '.':
            continue

        end_of_chunk = find_end_of_chunk(i, disk)
        if end_of_chunk - i >= size:
            return i

    return -1


def move_chunk(source: int, target: int, size: int, disk: DISK_MAP):
    if source == -1 or target == -1:
        return
    
    for i in range(size):
        disk[target + i] = disk[source + i]
        disk[source + i] = '.'


def solve_second(disk_map: str):
    disk = input_to_representation(disk_map)

    cur_pos = len(disk) - 1
    last_file_id = 10000
    while cur_pos > 0:
        if disk[cur_pos] == '.':
            cur_pos -= 1
            continue

        if disk[cur_pos] >= last_file_id:
            cur_pos -= 1
            continue

        last_file_id = disk[cur_pos]
        chunk_start = find_start_of_chunk(cur_pos, disk)
        chunk_size = cur_pos - chunk_start + 1

        free_chunk_start = find_free_chunk(chunk_size, chunk_start, disk)
        move_chunk(chunk_start, free_chunk_start, chunk_size, disk)
        cur_pos = chunk_start - 1

    return compute_checksum(disk)


if __name__ == '__main__':
    disk_map = read_input()
    print('first solution: ', solve_first(disk_map))
    print('second solution: ', solve_second(disk_map))