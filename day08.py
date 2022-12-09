RAW = """30373
25512
65332
33549
35390"""

def parse(raw: str) -> list[list[int]]:
    return [[int(c) for c in x] for x in raw.splitlines()]

TREES = parse(RAW)

def visible_trees(trees: list[int]) -> list[bool]:
    # if the trees have the heights in order, which are visible?
    tallest = -1
    res = []

    for tree in trees:
        if tree > tallest:
            res.append(True)
            tallest = tree
        else:
            res.append(False)

    return res

def visibilities(trees: list[list[int]]) -> list[list[list[str]]]:
    nr = len(trees)
    nc = len(trees[0])

    res = [[[] for c in row] for row in trees]

    # do each direction

    # left to right
    for r in range(nr):
        for i, visible in enumerate(visible_trees(trees[r])):
            if visible:
                res[r][i].append("L")
    
    # right to left
    for r in range(nr):
        for i, visible in enumerate(visible_trees(trees[r][::-1])):
            if visible:
                res[r][nc - i - 1].append("R")

    # top to bottom
    for c in range(nc):
        for i, visible in enumerate(visible_trees([row[c] for row in trees])):
            if visible:
                res[i][c].append("T")

    # bottom to top
    for c in range(nc):
        for i, visible in enumerate(visible_trees([row[c] for row in trees][::-1])):
            if visible:
                res[nr - i - 1][c].append("B")

    return res

def count_visibilities(trees: list[list[int]]) -> int:
    vis = visibilities(trees)
    return sum(bool(x) for row in vis for x in row)

assert count_visibilities(TREES) == 21

with open('day08.txt') as f:
    trees = parse(f.read())
    print(count_visibilities(trees))

def viewing_distance(trees: list[list[int]], i: int, j: int) -> list[int]:
    original_i, original_j = i, j 
    h = trees[i][j]

    nr = len(trees)
    nc = len(trees[0])

    res = []

    # left
    vd = 0
    while j > 0:
        j -= 1
        vd += 1

        #print("left", i, j, vd, trees[i][j], h)

        if trees[i][j] >= h:
            break 

    res.append(vd)

    # right
    i, j, vd = original_i, original_j, 0
    while j < nc - 1:
        j += 1
        vd += 1

        #print("right", i, j, vd, trees[i][j], h)

        if trees[i][j] >= h:
            break

    res.append(vd)

    # up
    i, j, vd = original_i, original_j, 0
    while i > 0:
        i -= 1
        vd += 1

        #print("up", i, j, vd, trees[i][j], h)

        if trees[i][j] >= h:
            break

    res.append(vd)

    # down
    i, j, vd = original_i, original_j, 0
    while i < nr - 1:
        i += 1
        vd += 1

        #print("down", i, j, vd, trees[i][j], h)

        if trees[i][j] >= h:
            break

    res.append(vd)

    return res

def product(xs):
    res = 1
    for x in xs:
        res *= x
    return res

def best_location(trees: list[list[int]]) -> int:
    nr = len(trees)
    nc = len(trees[0])

    return max(product(viewing_distance(trees, i, j))
               for i in range(nr) 
               for j in range(nc)
               )


assert best_location(TREES) == 8

print(best_location(trees))