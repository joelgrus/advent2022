from dataclasses import dataclass
from typing import Tuple

@dataclass
class Range:
    lo: int
    hi: int

    @staticmethod
    def parse(s: str) -> 'Range':
        lo, hi = s.split("-")
        return Range(int(lo), int(hi))

    def contains(self, other: 'Range') -> bool:
        return self.lo <= other.lo and self.hi >= other.hi

    def overlap(self, other: 'Range') -> bool:
        if max(self.lo, other.lo) <= min(self.hi, other.hi):
            return True
        else:
            return False
        


Pair = Tuple[Range, Range]

def make_pairs(raw: str) -> list[Pair]:
    preranges = [row.split(",") for row in raw.splitlines()]
    return [
        (Range.parse(r1), Range.parse(r2)) 
        for r1, r2 in preranges
]

def count_containing_pairs(pairs: list[Pair]) -> int:
    return sum(
        (p1.contains(p2) or p2.contains(p1))
        for p1, p2 in pairs
    )

def count_overlapping_pairs(pairs: list[Pair]) -> int:
    return sum(
        p1.overlap(p2)
        for p1, p2 in pairs
    )

RAW = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

PAIRS = make_pairs(RAW)

assert count_containing_pairs(PAIRS) == 2
assert count_overlapping_pairs(PAIRS) == 4

with open('day04.txt') as f:
    raw = f.read()
pairs = make_pairs(raw)

print(count_containing_pairs(pairs))
print(count_overlapping_pairs(pairs))