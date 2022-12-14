import logging
from dataclasses import dataclass
from string import ascii_lowercase
from collections import deque
from typing import Tuple

DEBUG = True
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

RAW = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

heights = {c: i for i, c in enumerate(ascii_lowercase)}
heights["S"] = heights["a"]
heights["E"] = heights["z"]

Grid = list[list[str]]

def parse(raw: str) -> Grid:
    return [list(line) for line in raw.splitlines()]

def find_shortest_path(grid: Grid, pos: Tuple[int, int] = (-1, -1)) -> int:

    if pos == (-1, -1):
        for i, row in enumerate(grid):
            for j, c in enumerate(row):
                if c == "S":
                    pos = (i, j)
    assert pos != (-1, -1)

    queue: deque[Tuple[Tuple[int, int], int]] = deque([(pos, 0)])
    visited = set([pos])

    while queue:
        pos, steps = queue.popleft()
        i, j = pos
        if grid[i][j] == "E":
            return steps
        height = heights[grid[i][j]]

        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            i2, j2 = i + di, j + dj
            if (i2, j2) in visited:
                continue
            if i2 < 0 or i2 >= len(grid) or j2 < 0 or j2 >= len(grid[0]):
                continue
            if heights[grid[i2][j2]] > height + 1:
                continue

            visited.add((i2, j2))
            queue.append(((i2, j2), steps + 1))

    raise ValueError("No path found")

def find_shortest_path_from_an_a(grid: Grid) -> int:
    # find all the as
    apos = [
        (i, j)
        for i, row in enumerate(grid)
        for j, c in enumerate(row)
        if c == "a" or c == "S"
    ]

    #print(apos)

    # keep track of the shortest path from each a
    so_far: dict[Tuple[int, int], int] = {}
    # got to beat this
    best_so_far = len(grid) * len(grid[0]) + 1

    for start_pos in apos:
        #print()
        #print(start_pos, so_far)
        queue: deque[Tuple[Tuple[int, int], int]] = deque([(start_pos, 0)])
        visited = set([start_pos])

        while queue:
            pos, steps = queue.popleft()
            #print(pos, steps, queue)
            i, j = pos
            if grid[i][j] == "E":
                so_far[start_pos] = steps
                break  # out of the while
            # elif (i, j) in so_far and :
            #     so_far[start_pos] = steps + so_far[(i, j)]
            #     break # out of the while

            height = heights[grid[i][j]]

            for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                i2, j2 = i + di, j + dj
                if (i2, j2) in visited:
                    continue
                if i2 < 0 or i2 >= len(grid) or j2 < 0 or j2 >= len(grid[0]):
                    continue
                if heights[grid[i2][j2]] > height + 1:
                    continue

                visited.add((i2, j2))
                queue.append(((i2, j2), steps + 1))

    print(so_far)
    print(min(so_far.values()))
    return min(so_far.values())

GRID = parse(RAW)
assert find_shortest_path(GRID) == 31
assert find_shortest_path_from_an_a(GRID) == 29

with open('day12.txt') as f:
    grid = parse(f.read())

print(find_shortest_path(grid))
print(find_shortest_path_from_an_a(grid))