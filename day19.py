import re
from dataclasses import dataclass
from typing import NamedTuple, Iterator
from collections import deque
import heapq
import tqdm

RAW = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

# Blueprint 1:
#   Each ore robot costs 4 ore.
#   Each clay robot costs 2 ore.
#   Each obsidian robot costs 3 ore and 14 clay.
#   Each geode robot costs 2 ore and 7 obsidian.

rgx = r"Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian."

@dataclass
class Blueprint:
    id: int
    ore_robot_ore_cost: int
    clay_robot_ore_cost: int
    obsidian_robot_ore_cost: int
    obsidian_robot_clay_cost: int
    geode_robot_ore_cost: int
    geode_robot_obsidian_cost: int

    @staticmethod
    def from_string(s) -> 'Blueprint':
        match = re.match(rgx, s)
        if match:
            return Blueprint(*[int(x) for x in match.groups()])
        else:
            raise ValueError(f"Failed to parse blueprint: {s}")

BLUEPRINTS = [Blueprint.from_string(s) for s in RAW.splitlines()]


class State(NamedTuple):
    time: int = 0
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    ore_robots: int = 1
    clay_robots: int = 0
    obsidian_robots: int = 0
    geode_robots: int = 0


    def overestimate_max_geodes(self, blueprint: Blueprint, max_time: int = 24) -> int:
        geodes = self.geode
        geode_robots = self.geode_robots
        time = self.time
        while time < max_time:
            time += 1
            geodes += geode_robots
            geode_robots += 1
        return geodes

    def priority(self, blueprint: Blueprint) -> tuple:
        return (
            -self.overestimate_max_geodes(blueprint),
            -self.geode_robots,
            -self.geode,
            -self.obsidian_robots,
            -self.obsidian,
            -self.clay,
        )

    def next_states(self, blueprint: Blueprint) -> Iterator['State']:
        new_time = self.time + 1
        new_ore = self.ore + self.ore_robots
        new_clay = self.clay + self.clay_robots
        new_obsidian = self.obsidian + self.obsidian_robots
        new_geode = self.geode + self.geode_robots

        # build nothing:
        yield self._replace(time=new_time, ore=new_ore, clay=new_clay, obsidian=new_obsidian, geode=new_geode)

        # build ore robot
        if self.ore >= blueprint.ore_robot_ore_cost:
            yield self._replace(time=new_time, ore=new_ore - blueprint.ore_robot_ore_cost, clay=new_clay, obsidian=new_obsidian, geode=new_geode, ore_robots=self.ore_robots + 1)

        # build clay robot
        if self.ore >= blueprint.clay_robot_ore_cost:
            yield self._replace(time=new_time, ore=new_ore - blueprint.clay_robot_ore_cost, clay=new_clay, obsidian=new_obsidian, geode=new_geode, clay_robots=self.clay_robots + 1)

        # build obsidian robot
        if self.ore >= blueprint.obsidian_robot_ore_cost and self.clay >= blueprint.obsidian_robot_clay_cost:
            yield self._replace(time=new_time, ore=new_ore - blueprint.obsidian_robot_ore_cost, clay=new_clay - blueprint.obsidian_robot_clay_cost, obsidian=new_obsidian, geode=new_geode, obsidian_robots=self.obsidian_robots + 1)

        # build geode robot
        if self.ore >= blueprint.geode_robot_ore_cost and self.obsidian >= blueprint.geode_robot_obsidian_cost:
            yield self._replace(time=new_time, ore=new_ore - blueprint.geode_robot_ore_cost, clay=new_clay, obsidian=new_obsidian - blueprint.geode_robot_obsidian_cost, geode=new_geode, geode_robots=self.geode_robots + 1)


def max_geodes(blueprint: Blueprint, max_time: int = 24) -> int:
    q = []
    state = State()
    omg = state.overestimate_max_geodes(blueprint, max_time)
    best = -1
    best_omg = -omg
    heapq.heappush(q, ((-omg, -state.geode_robots, -state.geode), state))

    seen = {state}

    while q:
        priority, state = heapq.heappop(q)
        omg = priority[0]
        if omg > best_omg:
            print("new omg", omg)
            print(state)
            best_omg = omg
        #print(state)
        #print(omg)
        #print(len(q))
        #print()

        if -omg < best:
            return best

        if omg == 0:
            return 0

        if state.time >= max_time:
            continue

        for new_state in state.next_states(blueprint):
            if new_state in seen:
                continue
            else:
                seen.add(new_state)
            #print("new state")
            #print(new_state)
            #print()
            if new_state.geode > best:
                best = new_state.geode
                print("new best", new_state)
                print("best omg", best_omg)
            new_priority = ( -new_state.overestimate_max_geodes(blueprint, max_time), -new_state.geode_robots, -new_state.geode)
            heapq.heappush(q, (new_priority, new_state))

    raise ValueError()

def quality_level(blueprint: Blueprint, max_time: int = 24) -> int:
    return max_geodes(blueprint, max_time) * blueprint.id 

def total_quality_level(blueprints: list[Blueprint], max_time: int = 24) -> int:
    total = 0

    for blueprint in tqdm.tqdm(blueprints):
        print(blueprint)
        ql = quality_level(blueprint, max_time)
        print(ql)
        total += ql
    
    return total

with open('day19.txt') as f:
    raw = f.read()

blueprints = [Blueprint.from_string(s) for s in raw.splitlines()]

#print(total_quality_level(blueprints, 24))

def geode_product(blueprints: list[Blueprint], max_time: int = 32) -> int:
    product = 1

    for blueprint in tqdm.tqdm(blueprints):
        print(blueprint)
        geodes = max_geodes(blueprint, max_time)
        print(geodes)
        product *= geodes

    return product

print(geode_product(blueprints[:3], 32))