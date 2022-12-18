from dataclasses import dataclass, field
from typing import NamedTuple, Optional
from collections import deque
import heapq
import re

RAW = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

rgx = r"Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z, ]+)"

@dataclass
class Valve:
    name: str
    flow: int
    tunnels: list[str]

    @staticmethod
    def from_string(s: str) -> "Valve":
        res = re.match(rgx, s)
        if res:
            name, flow, tunnels = res.groups()
        else:
            raise ValueError(f"Could not parse {s}")
        return Valve(name, int(flow), tunnels.split(", "))

class QItem(NamedTuple):
    negative_best_possible: int
    loc: str
    time: int
    released: int
    open: set[str]
    current_path: list[str]


@dataclass
class Network:
    valves: list[Valve]
    valves_by_name: dict[str, Valve] = field(default_factory=dict)

    def best_possible(self, so_far: int, remaining_steps: int, open: set[str]) -> int:
        # smallest to largest
        closed_flows = sorted([v.flow for v in self.valves if v.name not in open])

        tot = so_far
        while remaining_steps > 0 and closed_flows:
            tot += closed_flows.pop() * remaining_steps
            remaining_steps -= 1

        return tot


    @staticmethod
    def from_string(s: str) -> "Network":
        valves = [Valve.from_string(line) for line in s.splitlines()]
        by_name = {v.name: v for v in valves}
        return Network(valves, by_name)


    def most_pressure(self, num_steps: int = 30, start: str = "AA") -> int:
        valves_with_flow = {v.name for v in self.valves if v.flow > 0}

        best_possible = self.best_possible(0, num_steps, set())
        q = [QItem(-best_possible, start, 0, 0, set(), current_path=[])]

        best = -1

        count = 0

        while q:
            qitem = heapq.heappop(q)
            count += 1
            if count % 100_000 == 0:
                print(count)
                print(qitem)
                print(best)

            #print()
            #print("popping", qitem)
            nbp, loc, time, released, open, current_path = qitem
            steps_remaining = num_steps - time
            # The best remaining possibility is less than something we've already achieved
            if -nbp < best:
                return best
            # out of time or all good valves are open
            elif time == num_steps or valves_with_flow == open:
                if released > best:
                    best = released
                    #print("new best", best)
                    #print(qitem)
                continue
            valve = self.valves_by_name[loc]
            if valve.flow > 0 and loc not in open:
                #print("opening", valve)
                #print("steps remaining", steps_remaining)

                flow = valve.flow * (steps_remaining - 1)
                bp = self.best_possible(released + flow, steps_remaining - 1, open | {loc})
                item = QItem(
                    -bp,
                    loc,
                    time + 1,
                    released + flow,
                    open | {loc},
                    []  # reset current path when I open a valve
                )
                #print("pushing", item)
                heapq.heappush(q, item)
            for tunnel in valve.tunnels:
                if tunnel in current_path:
                    # backtracking is a waste of time
                    continue
                bp = self.best_possible(released, steps_remaining - 1, open)
                item = QItem(-bp, tunnel, time + 1, released, open, current_path + [tunnel])
                #print("pushing", item)
                heapq.heappush(q, item)

        return best

NETWORK = Network.from_string(RAW)
#print(NETWORK.most_pressure(30, 'AA'))

with open('day16.txt') as f:
    raw = f.read()
network = Network.from_string(raw)
# print(network.most_pressure(30, 'AA'))


### Elephants

class EQItem(NamedTuple):
    negative_best_possible: int
    loc: str
    elephant_loc: str
    time: int
    released: int
    open: set[str]
    current_path: list[str]
    elephant_current_path: list[str]


