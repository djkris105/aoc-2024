from typing import Tuple, List, Dict, Set
from collections import defaultdict


OrderingHashTable = Dict[int, Set[int]]
INPUT_FILE = "input.txt"


class OrderingRule:
    def __init__(self, before: int, after: int) -> None:
        self.before = before
        self.after = after

    @staticmethod
    def parse(text: str):
        return OrderingRule(*(int(token) for token in text.split("|")))


class ProductionRule:
    def __init__(self, rules: List[int]) -> None:
        self.rules = rules

    def __len__(self) -> int:
        return len(self.rules)

    def __iter__(self):
        for i, item in enumerate(self.rules):
            yield item, self.rules[i + 1:]

    def __getitem__(self, index):
        return self.rules[index]
    
    def __setitem__(self, index, value):
        self.rules[index] = value

    def get_middle_rule(self) -> int:
        return self.rules[int((len(self) - 1) / 2)]

    @staticmethod
    def parse(text: str):
        return ProductionRule([int(token) for token in text.split(",")])


def make_ordering_hashtable(rules: List[OrderingRule]) -> OrderingHashTable:
    result: OrderingHashTable = defaultdict(set)
    
    for r in rules:
        result[r.before].add(r.after)

    return result


def are_values_before(ordering: OrderingHashTable, before: int, after: List[int]) -> bool:
    # check that the values in after do not have a rule telling them to be before "before"
    return all(is_value_before(ordering, before, a) for a in after)


def is_value_before(ordering: OrderingHashTable, before: int, after: int) -> bool:
    if not after in ordering:
        return True
    
    # this rules tells us if "before" should actually be after "after"
    rules = ordering[after]
    if before in rules:
        return False
    
    return True


def make_update_page_before(p_rule: ProductionRule, should_be_after_index: int, should_be_before_index: int) -> ProductionRule:
    rules = p_rule.rules
    p_rule.rules = rules[:should_be_after_index] + \
        [rules[should_be_before_index]] + \
            rules[should_be_after_index:should_be_before_index] + \
                rules[should_be_before_index + 1:]
    
    return p_rule


def swap_pages(p_rule: ProductionRule, i: int, j: int) -> ProductionRule:
    tmp = p_rule[i]
    p_rule[i] = p_rule[j]
    p_rule[j] = tmp
    return p_rule


def read_input() -> Tuple[List[OrderingRule], List[ProductionRule]]:
    ordering_rules: List[OrderingRule] = []
    production_rules: List[ProductionRule] = []

    with open(INPUT_FILE, 'r') as f:
        ordering_flag = True
        while ordering_flag:
            line = f.readline().strip()
            if len(line) == 0:
                ordering_flag = False
                break

            ordering_rules.append(OrderingRule.parse(line))

        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue

            production_rules.append(ProductionRule.parse(line))

    return ordering_rules, production_rules


def solve_first(ordering: List[OrderingRule], production: List[ProductionRule]) -> int:
    ordering_table = make_ordering_hashtable(ordering)
    result = 0

    for p_rule in production:
        valid = True

        for update_before, update_rest in p_rule:
            if not are_values_before(ordering_table, update_before, update_rest):
                valid = False
                break

        if valid:
            result += p_rule.get_middle_rule()

    return result


def solve_second(ordering: List[OrderingRule], production: List[ProductionRule]) -> int:
    ordering_table = make_ordering_hashtable(ordering)
    result = 0

    for p_rule in production:
        valid = True

        i = 0
        while i < len(p_rule):
            x = p_rule[i]
            
            j = i + 1
            while j < len(p_rule):
                y = p_rule[j]
                if not is_value_before(ordering_table, x, y):
                    valid = False

                    # must but y before x, then update the variables
                    p_rule = swap_pages(p_rule, i, j)
                    # p_rule = make_update_page_before(p_rule, i, j)
                    x = y

                    # restart check
                    j = i
                j += 1
            i += 1

        if not valid:
            result += p_rule.get_middle_rule()

    return result


if __name__ == '__main__':
    ordering, production = read_input()
    print('first solution: ', solve_first(ordering, production))
    print('second solution: ', solve_second(ordering, production))