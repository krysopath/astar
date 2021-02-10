import heapq
from typing import List, Tuple, Dict, Optional


import graphs as g


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, g.T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: g.T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> g.T:
        return heapq.heappop(self.elements)[1]


def heuristic(a: g.GridLocation, b: g.GridLocation) -> float:
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph: g.WeightedGraph, start: g.Location, goal: g.Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)

    came_from: Dict[g.Location, Optional[g.Location]] = {}
    cost_so_far: Dict[g.Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: g.Location = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


# diagram4 = GridWithWeights(1024, 1024)
# diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
# diagram4.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
#                                        (4, 3), (4, 4), (4, 5), (4, 6),
#                                        (4, 7), (4, 8), (5, 1), (5, 2),
#                                        (5, 3), (5, 4), (5, 5), (5, 6),
#                                        (5, 7), (5, 8), (6, 2), (6, 3),
#                                        (6, 4), (6, 5), (6, 6), (6, 7),
#                                        (7, 3), (7, 4), (7, 5)]}
#
# came_from, cost_so_far = a_star_search(diagram4, (3, 4), (7, 5))

#save_graph(diagram4)


