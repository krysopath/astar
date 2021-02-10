import noise
import random

#SEED = 2.998192384729384
SEED = random.random()


def linmap(t, a, b, c, d):
    return c + ((d-c)/(b-a)) * (t - a)


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def value(self):
        return noise.snoise3(self.x/25, self.y/25, SEED*100, octaves=3)

    def __str__(self):
        val = linmap(self.value(), -1, 1, 0, 1)
        if val <= .1:
            return "0"
        elif val <= .2:
            return "1"
        elif val <= .3:
            return "2"
        elif val <= .4:
            return "3"
        elif val <= .5:
            return "4"
        elif val <= .6:
            return "5"
        elif val <= .7:
            return "6"
        elif val <= .8:
            return "7"
        elif val <= .9:
            return "8"
        elif val <= 1:
            return "9"
        else:
            return "."


class Map:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.positions = {}

        self.width, self.height = self.dimensions

        for x in range(self.width):
            for y in range(self.height):
                self.positions[(x, y)] = Position(x, y)

    def get(self, coord):
        return self.positions[coord]

    def __str__(self):
        return "\n".join(
            ["".join(
                [f"{self.positions[(x, y)]}" for x in range(self.width)]
            ) for y in range(self.height)]
        )


def main():
    m = Map((60*1, 20*1))
    print(m)


if __name__ == '__main__':
    main()

