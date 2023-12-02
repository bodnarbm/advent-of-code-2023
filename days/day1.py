import re

WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
DIGITS = list(range(10))

WORD_VALUE_MAP = {word: idx + 1 for idx, word in enumerate(WORDS)}
DIGIT_VALUE_MAP = {str(digit): digit for digit in DIGITS}
COMBINED_VALUE_MAP = {**WORD_VALUE_MAP, **DIGIT_VALUE_MAP}


def process(lines: list[str], values: dict[str, int]):
    tokens = "|".join(values.keys())
    line_rex = re.compile(
        f"(?P<first>{tokens}).*(?P<second>{tokens})|(?P<only>{tokens})"
    )
    sum = 0
    for line in lines:
        match = line_rex.search(line)
        first = match.group("first") or match.group("only")
        second = match.group("second") or match.group("only")
        sum += COMBINED_VALUE_MAP[first] * 10 + COMBINED_VALUE_MAP[second]
    return sum


def main():
    with open("inputs/day1.txt") as f:
        lines = f.readlines()
    part1 = process(lines, DIGIT_VALUE_MAP)
    print(f"part1: {part1}")
    part2 = process(lines, COMBINED_VALUE_MAP)
    print(f"part2: {part2}")


if __name__ == "__main__":
    main()
