from typing import List, Tuple, Set, Optional
from enum import Enum
from collections import Counter

import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)


INPUT_FILE = "input.txt"


class Dir(Enum):
    N = 0
    S = 1
    W = 2
    E = 3

    def turn_90_degrees(self):
        if self == Dir.N:
            return Dir.E
        if self == Dir.E:
            return Dir.S
        if self == Dir.S:
            return Dir.W
        return self.N


Vector = Tuple[int, int, Dir]


class Map:
    def __init__(self, width: int, height: int, obstacles: List[Tuple[int, int]]) -> None:
        self.width = width
        self.height = height
        self.obstacle_set = {(x, y) for x, y in obstacles}
    
    def __contains__(self, other: Tuple[int, int]) -> bool:
        return other in self.obstacle_set

    def is_out_of_bounds(self, position: Tuple[int, int]) -> bool:
        x, y = position
        if x < 0 or y < 0:
            return True
        
        if x >= self.width or y >= self.height:
            return True
        
        return False


class Guard:
    def __init__(self, starting_pos: Tuple[int, int], direction: Dir): # starting position (x, y)
        self.x = starting_pos[0]
        self.y = starting_pos[1]
        self.direction = direction

    def next_state(self, position: Tuple[int, int], direction: Dir):
        self.x = position[0]
        self.y = position[1]
        self.direction = direction

    def get_vector(self) -> Vector:
        return (self.x, self.y, self.direction)
    
    def get_copy(self):
        return Guard((self.x, self.y), self.direction)


class Trace:
    trace_list: List[Vector]
    trace_set: Counter[Vector]

    def __init__(self):
        self.trace_list = []
        self.trace_set = Counter()

    def add(self, v: Vector):
        self.trace_list.append(v)
        self.trace_set[v] += 1

    def pop(self) -> Vector:
        last_vector = self.trace_list.pop()
        self.trace_set[last_vector] -= 1
        
        if self.trace_set[last_vector] == 0:
            self.trace_set.pop(last_vector)


class LoopConfiguration:
    def __init__(self, loop_configuration: Counter[Vector], jolly_used: Tuple[int, int]) -> None:
        self.loop_configuration = loop_configuration
        self.loop_identity = frozenset(loop_configuration.keys())
        self.jolly_used = jolly_used

    def __eq__(self, value: object) -> bool:
        if isinstance(value, LoopConfiguration):
            return self.loop_identity == value.loop_identity
        
        return False
    
    def __hash__(self) -> int:
        return hash(self.loop_identity)


class DebugHelper:
    @staticmethod
    def get_guard_position(g: Guard):
        if g.direction == Dir.N:
            return '^'
        elif g.direction == Dir.E:
            return '>'
        elif g.direction == Dir.W:
            return '<'
        elif g.direction == Dir.S:
            return 'v'

    @staticmethod
    def print_state(m: Map, g: Guard, marked: Set[Tuple[int, int]] = set(), jolly: Optional[Tuple[int, int]] = None):
        buffer = ''

        for y in range(m.height):
            for x in range(m.width):
                if (x, y) in marked:
                    buffer += 'X'
                elif (x, y) in m:
                    buffer += '#'
                elif g.x == x and g.y == y:
                    buffer += DebugHelper.get_guard_position(g)
                elif jolly is not None and (x, y) == jolly:
                    buffer += 'O'
                else:
                    buffer += '.'
            
            buffer += '\n'

        print(buffer)

    @staticmethod
    def vector_to_marked(vector: Set[Vector]) -> Set[Tuple[int, int]]:
        marked: Set[Tuple[int, int]] = set()

        for v in vector:
            marked.add((v[0], v[1]))
    
        return marked


def next_position_by_direction(guard: Guard):
    d = guard.direction
    x, y = guard.x, guard.y
    if d == Dir.N:
        return x, y - 1
    elif d == Dir.S:
        return x, y + 1
    elif d == Dir.E:
        return x + 1, y
    elif d == Dir.W:
        return x - 1, y

    raise Exception("Direction not handled", d)


