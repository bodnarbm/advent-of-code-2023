from lark import Lark, Transformer
from typing import Literal
from dataclasses import dataclass

GRAMMAR = r"""
?games: game+

game: "Game" game_id ":" sets

sets: set (";" set)*

set: subset ("," subset)*

subset: count color

game_id: INT
count: INT
!color: "red" | "green" | "blue"

%import common.INT
%import common.WS
%ignore WS
"""


@dataclass
class Subset:
    count: int
    color: Literal["red", "green", "blue"]


@dataclass
class Set:
    subsets: list[Subset]


@dataclass
class Game:
    id: int
    sets: list[Set]


class GamesTransformer(Transformer):
    def color(self, tokens):
        return tokens[0].value

    def count(self, tokens):
        return int(tokens[0].value)

    def subset(self, tokens):
        return Subset(tokens[0], tokens[1])

    def set(self, tokens):
        return Set(tokens)

    def game_id(self, tokens):
        return int(tokens[0].value)

    def sets(self, tokens):
        return tokens

    def game(self, tokens):
        return Game(tokens[0], tokens[1])

    def games(self, tokens):
        return tokens


def parse_games(input: str) -> list[Game]:
    l = Lark(GRAMMAR, start="games")
    tree = l.parse(input)
    games = GamesTransformer().transform(tree)
    return games


SAMPLE = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

PART_1_CONSTRANTS = {"red": 12, "green": 13, "blue": 14}


def is_valid(game: Game) -> bool:
    for set in game.sets:
        color_counts = {subset.color: subset.count for subset in set.subsets}
        for color in PART_1_CONSTRANTS:
            if color_counts.get(color, 0) > PART_1_CONSTRANTS[color]:
                return False
    return True


def minumum_needed(game: Game) -> dict[str, int]:
    maxes = {}
    for set in game.sets:
        for subset in set.subsets:
            maxes[subset.color] = max(maxes.get(subset.color, 0), subset.count)
    return maxes


def power(cubes: dict[str, int]) -> int:
    product = 1
    for color in cubes:
        product *= cubes[color]
    return product


def process_part1(games: list[Game]) -> int:
    return sum(game.id for game in games if is_valid(game))


def process_part2(games: list[Game]) -> int:
    return sum(power(minumum_needed(game)) for game in games)


def main():
    with open("inputs/day2.txt") as f:
        lines = f.readlines()
    input = "\n".join(lines)
    games = parse_games(input)
    part1 = process_part1(games)
    print(f"part1: {part1}")
    part2 = process_part2(games)
    print(f"part2: {part2}")


if __name__ == "__main__":
    main()
