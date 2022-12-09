"""
--- Day 4: Camp Cleanup ---

Space needs to be cleared before the last supplies can be unloaded from the ships, and so several Elves have been assigned the job of cleaning up sections of the camp. Every section has a unique ID number, and each Elf is assigned a range of section IDs.

However, as some of the Elves compare their section assignments with each other, they've noticed that many of the assignments overlap. To try to quickly find overlaps and reduce duplicated effort, the Elves pair up and make a big list of the section assignments for each pair (your puzzle input).

For example, consider the following list of section assignment pairs:

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8

For the first few pairs, this list means:

    Within the first pair of Elves, the first Elf was assigned sections 2-4 (sections 2, 3, and 4), while the second Elf was assigned sections 6-8 (sections 6, 7, 8).
    The Elves in the second pair were each assigned two sections.
    The Elves in the third pair were each assigned three sections: one got sections 5, 6, and 7, while the other also got 7, plus 8 and 9.

This example list uses single-digit section IDs to make it easier to draw; your actual list might contain larger numbers. Visually, these pairs of section assignments look like this:

.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

...45678.  4-8
.23456...  2-6

Some of the pairs have noticed that one of their assignments fully contains the other. For example, 2-8 fully contains 3-7, and 6-6 is fully contained by 4-6. In pairs where one assignment fully contains the other, one Elf in the pair would be exclusively cleaning sections their partner will already be cleaning, so these seem like the most in need of reconsideration. In this example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?

--- Part Two ---

It seems like there is still quite a bit of duplicate work planned. Instead, the Elves would like to know the number of pairs that overlap at all.

In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't overlap, while the remaining four pairs (5-7,7-9, 2-8,3-7, 6-6,4-6, and 2-6,4-8) do overlap:

    5-7,7-9 overlaps in a single section, 7.
    2-8,3-7 overlaps all of the sections 3 through 7.
    6-6,4-6 overlaps in a single section, 6.
    2-6,4-8 overlaps in sections 4, 5, and 6.

So, in this example, the number of overlapping assignment pairs is 4.

In how many assignment pairs do the ranges overlap?
"""

import fileinput
import re
from inspect import cleandoc
from typing import Iterable, NamedTuple

_LINE_PATTERN = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')


class SectionAssignment(NamedTuple):
    """Section assignment for a given elf."""

    start: int
    end: int


class ElfPair(NamedTuple):
    """Pair of two elf section assignments."""

    first: SectionAssignment
    second: SectionAssignment


def parse_pair_line(line: str) -> ElfPair:
    """Parse a data line into a pair of elf section assignments."""
    line.strip()
    matches = _LINE_PATTERN.match(line)
    if matches is None:
        raise ValueError(f'Input not in correct format: {line}')
    first_start = int(matches.group(1))
    first_end = int(matches.group(2))
    second_start = int(matches.group(3))
    second_end = int(matches.group(4))
    pair = ElfPair(
        SectionAssignment(first_start, first_end),
        SectionAssignment(second_start, second_end),
    )
    return pair


def determine_if_redundant_assignment(pair: ElfPair) -> bool:
    """Determine if a pair of elves has a redundant assignment."""
    first, second = pair
    return (first.start >= second.start and first.end <= second.end) or (
        second.start >= first.start and second.end <= first.end
    )


def determine_if_overlapping_assignment(pair: ElfPair) -> bool:
    """Determine if a pair of elves has any overlap in their assignment."""
    first, second = pair
    return (first.start >= second.start and first.start <= second.end) or (
        second.start >= first.start and second.start <= first.end
    )


def find_number_of_redundant_assignments(data_lines: Iterable[str]) -> int:
    """Find number of redundant assignments for each pair of elves."""
    return [
        determine_if_redundant_assignment(parse_pair_line(line)) for line in data_lines
    ].count(True)


def find_number_of_overlapping_assignments(data_lines: Iterable[str]) -> int:
    """Find number of overlapping assignments for each pair of elves."""
    return [
        determine_if_overlapping_assignment(parse_pair_line(line))
        for line in data_lines
    ].count(True)


def main() -> int:
    """Main entry point."""
    redundancies = find_number_of_redundant_assignments(
        fileinput.input(encoding='utf-8')
    )
    print(f'Part 1: {redundancies}')
    overlaps = find_number_of_overlapping_assignments(fileinput.input(encoding='utf-8'))
    print(f'Part 2: {overlaps}')
    return 0


def examples() -> None:
    """Given example cases."""
    sample_input = cleandoc(
        """
        2-4,6-8
        2-3,4-5
        5-7,7-9
        2-8,3-7
        6-6,4-6
        2-6,4-8
        """
    ).splitlines(keepends=True)
    assert find_number_of_redundant_assignments(sample_input) == 2
    assert find_number_of_overlapping_assignments(sample_input) == 4


if __name__ == '__main__':
    examples()
    raise SystemExit(main())
