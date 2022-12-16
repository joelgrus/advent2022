
from dataclasses import dataclass
import re
import tqdm

RAW = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

point_rgx = r"x=(\-?[0-9]+), y=(\-?[0-9]+)"

XY = tuple[int, int]
Interval = tuple[int, int]


@dataclass
class Sensor:
    position: XY
    beacon: XY

    @staticmethod
    def from_string(s: str) -> "Sensor":
        (x1, y1), (x2, y2) = re.findall(point_rgx, s)
        return Sensor((int(x1), int(y1)), (int(x2), int(y2)))


SENSORS = [Sensor.from_string(s) for s in RAW.splitlines()]


def find_allowable(
    bad_intervals: list[Interval],
    lo: int, 
    hi: int
) -> int | None:

    # ascending by left endpoint
    intervals_lo_to_hi = sorted(bad_intervals)

    # descending by right endpoint
    intervals_hi_to_lo = sorted(bad_intervals, key=lambda pair: pair[1], reverse=True)

    print(bad_intervals)
    print(intervals_lo_to_hi)
    print(intervals_hi_to_lo)

    left = lo - 1

    for x, y in intervals_lo_to_hi:
        if x > left + 1:
            break
        else:
            left = max(left, y)

    right = hi + 1

    for x, y in intervals_hi_to_lo:
        if y < right - 1:
            break
        else:
            right = min(right, x)

    print(left, right)

    if left + 1 < right:
        return left + 1
    else:
        return None


def find_unallowable_columns(sensors: list[Sensor], row: int) -> set[int]:
    unallowable_intervals: list[Interval] = []

    for sensor in sensors:
        x, y = sensor.position
        bx, by = sensor.beacon

        dist = abs(x - bx) + abs(y - by)

        dist_from_row = abs(y - row)
        remaining = dist - dist_from_row

        if remaining < 0:
            continue
        else:
            lo = x - remaining
            hi = x + remaining

            if (lo, row) == (bx, by):
                lo += 1
            elif (hi, row) == (bx, by):
                hi -= 1

            if lo <= hi:
                unallowable_intervals.append((lo, hi))

    return set.union(*[set(range(lo, hi + 1)) for lo, hi in unallowable_intervals])
        
            

assert len(find_unallowable_columns(SENSORS, 10)) == 26

with open('day15.txt') as f:
    raw = f.read()

sensors = [Sensor.from_string(s) for s in raw.splitlines()]

#uc = find_unallowable_columns(sensors, 2_000_000)

#print(uc)
#print(len(uc))


def find_allowable_column(
    sensors: list[Sensor], 
    row: int,
    lo: int, 
    hi: int
) -> int | None:
    unallowable_intervals: list[Interval] = []

    for sensor in sensors:
        print(sensor)
        x, y = sensor.position
        bx, by = sensor.beacon

        dist = abs(x - bx) + abs(y - by)

        dist_from_row = abs(y - row)
        remaining = dist - dist_from_row

        if remaining < 0:
            continue
        else:
            a = x - remaining
            b = x + remaining

            if (a, row) == (bx, by):
                a += 1
            elif (b, row) == (bx, by):
                b -= 1

            print(a, b)
            if a <= b:
                unallowable_intervals.append((a, b))

    print(unallowable_intervals)
    col = find_allowable(unallowable_intervals, lo, hi)
    print(col)

    if col is not None and (row, col) not in {s.position for s in sensors} | {s.beacon for s in sensors}:
        return col
    else:
        return None


def find_beacon(sensors: list[Sensor], lo: int, hi: int) -> XY:
    for i in range(lo, hi + 1):
        print()
        col = find_allowable_column(sensors, i, lo, hi)
        print(i, col)
        if col is not None:
            yield (i, col)
#    raise ValueError()

print(list(find_beacon(SENSORS, 0, 20)))

# for i in range()
# uc = find_allowable_column(sensors, 2_000_002, 0, 4_000_000)
# print(uc)

def solve(sensors: list[Sensor], lo: int, hi: int) -> XY | None:
    for i in tqdm.trange(lo, hi + 1):
        # find all the locations in row i that cannot be a beacon
        # do this by finding the intervals ruled out by each sensor
        intervals = []

        for sensor in sensors:
            x, y = sensor.position
            bx, by = sensor.beacon
            dist = abs(x - bx) + abs(y - by)
            dist_from_row = abs(y - i)
            remaining = dist - dist_from_row

            if remaining < 0:
                continue
            else:
                left = x - remaining
                right = x + remaining

                if left <= right:
                    intervals.append((left, right))

        #print(i, intervals)
        lo_to_hi = sorted(intervals)
        hi_to_lo = sorted(intervals, key=lambda pair: pair[1], reverse=True)

        left = lo - 1
        right = hi + 1

        for x, y in lo_to_hi:
            #print(left, "-", x, y)
            if x > left + 1:
                break
            else:
                left = max(left, y)

        for x, y in hi_to_lo:
            if y < right - 1:
                break
            else:
                right = min(right, x)

        if left < right:
            assert left == right - 2
            return (i, left + 1)

res = solve(sensors, 0, 4_000_000)
if res is not None:
    print(res)
    y, x = res
    print(x * 4000000 + y)