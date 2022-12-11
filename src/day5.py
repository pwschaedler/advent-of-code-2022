"""
--- Day 5: Supply Stacks ---

The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3

In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3

Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3

Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3

The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each
stack?

--- Part Two ---

As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3

However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3

Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3

Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3

In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?
"""

import fileinput
import re
from inspect import cleandoc
from typing import Iterable, NamedTuple

INSTRUCTION_PATTERN = re.compile(r'move (\d+) from (\d+) to (\d+)')


class Instruction(NamedTuple):
    """Instruction data container."""

    quantity: int
    from_stack: int
    to_stack: int


class Scenario(NamedTuple):
    """Container for all scenario data."""

    stacks: list[list[str]]
    instructions: list[Instruction]


def parse_input(lines: Iterable) -> Scenario:
    """Parse all input into different structures."""
    all_lines = ''.join(lines)
    stack_lines, instruction_lines = all_lines.split('\n\n')
    return Scenario(
        parse_stacks(stack_lines.splitlines()),
        parse_instructions(instruction_lines.splitlines()),
    )


def parse_stacks(lines: list[str]) -> list[list[str]]:
    """Parse stack text description into actual stacks of labels."""
    stack_labels = lines.pop().rstrip()
    num_stacks = int(stack_labels[-1])
    stacks: list[list[str]] = [[] for _ in range(num_stacks)]

    for line in lines[::-1]:
        for idx, label in enumerate(line[1::4]):
            if not label.isspace():
                stacks[idx].append(label)

    return stacks


def parse_instructions(lines: list[str]) -> list[Instruction]:
    """Parse instruction lines into data structure."""
    instructions: list[Instruction] = []
    for line in lines:
        matches = re.match(INSTRUCTION_PATTERN, line)
        if matches is None:
            raise ValueError('Instructions in wrong format.')
        instruction = Instruction(
            int(matches.group(1)), int(matches.group(2)) - 1, int(matches.group(3)) - 1
        )
        instructions.append(instruction)
    return instructions


def run_instructions_9000(
    stacks: list[list[str]], instructions: list[Instruction]
) -> str:
    """
    Run the given instructions to move crates around stacks. Return labels of
    the top crates as a single string.
    """
    for instruction in instructions:
        for _ in range(instruction.quantity):
            stacks[instruction.to_stack].append(stacks[instruction.from_stack].pop())
    return ''.join([stack[-1] for stack in stacks])


def run_instructions_9001(
    stacks: list[list[str]], instructions: list[Instruction]
) -> str:
    """
    Run the given instructions using the CrateMover 9001, which moves
    multiple crates at the same time.
    """
    for instruction in instructions:
        from_front = stacks[instruction.from_stack][: -instruction.quantity]
        from_back = stacks[instruction.from_stack][-instruction.quantity :]
        stacks[instruction.to_stack] += from_back
        stacks[instruction.from_stack] = from_front
    return ''.join([stack[-1] for stack in stacks])


def solve_part1(lines: Iterable[str]) -> str:
    """Parse input and run instructions."""
    scenario = parse_input(lines)
    return run_instructions_9000(scenario.stacks, scenario.instructions)


def solve_part2(lines: Iterable[str]) -> str:
    """Parse input and run instructions for part 2."""
    scenario = parse_input(lines)
    return run_instructions_9001(scenario.stacks, scenario.instructions)


def main() -> int:
    """Main entry point."""
    final_state_9000 = solve_part1(fileinput.input(encoding='utf-8'))
    print(f'Part 1: {final_state_9000}')
    final_state_9001 = solve_part2(fileinput.input(encoding='utf-8'))
    print(f'Part 2: {final_state_9001}')
    return 0


def examples() -> None:
    """Given example cases."""
    sample_input = cleandoc(
        """
            [D]
        [N] [C]
        [Z] [M] [P]
         1   2   3

        move 1 from 2 to 1
        move 3 from 1 to 3
        move 2 from 2 to 1
        move 1 from 1 to 2
        """
    ).splitlines(keepends=True)
    assert solve_part1(sample_input) == 'CMZ'
    assert solve_part2(sample_input) == 'MCD'


if __name__ == '__main__':
    examples()
    raise SystemExit(main())
