import math
import ProblemSpec
import Obstacle
import ASVconfig
import Rectangle2D
import line2D

class Tester:
    """
        Implementation of the Tester class in python
    """
    MAX_STEP = 0.001
    MIN_BOOM_LENGTH = 0.05
    MAX_BOOM_LENGTH = 0.05
    #Rectangle2D is defined as a tuple of x, y, w, h
    BOUNDS = (0,0,1,1)
    DEFAULT_MAX_ERROR = 1e-5

    def __init__(self, maxError = DEFAULT_MAX_ERROR):
        """
            Constructor.
        """
        self.maxError = maxError
        self.lenientBounds = grow(BOUNDS, self.maxError)

        self.ps = ProblemSpec()

    def getMinimumArea(self, asvCount):
        """
            Returns the minimum area required for the given number of ASVs.

            @param asvCount the number of ASVs

            @return the minimum area required
        """
        radius = 0.007 * (asvCount - 1)
        return(math.pi * radius**2)

    def grow(self, rect, delta):
        """
            Creates a new rectangle2d (x,y,w,h) that is grown by delta in each direction
            compared to the give nrectangle2d

            @param rect the Rectangle2d to expand

            @param delta the amount to expand by

            @return a Rectangle2d expanded by delta in each direction
        """
        return ((rect[0] - delta/2, rect[1] - delta/2, rect[2] + delta, rect[3] + delta))

    def hasInitialFirst(self):
        """
            @return whether the first cfg is the initial cfg
        """
        try:
            return(self.ps.getPath()[0].maxDistance(self.ps.getInitialState())) <= self.maxError
        except BaseException e:
            print("ProblemSpec not initialised")
            return (False)

    def testInitialFirst(self, testNo, verbose):
        """
            Checks that the first configuration in the solution path is the initial
            configuration
        """
        print("Test " + str(testNo) + ": Initial state")
        if (!hasInitialFirst()):
            print("FAILED: Solution must start at initial state.")
            return (False)
        else:
            print("Passed.")
            return (True)

    def hasGoalLast(self):
        """
            @return whether the last config is the goal config
        """
        try:
            path = self.ps.getPath()
            return (path[-1].maxDistance(self.ps.getGoalState())) <= self.maxError
        except BaseException e:
            print("ProblemSpec not initialised")
            return (False)

    def testGoalLast(self, testNo, verbose):
        """
            Checks that the last configuration in the solution path is the goal
            configuration
        """
        print("Test " + str(testNo) + ": Goal state")
        if (!hasGoalLast()):
            print("FAILED: Solution path must end at goal state.")
            return (False)
        else:
            print("Passed.")
            return (True)

    def addToAll(self, oldList, delta):
        """
            Copies a list and increments each value by delta

            @param list the list of integers to add to

            @param delta the number to modify each element by

            @return a copy of the list where each value is incremented by delta
        """
        newList = oldList[:]
        for i in newList:
            i += delta
        return (newList)

    def isValidStep(self, cfg0, cfg1):
        """
            Determines whether the step from s0 to s1 is a valid primitive step.

            @param cfg0 A configuration

            @param cfg1 Another configuration

            @return whether the step from s0 to s1 is a valid step
        """
        return (cfg0.maxDistance(cfg1) <= self.maxError + MAX_STEP)

    def getInvalidSteps(self):
        """
            @return the preceding path indices of any invalid steps.
        """
        badSteps = []
        path = self.ps.getPath()
        state = path[0]
        for i in range(1,len(path)):
            nextState = path[i]
            if (!isValidStep(state,nextState)):
                badSteps.append(i-1)
            state = nextState
        return (badSteps)

    def testValidSteps(self, testNo, verbose):
        """
            Checks that the steps in between configurations do not exeed the maximum
            primitive step distance
        """
        print("Test " + str(testNo) + ": Step sizes")
        badSteps = getInvalidSteps()
        if badSteps:
            print("FAILED: Distance exceeds 0.001 for "+str(len(badSteps))+" of "+str(len(self.ps.getPath()) - 1)+" step(s).")
            if verbose:
                print("Starting line for each invalid step:")
                print(str(addToAll(badSteps,2)))
            return (False)
        else:
            print("Passed.")
            return (True)

    def hasValidBoomLengths(self, cfg):
        """
            Determines whether the booms in the given config have valid lengths
        """
        points = cfg.getASVPositions()
        for i in range(1, len(points)):
            p0 = points[i-1]
            p1 = points[i]
            boomLength = math.sqrt(abs(p1[0]-p0[0])**2 + abs(p1[1]-p0[1])**2)
            if boomLength < MIN_BOOM_LENGTH - maxError:
                return (False)
            elif boomLength > MAX_BOOM_LENGTH + maxError:
                return (False)
        return (True)

    def getInvalidBoomStates(self):
        """
            @return the path indices of any states with invalid booms.
        """
        badStates = []
        path = self.ps.getPath()
        for i in range(len(path)):
            if not hasValidBoomLengths(path[i]):
                badStates.append(i)
        return (badStates)

    def testBoomLengths(self, testNo, verbose):
        """
            Checks that the booms in each config have length within the allowable range
        """
        print("Test " + str(testNo) + ": Boom lengths")
        badStates = getInvalidBoomStates()
        if badStates:
            print("FAILED: Invalid boomlength for " + str(len(badStates)) + " of "
                  + str(len(self.ps.getPath())) + " state(s)")

            if verbose:
                print ("Line for each invalid cfg:")
                print(str(addToAll(badStates,2)))

            return (False)
        else:
            print("Passed.")
            return (True)


    def normaliseAngle(self, angle):
        """
            Normalises an angle to the range (-pi, pi)

            @param angle the angel to normalise

            @return the normalised angle
        """
        while angle <= -math.pi:
            angle += 2 * math.pi
        while angle > math.pi:
            angle -= 2* math.pi
        return (angle)

    def isConvex(self, cfg):
        """
            Determines whether the given config is convex

            @param cfg the configuration to test

            @return whether the given config is convex
        """
        points = cfg.getASVPositions()
        points.append(points[0])
        points.append(points[1])

        requiredSign = 0.0
        totalTurned = 0.0
        p0 = points[0]
        p1 = points[1]
        angle = math.atan2(p1[1] - p0[1], p1[0] - p0[0])

        for i in range(2,len(points)):
            p2 = points[i]
            nextAngle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
            turningAngle = normaliseAngle(nextAngle - angle)

            if turningAngle == math.pi:
                return(False)

            totalTurned += abs(turningAngle)
            if totalTurned > 3 * math.pi:
                return(False)

            turnSign = 0
            if turningAngle < -self.maxError:
                turnSign = -1
            elif turningAngle > self.maxError:
                turnSign = 1
            else:
                turnSign = 0

            if turnSign * requiredSign < 0:
                return(False)
            elif turnSign != 0:
                requiredSign = turnSign

            p0 = p1
            p1 = p2
            angle = nextAngle

        return (True)


    def getNonConvexStates(self):
        """
            @return the path indices of any non-convex states
        """
        badStates = []
        path = self.ps.getPath()
        for i in range(len(path)):
            if not isConvex(path[i]):
                badStates.append(i)
        return (badStates)

    def testConvexity(self,testNo, verbose):
        """
            Checks that each config in the path is convex (and hence also
            not self intersection)
        """
        print("Test " + str(testNo) + ": Convexity")
        badStates = getNonConvexStates()
        if badStates:
            print("FAILED: " + str(len(badStates)) + " out of " + str(len(self.ps.getPath())) + " state(s) are not convex.")

            if verbose:
                print ("Line for each invalid cfg:")
                print(str(addToAll(badStates,2)))

            return(False)
        else:
            print("Passed.")
            return (True)

    def hasEnoughArea(self, cfg):
        """
            Determines whether the given config has sufficient area

            @param cfg the config to test

            @return whether the given configuration has sufficient area
        """
        total = 0
        points = cfg.getASVPositions()
        points.append(points[0])
        points.append(points[1])

        for i in range(1, len(points)-1):
            total += points[i][0] * (points[i+1][1] - points[i-1][1])

        area = abs(total)/2
        return (area >= getMinimumArea(cfg.getASVCount()) - self.maxError)

    def getInvalidAreaStates(self):
        """
            @return the path indices of any states with insufficient area
        """
        path = self.ps.getPath()
        badStates = []
        for i in range(len(path)):
            if not hasEnoughArea(path[i]):
                badStates.append(i)

        return(badStates)

    def testAreas(self, testNo, verbose):
        """
            Checks whether each config has sufficient internal area
        """
        print("Test " + str(testNo) + ": Areas")
        badStates = getInvalidAreaStates()
        if badStates:
            print("FAILED: " + str(len(badStates)) + " of " + str(len(self.ps.getPath())) + " state(s) have insufficient area.")

            if verbose:
                print ("Line for each invalid cfg:")
                print(str(addToAll(badStates,2)))

            return (False)
        else:
            print("Passed.")
            return (True)


    def fitsBounds(self, cfg):
        """
            Determines whether the given cfg fits wholly within the bounds

            @param cfg the configuration to test

            @return whether the given cfg fits wholly within the bounds
        """
        c = [False,False,False,False]
        for p in cfg.getASVPositions():
            c[0] = p[0] > self.lenientBounds[0]
            c[1] = p[1] > self.lenientBounds[1]
            c[2] = p[0] < self.lenientBounds[0] + self.lenientBounds[2]
            c[3] = p[1] < self.lenientBounds[1] + self.lenientBounds[3]
            if c[0] and c[1] and c[2] and c[3]:
                return (True)
        return (False)

    def getOutOfBoundsStates(self):
        """
            @return the path indices of any states that are out of bounds.
        """
        path = self.ps.getPath()
        badStates = []
        for i in range(len(path)):
            if (!fitsBounds(path[i])):
                badStates.append(i)
        return (badStates)

    def testBounds(self, testNo, verbose):
        """
            Checks that each configuration fits within the workspace bounds.

            @param testNo the test number

            @param verbose whether to output more information about the test on failure

            @return whether the test was successful or not
        """
        print("Test " + str(testNo) + ": Bounds")
        badStates = getOutOfBoundsStates()
        if badStates:
            print("FAILED: " + str(len(badStates)) + " of " + str(len(self.ps.getPath())) +
                  " state(s) go out of the workspace bounds.")

            if verbose:
                print ("Line for each invalid cfg:")
                print(str(addToAll(badStates,2)))

            return (False)
        else:
            print("Passed.")
            return (True)


    def hasCollision(self, cfg, obs):
        """
            Determines whether the given config collides with any given obstacles

            @param cfg
                the config to test

            @param obs
                the obstacles to test against (single obstacles can be a list of dimension 1)

            @return whether the given config collides with the given obstacles
        """
        points = cfg.getASVPositions()
        for o in obs:
            lenientParams = grow(o.getRect(), -self.maxError)
            lenientRect = Rectangle2D(lenientParams[0],lenientParams[1],lenientParams[2],lenientParams[3])

            for i in range(1, len(points)):
                if (line2D(points[i-1],points[i]).intersectsRect(lenientRect)):
                    return (True)

        return (False)

    def getCollidingStates(self):
        """
            Returns the path indices of any states that collide with obstacles
        """
        path = self.ps.getPath
        badStates = []

        for i in range(len(path)):
            if (hasCollision(path[i], self.ps.getObstacles())):
                badStates.append(i)
        return (badStates)

    def testCollisions(self, testNo, verbose):
        """
            Checks that each configuration does not collide with obstacles

            @param testNo the test number

            @param verbose whether to output more information about the test on failure

            @return whether the test was successful or not
        """
        print("Test " + str(testNo) + ": Collisions")
        badStates = getCollidingStates()
        if badStates:
            print("FAILED: " + str(len(badStates)) + " of " + str(len(self.ps.getPath())) +
                  " state(s) collide with obstacles.")

            if verbose:
                print ("Line for each invalid cfg:")
                print(str(addToAll(badStates,2)))

            return (False)
        else:
            print("Passed.")
            return (True)

    def testTotalCost(self, testNO, verbose):
        """
            Checks that the total cost of the solution is correctly calculated

            @param testNo the test number

            @param verbose whether to output more information about the test on failure

            @return whether the test was successful or not
        """
        print("Test " + str(testNo) + ": Solution cost")
        cost = self.ps.getSolutionCost()
        actualCost = self.ps.calculateTotalCost()
        if (abs(cost - actualCost) > self.maxError):
            print("FAILED: Incorrect solution cost; was "+str(cost)+" but should have been "+str(actualCost))
            return (False)
        else:
            print("Passed.")
            return (True)

    def testByName(self, testName, testNo, verbose):
        """
            Runs a test by its name
        """
        if (testName == "initial"):
            return testInitialFirst(testNo, verbose)
        elif (testName == "goal"):
			return testGoalLast(testNo, verbose)
        elif (testName == "steps"):
			return testValidSteps(testNo, verbose)
        elif (testName == "booms"):
			return testBoomLengths(testNo, verbose)
        elif (testName == "convexity"):
			return testConvexity(testNo, verbose)
        elif (testName == "areas"):
			return testAreas(testNo, verbose)
        elif (testName == "bounds"):
			return testBounds(testNo, verbose)
        elif (testName == "collisions"):
			return testCollisions(testNo, verbose)
        elif (testName == "cost"):
			return testTotalCost(testNo, verbose)
        return (True)