@dataclass
class ENetwork:
    valves: list[Valve]
    valves_by_name: dict[str, Valve] = field(default_factory=dict)

    def best_possible(self, so_far: int, remaining_steps: int, open: set[str]) -> int:
        # smallest to largest
        closed_flows = sorted([v.flow for v in self.valves if v.name not in open])

        tot = so_far
        while remaining_steps > 0 and closed_flows:
            # for me
            new_flow = closed_flows.pop()

            # for the elephant
            if closed_flows:
                new_flow += closed_flows.pop()

            tot += new_flow * remaining_steps
            remaining_steps -= 1

        return tot


    @staticmethod
    def from_string(s: str) -> "ENetwork":
        valves = [Valve.from_string(line) for line in s.splitlines()]
        by_name = {v.name: v for v in valves}
        return ENetwork(valves, by_name)


    def most_pressure(self, num_steps: int = 26, start: str = "AA") -> int:
        valves_with_flow = {v.name for v in self.valves if v.flow > 0}

        best_possible = self.best_possible(0, num_steps, set())
        q = [EQItem(-best_possible, start, start, 0, 0, set(), [], [])]

        best = -1

        count = 0

        while q:
            qitem = heapq.heappop(q)
            #print(qitem)
            count += 1
            if count % 100_000 == 0:
                print(count)
                print(qitem)
                print("best", best)
                print("qsize", len(q))

            #print()
            #print("popping", qitem)
            nbp, loc, eloc, time, released, open, current_path, e_path = qitem
            steps_remaining = num_steps - time
            # The best remaining possibility is less than something we've already achieved
            if -nbp < best:
                return best
            # out of time or all good valves are open
            if released > best:
                best = released
                print("new best", best)
                print(qitem)
            if time == num_steps or valves_with_flow == open:
                continue

            valve = self.valves_by_name[loc]
            evalve = self.valves_by_name[eloc]

            choices = []
            echoices = []

            # by convention, I always open a valve first
            if valve.flow > 0 and loc not in open:
                # I can open a valve
                choices.append(None)
            if evalve.flow > 0 and eloc not in open and eloc != loc:
                # elephant can open a valve
                echoices.append(None)

            # I can go to any tunnel that's not on my current path
            choices.extend([t for t in valve.tunnels if t not in current_path])

            # elephant can go to any tunnel that's not on its current path
            echoices.extend([t for t in evalve.tunnels if t not in e_path])

            for choice in choices:
                new_loc = loc if choice is None else choice
                added_flow1 = ((steps_remaining - 1) * valve.flow) if choice is None else 0
                new_open1 = (open | {loc}) if choice is None else open
                new_path = [] if choice is None else current_path + [choice]
                for echoice in echoices:
                    new_eloc = eloc if echoice is None else echoice
                    new_open = (new_open1 | {eloc}) if echoice is None else new_open1
                    new_epath = [] if echoice is None else e_path + [echoice]
                    added_flow2 = ((steps_remaining - 1) * evalve.flow) if echoice is None else 0
                    new_released = released + added_flow1 + added_flow2
                    #print(choice, echoice, new_released, " = ", released, added_flow1, added_flow2 )
                    new_nbp = -self.best_possible(new_released, steps_remaining - 1, new_open)

                    item = EQItem(
                        new_nbp,
                        new_loc,
                        new_eloc,
                        time + 1,
                        new_released,
                        new_open,
                        new_path,
                        new_epath
                    )

                    heapq.heappush(q, item)

ENETWORK = ENetwork.from_string(RAW)

#print(ENETWORK.most_pressure(26, 'AA'))

#enetwork = ENetwork.from_string(raw)
#print(enetwork.most_pressure(26, 'AA'))


#######
# Optimized
#######

class OQItem(NamedTuple):
    negative_best_possible: int
    loc: str
    elephant_loc: str
    time: int
    etime: int
    released: int
    open: set[str]
    prev: Optional['OQItem'] = None


