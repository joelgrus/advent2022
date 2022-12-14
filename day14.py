from itertools import count

RAW = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

Point = tuple[int, int]
Path = list[Point]
World = dict[Point, str]


def parse_path(line: str) -> Path:
    path = []
    for part in line.split(" -> "):
        x, y = part.split(",")
        path.append((int(x), int(y)))
    return path

def make_world(paths: list[Path]) -> World:
    world = {}
    for path in paths:
        for (x1, y1), (x2, y2) in zip(path, path[1:]):
            if x1 == x2:
                y1, y2 = min(y1, y2), max(y1, y2)
                for y in range(y1, y2 + 1):
                    world[(x1, y)] = "#"
            elif y1 == y2:
                x1, x2 = min(x1, x2), max(x1, x2)
                for x in range(x1, x2 + 1):
                    world[(x, y1)] = "#"
            else: 
                raise ValueError("Invalid path")
    return world


def simulate_sand(paths: list[Path], entry_x: int = 500) -> int:
    world = make_world(paths)
    bottom = max(y for x, y in world)

    for i in count():
        falling = True
        x, y = entry_x, 0

        while falling:
            # fell out the bottom of the world, so we're done
            if y > bottom:
                return i

            down = (x, y + 1)
            down_left = (x - 1, y + 1)
            down_right = (x + 1, y + 1)

            if down not in world:
                y += 1
            elif down_left not in world:
                x -= 1
                y += 1
            elif down_right not in world:
                x += 1
                y += 1
            else:
                world[(x, y)] = "o"
                break

    raise ValueError("Simulation failed")

PATHS = [parse_path(line) for line in RAW.splitlines()]
assert simulate_sand(PATHS) == 24

with open('day14.txt') as f:
    raw = f.read()
paths = [parse_path(line) for line in raw.splitlines()]
print(simulate_sand(paths))

def show(world: World):
    min_x = min(x for x, y in world)
    max_x = max(x for x, y in world)
    min_y = min(y for x, y in world)
    max_y = max(y for x, y in world)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(world.get((x, y), "."), end="")
        print()

def simulate_sand2(paths: list[Path], entry_x: int = 500) -> int:
    world = make_world(paths)

    # bottom behaves differently for part 2
    bottom = max(y for x, y in world) + 1

    for i in count(1):
        x, y = entry_x, 0

        while True:
            # fell out the bottom of the world, so we're done
            down = (x, y + 1)
            down_left = (x - 1, y + 1)
            down_right = (x + 1, y + 1)

            if y < bottom  and down not in world:
                y += 1
            elif y < bottom  and down_left not in world:
                x -= 1
                y += 1
            elif y < bottom and down_right not in world:
                x += 1
                y += 1
            else:
                world[(x, y)] = "o"

                #show(world)
                #print()

                if (x, y) == (entry_x, 0):
                    return i
                break

    raise ValueError("Simulation failed")


assert simulate_sand2(PATHS) == 93
print(simulate_sand2(paths))