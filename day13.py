from itertools import zip_longest
from functools import cmp_to_key

RAW = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

Packet = list 
Pair = tuple[Packet, Packet]

def parse(raw: str) -> list[Pair]:
    """Parse the raw input into a list of pairs of packets."""
    pairs = []
    for pair in raw.split("\n\n"):
        p1, p2 = pair.split("\n")
        pairs.append((eval(p1), eval(p2)))
    return pairs

PAIRS = parse(RAW)

def compare(p1: Packet, p2: Packet) -> int:
    """are the packets in the right order"""
    match (p1, p2):
        case (int(), int()):
            if p1 < p2:
                return -1  # good
            elif p1 > p2:
                return 1  # bad
            else:
                return 0  # continue checking
        case (int(), list()):
            return compare([p1], p2)
        case (list(), int()):
            return compare(p1, [p2])
        case (list(), list()):
            for a, b in zip_longest(p1, p2):
                if a is None:
                    # a ran out first
                    return -1
                elif b is None:
                    # b ran out first
                    return 1
                else:
                    # neither ran out first
                    result = compare(a, b)
                    if result != 0:
                        return result
            return 0
            
def right_order_sum(pairs: list[Pair]) -> int:
    res = 0
    for i, (p1, p2) in enumerate(pairs):
        result = compare(p1, p2)
        if result == -1:
            res += i + 1

    return res

assert right_order_sum(PAIRS) == 13

with open('day13.txt') as f:
    raw = f.read()
pairs = parse(raw)

print(right_order_sum(pairs))


def find_divider_packets(pairs: list[Pair]) -> int:
    # flatten
    p1 = [[2]]
    p2 = [[6]]

    packets = [p for pair in pairs for p in pair] + [p1, p2]
    key = cmp_to_key(compare)
    packets.sort(key=key)

    a = packets.index(p1) + 1
    b = packets.index(p2) + 1

    return a * b

assert find_divider_packets(PAIRS) == 140

print(find_divider_packets(pairs))