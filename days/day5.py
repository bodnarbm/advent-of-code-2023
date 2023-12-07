from lark import Lark, Transformer, v_args
from typing import Optional
from dataclasses import dataclass
from collections import defaultdict

GRAMMAR = r"""
?almanac: seeds maps

seeds: "seeds:" INT+

maps: map+

map: category "-to-" category "map:" map_line+

map_line: INT INT INT

?category: WORD

%import common.INT
%import common.WS
%import common.WORD
%ignore WS
"""


@dataclass
class ConversionRange:
    source_start: int
    dest_start: int
    range_len: Optional[int] = None

class Converter:
    def __init__(self, ranges: list[ConversionRange]) -> None:
        sorted_ranges = sorted(ranges, key=lambda r: r.source_start)
        self.ranges = []
        next_start = 0
        for r in sorted_ranges:
            if r.source_start > next_start:
                self.ranges.append(ConversionRange(next_start, next_start, r.source_start - next_start))
                next_start = r.source_start
            self.ranges.append(r)
            next_start += r.range_len
        self.ranges.append(ConversionRange(next_start, next_start, None))
        self.ranges = sorted(self.ranges, key=lambda r: r.source_start, reverse=True)

    def convert_value(self, value: int) -> int:
        closest_range = next(filter(lambda r: r.source_start <= value, self.ranges))
        return closest_range.dest_start + (value - closest_range.source_start)
    
    def convert_range(self, range: (int, int)) -> list[(int, int)]:
        range_start, range_length = range
        
        ranges = []
        current = range_start
        while current < range_start + range_length:
            closest_range = next(filter(lambda r: r.source_start <= current, self.ranges))
            s = closest_range.dest_start + (current - closest_range.source_start)
            if closest_range.range_len:
                l = min(closest_range.source_start + closest_range.range_len - current, range_start + range_length - current)
            else:
                l = range_start + range_length - current
            ranges.append((s, l))
            current += l
        return ranges
        

@dataclass
class Almanac:
    seeds: list[int]
    maps: dict[str, dict[str, list[ConversionRange]]]

class AlmanacTransformer(Transformer):
    map_line = list
    INT = int
    WORD = str
    almanac = v_args(inline=True)(Almanac)

    @v_args(inline=True)
    def seeds(self, *seeds):
        return seeds
    
    @v_args(inline=True)
    def maps(self, *maps):
        mapping = defaultdict(dict[list])
        for m in maps:
            source, dest, ranges = m
            mapping[source][dest] = ranges
        return mapping


    @v_args(inline=True)
    def map(self, source, dest, *map_lines):
        ranges = [ConversionRange(src, dst, l) for dst, src, l in map_lines]
        converter = Converter(ranges)
        return (source, dest, converter)


def parse_almanac(input: str) -> Almanac:
    l = Lark(GRAMMAR, start="almanac")
    tree = l.parse(input)
    games = AlmanacTransformer().transform(tree)
    return games


SAMPLE = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def process_part1(almanac: Almanac) -> int:
    minimum_location = None
    for seed in almanac.seeds:
        category = "seed"
        value = seed
        while category != "location":
            dest = next(iter(almanac.maps[category]))
            value = almanac.maps[category][dest].convert_value(value)
            category = dest
        if minimum_location is None or value < minimum_location:
            minimum_location = value
    return minimum_location


def process_part2(almanac: Almanac) -> int:
    ranges = [(almanac.seeds[i], almanac.seeds[i+1]) for i in range(0, len(almanac.seeds), 2)]
    category = "seed"
    while category != "location":
        dest = next(iter(almanac.maps[category]))
        ranges = [almanac.maps[category][dest].convert_range(r) for r in ranges]
        ranges = [r for sublist in ranges for r in sublist]
        category = dest
    return min(map(lambda r: r[0], ranges))


def main():
    with open("inputs/day5.txt") as f:
        lines = f.readlines()
    input = "\n".join(lines)
    cards = parse_almanac(input)
    part1 = process_part1(cards)
    print(f"part1: {part1}")
    part2 = process_part2(cards)
    print(f"part2: {part2}")


if __name__ == "__main__":
    main()
