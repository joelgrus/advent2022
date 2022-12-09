from typing import NamedTuple
from dataclasses import dataclass

RAW = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

def sgn(n: int):
    if n == 0:
        return 0
    elif n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        raise ValueError

@dataclass
class Rope:
    hx: int = 0
    hy: int = 0
    tx: int = 0
    ty: int = 0

    def move_head(self, direction: str):
        if direction == "U":
            self.hy += 1
        elif direction == "D":
            self.hy -= 1
        elif direction == "L":
            self.hx -= 1
        elif direction == "R":
            self.hx += 1

        self.move_tail()

    def move_tail(self):
        dx = self.hx - self.tx
        dy = self.hy - self.ty 

        if abs(dx) <= 1 and abs(dy) <= 1:
            return
        else:
            self.tx += sgn(dx)
            self.ty += sgn(dy)

    def run(self, instructions: str):
        visited = {(self.tx, self.ty)}
        # print(self)
        for instruction in instructions.splitlines():
            direction, distance = instruction.split()
            for _ in range(int(distance)):
                self.move_head(direction)
                visited.add((self.tx, self.ty))
                # print(self)
        return len(visited)

rope = Rope()
assert rope.run(RAW) == 13

with open('day09.txt') as f:
    raw = f.read()

rope = Rope()
print(rope.run(raw))

class LongRope:
    def __init__(self, n: int = 10):
        self.n = n
        self.xs = [0 for _ in range(n)]
        self.ys = [0 for _ in range(n)]

    def __repr__(self):
        return f"LongRope({self.xs}, {self.ys})"

    def move_head(self, direction: str):
        # print("move head", self, direction)
        if direction == "U":
            self.ys[0] += 1
        elif direction == "D":
            self.ys[0] -= 1
        elif direction == "L":
            self.xs[0] -= 1
        elif direction == "R":
            self.xs[0] += 1

        self.move_tail(1)

    def move_tail(self, i: int):
        if i == self.n:
            return

        # print("move tail", self, i)

        dx = self.xs[i-1] - self.xs[i]
        dy = self.ys[i-1] - self.ys[i]

        if abs(dx) <= 1 and abs(dy) <= 1:
            pass
        else:
            self.xs[i] += sgn(dx)
            self.ys[i] += sgn(dy)

        self.move_tail(i+1)

    def run(self, instructions: str):
        visited = {(self.xs[-1], self.ys[-1])}
        # print(self)
        for instruction in instructions.splitlines():
            direction, distance = instruction.split()
            for _ in range(int(distance)):
                self.move_head(direction)
                visited.add((self.xs[-1], self.ys[-1]))
                # print(self)
        return len(visited)

long_rope = LongRope(2)
assert long_rope.run(RAW) == 13

long_rope = LongRope(10)
print(long_rope.run(raw))