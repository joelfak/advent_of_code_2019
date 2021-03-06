import re

from heapq import heappop, heappush
from collections import Counter, defaultdict
from copy import deepcopy
from intcode import Computer


def next_pos(y, x, command):
    if command == 1:
        return y - 1, x
    if command == 2:
        return y + 1, x
    if command == 3:
        return y, x - 1
    return y, x + 1


def explore(d):   
    ymin = -100
    ymax = 100
    xmin = -100
    xmax = 100
    
    walls = set()
    seen = { (0, 0) }
    frontier = [(Computer(d, 1), 1, 0, 0), (Computer(d, 2), 2, 0, 0), (Computer(d, 3), 3, 0, 0), (Computer(d, 4), 4, 0, 0)]
    oy, ox = -1, -1

    for computer, command, y, x in frontier:
        _, retval = computer.get_output()
        ny, nx = next_pos(y, x, command)

        if retval == 0:
            walls.add((ny, nx))
            continue
        elif retval == 2:
            oy = ny
            ox = nx

        seen.add((ny, nx))

        if ny > ymin and (ny - 1, nx) not in walls | seen:
            newcomp = deepcopy(computer)
            newcomp.set_input(1)
            frontier.append((newcomp, 1, ny, nx))
        if ny < ymax and (ny + 1, nx) not in walls | seen:
            newcomp = deepcopy(computer)
            newcomp.set_input(2)
            frontier.append((newcomp, 2, ny, nx))
        if nx > xmin and (ny, nx - 1) not in walls | seen:
            newcomp = deepcopy(computer)
            newcomp.set_input(3)
            frontier.append((newcomp, 3, ny, nx))
        if nx < xmax and (ny, nx + 1) not in walls | seen:
            newcomp = deepcopy(computer)
            newcomp.set_input(4)
            frontier.append((newcomp, 4, ny, nx))

        
    return walls, seen, oy, ox


def flood_fill(walls, seen, oxygen):
    minutes = 0

    while seen - oxygen:
        newox = set()

        for oy, ox in oxygen:
            if (oy - 1, ox) in seen - oxygen and (oy - 1, ox) not in newox:
                newox.add((oy - 1, ox))
            if (oy + 1, ox) in seen - oxygen and (oy + 1, ox) not in newox:
                newox.add((oy + 1, ox))
            if (oy, ox - 1) in seen - oxygen and (oy, ox - 1) not in newox:
                newox.add((oy, ox - 1))
            if (oy, ox + 1) in seen - oxygen and (oy, ox + 1) not in newox:
                newox.add((oy, ox + 1))

        oxygen |= newox

        minutes += 1

    return minutes


def solve(d):
    walls, seen, oy, ox = explore(d)

    return flood_fill(walls, seen, { (oy, ox) })
    

def read_and_solve():
    with open('input_15.txt') as f:
        data = list(map(int, f.readline().split(',')))
        return solve(data)

if __name__ == '__main__':
    print(read_and_solve())