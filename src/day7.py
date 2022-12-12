"""
--- Day 7: No Space Left On Device ---

You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

    cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
        cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
        cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
        cd / switches the current directory to the outermost directory, /.
    ls means list. It prints out all of the files and directories immediately contained by the current directory:
        123 abc means that the current directory contains a file named abc with size 123.
        dir xyz means that the current directory contains a directory named xyz.

Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

    The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
    The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
    Directory d has total size 24933642.
    As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum
of the total sizes of those directories?

--- Part Two ---

Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least 30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

    Delete directory e, which would increase unused space by 584.
    Delete directory a, which would increase unused space by 94853.
    Delete directory d, which would increase unused space by 24933642.
    Delete directory /, which would increase unused space by 48381165.

Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?
"""

from __future__ import annotations

import fileinput
from dataclasses import dataclass
from inspect import cleandoc
from typing import Iterable, Protocol


class Inode(Protocol):
    """General Inode representation."""

    name: str

    @property
    def size(self) -> int:
        ...


@dataclass
class File:
    """Individual file representation."""

    name: str
    size: int
    parent: Directory


@dataclass
class Directory:
    """Directory representation."""

    name: str
    parent: Directory | None
    children: list[Inode]

    @property
    def size(self) -> int:
        return sum(child.size for child in self.children)


def parse_input(input_lines: Iterable[str]) -> Directory:
    """Parse the input log and return the filesystem tree structure."""
    root = Directory('/', None, [])

    cwd = root
    cwd_subdirs: dict[str, Directory] = {}
    for line in input_lines:
        line = line.strip()

        if line[:4] == '$ cd':
            dest_name = line[5:]
            if dest_name == '..':
                assert cwd.parent is not None
                cwd = cwd.parent
                cwd_subdirs = {
                    child.name: child
                    for child in cwd.children
                    if isinstance(child, Directory)
                }
            elif dest_name == '/':
                cwd = root
                cwd_subdirs = {
                    child.name: child
                    for child in cwd.children
                    if isinstance(child, Directory)
                }
            else:
                cwd = cwd_subdirs[dest_name]
                cwd_subdirs = {}

        elif line[:4] == '$ ls':
            pass  # Don't have to do anything, just read next output

        else:  # Must be output giving us new inodes
            tokens = line.split()
            if tokens[0] == 'dir':
                new_dir = Directory(tokens[1], cwd, [])
                cwd.children.append(new_dir)
                cwd_subdirs[tokens[1]] = new_dir
            else:
                new_file = File(tokens[1], int(tokens[0]), cwd)
                cwd.children.append(new_file)

    return root


def print_filesystem(inode: Inode, indent_level: int) -> None:
    """Print the filesystem tree for debugging."""
    indent = '  ' * indent_level
    inode_type = 'dir' if isinstance(inode, Directory) else 'file'
    type_label = f'({inode_type}, size={inode.size})'

    print(f'{indent}- {inode.name} {type_label}')

    if isinstance(inode, Directory):
        for child in inode.children:
            print_filesystem(child, indent_level + 1)


def calculate_sum_of_small_dirs(directory: Directory) -> int:
    """Calculate sum of directories if size <= 100,000 recursively."""
    size_if_small = directory.size if directory.size <= 100_000 else 0
    for child in directory.children:
        if isinstance(child, Directory):
            size_if_small += calculate_sum_of_small_dirs(child)
    return size_if_small


def find_sum_of_small_dirs(input_lines: Iterable[str]) -> int:
    """
    Find all directories with a total size of at most 100,000 and return
    their sum.
    """
    root = parse_input(input_lines)
    return calculate_sum_of_small_dirs(root)


def get_dirs_sizes(directory: Directory) -> list[int]:
    """Get sizes of all directories recursively."""
    return [directory.size] + sum(
        [
            get_dirs_sizes(child)
            for child in directory.children
            if isinstance(child, Directory)
        ],
        [],
    )


def find_smallest_deletable_directory(input_lines: Iterable[str]) -> int:
    """
    Find the smallest directory to delete that gives us enough free space.
    Return the size of that directory.
    """
    total_disk_space = 70_000_000
    total_needed_space = 30_000_000

    root = parse_input(input_lines)
    current_free_space = total_disk_space - root.size
    needed_space = total_needed_space - current_free_space

    dir_sizes = get_dirs_sizes(root)
    big_enough_dirs = filter(lambda size: size >= needed_space, dir_sizes)
    return min(big_enough_dirs)


def main() -> int:
    """Main entry point."""
    examples()

    sum_of_small_dirs = find_sum_of_small_dirs(fileinput.input(encoding='utf-8'))
    print(f'Part 1: {sum_of_small_dirs}')
    smallest_deletable_dir_size = find_smallest_deletable_directory(
        fileinput.input(encoding='utf-8')
    )
    print(f'Part 2: {smallest_deletable_dir_size}')

    return 0


def examples() -> None:
    """Given example cases."""
    sample_input = cleandoc(
        """
        $ cd /
        $ ls
        dir a
        14848514 b.txt
        8504156 c.dat
        dir d
        $ cd a
        $ ls
        dir e
        29116 f
        2557 g
        62596 h.lst
        $ cd e
        $ ls
        584 i
        $ cd ..
        $ cd ..
        $ cd d
        $ ls
        4060174 j
        8033020 d.log
        5626152 d.ext
        7214296 k
        """
    ).splitlines(keepends=True)
    assert find_sum_of_small_dirs(sample_input) == 95437
    assert find_smallest_deletable_directory(sample_input) == 24933642


if __name__ == '__main__':
    raise SystemExit(main())
