#!/usr/bin/env python3

from helpfunctions import *
import unittest, sys, math
from collections import defaultdict
from pprint import pprint
from functools import reduce

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

    def getClockwiseAngleFromNegativeY(self):
        angle = self.getAngle() + math.pi/2
        if angle < 0:
            angle += 2*math.pi
        return angle

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

def calculateVisibleAsteroids(asteroidMap, base, verbose=False):
    d = defaultdict(list)
    for asteroid in getSetOfAsteroids(asteroidMap):
        if asteroid != base:
            vectorToAsteroid = Vector.fromObject(asteroid - base)
            d[vectorToAsteroid.getMinimalVector()].append(vectorToAsteroid)

    for direction, vectors in d.items():
        vectors.sort(key=lambda vector: vector.getLength())

    if verbose:
        pprint(d)

    return d

def getNumberOfVisibleAsteroids(asteroidMap, base, verbose=False):
    d = calculateVisibleAsteroids(asteroidMap, base, verbose)
    return len(d)

def findBestBaseLocation(asteroidMap, verbose=False):
    asteroids = getSetOfAsteroids(asteroidMap)
    p = max(asteroids, key = lambda x: getNumberOfVisibleAsteroids(asteroidMap, x))
    return (p, getNumberOfVisibleAsteroids(asteroidMap, p, verbose=verbose))

def findBaseInMap(asteroidMap):
    for y in range(len(asteroidMap)):
        for x in range(len(asteroidMap[y])):
            if asteroidMap[y][x] == 'X':
                return Point(x, y)
    return None

def destroyAsteroids(asteroidMap, numAsteroidsToDestroy=math.inf, findBestBase=False, verbose=False):
    if findBestBase:
        base = findBestBaseLocation(asteroidMap, verbose=verbose)[0]
    else:
        base = findBaseInMap(asteroidMap)

    directionsMap = calculateVisibleAsteroids(asteroidMap, base, verbose)
    sortedDirections = sorted(directionsMap.keys(), key=lambda vector: vector.getClockwiseAngleFromNegativeY())

    numberOfDestroyedAsteroids = 0
    latestDestroyedAsteroid = None
    done = False
    while sum([len(vector) for vector in directionsMap.values()]) > 0:
        for direction in sortedDirections:
            if len(directionsMap[direction]) > 0:
                latestDestroyedAsteroid = base + directionsMap[direction].pop(0)
                numberOfDestroyedAsteroids += 1
                if numberOfDestroyedAsteroids >= numAsteroidsToDestroy:
                    done = True
                    break
        if done:
            break

    if verbose:
        print("NumberOfDestroyedAsteroids: {}".format(numberOfDestroyedAsteroids))
    return latestDestroyedAsteroid

def part1(asteroidMap):
    asteroidMap = [[char for char in row] for row in asteroidMap]
    return findBestBaseLocation(asteroidMap)

def part2(asteroidMap):
    asteroidMap = [[char for char in row] for row in asteroidMap]
    asteroid = destroyAsteroids(asteroidMap, 200, findBestBase=True)
    return asteroid.x*100+asteroid.y

## Unit tests ########################################################

class TestDay10_part1(unittest.TestCase):
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
        self.assertEqual(findBestBaseLocation(asteroidMap, verbose=False), (Point(11,13), 210))

class TestDay10_part2_map1(unittest.TestCase):
    asteroidMap1 = [ '.#....#####...#..',
                    '##...##.#####..##',
                    '##...#...#.#####.',
                    '..#.....X...###..',
                    '..#.#.....#....##' ]
    asteroidMap1 = [[char for char in row] for row in asteroidMap1]

    def test_findBaseInMap(self):
        self.assertEqual(findBaseInMap(self.asteroidMap1), Point(8,3))

    def test_destroyAsteroids1(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 4), Point(10, 0))

    def test_destroyAsteroids2(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 7), Point(12, 1))

    def test_destroyAsteroids3(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 36), Point(14, 3))

class TestDay10_part2_map2(unittest.TestCase):
    asteroidMap1 = [   '.#..##.###...#######',
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
    asteroidMap1 = [[char for char in row] for row in asteroidMap1]

    def test_destroyAsteroids1(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 1, findBestBase=True), Point(11,12))

    def test_destroyAsteroids2(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 2, findBestBase=True), Point(12,1))

    def test_destroyAsteroids3(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 3, findBestBase=True), Point(12,2))

    def test_destroyAsteroids4(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 10, findBestBase=True), Point(12,8))

    def test_destroyAsteroids5(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 20, findBestBase=True), Point(16,0))

    def test_destroyAsteroids6(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 50, findBestBase=True), Point(16,9))

    def test_destroyAsteroids7(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 100, findBestBase=True), Point(10,16))

    def test_destroyAsteroids8(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 199, findBestBase=True), Point(9,6))

    def test_destroyAsteroids9(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 200, findBestBase=True), Point(8,2))

    def test_destroyAsteroids10(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 201, findBestBase=True), Point(10,9))

    def test_destroyAsteroids11(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, 299, findBestBase=True), Point(11,1))

    def test_destroyAsteroids12(self):
        self.assertEqual(destroyAsteroids(self.asteroidMap1, findBestBase=True), Point(11,1))

## Main ########################################################

if __name__ == '__main__':

    print("Advent of code day 10")
    print("Part1 result: {}".format(part1(getStringsFromFile(sys.argv[1]))))
    print("Part2 result: {}".format(part2(getStringsFromFile(sys.argv[1]))))
