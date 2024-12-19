from typing import List, Tuple


INPUT_FILENAME = 'input.txt'


class Mul:
    def __init__(self, first: int, second: int) -> None:
        self.first = first
        self.second = second

    def value(self):
        return self.first * self.second


def read_input() -> List[str]:
    data = []

    with open(INPUT_FILENAME, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) <= 0:
                continue

            data.append(line)

    return data


def extract_safe_muls(line: str, second_solution_parser = False) -> List[Mul]:
    i = 0
    muls = []
    active = True

    while i < len(line):

        if second_solution_parser:
            value, j = consume_do_instruction(line, i)
            if value:
                active = True
                i = j
                continue

            value, j = consume_dont_instruction(line, i)
            if value:
                active = False
                i = j
                continue

        value, j = consume_mul_instruction(line, i)
        if value is not None:
            if active: 
                muls.append(value)

            i = j
            continue

        i += 1

    return muls


def consume_do_instruction(line: str, i: int):
    return extract_do(line, i)


def consume_dont_instruction(line: str, i: int):
    return extract_dont(line, i)


def consume_mul_instruction(line: str, i: int):
    is_mul_start, i = extract_mul(line, i)
    if not is_mul_start:
        return None, i

    first_number, i = extract_num(line, i)
    if first_number is None:
        return None, i

    cond, i = check_char(line, i, ',')
    if not cond:
        return None, i

    second_number, i = extract_num(line, i)
    if second_number is None:
        return None, i

    cond, i = check_char(line, i, ')')
    if not cond:
        return None, i

    return Mul(first_number, second_number), i


def check_str(line: str, i: int, eq_to: str) -> Tuple[bool, int]:
    cond = line[i:i+len(eq_to)] == eq_to
    return cond, i + len(eq_to) if cond else i


def check_char(line: str, i: int, c: str):
    cond = line[i] == c
    return cond, i + 1 if cond else i


def extract_mul(line: str, i: int):
    return check_str(line, i, 'mul(')


def extract_do(line: str, i: int):
    return check_str(line, i, 'do()')


def extract_dont(line: str, i: int):
    return check_str(line, i, 'don\'t()')


def extract_num(line: str, i: int):
    acc = ''
    if not line[i].isdigit():
        return None, i
    
    acc += line[i]
    i += 1

    for _ in range(2):
        if line[i].isdigit():
            acc += line[i]
            i += 1

    return int(acc), i


def first_solution(data: List[str]):
    return sum(mm.value() for m in data for mm in extract_safe_muls(m))


def second_solution(data: List[str]):
    data = ''.join(data)
    return sum(mul.value() for mul in extract_safe_muls(data, second_solution_parser=True))


if __name__ == '__main__':
    data = read_input()
    print('first solution:', first_solution(data))
    print('second solution:', second_solution(data))