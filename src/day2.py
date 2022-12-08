"""
--- Day 2: Rock Paper Scissors ---

The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage, a giant Rock Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape. Then, a winner for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z

This strategy guide predicts and recommends the following:

    In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
    In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
    The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.

In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your
strategy guide?

--- Part Two ---

The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated. The example above now goes like this:

    In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
    In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
    In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.

Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?
"""

import fileinput
from enum import IntEnum
from inspect import cleandoc
from typing import Iterable


class Move(IntEnum):
    """Represents a possible Rock, Paper, Scissors move."""

    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(IntEnum):
    """Represents a possible Rock, Paper, Scissors result."""

    LOSS = 0
    DRAW = 3
    WIN = 6


OPPONENT_MOVE_LABEL = {'A': Move.ROCK, 'B': Move.PAPER, 'C': Move.SCISSORS}
SELF_MOVE_LABEL = {'X': Move.ROCK, 'Y': Move.PAPER, 'Z': Move.SCISSORS}
RESULT_FROM_ROUND: dict[tuple[Move, Move], Result] = {
    (Move.ROCK, Move.ROCK): Result.DRAW,
    (Move.ROCK, Move.PAPER): Result.LOSS,
    (Move.ROCK, Move.SCISSORS): Result.WIN,
    (Move.PAPER, Move.ROCK): Result.WIN,
    (Move.PAPER, Move.PAPER): Result.DRAW,
    (Move.PAPER, Move.SCISSORS): Result.LOSS,
    (Move.SCISSORS, Move.ROCK): Result.LOSS,
    (Move.SCISSORS, Move.PAPER): Result.WIN,
    (Move.SCISSORS, Move.SCISSORS): Result.DRAW,
}
"""Maps (self_move, opponent_move) to result."""

CORRECTED_RESULT_LABEL = {'X': Result.LOSS, 'Y': Result.DRAW, 'Z': Result.WIN}
SELF_MOVE_FROM_DESIRED_RESULT: dict[tuple[Move, Result], Move] = {
    (opponent_move, result): self_move
    for (self_move, opponent_move), result in RESULT_FROM_ROUND.items()
}
"""Maps (opponent_move, result) to self_move."""


def calculate_points(self_move: Move, opponent_move: Move) -> int:
    """Calculate the points from a given round."""
    return self_move + RESULT_FROM_ROUND[(self_move, opponent_move)]


def get_strategy_point_sum(strategy: Iterable[str]) -> int:
    """Get the number of points a strategy would result in."""
    points = 0
    for line in strategy:
        line.strip()
        opponent_label, self_label = line.split()
        opponent_move = OPPONENT_MOVE_LABEL[opponent_label]
        self_move = SELF_MOVE_LABEL[self_label]
        points += calculate_points(self_move, opponent_move)
    return points


def get_corrected_strategy_point_sum(strategy: Iterable[str]) -> int:
    """
    Get the number of points a strategy would result in, given corrected
    instructions.
    """
    points = 0
    for line in strategy:
        line.strip()
        opponent_label, desired_result_label = line.split()
        opponent_move = OPPONENT_MOVE_LABEL[opponent_label]
        desired_result = CORRECTED_RESULT_LABEL[desired_result_label]
        self_move = SELF_MOVE_FROM_DESIRED_RESULT[(opponent_move, desired_result)]
        points += calculate_points(self_move, opponent_move)
    return points


def main() -> int:
    strategy_points = get_strategy_point_sum(fileinput.input(encoding='utf-8'))
    print(f'Part 1: {strategy_points}')
    corrected_strategy_points = get_corrected_strategy_point_sum(
        fileinput.input(encoding='utf-8')
    )
    print(f'Part 2: {corrected_strategy_points}')
    return 0


def example_part1() -> None:
    """Given example case for part 1."""
    sample_input = cleandoc(
        """
        A Y
        B X
        C Z
        """
    ).splitlines(keepends=True)
    assert get_strategy_point_sum(sample_input) == 15


def example_part2() -> None:
    """Given example case for part 2."""
    sample_input = cleandoc(
        """
        A Y
        B X
        C Z
        """
    ).splitlines(keepends=True)
    assert get_corrected_strategy_point_sum(sample_input) == 12


if __name__ == '__main__':
    example_part1()
    example_part2()
    raise SystemExit(main())
