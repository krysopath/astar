import numpy as np

from typing import List, Tuple, Protocol, TypeVar, Iterator, Dict
from time import time

import helper as h


T = TypeVar('T')
Location = TypeVar('Location')


class Graph(Protocol):
    def neighbors(self, id: Location) -> List[Location]: pass


GridLocation = Tuple[int, int]


class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: List[GridLocation] = []

    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]  # E W N S

        if (x + y) % 2 == 0:     # see A* "Ugly paths" for an explanation
            neighbors.reverse()  # S N W E

        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results

    def __iter__(self):
        return ((x, y) for y in range(self.height) for x in range(self.width))


class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass


class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: Dict[GridLocation, float] = {}
        self.start = time()

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)

    def as_pixels(self, **kwargs):
        rgb = np.zeros([self.width, self.height, 3], dtype=np.uint8)
        t = (time()-self.start)/1000

        for location in self:
            x, y = location
            rgb[x, y] = h.make_pixel((x, y, t), **kwargs)

        return rgb