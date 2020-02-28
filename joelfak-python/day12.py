#!/usr/bin/env python3

from helpfunctions import *
import unittest, sys
import math

class Vector3d:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def fromObject(cls, orig):
        return cls(orig.x, orig.y, orig.z)

    @classmethod
    def fromList(cls, list):
        return cls(list[0], list[1], list[2])

    def toTuple(self):
        return (self.x, self.y, self.z)

    def __add__(self, other):
        return Vector3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and self.z == other.z)

    def __hash__(self):
        return 1000000000000*int(self.x) + 1000000*int(self.y) + int(self.z)

    def getLength(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def getUnitVector(self):
        l = list(map(lambda v: 1 if v>0 else (-1 if v<0 else 0), self.toTuple()))
        return Vector3d.fromList(l)

    def __repr__(self):
        return "Vector3d (x: {}, y: {}, z: {})".format(self.x, self.y, self.z)

class Moon:
    def __init__(self, position=(0,0,0), velocity=(0,0,0)):
        self.position = Vector3d.fromList(position)
        self.velocity = Vector3d.fromList(velocity)

    def applyGravityOfMoon(self, otherMoon):
        self.velocity += (otherMoon.position - self.position).getUnitVector()
        return self

    def applyGravityOfMoons(self, otherMoons):
        for moon in otherMoons:
            self.applyGravityOfMoon(moon)
        return self

    def applyVelocity(self):
        self.position += self.velocity
        return self

    def getPositionAndVelocity(self):
        return (self.position, self.velocity)

    def getState(self):
        return (self.position.toTuple(), self.velocity.toTuple())

    def getPotentialEnergy(self):
        return sum((map(abs, self.position.toTuple())))

    def getKineticEnergy(self):
        return sum((map(abs, self.velocity.toTuple())))

    def getTotalEnergy(self):
        return self.getPotentialEnergy() * self.getKineticEnergy()

    def getEnergyVector(self):
        return [self.getPotentialEnergy(), self.getKineticEnergy(), self.getTotalEnergy()]

from pprint import pprint

class MoonSystem:
    def __init__(self, moons=[]):
        self.moons = moons
        self.simulationCycles = 0
        self.visitedStates = set()
        self.saveState()
        self.x = [moon.position.x for moon in self.moons]
        self.y = [moon.position.y for moon in self.moons]
        self.z = [moon.position.z for moon in self.moons]
        self.vel_x = [moon.velocity.x for moon in self.moons]
        self.vel_y = [moon.velocity.y for moon in self.moons]
        self.vel_z = [moon.velocity.z for moon in self.moons]

    def simulateOneStep(self):
        for moon in self.moons:
            moon.applyGravityOfMoons(self.moons)
        for moon in self.moons:
            moon.applyVelocity()

    def simulate(self, steps=1):
        for step in range(steps):
            self.simulateOneStep()
            self.saveState()
        return self

    def getTotalSystemEnergy(self):
        return sum(moon.getTotalEnergy() for moon in self.moons)

    def getCurrentState(self):
        return tuple([moon.getState() for moon in self.moons])

    def saveState(self):
        self.visitedStates.add(self.getCurrentState())

    def printVisitedStates(self):
        pprint(self.visitedStates)

    def simulateUntilPreviousState_old(self, verbose=0):
        while True:
            self.simulateOneStep()
            self.simulationCycles += 1
            if verbose > 0 and self.simulationCycles % verbose == 0:
                print("Cycles: {}".format(self.simulationCycles))
            if self.getCurrentState() in self.visitedStates:
                break
            self.saveState()

    def simulateUntilPreviousState(self, verbose=0):
        self.velocity += (otherMoon.position - self.position).getUnitVector()

        return

    def getSimulationCycles(self):
        return self.simulationCycles

def part1():
    ms = MoonSystem([Moon((16, -11, 2)), Moon((0, -4, 7)), Moon((6, 4, -10)), Moon((-3, -2, -4))])
    ms.simulate(1000)
    return ms.getTotalSystemEnergy()

def part2(data):
    return 0

## Unit tests ########################################################

class TestVector3d(unittest.TestCase):
    def test_fromList(self):
        self.assertEqual(Vector3d.fromList([2,3,4]), Vector3d(2,3,4))

    def test_toTuple(self):
        self.assertEqual(Vector3d(2,3,4).toTuple(), (2,3,4))

    def test_add(self):
        self.assertEqual(Vector3d(1,2,-3) + Vector3d(3,-1,5), Vector3d(4,1,2))

    def test_subtract(self):
        self.assertEqual(Vector3d(3,2,6) - Vector3d(2,4,-2), Vector3d(1,-2,8))

    def test_getLength(self):
        self.assertEqual(Vector3d(4,4,7).getLength(), 9)

    def test_getUnitVector(self):
        self.assertEqual(Vector3d(2,-3,0).getUnitVector(), Vector3d(1,-1,0))

class TestMoon(unittest.TestCase):
    def test_applyGravityOfMoon(self):
        self.assertEqual(Moon((3,5,0)).applyGravityOfMoon(Moon((5,3,0))).velocity,
                         Vector3d(1,-1,0))

    def test_applyGravityOfMoons(self):
        otherMoons = [Moon((1,2,2)), Moon((3,4,4))]
        self.assertEqual(Moon((3,1,3)).applyGravityOfMoons(otherMoons).velocity,
                         Vector3d(-1, 2, 0))

    def test_applyVelocity(self):
        self.assertEqual(Moon((1,2,3), velocity=(2,-3,0)).applyVelocity().position,
                         Vector3d(3,-1,3))

    def test_getPotentialEnergy(self):
        self.assertEqual(Moon((1,-2,3), velocity=(2,-3,0)).getPotentialEnergy(), 6)

    def test_getKineticEnergy(self):
        self.assertEqual(Moon((1,-2,3), velocity=(2,-3,0)).getKineticEnergy(), 5)

    def test_getTotalEnergy(self):
        self.assertEqual(Moon((1,-2,3), velocity=(2,-3,0)).getTotalEnergy(), 30)

class TestMoonSystem(unittest.TestCase):
    def test_simpleSystem(self):
        moon1 = Moon((3,5,0))
        moon2 = Moon((6,2,0))
        MoonSystem([moon1, moon2]).simulate()
        self.assertEqual(moon1.getPositionAndVelocity(), (Vector3d(4,4,0), Vector3d(1,-1,0)))
        self.assertEqual(moon2.getPositionAndVelocity(), (Vector3d(5,3,0), Vector3d(-1,1,0)))

    def test_sampleSystem0steps(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        MoonSystem(moons)
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d(-1,  0, 2), Vector3d( 0, 0, 0)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 2,-10,-7), Vector3d( 0, 0, 0)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 4, -8, 8), Vector3d( 0, 0, 0)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 3,  5,-1), Vector3d( 0, 0, 0)))

    def test_sampleSystem1step(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        MoonSystem(moons).simulate()
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d( 2,-1, 1), Vector3d( 3,-1,-1)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 3,-7,-4), Vector3d( 1, 3, 3)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 1,-7, 5), Vector3d(-3, 1,-3)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 2, 2, 0), Vector3d(-1,-3, 1)))

    def test_sampleSystem2steps(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        MoonSystem(moons).simulate(2)
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d( 5,-3,-1), Vector3d( 3,-2,-2)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 1,-2, 2), Vector3d(-2, 5, 6)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 1,-4,-1), Vector3d( 0, 3,-6)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 1,-4, 2), Vector3d(-1,-6, 2)))

    def test_sampleSystem3steps(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        MoonSystem(moons).simulate(3)
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d( 5,-6,-1), Vector3d( 0,-3, 0)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 0, 0, 6), Vector3d(-1, 2, 4)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 2, 1,-5), Vector3d( 1, 5,-4)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 1,-8, 2), Vector3d( 0,-4, 0)))

    def test_sampleSystem4steps(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        MoonSystem(moons).simulate(4)
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d( 2,-8, 0), Vector3d(-3,-2, 1)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 2, 1, 7), Vector3d( 2, 1, 1)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 2, 3,-6), Vector3d( 0, 2,-1)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 2,-9, 1), Vector3d( 1,-1,-1)))

    def test_sampleSystem5steps(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        MoonSystem(moons).simulate(5)
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d(-1,-9, 2), Vector3d(-3,-1, 2)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 4, 1, 5), Vector3d( 2, 0,-2)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 2, 2,-4), Vector3d( 0,-1, 2)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 3,-7,-1), Vector3d( 1, 2,-2)))

    def test_sampleSystem6steps(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        MoonSystem(moons).simulate(6)
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d(-1,-7, 3), Vector3d( 0, 2, 1)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 3, 0, 0), Vector3d(-1,-1,-5)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 3,-2, 1), Vector3d( 1,-4, 5)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 3,-4,-2), Vector3d( 0, 3,-1)))

    def test_sampleSystem7steps(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        MoonSystem(moons).simulate(7)
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d( 2,-2, 1), Vector3d( 3, 5,-2)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 1,-4,-4), Vector3d(-2,-4,-4)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 3,-7, 5), Vector3d( 0,-5, 4)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 2, 0, 0), Vector3d(-1, 4, 2)))

    def test_sampleSystem8steps(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        MoonSystem(moons).simulate(8)
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d( 5, 2,-2), Vector3d( 3, 4,-3)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 2,-7,-5), Vector3d( 1,-3,-1)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 0,-9, 6), Vector3d(-3,-2, 1)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 1, 1, 3), Vector3d(-1, 1, 3)))

    def test_sampleSystem9steps(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        MoonSystem(moons).simulate(9)
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d( 5, 3,-4), Vector3d( 0, 1,-2)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 2,-9,-3), Vector3d( 0,-2, 2)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 0,-8, 4), Vector3d( 0, 1,-2)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 1, 1, 5), Vector3d( 0, 0, 2)))

    def test_sampleSystem10steps(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        MoonSystem(moons).simulate(10)
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d( 2, 1,-3), Vector3d(-3,-2, 1)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 1,-8, 0), Vector3d(-1, 1, 3)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 3,-6, 1), Vector3d( 3, 2,-3)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 2, 0, 4), Vector3d( 1,-1,-1)))

    def test_sampleSystemEnergy10steps(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        moonSystem = MoonSystem(moons)
        moonSystem.simulate(10)
        self.assertEqual(moons[0].getEnergyVector(), [6,6,36])
        self.assertEqual(moons[1].getEnergyVector(), [9,5,45])
        self.assertEqual(moons[2].getEnergyVector(), [10,8,80])
        self.assertEqual(moons[3].getEnergyVector(), [6,3,18])
        self.assertEqual(moonSystem.getTotalSystemEnergy(), 179)

    def test_sampleSystem2_100steps(self):
        moons = [Moon((-8, -10, 0)), Moon((5, 5, 10)), Moon((2, -7, 3)), Moon((9, -8, -3))]
        MoonSystem(moons).simulate(100)
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d(  8, -12,  -9), Vector3d(-7,   3,   0)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 13,  16,  -3), Vector3d( 3, -11,  -5)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d(-29, -11,  -1), Vector3d(-3,   7,   4)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 16, -13,  23), Vector3d( 7,   1,   1)))

    def test_sampleSystem2_Energy100steps(self):
        moons = [Moon((-8, -10, 0)), Moon((5, 5, 10)), Moon((2, -7, 3)), Moon((9, -8, -3))]
        moonSystem = MoonSystem(moons)
        moonSystem.simulate(100)
        self.assertEqual(moons[0].getEnergyVector(), [29,10,290])
        self.assertEqual(moons[1].getEnergyVector(), [32,19,608])
        self.assertEqual(moons[2].getEnergyVector(), [41,14,574])
        self.assertEqual(moons[3].getEnergyVector(), [52,9,468])
        self.assertEqual(moonSystem.getTotalSystemEnergy(), 1940)

