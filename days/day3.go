package main

import (
	"fmt"
	"log"
	"os"
	"strings"
)

// Create a padded schematic based on the input lines
func makeSchematic(lines []string) [][]rune {
	h := len(lines)
	w := len(lines[0])
	schematic := make([][]rune, h+2)

	// fill first row with dots
	schematic[0] = make([]rune, w+2)
	for i := range schematic[0] {
		schematic[0][i] = '.'
	}

	for i, line := range lines {
		schematic[i+1] = make([]rune, w+2)
		schematic[i+1][0] = '.'
		schematic[i+1][w+1] = '.'
		for j, char := range line {
			schematic[i+1][j+1] = char
		}
	}

	// fill last row with dots
	schematic[h+1] = make([]rune, w+2)
	for i := range schematic[h+1] {
		schematic[h+1][i] = '.'
	}

	return schematic
}

func isSymbol(r rune) bool {
	return r != '.' && (r < '0' || r > '9')
}

func isNumber(r rune) bool {
	return r >= '0' && r <= '9'
}

func part1(lines []string) int {
	schematic := makeSchematic(lines)
	sum := 0

	for r := 1; r < len(schematic)-1; r++ {
		c := 0
		for c < len(schematic[r]) {
			// seek to first number
			for c < len(schematic[r]) && !isNumber(schematic[r][c]) {
				c++
			}
			found := false
			num := 0
			// check if left, top-left or bottom left are symbols
			if isSymbol(schematic[r-1][c-1]) || isSymbol(schematic[r][c-1]) || isSymbol(schematic[r+1][c-1]) {
				found = true
			}
			// seek to the next not number
			for c < len(schematic[r]) && isNumber(schematic[r][c]) {
				// check if the top or bottom are symbols
				if isSymbol(schematic[r-1][c]) || isSymbol(schematic[r+1][c]) {
					found = true
				}
				num = num*10 + int(schematic[r][c]-'0')
				c++
			}

			// if c is not the end of the row, check if the right, top-right, bottom-right are symbols
			if c < len(schematic[r]) && (isSymbol(schematic[r-1][c]) || isSymbol(schematic[r][c]) || isSymbol(schematic[r+1][c])) {
				found = true
			}

			if found {
				sum += num
			}
			c++
		}
	}

	return sum
}

// given a cell of the schematic that is part of a number, expand to the left and right and extract the number
func expandNumber(schematic [][]rune, r, c int) int {
	cur := c
	// rewind to beginning of number
	for cur > 0 && isNumber(schematic[r][cur-1]) {
		cur--
	}

	num := 0
	for cur < len(schematic[r]) && isNumber(schematic[r][cur]) {
		num = num*10 + int(schematic[r][cur]-'0')
		cur++
	}
	return num
}

func part2(lines []string) int {
	schematic := makeSchematic(lines)

	sum := 0
	for r := 1; r < len(schematic)-1; r++ {
		for c := 0; c < len(schematic[r]); c++ {
			// skip non gear icon cells
			if schematic[r][c] != '*' {
				continue
			}

			partNumbers := make([]int, 0)

			// check if top
			if isNumber(schematic[r-1][c]) {
				num := expandNumber(schematic, r-1, c)
				partNumbers = append(partNumbers, num)
			} else {
				// check if top-left
				if isNumber(schematic[r-1][c-1]) {
					num := expandNumber(schematic, r-1, c-1)
					partNumbers = append(partNumbers, num)
				}

				// check if top-right
				if isNumber(schematic[r-1][c+1]) {
					num := expandNumber(schematic, r-1, c+1)
					partNumbers = append(partNumbers, num)
				}
			}

			// check if left
			if isNumber(schematic[r][c-1]) {
				num := expandNumber(schematic, r, c-1)
				partNumbers = append(partNumbers, num)
			}

			// check if right
			if isNumber(schematic[r][c+1]) {
				num := expandNumber(schematic, r, c+1)
				partNumbers = append(partNumbers, num)
			}

			// check if bottom
			if isNumber(schematic[r+1][c]) {
				num := expandNumber(schematic, r+1, c)
				partNumbers = append(partNumbers, num)
			} else {
				// check if bottom-left
				if isNumber(schematic[r+1][c-1]) {
					num := expandNumber(schematic, r+1, c-1)
					partNumbers = append(partNumbers, num)
				}

				// check if bottom-right
				if isNumber(schematic[r+1][c+1]) {
					num := expandNumber(schematic, r+1, c+1)
					partNumbers = append(partNumbers, num)
				}
			}

			if len(partNumbers) == 2 {
				// it is a gear, compute gear ratio
				ratio := partNumbers[0] * partNumbers[1]
				sum += ratio
			}
		}
	}
	return sum
}

func main() {
	content, err := os.ReadFile("inputs/day3.txt")
	if err != nil {
		log.Fatal(err)
	}

	lines := strings.Split(string(content), "\n")

	sum := part1(lines)
	fmt.Printf("Part 1: %v\n", sum)

	sum = part2(lines)
	fmt.Printf("Part 2: %v\n", sum)
}
