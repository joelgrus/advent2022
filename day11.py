from typing import Callable
import operator


# An operation takes old and returns new
Operation = Callable[[int], int]

# A test takes worry and returns a monkey id
Test = Callable[[int], int]

class Monkey:
    def __init__(self, id: int, items: list[int], operation: Operation, test: Test):
        self.id = id 
        self.items = items
        self.operation = operation
        self.test = test

    @staticmethod
    def from_string(s: str) -> 'Monkey':
        lines = s.splitlines()

        id = int(lines[0].split()[-1].replace(":",""))
        items = [int(i) for i in lines[1].split(":")[-1].split(",")]

        operation = Monkey.parse_operation(lines[2])
        test = Monkey.parse_test(lines[3:6])

        return Monkey(id, items, operation, test)

    @staticmethod
    def parse_operation(s: str) -> Operation:
        new = s.split("=")[-1].strip()
        l, op, r = new.split()

        if op == "*":
            fn = operator.mul
        elif op == "+":
            fn = operator.add
        elif op == "-":
            fn = operator.sub
        elif op == "/":
            fn = operator.truediv

        match [l, r]:
            case ["old", "old"]:
                return lambda x: fn(x, x)
            case ["old", n]:
                return lambda x: fn(x, int(n))
            case [n, "old"]:
                return lambda x: fn(int(n), x)
            case [n, m]:
                return lambda x: fn(int(n), int(m))
            case _:
                raise ValueError(f"Invalid operation {s}")

    @staticmethod
    def parse_test(lines: list[str]) -> Test:
        test, if_true, if_false = lines
        monkey_if_true = int(if_true.split()[-1])
        monkey_if_false = int(if_false.split()[-1])
        divisible_by = int(test.split()[-1])

        test = lambda x: monkey_if_true if x % divisible_by == 0 else monkey_if_false
        test.divisible_by = divisible_by
        return test

    @staticmethod
    def parse_all(s: str) -> list['Monkey']:
        return [Monkey.from_string(m) for m in s.split("\n\n")]


class KeepAway:
    def __init__(self, monkeys: list[Monkey], use_relief: bool = True):
        self.monkeys = monkeys
        self.inspection_counts = {monkey.id: 0 for monkey in monkeys}
        self.use_relief = use_relief

        self.modulus = 1
        for monkey in self.monkeys:
            self.modulus *= monkey.test.divisible_by

    def take_turn(self, monkey: Monkey) -> None:
        #print("monkey", monkey.id, "has", monkey.items)
        for worry_level in monkey.items:
            #print("worry level", worry_level)

            # inspect
            self.inspection_counts[monkey.id] += 1
            worry_level = monkey.operation(worry_level)
            #print("worry level after operation", worry_level)

            # relief
            if self.use_relief:
                worry_level = worry_level // 3
            #print("worry level after relief", worry_level)

            # modulus
            worry_level = worry_level % self.modulus
            #print("worry level after modulus", worry_level)

            # test
            target = monkey.test(worry_level)
            #print("target monkey", target)

            assert target != monkey.id, "Monkey can't throw to itself"

            # throw
            self.monkeys[target].items.append(worry_level)

        monkey.items.clear()

    def round(self):
        for monkey in self.monkeys:
            self.take_turn(monkey)

RAW = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


MONKEYS = Monkey.parse_all(RAW)
KEEP_AWAY = KeepAway(MONKEYS)

def monkey_business_level(game: KeepAway, nr: int = 20) -> int:
    for _ in range(nr):
        game.round()
    ics = sorted(game.inspection_counts.values(), reverse=True)
    return ics[0] * ics[1]

assert monkey_business_level(KeepAway(Monkey.parse_all(RAW))) == 10605
assert monkey_business_level(KeepAway(Monkey.parse_all(RAW), use_relief=False), nr=10000) == 2713310158

with open('day11.txt') as f:
    raw = f.read()

monkeys = Monkey.parse_all(raw)
keep_away = KeepAway(monkeys)
print(monkey_business_level(keep_away))

monkeys = Monkey.parse_all(raw)
keep_away = KeepAway(monkeys, use_relief=False)
print(monkey_business_level(keep_away, nr=10000))
