from dataclasses import dataclass, field
import tqdm

RAW = """1
2
-3
3
-2
0
4"""

NUMBERS = [int(x) for x in RAW.splitlines()]

@dataclass
class Node:
    n: int
    next: 'Node' = field(init=False)
    prev: 'Node' = field(init=False)


@dataclass
class EncryptedFile:
    numbers: list[int]
    decryption_key: int = 1
    nodes: list[Node] = field(init=False)
    i: int = 0
    n: int = 0

    def __str__(self) -> str:
        out = []
        node = self.nodes[0]
        for _ in range(self.n):
            out.append(node.n)
            node = node.next

        return ",".join(str(x) for x in out)

    def __post_init__(self):
        self.nodes = [Node(n * self.decryption_key) for n in self.numbers]
        self.n = len(self.numbers)
        for i, node in enumerate(self.nodes):
            node.prev = self.nodes[i - 1]
            node.next = self.nodes[(i + 1) % len(self.nodes)]

    def mix(self):
        for i in range(self.n):
            #print(i, str(self))
            self.step()

    def grove(self) -> int:
        # find 0
        node = self.nodes[0]
        while node.n != 0:
            node = node.next

        outputs = []
        for _ in range(3):
            for _ in range(1000):
                node = node.next
            outputs.append(node.n)

        return sum(outputs)                
    

    def step(self):
        #print("step", self.i)
        node = self.nodes[self.i]
        to_move = node.n % (self.n - 1)
        #print("node", node.n, "to_move", to_move)
        for _ in range(to_move):
            before = node.prev
            after = node.next
            after_after = after.next

            # hook up before to after 
            before.next = after
            after.prev = before

            # hook up after to node
            after.next = node
            node.prev = after

            # hook up node to after_after
            node.next = after_after
            after_after.prev = node

        self.i = (self.i + 1) % len(self.numbers)


EF = EncryptedFile(NUMBERS)
EF.mix()
assert EF.grove() == 3

KEY = 811589153
EF = EncryptedFile(NUMBERS, KEY)
for _ in range(10):
    EF.mix()
assert EF.grove() == 1623178306


with open('day20.txt') as f:
    raw = f.read()
numbers = [int(x) for x in raw.splitlines()]

# part 1
#ef = EncryptedFile(numbers)
#ef.mix()
#print(ef.grove())

ef = EncryptedFile(numbers, KEY)
for _ in tqdm.trange(10):
    ef.mix()
print(ef.grove())