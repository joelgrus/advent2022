from dataclasses import dataclass, field
from typing import Union


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
class Specific:
    name: str
    value: int

@dataclass
class MathOp:
    name: str
    op: str
    left_name: str
    right_name: str
    left: Union[Specific, 'MathOp'] = field(init=False)
    right: Union[Specific, 'MathOp'] = field(init=False)

Monkey = Specific | MathOp

def parse(line: str) -> Monkey:
    name, rest = line.split(": ")
    if " " in rest:
        left, op, right = rest.split(" ")
        return MathOp(name, op, left, right)
    else:
        return Specific(name, int(rest))

@dataclass
class Monkeys:
    monkeys: dict[str, Monkey]
    order: list[Monkey] = field(init=False)
    root: Monkey = field(init=False)

    def __post_init__(self):
        self.root = self.monkeys['root']

        # topological sort
        self.order = []
        sorted_monkeys = set()

        for monkey in self.monkeys.values():
            match monkey:
                case Specific(name=name):
                    self.order.append(monkey)
                    sorted_monkeys.add(name)

        while len(self.order) < len(self.monkeys):
            for name, monkey in self.monkeys.items():
                if name in sorted_monkeys:
                    continue
                
                match monkey:
                    case MathOp(name=name, left_name=left_name, right_name=right_name) if left_name in sorted_monkeys and right_name in sorted_monkeys:
                        monkey.left = self.monkeys[left_name]
                        monkey.right = self.monkeys[right_name]
                        self.order.append(monkey)
                        sorted_monkeys.add(name)

    @staticmethod
    def parse(raw: str) -> 'Monkeys':
        monkeys = [parse(line) for line in raw.splitlines()]
        return Monkeys({m.name: m for m in monkeys})

    # find all monkeys that are rooted at a given monkey
    def rooted_at(self, monkey: Monkey) -> set[str]:
        match monkey:
            case Specific(name=name):
                return {name}
            case MathOp(name=name, left=left, right=right):
                return self.rooted_at(left) | self.rooted_at(right) | {name}

    def calculate(self, monkey: Monkey | None = None) -> int:
        if monkey is None:
            monkey = self.root
        match monkey:
            case Specific(value=value):
                return value
            case MathOp(op=op, left=left, right=right):
                left_value = self.calculate(left)
                right_value = self.calculate(right)
                match op:
                    case "+":
                        return left_value + right_value
                    case "-":
                        return left_value - right_value
                    case "*":
                        return left_value * right_value
                    case "/":
                        return left_value // right_value
                    case _:
                        raise ValueError("Unknown op")
            case _:
                raise ValueError("Unknown monkey")

    def find_human_value(self) -> int:
        # first, find path
        path = [self.monkeys['humn']]

        while True:
            if path[-1] == self.root:
                break
            for monkey in self.monkeys.values():
                match monkey:
                    case MathOp(left=left, right=right) if left == path[-1] or right == path[-1]:
                        path.append(monkey)

        # now path is [humn, ..., root]
        target_value = 0

        while path:
            match path.pop():
                case MathOp(name='root', left=left, right=right):
                    target_value = self.calculate(right) if left == path[-1] else self.calculate(left)
                    print("root: target value", target_value)
                case MathOp(name='humn') | Specific(name='humn'):
                    print("humn: target value", target_value)
                    return target_value
                case MathOp(op=op, left=left, right=right):
                    if left == path[-1]:
                        known = 'right'
                        child_value = self.calculate(right)
                    else:
                        known = 'left'
                        child_value = self.calculate(left)

                    print("op", op, "left", left, "right", right)
                    print("target value", target_value)
                    print("known", known)
                    print("child value", child_value)
                    

                    match op:
                        case "+":
                            # target = child + new_target
                            # new_target = target - child
                            target_value = target_value - child_value
                        case "-" if known == 'left':
                            # target = child - new_target
                            # new_target = child - target
                            target_value = child_value - target_value
                        case "-" if known == 'right':
                            # target = new_target - child
                            # new_target = child + target
                            target_value = child_value + target_value
                        case "*":
                            # target = child * new_target
                            # new_target = target / child
                            target_value = target_value // child_value
                        case "/" if known == 'left':
                            # target = child / new_target
                            # new_target = child / target
                            target_value = child_value // target_value
                        case "/" if known == 'right':
                            # target = new_target / child
                            # new_target = child * target
                            target_value = child_value * target_value
                        case _:
                            raise ValueError("Unknown op")

        raise ValueError("No path to human")  



MONKEYS = Monkeys.parse(RAW)
assert MONKEYS.calculate() == 152
assert MONKEYS.find_human_value() == 301

with open('day21.txt') as f:
    monkeys = Monkeys.parse(f.read())
    print(monkeys.calculate())
    print(monkeys.find_human_value())
