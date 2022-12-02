from enum import Enum

class Rps(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @staticmethod
    def parse(s) -> 'Rps':
        if s in ('A', 'X'):
            return Rps.ROCK
        elif s in ('B', 'Y'):
            return Rps.PAPER
        elif s in ('C', 'Z'):
            return Rps.SCISSORS
        else:
            raise ValueError('invalid choice')

    def find_choice(self, result: str) -> 'Rps':
        if result == 'Y':
            # draw
            return self
        elif result == 'X':
            # need to lose
            if self == Rps.ROCK:
                return Rps.SCISSORS
            elif self == Rps.PAPER:
                return Rps.ROCK
            else:
                return Rps.PAPER
        elif result == 'Z':
            # need to win
            if self == Rps.ROCK:
                return Rps.PAPER
            elif self == Rps.PAPER:
                return Rps.SCISSORS
            else:
                return Rps.ROCK
        else:
            raise ValueError('invalid result')


def score(opponent: Rps, me: Rps):
    opponent_value = opponent.value
    me_value = me.value

    delta = (opponent_value - me_value) % 3

    if delta == 0:
        # draw is worth 3
        return me_value + 3
    elif delta == 1:
        # loss is worth 0
        return me_value 
    elif delta == 2:
        # win is worth 6
        return me_value + 6



RAW = """A Y
B X
C Z"""

def parse(raw: str) -> list[list[Rps]]:
    return [
        [Rps.parse(s) for s in line.split()]
        for line in raw.strip().splitlines()
    ]

def score_all(lines):
    return sum(score(*line) for line in lines)

lines = parse(RAW)
assert score_all(parse(RAW)) == 15

with open('day02.txt') as f:
    raw = f.read()
    lines = parse(raw)
    print(score_all(lines))

def parse2(raw: str) -> list[list[Rps]]:
    out = []
    for line in raw.strip().splitlines():
        opponent, result = line.split()
        opponent = Rps.parse(opponent)
        me = opponent.find_choice(result)
        out.append((opponent, me))
    return out

assert score_all(parse2(RAW)) == 12

lines2 = parse2(raw)
print(score_all(lines2))
