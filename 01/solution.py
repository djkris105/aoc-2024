from typing import List

def read_file():
    with open('input.txt', 'r') as f:
        first_list = []
        second_list = []

        for line in f:
            line = line.strip()
            if len(line) == 0:
                break

            tokens = line.split("   ")
            first_list.append(int(tokens[0]))
            second_list.append(int(tokens[1]))

    return sorted(first_list), sorted(second_list)


def solution_first(first: List[int], second: List[int]):
    acc = 0

    while len(first) > 0:
        x = first.pop(0)
        y = second.pop(0)

        acc += abs(x - y)

    return acc


def solution_second(first: List[int], second: List[int]):
    acc = 0

    for x in first:
        ntimes = sum(1 for y in second if y == x)
        acc += x * ntimes
    
    return acc


if __name__ == '__main__':
    f, s = read_file()
    distance = solution_second(f, s)

    print(distance)
