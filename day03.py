from string import ascii_lowercase, ascii_uppercase

CHARS = '.' + ascii_lowercase + ascii_uppercase


def priority(c: str) -> int:
    return CHARS.index(c)


assert priority('a') == 1
assert priority('L') == 38

def find_duplicate(rucksack: str) -> str:
    n = len(rucksack)

    compartment1 = rucksack[:n // 2]
    compartment2 = rucksack[n // 2:]

    intersection = set(compartment1) & set(compartment2)

    assert len(intersection) == 1

    return intersection.pop()

RAW = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

RUCKSACKS = RAW.strip().split('\n')

assert sum(
    priority(find_duplicate(rucksack))
    for rucksack in RUCKSACKS
) == 157

rucksacks = open('day03.txt').read().strip().split('\n')

print(sum(
    priority(find_duplicate(rucksack))
    for rucksack in rucksacks
))

def groups_of_three(rucksacks: list[str]) -> list[list[str]]:
    return [
        rucksacks[i:i+3]
        for i in range(0, len(rucksacks), 3)
    ]

def find_duplicate_in_group(rucksack_group: list[str]) -> str:
    items = set(rucksack_group[0])
    for rucksack in rucksack_group[1:]:
        items &= set(rucksack)

    assert len(items) == 1

    return items.pop()

assert sum(
    priority(find_duplicate_in_group(group))
    for group in groups_of_three(RUCKSACKS)
) == 70

print(
    sum(
        priority(find_duplicate_in_group(group)) 
        for group in groups_of_three(rucksacks)
        )
)