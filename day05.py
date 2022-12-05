from dataclasses import dataclass
import re
import copy

RAW = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

MOVE_RGX = r"move (\d+) from (\d+) to (\d+)"

Stack = list[str]
Stacks = dict[int, Stack]

def get_stacks(raw: str) -> Stacks:
    lines = list(reversed(raw.splitlines()))
    cols = {int(c): i for i, c in enumerate(lines[0]) if c != " "}
    stacks = {
        c: [line[i] for line in lines[1:] if line[i] != " "]
        for c, i in cols.items()
    }

    return stacks


def tops(stacks: Stacks) -> str:
    return ''.join(stack[-1] for stack in stacks.values())


@dataclass
class Move:
    quantity: int
    from_: int
    to: int


@dataclass 
class Problem:
    stacks: Stacks
    moves: list[Move]

    def move(self, move: Move) -> None:
        for _ in range(move.quantity):
            self.stacks[move.to].append(self.stacks[move.from_].pop())

    def move9001(self, move: Move) -> None:
        to_move = self.stacks[move.from_][-move.quantity:]
        self.stacks[move.from_] = self.stacks[move.from_][:-move.quantity]
        self.stacks[move.to] += to_move

    def run(self, model: int = 9000) -> None:
        # print(self.stacks)
        for move in self.moves:
            # print(move)
            if model == 9000:
                self.move(move)
            elif model == 9001:
                self.move9001(move)
            else:
                raise ValueError("Invalid model")
            # print(self.stacks)

def get_moves(raw: str) -> list[Move]:
    return [Move(*[int(x) for x in row]) for row in re.findall(MOVE_RGX, raw)]

def get_problem(raw: str) -> Problem:
    raw_stacks, raw_moves = raw.split("\n\n")

    stacks = get_stacks(raw_stacks)
    moves = get_moves(raw_moves)
    return Problem(stacks, moves)

PROBLEM = get_problem(RAW)
PROBLEM.run()

assert tops(PROBLEM.stacks) == "CMZ"

PROBLEM = get_problem(RAW)
PROBLEM.run(model=9001)

assert tops(PROBLEM.stacks) == "MCD"

with open('day05.txt') as f:
    raw = f.read()

problem = get_problem(raw)
problem.run()

print(tops(problem.stacks))


problem = get_problem(raw)
problem.run(model=9001)

print(tops(problem.stacks))