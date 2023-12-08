from lark import Lark, Transformer, v_args
from typing import Optional
from dataclasses import dataclass
from collections import defaultdict

GRAMMAR = r"""
?start: times distances

times: "Time:" INT+
distances: "Distance:" INT+

%import common.INT
%import common.WS
%import common.WORD
%ignore WS
"""    

PART2_GRAMMAR = r"""
?start: times distances

times: "Time:" spaced_number
distances: "Distance:" spaced_number

spaced_number: DIGIT+

%import common.INT
%import common.DIGIT
%import common.WS
%import common.WORD
%ignore WS
"""

@dataclass
class InputData:
    races: list[(int, int)]

class InputTransformer(Transformer):
    INT = int
    DIGIT = str
    times = list
    distances = list
    
    @v_args(inline=True)
    def start(self, times, distances):
        return InputData(list(zip(times, distances)))
    
    @v_args(inline=True)
    def spaced_number(self, *args):
        return int(''.join(args))


def parse_input(input: str, grammar = GRAMMAR) -> InputData:
    l = Lark(grammar, start="start")
    tree = l.parse(input)
    data = InputTransformer().transform(tree)
    return data


SAMPLE = """Time:      7  15   30
Distance:  9  40  200"""


def dist(total_time: int, hold_time: int) -> int:
        return (total_time - hold_time) * hold_time

def process_part1(data: InputData) -> int:        
    ways = 1
    for time, distance in data.races:
        ways *= sum([1 for h in range(1, time) if dist(time, h) > distance])
    return ways

def process_part2(data: InputData) -> int:
    time, distance = data.races[0]
    return sum([1 for h in range(1, time) if dist(time, h) > distance])


def main():
    with open("inputs/day6.txt") as f:
        lines = f.readlines()
    input = "\n".join(lines)
    data = parse_input(input)
    part1 = process_part1(data)
    print(f"part1: {part1}")

    data = parse_input(input, PART2_GRAMMAR)
    part2 = process_part2(data)
    print(f"part2: {part2}")


if __name__ == "__main__":
    main()
