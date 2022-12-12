"""
--- Day 8: Treetop Tree House ---

The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

    The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
    The top-middle 5 is visible from the top and right.
    The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
    The left-middle 5 is visible, but only from the right.
    The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
    The right-middle 3 is visible from the right.
    In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?

--- Part Two ---

Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

    Looking up, its view is not blocked; it can see 1 tree (of height 3).
    Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
    Looking right, its view is not blocked; it can see 2 trees.
    Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).

A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390

    Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
    Looking left, its view is not blocked; it can see 2 trees.
    Looking down, its view is also not blocked; it can see 1 tree.
    Looking right, its view is blocked at 2 trees (by a massive tree of height 9).

This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?
"""

import fileinput
import math
from inspect import cleandoc
from typing import Iterable, TypeAlias

Grid: TypeAlias = list[list[int]]
Point: TypeAlias = tuple[int, int]


def parse_grid(lines: Iterable[str]) -> Grid:
    """Parse grid into 2D array."""
    return [[int(char) for char in line.strip()] for line in lines]


def determine_visible_in_ray(grid: Grid, ray: list[Point]) -> list[Point]:
    """
    Determine which points in the ray are visible when checking both directions
    (front and back along the same ray). Return the points which are visible.
    """
    # Forward pass
    max_height = -1
    visible: set[Point] = set()
    for point in ray:
        if grid[point[0]][point[1]] > max_height:
            visible.add(point)
            max_height = grid[point[0]][point[1]]

    # Backward pass
    max_height = -1
    for point in ray[::-1]:
        if grid[point[0]][point[1]] > max_height:
            visible.add(point)
            max_height = grid[point[0]][point[1]]

    return list(visible)


def determine_visible_from_treehouse(
    grid: Grid, ray: list[Point], blocking_height: int
) -> int:
    """Determine which points are visible from the treehouse."""
    for i, point in enumerate(ray):
        px, py = point
        if grid[px][py] >= blocking_height:
            return i + 1
    return len(ray)


def calculate_visible_trees(lines: Iterable[str]) -> int:
    """Calculate how many trees are visible in the grid."""
    grid = parse_grid(lines)
    grid_size = len(grid)
    visible_grid = [[False for _ in row] for row in grid]
    left_right_rays = [
        [(row_idx, col_idx) for col_idx in range(grid_size)]
        for row_idx in range(grid_size)
    ]
    up_down_rays = [
        [(row_idx, col_idx) for row_idx in range(grid_size)]
        for col_idx in range(grid_size)
    ]

    for ray in left_right_rays + up_down_rays:
        visible = determine_visible_in_ray(grid, ray)
        for point in visible:
            visible_grid[point[0]][point[1]] = True

    flat_grid: list[bool] = sum(visible_grid, [])
    return flat_grid.count(True)


def get_scenic_score(grid: Grid, point: Point) -> int:
    """Get the scenic score of a given tree."""
    grid_size = len(grid)
    px, py = point
    height = grid[px][py]
    rays = [
        [(px, col) for col in range(py + 1, grid_size)],  # Going right
        [(px, col) for col in range(py - 1, -1, -1)],  # Going left
        [(row, py) for row in range(px - 1, -1, -1)],  # Going up
        [(row, py) for row in range(px + 1, grid_size)],  # Going down
    ]
    return math.prod(
        [determine_visible_from_treehouse(grid, ray, height) for ray in rays]
    )


def find_highest_scenic_score(lines: Iterable[str]) -> int:
    """Find the highest scenic score."""
    grid = parse_grid(lines)
    grid_size = len(grid)
    all_points = [(x, y) for x in range(grid_size) for y in range(grid_size)]
    scenic_scores = [get_scenic_score(grid, point) for point in all_points]
    return max(scenic_scores)


def main() -> int:
    """Main entry point."""
    examples()

    visible_trees = calculate_visible_trees(fileinput.input(encoding='utf-8'))
    print(f'Part 1: {visible_trees}')
    scenic_score = find_highest_scenic_score(fileinput.input(encoding='utf-8'))
    print(f'Part 2: {scenic_score}')

    return 0


def examples() -> None:
    """Given example cases."""
    sample_input = cleandoc(
        """
        30373
        25512
        65332
        33549
        35390
        """
    ).splitlines(keepends=True)
    assert calculate_visible_trees(sample_input) == 21
    assert find_highest_scenic_score(sample_input) == 8


if __name__ == '__main__':
    raise SystemExit(main())