def solve_first(p_map: Map, guard: Guard) -> Set[Tuple[int, int]]:
    marked: Set[Tuple[int, int]] = { (guard.x, guard.y) }

    while True:
        next_position = next_position_by_direction(guard)
        if p_map.is_out_of_bounds(next_position):
            break

        if next_position in p_map:  # is an obstacle
            guard.direction = guard.direction.turn_90_degrees()
            continue

        guard.x = next_position[0]
        guard.y = next_position[1]
        marked.add(next_position)

    return marked


def solve_second(p_map: Map, starting_guard: Guard) -> List[LoopConfiguration]:

    def would_make_a_loop(position: Tuple[Vector], previous: Set[Vector]) -> bool:
        return position in previous

    def next_state(prev: Trace, guard: Guard, jolly_used: Optional[Tuple[int, int]], results: Set[LoopConfiguration]):
        guard = guard.get_copy()

        should_pop: bool = len(prev.trace_list) == 0 or prev.trace_list[-1] != guard.get_vector()
        if should_pop:
            prev.add(guard.get_vector())

        next_position = next_position_by_direction(guard)

        # if oob, we didn't find a loop
        if p_map.is_out_of_bounds(next_position):
            if should_pop: prev.pop()
            return
        
        # if an obstacle is found, we have to turn right
        if next_position in p_map or next_position == jolly_used:
            guard.direction = guard.direction.turn_90_degrees()

            if not would_make_a_loop(guard.get_vector(), prev.trace_set):
                next_state(prev, guard, jolly_used, results)
            else:
                results.add(LoopConfiguration(prev.trace_set.copy(), jolly_used))

            if should_pop: prev.pop()
            return

        if would_make_a_loop(next_position, prev.trace_set):
            # we found a loop! register and return
            results.add(LoopConfiguration(prev.trace_set.copy(), jolly_used))
            if should_pop: prev.pop()
            return
        
        # it doesn't make a loop, so we can either continue going in that direction
        # or try to put an obstacle
        # let's try to put a jolly first
        if jolly_used is None:
            next_state(prev, guard, next_position, results)
        
        # continue without putting out a jolly
        guard.x = next_position[0]
        guard.y = next_position[1]

        next_state(prev, guard, jolly_used, results)
        if should_pop: prev.pop()

    trace = Trace()
    results: Set[LoopConfiguration] = set()

    next_state(trace, starting_guard, None, results)
    return results


def read_input() -> Tuple[Map, Guard]:
    map_data = []
    guard_starting_pos = None
    guard_starting_dir = None

    with open(INPUT_FILE, 'r') as f:
        cur_x = -1
        cur_y = -1

        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            
            cur_x = -1
            cur_y += 1
            for c in line:
                cur_x += 1

                if c == '#':
                    map_data.append((cur_x, cur_y))
                elif c == '^':
                    guard_starting_pos = (cur_x, cur_y)
                    guard_starting_dir = Dir.N
                elif c == '>':
                    guard_starting_pos = (cur_x, cur_y)
                    guard_starting_dir = Dir.E
                elif c == 'v':
                    guard_starting_pos = (cur_x, cur_y)
                    guard_starting_dir = Dir.S
                elif c == '<':
                    guard_starting_pos = (cur_x, cur_y)
                    guard_starting_dir = Dir.W
    
    return Map(cur_x + 1, cur_y + 1, map_data), Guard(guard_starting_pos, guard_starting_dir)


if __name__ == '__main__':
    p_map, guard = read_input()
    # marked = solve_first(p_map, guard.get_copy())
    # print('First solution', len(marked))

    loop_configuration = solve_second(p_map, guard.get_copy())
    for configuration in loop_configuration:
        DebugHelper.print_state(p_map, guard, DebugHelper.vector_to_marked(configuration.loop_configuration), configuration.jolly_used)
    print('Second solution', len(loop_configuration))