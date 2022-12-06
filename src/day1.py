"""
--- Day 1: Calorie Counting ---

Santa's reindeer typically eat regular reindeer food, but they need a lot of magical energy to deliver presents on Christmas. For that, their favorite snack is a special type of star fruit that only grows deep in the jungle. The Elves have brought you on their annual expedition to the grove where the fruit grows.

To supply enough magical energy, the expedition needs to retrieve a minimum of fifty stars by December 25th. Although the Elves assure you that the grove has plenty of fruit, you decide to grab any fruit you see along the way, just in case.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

The jungle must be too overgrown and difficult to navigate in vehicles or access from the air; the Elves' expedition traditionally goes on foot. As your boats approach land, the Elves begin taking inventory of their supplies. One important consideration is food - in particular, the number of Calories each Elf is carrying (your puzzle input).

The Elves take turns writing down the number of Calories contained by the various meals, snacks, rations, etc. that they've brought with them, one item per line. Each Elf separates their own inventory from the previous Elf's inventory (if any) by a blank line.

For example, suppose the Elves finish writing their items' Calories and end up with the following list:

1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

This list represents the Calories of the food carried by five Elves:

    The first Elf is carrying food with 1000, 2000, and 3000 Calories, a total of 6000 Calories.
    The second Elf is carrying one food item with 4000 Calories.
    The third Elf is carrying food with 5000 and 6000 Calories, a total of 11000 Calories.
    The fourth Elf is carrying food with 7000, 8000, and 9000 Calories, a total of 24000 Calories.
    The fifth Elf is carrying one food item with 10000 Calories.

In case the Elves get hungry and need extra snacks, they need to know which Elf to ask: they'd like to know how many Calories are being carried by the Elf carrying the most Calories. In the example above, this is 24000 (carried by the fourth Elf).

Find the Elf carrying the most Calories. How many total Calories is that Elf
carrying?

--- Part Two ---

By the time you calculate the answer to the Elves' question, they've already realized that the Elf carrying the most Calories of food might eventually run out of snacks.

To avoid this unacceptable situation, the Elves would instead like to know the total Calories carried by the top three Elves carrying the most Calories. That way, even if one of those Elves runs out of snacks, they still have two backups.

In the example above, the top three Elves are the fourth Elf (with 24000 Calories), then the third Elf (with 11000 Calories), then the fifth Elf (with 10000 Calories). The sum of the Calories carried by these three elves is 45000.

Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?
"""

import fileinput
import heapq
import inspect
from typing import Iterable


class TopNHeap:
    """Heap that only holds N values at most."""

    def __init__(self, n: int) -> None:
        self.data: list[int] = []
        self._n = n

    def push(self, val: int) -> None:
        """
        Push new value onto heap and ensure max number of values is not
        passed.
        """
        if len(self.data) < self._n:
            heapq.heappush(self.data, val)
        else:
            heapq.heappushpop(self.data, val)

    def sum(self) -> int:
        """Get sum of all values."""
        return sum(self.data)


def find_most_calories(input_lines: Iterable[str]) -> int:
    """
    Find the elf carrying the most calories and return the total calories
    they have.
    """
    max_calories = -1
    current = 0
    for line in input_lines:
        line = line.strip()
        if line == '':
            max_calories = max(max_calories, current)
            current = 0
        else:
            current += int(line)
    max_calories = max(max_calories, current)  # Last chunk
    return max_calories


def find_top_3_calories(input_lines: Iterable[str]) -> int:
    """
    Find the top three elves carrying the most calories and return the total
    calories they have.
    """
    num_top_elves = 3
    tops = TopNHeap(num_top_elves)

    current = 0
    for line in input_lines:
        line = line.strip()
        if line == '':
            tops.push(current)
            current = 0
        else:
            current += int(line)
    tops.push(current)  # Last chunk

    return tops.sum()


def main() -> int:
    calories = find_most_calories(fileinput.input(encoding='utf-8'))
    print(f'Part 1: {calories}')
    top_3_calories = find_top_3_calories(fileinput.input(encoding='utf-8'))
    print(f'Part 2: {top_3_calories}')
    return 0


def example_part1() -> None:
    """Given example case for part 1."""
    sample_input = inspect.cleandoc(
        """
        1000
        2000
        3000

        4000

        5000
        6000

        7000
        8000
        9000

        10000
        """
    ).splitlines(keepends=True)
    assert find_most_calories(sample_input) == 24000


def example_part2() -> None:
    """Given example case for part 2."""
    sample_input = inspect.cleandoc(
        """
        1000
        2000
        3000

        4000

        5000
        6000

        7000
        8000
        9000

        10000
        """
    ).splitlines(keepends=True)
    assert find_top_3_calories(sample_input) == 45000


if __name__ == '__main__':
    example_part1()
    example_part2()
    raise SystemExit(main())
