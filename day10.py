from dataclasses import dataclass, field
from typing import Iterator

@dataclass
class Device:
    X: int = 1
    cycle: int = 1
    signal_strengths: list[int] = field(default_factory=list)
    xs: list[int] = field(default_factory=list)


    def step(self, instruction: str) -> int:
        print("cycle", self.cycle, "X", self.X, "addxs")
        print("instruction", instruction)
        print("prev signal_strengths", self.signal_strengths[-2:])

        signal_strength = self.X * self.cycle
        print("signal strength", signal_strength)

        match instruction.split():
            case ["noop"]:
                self.signal_strengths.append(signal_strength)
                self.xs.append(self.X)
                self.cycle += 1       
            case ["addx", n]:
                self.signal_strengths.append(signal_strength)
                self.xs.append(self.X)
                self.cycle += 1
                self.signal_strengths.append(self.X * self.cycle)
                self.xs.append(self.X)
                self.cycle += 1
                self.X += int(n)

        return signal_strength

    def run(self, instructions: str) -> None:
        for instruction in instructions.splitlines():
            self.step(instruction)


RAW1 = """noop
addx 3
addx -5"""

DEVICE1 = Device()
DEVICE1.run(RAW1)

def run(instructions: str) -> int:
    device = Device()
    device.run(instructions)

    idxs = [20, 60, 100, 140, 180, 220]

    return sum(
        device.signal_strengths[idx-1]
        for idx in idxs
    )

RAW2 = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

assert run(RAW2) == 13140

with open('day10.txt') as f:
    raw = f.read()

print(run(raw))

# now we need to draw
device = Device()
device.run(raw)

def visualize(xs: list[int]) -> str:
    res = []
    for row in range(6):
        outrow = []
        for col in range(40):
            idx = row * 40 + col
            x = xs[idx]

            if abs(x - col) <= 1:
                outrow.append("X")
            else:
                outrow.append(".")
        res.append(outrow)

    return "\n".join("".join(row) for row in res)