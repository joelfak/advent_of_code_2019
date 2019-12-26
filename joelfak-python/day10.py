#!/usr/bin/env python3

from helpfunctions import *
import unittest, sys, math
from collections import defaultdict
from pprint import pprint

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def fromObject(cls, orig):
        return cls(orig.x, orig.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __repr__(self):
        return "Point (x: {}, y: {})".format(self.x, self.y)

    def __hash__(self):
        return 1000000*int(self.x) + int(self.y)

class Vector(Point):
    def __repr__(self):
        return "Vector (x: {}, y: {})".format(self.x, self.y)

    def getLength(self):
        return math.sqrt(self.x**2 + self.y**2)

    def getAngle(self):
        return math.atan2(self.y, self.x)

    def getMinimalVector(self):
        gcd = math.gcd(self.x, self.y)
        if gcd == 0:
            return Vector(0, 0)
        return Vector(self.x / gcd, self.y / gcd)

def getSetOfAsteroids(asteroidMap):
    visibleAsteroids = set()
    for y in range(len(asteroidMap)):
        for x in range(len(asteroidMap[y])):
            if asteroidMap[y][x] == '#':
                visibleAsteroids.add(Point(x,y))
    return visibleAsteroids

def getNumberOfVisibleAsteroids(asteroidMap, base):
    d = defaultdict(list)
    for y in range(len(asteroidMap)):
        for x in range(len(asteroidMap[y])):
            if asteroidMap[y][x] == '#':
                asteroid = Point(x, y)
                vectorToAsteroid = Vector.fromObject(asteroid - base)
                d[vectorToAsteroid.getMinimalVector()].append(asteroid)
    # pprint(d)
    return len(d) - 1

def findBestBaseLocation(asteroidMap):
    asteroids = getSetOfAsteroids(asteroidMap)
    p = max(asteroids, key = lambda x: getNumberOfVisibleAsteroids(asteroidMap, x))
    return (p, getNumberOfVisibleAsteroids(asteroidMap, p))

def part1(asteroidMap):
    asteroidMap = [[char for char in row] for row in asteroidMap]
    return findBestBaseLocation(asteroidMap)

def part2(data):
    return 0

## Unit tests ########################################################

class TestDay10(unittest.TestCase):
    asteroidMap1 = [ '.#..#',
                    '.....',
                    '#####',
                    '....#',
                    '...##' ]
    asteroidMap1 = [[char for char in row] for row in asteroidMap1]

    def test_getListOfAsteroids(self):
        self.assertEqual(getSetOfAsteroids(self.asteroidMap1), set([
                                    Point(0,2),
                                    Point(1,0), Point(1,2),
                                    Point(2,2),
                                    Point(3,2), Point(3,4),
                                    Point(4,0), Point(4,2), Point(4,3), Point(4,4)]))

    def test_getNumberOfVisibleAsteroids_1_0(self):
        self.assertEqual(getNumberOfVisibleAsteroids(self.asteroidMap1, Point(1,0)), 7)

    def test_getNumberOfVisibleAsteroids_4_0(self):
        self.assertEqual(getNumberOfVisibleAsteroids(self.asteroidMap1, Point(4,0)), 7)

    def test_getNumberOfVisibleAsteroids_0_2(self):
        self.assertEqual(getNumberOfVisibleAsteroids(self.asteroidMap1, Point(0,2)), 6)

    def test_getNumberOfVisibleAsteroids_1_2(self):
        self.assertEqual(getNumberOfVisibleAsteroids(self.asteroidMap1, Point(1,2)), 7)

    def test_getNumberOfVisibleAsteroids_2_2(self):
        self.assertEqual(getNumberOfVisibleAsteroids(self.asteroidMap1, Point(2,2)), 7)

    def test_getNumberOfVisibleAsteroids_3_2(self):
        self.assertEqual(getNumberOfVisibleAsteroids(self.asteroidMap1, Point(3,2)), 7)

    def test_getNumberOfVisibleAsteroids_4_2(self):
        self.assertEqual(getNumberOfVisibleAsteroids(self.asteroidMap1, Point(4,2)), 5)

    def test_getNumberOfVisibleAsteroids_4_3(self):
        self.assertEqual(getNumberOfVisibleAsteroids(self.asteroidMap1, Point(4,3)), 7)

    def test_getNumberOfVisibleAsteroids_3_4(self):
        self.assertEqual(getNumberOfVisibleAsteroids(self.asteroidMap1, Point(3,4)), 8)

    def test_getNumberOfVisibleAsteroids_4_4(self):
        self.assertEqual(getNumberOfVisibleAsteroids(self.asteroidMap1, Point(4,4)), 7)

    def test_findBestBaseLocation(self):
        self.assertEqual(findBestBaseLocation(self.asteroidMap1), (Point(3,4), 8))

    def test_map2(self):
        asteroidMap = [ '......#.#.',
                        '#..#.#....',
                        '..#######.',
                        '.#.#.###..',
                        '.#..#.....',
                        '..#....#.#',
                        '#..#....#.',
                        '.##.#..###',
                        '##...#..#.',
                        '.#....####']
        asteroidMap = [[char for char in row] for row in asteroidMap]
        self.assertEqual(findBestBaseLocation(asteroidMap), (Point(5,8), 33))

    def test_map3(self):
        asteroidMap = [ '#.#...#.#.',
                        '.###....#.',
                        '.#....#...',
                        '##.#.#.#.#',
                        '....#.#.#.',
                        '.##..###.#',
                        '..#...##..',
                        '..##....##',
                        '......#...',
                        '.####.###.' ]
        asteroidMap = [[char for char in row] for row in asteroidMap]
        self.assertEqual(findBestBaseLocation(asteroidMap), (Point(1,2), 35))

    def test_map4(self):
        asteroidMap = [ '.#..#..###',
                        '####.###.#',
                        '....###.#.',
                        '..###.##.#',
                        '##.##.#.#.',
                        '....###..#',
                        '..#.#..#.#',
                        '#..#.#.###',
                        '.##...##.#',
                        '.....#.#..' ]
        asteroidMap = [[char for char in row] for row in asteroidMap]
        self.assertEqual(findBestBaseLocation(asteroidMap), (Point(6,3), 41))

    def test_map5(self):
        asteroidMap = [ '.#..##.###...#######',
                        '##.############..##.',
                        '.#.######.########.#',
                        '.###.#######.####.#.',
                        '#####.##.#.##.###.##',
                        '..#####..#.#########',
                        '####################',
                        '#.####....###.#.#.##',
                        '##.#################',
                        '#####.##.###..####..',
                        '..######..##.#######',
                        '####.##.####...##..#',
                        '.#####..#.######.###',
                        '##...#.##########...',
                        '#.##########.#######',
                        '.####.#.###.###.#.##',
                        '....##.##.###..#####',
                        '.#.#.###########.###',
                        '#.#.#.#####.####.###',
                        '###.##.####.##.#..##' ]
        asteroidMap = [[char for char in row] for row in asteroidMap]
        self.assertEqual(findBestBaseLocation(asteroidMap), (Point(11,13), 210))
## Main ########################################################

if __name__ == '__main__':

    print("Advent of code day 10")
    print("Part1 result: {}".format(part1(getStringsFromFile(sys.argv[1]))))
    # print("Part2 result: {}".format(part2(getIntsFromFile(sys.argv[1]))))
