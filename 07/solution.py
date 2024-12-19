from typing import List, Tuple
from enum import Enum


class ElephantOperators(Enum):
    CONCAT = 0
    ADD = 1
    MUL = 2

    def combine(self, left: int, right: int) -> int:
        if self == ElephantOperators.CONCAT:
            return int(str(left) + str(right))
        if self == ElephantOperators.ADD:
            return left + right
        if self == ElephantOperators.MUL:
            return left * right


class CalibrationTest:
    def __init__(self, calibration_value: int, equation_terms: List[int]):
        self.calibration_value = calibration_value
        self.equation_terms = equation_terms

    def __repr__(self):
        return str(self.calibration_value) + ': ' + ' '.join(str(t) for t in self.equation_terms)


INPUT_FILE = "input.txt"


def read_input() -> List[CalibrationTest]:
    data: List[CalibrationTest] = []

    with open(INPUT_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue

            tokens = line.split(":")
            calibration_value = int(tokens[0])
            eq_terms = [int(t) for t in tokens[1].split(" ") if len(t.strip()) > 0]

            data.append(CalibrationTest(calibration_value, eq_terms))

    return data


def search_combinatorial_equality(acc: int, 
                                  terms: List[int], 
                                  supported_operators: List[ElephantOperators], 
                                  search_value: int,
                                  trace: List[ElephantOperators]) -> Tuple[bool, List[ElephantOperators]]:
    if len(terms) == 0:
        if acc == search_value:
            return True, trace
        return False, trace
    
    for op in supported_operators:
        
        test, result_trace = search_combinatorial_equality(op.combine(acc, terms[0]), terms[1:], supported_operators, search_value, trace + [op])

        # small early exit optimization
        if test:
            return True, result_trace

    return False, trace


def test_solution(c: CalibrationTest, trace: List[ElephantOperators]):
    acc = c.equation_terms[0]
    for i, term in enumerate(c.equation_terms[1:]):
        acc = trace[i].combine(acc, term)
    
    if acc != c.calibration_value:
        raise Exception("Exception with equation solving for", c, "with trace", trace)


def solve_first(data: List[CalibrationTest]):
    supported_ops = [ElephantOperators.ADD, ElephantOperators.MUL]
    total = 0

    for d in data:
        pred = search_combinatorial_equality(0, d.equation_terms, supported_ops, d.calibration_value)
        if not pred:
            continue

        total += d.calibration_value

    return total


def solve_second(data: List[CalibrationTest]):
    supported_ops = [ElephantOperators.CONCAT, ElephantOperators.ADD, ElephantOperators.MUL]
    total = 0

    for d in data:
        pred, trace = search_combinatorial_equality(d.equation_terms[0], d.equation_terms[1:], supported_ops, d.calibration_value, [])
        if not pred:
            continue

        test_solution(d, trace)

        total += d.calibration_value

    return total


if __name__ == '__main__':
    data = read_input()
    # print('first solution:', solve_first(data))
    print('second solution:', solve_second(data))