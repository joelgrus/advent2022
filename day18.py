from typing import Iterator
from dataclasses import dataclass
from collections import deque

RAW = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

Point = tuple[int, int, int]

def neighbors(point: Point) -> Iterator[Point]:
    x, y, z = point
    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)


@dataclass
class Droplet:
    points: set[Point]
    xlo: int = 0
    xhi: int = 0
    ylo: int = 0
    yhi: int = 0
    zlo: int = 0
    zhi: int = 0

    def __post_init__(self):
        self.xlo = min(x for x, _, _ in self.points)
        self.xhi = max(x for x, _, _ in self.points)
        self.ylo = min(y for _, y, _ in self.points)
        self.yhi = max(y for _, y, _ in self.points)
        self.zlo = min(z for _, _, z in self.points)
        self.zhi = max(z for _, _, z in self.points)

    @staticmethod
    def parse(raw: str) -> 'Droplet':
        return Droplet({
            tuple(map(int, line.split(",")))
            for line in raw.splitlines()
        })

    def _surface_area(self, point: Point) -> int:
        return sum(neighbor not in self.points for neighbor in neighbors(point))

    def surface_area(self) -> int:
        return sum(self._surface_area(point) for point in self.points)

    def find_interior_points(self, point: Point) -> set[Point]:
        # a point is interior if it cannot escape the bounding box
        q = deque([point])
        seen = {point}

        while q:
            x, y, z = q.popleft()
            if x < self.xlo or x > self.xhi:
                return set()
            if y < self.ylo or y > self.yhi:
                return set()
            if z < self.zlo or z > self.zhi:
                return set()

            for neighbor in neighbors((x, y, z)):
                if neighbor not in seen and neighbor not in self.points:
                    seen.add(neighbor)
                    q.append(neighbor)

        return seen

    def interior_points(self) -> set[Point]:
        starting_points = {n for p in self.points for n in neighbors(p)} - self.points
        return {ip for p in starting_points for ip in self.find_interior_points(p)}

    def exterior_surface_area(self) -> int:
        interior_points = self.interior_points()
        filled_in = Droplet(self.points | interior_points)
        return filled_in.surface_area()


DROPLET = Droplet.parse(RAW)
assert DROPLET.surface_area() == 64
assert DROPLET.exterior_surface_area() == 58

with open('day18.txt') as f:
    raw = f.read()

droplet = Droplet.parse(raw)

print(droplet.surface_area())
print(droplet.exterior_surface_area())