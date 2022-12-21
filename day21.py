
"""
don't look at me, look at day21.v2.py
"""

from dataclasses import dataclass, field

RAW = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

@dataclass
class Monkey:
    name: str
    yell: int = 0
    op: str | None = None
    left: str | None = None
    right: str | None = None
    sorted: bool = False

    @staticmethod
    def parse(line: str) -> 'Monkey':
        name, rest = line.split(": ")
        if " " in rest:
            left, op, right = rest.split(" ")
            return Monkey(name, 0, op, left, right)
        else:
            return Monkey(name, int(rest))

@dataclass
class Monkeys:
    monkeys: dict[str, Monkey]
    order: list[str] = field(init=False)

    def __post_init__(self):
        # topological sort
        self.order = []
        sorted_monkeys = set()

        for monkey in self.monkeys.values():
            if monkey.op is None:
                self.order.append(monkey.name)
                sorted_monkeys.add(monkey.name)

        while len(self.order) < len(self.monkeys):
            for name, monkey in self.monkeys.items():
                if name in sorted_monkeys:
                    continue
                elif monkey.left in sorted_monkeys and monkey.right in sorted_monkeys:
                    self.order.append(name)
                    sorted_monkeys.add(name)

    @staticmethod
    def parse(raw: str) -> 'Monkeys':
        monkeys = [Monkey.parse(line) for line in raw.splitlines()]
        return Monkeys({m.name: m for m in monkeys})

    # find all monkeys that are rooted at a given monkey
    def rooted_at(self, name: str) -> set[str]:
        monkey = self.monkeys[name]
        match monkey:
            case Monkey(op=None):
                return {name}
            case Monkey(left=left, right=right):
                assert left is not None
                assert right is not None
                return self.rooted_at(left) | self.rooted_at(right) | {name}

    def dyell(self, root: str = 'root') -> int:
        to_consider = self.rooted_at(root)
        for name in self.order:
            if name not in to_consider:
                continue
            monkey = self.monkeys[name]              
            if monkey.op is None:
                continue

            assert monkey.left is not None
            assert monkey.right is not None
            if monkey.op == "+":
                monkey.yell = self.monkeys[monkey.left].yell + self.monkeys[monkey.right].yell
            elif monkey.op == "-":
                monkey.yell = self.monkeys[monkey.left].yell - self.monkeys[monkey.right].yell
            elif monkey.op == "*":
                monkey.yell = self.monkeys[monkey.left].yell * self.monkeys[monkey.right].yell
            elif monkey.op == "/":
                monkey.yell = self.monkeys[monkey.left].yell // self.monkeys[monkey.right].yell
        return self.monkeys[root].yell


    def find_humn_value(self):
        target = 'humn'
        path: list[tuple[str, str]] = [('-', 'humn')]

        while target != 'root':
            for name, monkey in self.monkeys.items():
                if monkey.left == target:
                    path.append(('L', name))
                    target = name
                    break
                elif monkey.right == target:
                    path.append(('R', name))
                    target = name
                    break
                else:
                    pass

        print("path", path)

        monkey = self.monkeys['root']
        if monkey.left == path[-1][1]:
            # find right value
            assert monkey.right is not None
            target_value = self.dyell(monkey.right)
        else:
            assert monkey.left is not None
            target_value = self.dyell(monkey.left)

        print('initial target value', target_value)

        # now get root off the path
        path.pop()

        while path:
            dir, name = path.pop()
            monkey = self.monkeys[name]

            print(dir, name, monkey)

            if name == 'humn':
                return target_value
            elif dir == 'L':
                assert monkey.right is not None
                right = self.monkeys[monkey.right]
                child_value = self.dyell(root=right.name)
            else:
                assert monkey.left is not None
                left = self.monkeys[monkey.left]
                child_value = self.dyell(root=left.name)

            print("child value", child_value)

            # have target_value, child_value, and op
            if monkey.op == "+":
                # target_value = child_value + x
                # x = target_value - child_value
                target_value = target_value - child_value
            elif monkey.op == "-" and dir == 'L':
                # target_value = x - child_value
                # x = target_value + child_value
                target_value = target_value + child_value
            elif monkey.op == "-" and dir == "R":
                # target_value = child_value - x
                # x = child_value - target_value
                target_value = child_value - target_value   
            elif monkey.op == "*":
                # target_value = child_value * x
                # x = target_value / child_value
                target_value = target_value // child_value
            elif monkey.op == "/" and dir == 'L':
                # target_value = x / child_value
                # x = target_value * child_value
                target_value = target_value * child_value
            elif monkey.op == "/" and dir == 'R':
                # target_value = child_value / x
                # x = child_value / target_value
                target_value = child_value // target_value
            else:
                raise Exception("Invalid op")

            print("op", monkey.op)
            print("new target", target_value)


MONKEYS = Monkeys.parse(RAW)

assert MONKEYS.dyell() == 152

with open('day21.txt') as f:
    monkeys = Monkeys.parse(f.read())
    print(monkeys.dyell())