@dataclass
class ONetwork:
    valves: list[Valve]
    valves_by_name: dict[str, Valve] = field(default_factory=dict)
    distances: dict[str, dict[str, int]] = field(default_factory=dict)
    names: set[str] = field(default_factory=set)

    def __post_init__(self):
        self.valves_by_name = {v.name: v for v in self.valves}
        self.distances = self.compute_distances()
        self.valves = [v for v in self.valves if v.flow > 0]
        self.names = {v.name for v in self.valves}

    def compute_distances(self) -> dict[str, dict[str, int]]:
        distances = {}
        for start in self.valves_by_name:
            distances[start] = {}
            q: deque[tuple[int, str]] = deque([(0, start)])
            while q:
                dist, loc = q.popleft()
                if loc in distances[start]:
                    continue
                distances[start][loc] = dist
                for tunnel in self.valves_by_name[loc].tunnels:
                    q.append((dist + 1, tunnel))

        # now clean things out

        for name, dists in distances.items():
            for v in self.valves:
                if v.flow == 0 or v.name == name:
                    del dists[v.name]

        return distances

    @staticmethod
    def from_string(s: str) -> "ONetwork":
        valves = [Valve.from_string(line) for line in s.splitlines()]
        return ONetwork(valves)

    def best_possible(self, so_far: int, remaining_steps: int, open: set[str]) -> int:
        # smallest to largest
        closed_flows = sorted([v.flow for v in self.valves if v.name not in open])

        tot = so_far
        while remaining_steps > 0 and closed_flows:
            # for me
            new_flow = closed_flows.pop()

            # for the elephant
            if closed_flows:
                new_flow += closed_flows.pop()

            tot += new_flow * remaining_steps
            # one to move, one to open
            remaining_steps -= 2

        return tot


    def most_pressure(self, num_steps: int = 26, start: str = "AA") -> int:
        best_possible = self.best_possible(0, num_steps, set())
        q = [OQItem(-best_possible, start, start, 0, 0, 0, set())]

        best = -1
        best_qitem = None
        count = 0

        while q:
            qitem = heapq.heappop(q)
            #print(qitem)
            count += 1
            if count % 100_000 == 0:
                print(count)
                print(qitem)
                print("best", best)
                print("qsize", len(q))

            #print()
            #print("popping", qitem)
            nbp, loc, eloc, time, etime, released, open, _ = qitem

            # The best remaining possibility is less than something we've already achieved
            if -nbp < best:
                return best

            # new best
            if released > best:
                best = released
                best_qitem = qitem
                print("new best", best)
                #print(qitem)

            # all open, so nothing else to do
            if len(open) == len(self.valves):
                continue

            # where I go first, if I am earlier than I have to
            if time <= etime and time < num_steps:
                steps_remaining = num_steps - time

                # # if it's not open I should open it
                # # otherwise why am I here?
                # if loc not in open and loc != start:
                #     new_open = open | {loc}
                #     added_flow = ((steps_remaining - 1) * valve.flow)
                #     new_released = released + added_flow
                #     new_nbp = -self.best_possible(new_released, steps_remaining - 1, new_open)
                #     heapq.heappush(q, OQItem(new_nbp, loc, eloc, time + 1, etime, new_released, new_open, prev=qitem))

                # move and open
                dists = self.distances[loc]
                for tunnel in set(dists) - open:
                    time_to_move = dists[tunnel]
                    added_flow = ((steps_remaining - time_to_move - 1) * self.valves_by_name[tunnel].flow)
                    #print("added flow", added_flow)
                    new_released = released + added_flow                    
                    #print("new released", new_released)
                    new_open = open | {tunnel}
                    new_nbp = -self.best_possible(new_released, steps_remaining - time_to_move - 1, new_open)
                    heapq.heappush(q, OQItem(new_nbp, tunnel, eloc, time + time_to_move + 1, etime, new_released, new_open, prev=qitem))

            # where the elephant goes first, if he is earlier then he has to
            if etime <= time and etime < num_steps:
                steps_remaining = num_steps - etime
                #evalve = self.valves_by_name[eloc]

                # # if it's not open I should open it 
                # # (otherwise why would I be here?)
                # if eloc not in open and eloc != start:
                #     new_open = open | {eloc}
                #     added_flow = ((steps_remaining - 1) * evalve.flow)
                #     new_released = released + added_flow
                #     new_nbp = -self.best_possible(new_released, steps_remaining - 1, new_open)
                #     heapq.heappush(q, OQItem(new_nbp, loc, eloc, time, etime + 1, new_released, new_open, prev=qitem))

                # if it is open, I should move
                dists = self.distances[eloc]
                for tunnel in set(dists) - open:
                    time_to_move = dists[tunnel]
                    added_flow = ((steps_remaining - time_to_move - 1) * self.valves_by_name[tunnel].flow)
                    #print("added flow", added_flow)
                    new_released = released + added_flow                    
                    #print("new released", new_released)
                    new_open = open | {tunnel}
                    new_nbp = -self.best_possible(new_released, steps_remaining - time_to_move - 1, new_open)
                    heapq.heappush(q, OQItem(new_nbp, loc, tunnel, time, etime + time_to_move + 1, new_released, new_open, prev=qitem))

        return best


ONETWORK = ONetwork.from_string(RAW)

#bq = ONETWORK.most_pressure(26, 'AA')

onetwork = ONetwork.from_string(raw)
best = onetwork.most_pressure(26, 'AA')
print(best)