class TestMoonSystem_part2(unittest.TestCase):
    def test_sampleSystem1(self):
        moons = [Moon((-1, 0, 2)), Moon((2, -10, -7)), Moon((4, -8, 8)), Moon((3, 5, -1))]
        ms = MoonSystem(moons)
        ms.simulateUntilPreviousState(100)
        self.assertEqual(ms.getSimulationCycles(), 2772)
        self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d(-1,  0, 2), Vector3d( 0, 0, 0)))
        self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 2,-10,-7), Vector3d( 0, 0, 0)))
        self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 4, -8, 8), Vector3d( 0, 0, 0)))
        self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 3,  5,-1), Vector3d( 0, 0, 0)))

    # def test_sampleSystem2(self):
    #     moons = [Moon((-8, -10, 0)), Moon((5, 5, 10)), Moon((2, -7, 3)), Moon((9, -8, -3))]
    #     ms = MoonSystem(moons)
    #     ms.simulateUntilPreviousState(10000)
    #     self.assertEqual(ms.getSimulationCycles(), 4686774924)
    #     self.assertEqual(moons[0].getPositionAndVelocity(), (Vector3d(-8, -10,  0), Vector3d( 0, 0, 0)))
    #     self.assertEqual(moons[1].getPositionAndVelocity(), (Vector3d( 5,   5, 10), Vector3d( 0, 0, 0)))
    #     self.assertEqual(moons[2].getPositionAndVelocity(), (Vector3d( 2,  -7,  3), Vector3d( 0, 0, 0)))
    #     self.assertEqual(moons[3].getPositionAndVelocity(), (Vector3d( 9,  -8, -3), Vector3d( 0, 0, 0)))

## Main ########################################################

if __name__ == '__main__':

    print("Advent of code day 12")
    print("Part1 result: {}".format(part1()))
    # print("Part2 result: {}".format(part2(getIntsFromFile(sys.argv[1]))))
