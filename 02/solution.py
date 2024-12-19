from typing import List


PROBLEM_INPUT = 'input.txt'


def read_input():
    reports = []

    with open(PROBLEM_INPUT, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue

            report = [int(level_str) for level_str in line.split(" ")]
            reports.append(report)
    
    return reports


def is_safe(report: List[int], remove_level = -1):
    if remove_level is not None and remove_level >= len(report):
        return False
    
    original_report = report
    report = report \
        if remove_level is None or remove_level < 0 \
        else report[:remove_level] + report[remove_level + 1:]

    direction = 1 if report[0] > report[1] else -1
    prev_value = report[0]

    for level in report[1:]:
        delta = prev_value - level
        prev_value = level

        if delta * direction <= 0 or abs(delta) > 3:
            if remove_level is None:
                return False

            return is_safe(original_report, remove_level + 1)
            
    return True


def first_solution(reports: List[List[int]]):
    return sum(1 for r in reports if is_safe(r, None))


def second_solution(reports: List[List[int]]):
    return sum(1 for r in reports if is_safe(r, -1))


if __name__ == '__main__':
    reports = read_input()
    safe_reports = first_solution(reports)
    print('first_solution', safe_reports)

    safe_w_dampener_reports = second_solution(reports)
    print('second_solution', safe_w_dampener_reports)