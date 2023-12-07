from lark import Lark, Transformer, v_args
from typing import Literal
from dataclasses import dataclass

GRAMMAR = r"""
?cards: card+

card: "Card" card_id ":" winning_numbers "|" my_numbers

?card_id: INT

winning_numbers: INT+

my_numbers: INT+

%import common.INT
%import common.WS
%ignore WS
"""


@dataclass
class Card:
    card_id: int
    winning_numbers: list[int]
    my_numbers: list[int]

    @property
    def matches(self):
        return len(set(self.winning_numbers) & set(self.my_numbers))

    @property
    def value(self):
        matches = self.matches
        if not matches:
            return 0
        return 2 ** (matches - 1)

@v_args(inline=True)
class GamesTransformer(Transformer):

    def INT(self, n):
        return int(n)
    
    def winning_numbers(self, *numbers):
        return numbers
    
    def my_numbers(self, *numbers):
        return numbers
    
    def card(self, card_id, winning_numbers, my_numbers):
        return Card(card_id, winning_numbers, my_numbers)
    
    def cards(self, *cards):
        return cards


def parse_cards(input: str) -> list[Card]:
    l = Lark(GRAMMAR, start="cards")
    tree = l.parse(input)
    games = GamesTransformer().transform(tree)
    return games


SAMPLE = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def process_part1(cards: list[Card]) -> int:
    return sum(card.value for card in cards)


def process_part2(cards: list[Card]) -> int:
    copies = [0 for _ in range(len(cards))]
    for i, card in enumerate(cards):
        copies[i] += 1
        matches = card.matches
        for j in range(matches):
            copies[i + j + 1] += copies[i]
    return sum(copies)


def main():
    with open("inputs/day4.txt") as f:
        lines = f.readlines()
    input = "\n".join(lines)
    cards = parse_cards(input)
    part1 = process_part1(cards)
    print(f"part1: {part1}")
    part2 = process_part2(cards)
    print(f"part2: {part2}")


if __name__ == "__main__":
    main()
