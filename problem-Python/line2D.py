import math
from shapely.geometry import LineString

class Line2D:
    """
        A python implementation of the java line2D class

        This has been stripped down to only the methods required for the supporting code
        so as to avoid collusion.

        Uses the shapely library for line section collision detection.
    """
    def __init__(self, c0, c1):
        """
            @param c0
                The first coordinate to construct the line from

            @param c1
                The second coordinate to construct the line to
        """
        self.c0 = c0
        self.c1 = c1

    def __equals__(self, line):
        other = line.getCoords()
        return(self.c0 == other[0] and self.c1 == other[1])

    def __str__(self):
        return(str(self.c0)+str(self.c1))

    def __contains__(self, point):
        #Cheaty simultanious equations
        vect = self.getVector()
        o = vect[0]
        d = vect[1]

        if d[0] and d[1]:
            val = (point[0] - o[0]) / d[0]

            if val > 1 or val < 0:
                #If it may be co linear but outside of bounds
                return (False)
            if val == ((point[1] - o[1]) / d[1]):
                return (True)
            return (False)

        elif d[0]:
            val = (point[0] - o[0]) / d[0]
            if val > 1 or val < 0:
                #If it may be co linear but outside of bounds
                return (False)
            elif point[1] != o[1]:
                return (False)
            return (True)

        elif d[1]:
            val = (point[1] - o[1]) / d[1]
            if val > 1 or val < 0:
                #If it may be co linear but outside of bounds
                return (False)
            elif point[1] != o[1]:
                return (False)
            return (True)

        else:
            return (point[0] == o[0] and point[1] == o[1])

    def getCoords(self):
        return([self.c0, self.c1])

    def getVector(self):
        """
            Gives a vector equation of the line

            @return the vector equation of the line
        """
        c0 = self.c0
        d0 = (self.c1[0] - c0[0], self.c1[1] - c0[1])
        return ((c0,d0))

    def intersectsRect(self, rect):
        """
            Determines Whether the line intersects the rectangle or not

            @param rect
                The rectangle to compare to

            @return
                Whether the line intersects the rectangle or not
        """
        midpoint = (self.c0[0]+0.5*self.c1[0], self.c0[1]+0.5*self.c1[1])
        length = math.sqrt((self.c1[0]-self.c0[0])**2 + (self.c1[1]-self.c0[1])**2)


        if rect.distance(midpoint) > length:
            return (False)
        elif rect.distance(midpoint) <= 0:
            return (True) #Point inside rectangle


        vect = rect.outcode(midpoint)
        r = rect.getRect()

        line = LineString([self.c0,self.c1])

        if vect[2] == 0:
            #if dx is 0
            rectLine = LineString([ (r[0],vect[1]), (r[0] + r[2],vect[1]) ])

            return (line.intersects(rectLine))
        elif vect[3] == 0:
            #if dy is 0
            rectLine = LineString([ (vect[0],r[1]), (vect[0],r[1] + r[3]) ])

            return (line.intersects(rectLine))
        elif vect[2] != 0 and vect[3] != 0:
            #If we are off a corner
            r1 = vect[0]
            r2 = vect[1]

            r1 += r[2] if vect[1] == r[1] else -r[2]
            r2 += r[3] if vect[0] == r[0] else -r[3]

            rectLine1 = LineString([ (vect[0],vect[1]), (r1,vect[1]) ])
            rectLine2 = LineString([ (vect[0],vect[1]), (vect[0],r2) ])


            return (line.intersects(rectLine1) or line.intersects(rectLine2))
        else:
            return (True) #This shouldn't happen: we have already tested for this
