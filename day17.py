from dataclasses import dataclass
from itertools import cycle
from typing import Iterator
import tqdm

"""
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

XY = tuple[int, int]

@dataclass
class Rock:
    """Treat me as immutable"""
    bottom_left: XY
    offsets: list[XY]

    def points(self) -> set[XY]:
        bx, by = self.bottom_left
        return {(bx + x, by + y) for x, y in self.offsets}

    def height(self) -> int:
        return max(y for x, y in self.points())

    def move(self, dx: int, dy: int) -> 'Rock':
        bx, by = self.bottom_left
        return Rock((bx + dx, by + dy), self.offsets)

OFFSETS = {
    # positive x is right, positive y is up
    "-": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "+": [        (1, 2),
          (0, 1), (1, 1), (2, 1), 
                  (1, 0)],
    "L": [                (2, 2),
                          (2, 1),
          (0, 0), (1, 0), (2, 0)],
    "I": [(0, 3),
          (0, 2),
          (0, 1),
          (0, 0)],
    "b": [(0, 1), (1, 1),
          (0, 0), (1, 0)]
}


#1234567#
# wall at (0, h) for all h
# wall at (8, h) for all h
# piece starts at (3, h) for whatever h

# c              (x, 4)
#                (x, 3)
#                (x, 2)
#                (x, 1)
#--------------  (x, 0)

def run(pattern: str) -> Iterator[dict]:
    """return the height of the tallest rock after num_steps"""
    occupied = set[XY]()
    gases = cycle(pattern)
    height = 0
    h = 0
    deleted = 0
    count = 0

    for rock_type in cycle(OFFSETS):
        count += 1

        floor = max(y for x, y in occupied) if occupied else 0
        bottom_left = (3, floor + 4)
        rock = Rock(bottom_left, OFFSETS[rock_type])
    
        #print(num_rocks, rock)

        while True:
            # blow with gas
            gas = next(gases)
            #print(gas, rock)

            if gas == "<":
                dx, dy = -1, 0
            elif gas == ">":
                dx, dy = 1, 0
            else:
                raise ValueError(f"bad gas {gas}")

            moved_rock = rock.move(dx, dy)
            pts = moved_rock.points()
            if any(x <= 0 for x, y in pts) or any(x >= 8 for x, y in pts) or pts & occupied:
                # hit a wall or another rock
                pass
            else:
                rock = moved_rock

            # try to fall
            moved_rock = rock.move(0, -1)
            pts = moved_rock.points()
            if any(y <= 0 for x, y in pts) or pts & occupied:
                # hit the floor or another rock
                # add all of my points to the occupied set
                occupied |= rock.points()
                height = max(height, rock.height())

                # check for a line
                line = []
                for _, y in pts:
                    if all((x, y) in occupied for x in range(1, 8)):
                        line.append(y)
                if line:
                    h = max(line)
                    # reset to 0
                    occupied = {(x, y - h) for x, y in occupied if y > h}
                    deleted += h
                    height -= h

                yield {
                    "height": height + deleted,
                    "time": count,
                    "line_completed": bool(line),
                    "delta": h if line else None
                }

                break # out of the while
            else:
                rock = moved_rock

    return occupied
    

GASES = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

def find_height(pattern: str, num_steps: int) -> int:
    height = {}
    it = run(pattern)

    for _ in range(num_steps):
        height = next(it)

    return height['height']

assert find_height(GASES, 2022) == 3068

with open('day17.txt') as f:
    gases = f.read().strip()

occ = find_height(gases, 2022)

print(occ)

def display(occupied: set[XY], nr: int = 10):
    y = max(y for x, y in occupied)

    for _ in range(min(nr, y)):
        print("|" + ''.join('#' if (x, y) in occupied else '.' for x in range(8)) + "|")
        y -= 1

# look for a pattern
import pandas as pd

it = run(gases)
df = pd.DataFrame([next(it) for _ in tqdm.trange(100_000)])

