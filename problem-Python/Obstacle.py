import math

class Obstacle:
    """
        This class represents one of the rectangular obstacles in Assignment 2, but in Python.

        It constructs an obstacle with the given coordinates (x,y) at the bottom-left hand corner,
        to the size of a given width and height.

        @param x = the x coordinate of the bottom left corner
        @param y = the y coordinate of the bottom left corner
        @param w = the width of the rectangle
        @param h = the height of the rectangle

        @Methods:
            getCoords

            __contains__(coord)
                enables coord in obstacle

            __equals__
                enables rectangle == obstacle

            distance(coord) where coord = (x,y)
                How far away the given point is from the closest point of the obstacle

            outcode(coord) where coord = (x,y)
                Vector (x,y,dx,dy) of mag (dx,dy) from closest point (x,y) of the obstacle

        @Author Loreith
    """

    def __init__(self, x=0, y=0, w=0, h=0):
        """
            All params optional so that second constructor method may be used.
        """
        self.rect = [x,y,w,h]

    def __equals__(self,rect):
        """
            Returns true if the rectangle is equal to self

            @param rect = [x,y,w,h]

            @return true if rect == self.rect. False if otherwise
        """
        for i in range(len(rect)):
            if rect[i] != self.rect[i]:
                return(False)
        return(True)

    def __contains__(self, coord):
        """
            Returns true if coordinate is in the obstacle

            @param coord = (x,y)

            @return true if coord is in rectangle, false if not
        """
        ownX = self.rect[0]
        ownY = self.rect[1]

        x = coord[0]
        y = coord[1]
        if (x > ownX and x < ownX + self.rect[2]):
            if (y > ownY and y < ownY + self.rect[3]):
                return(True)
        return(False)

    def construct(self, string):
        """
            Second constructor method:
                Constructs an obstacle from the representation used in the input file:
          	    that is, the x- and y- coordinates of all of the corners of the
          	    rectangle.

            @param string the string describing the obstacle
        """
        #xs = []
        #yx = []

        xMin = 0
        xMax = 0
        yMin = 0
        yMax = 0

        stringList = string.split(' ')

        for i in range(4):
            #xs.append(stringList[i*2])
            #ys.append(stringList[(i*2) + 1])

            xMin = stringList[i*2] if stringList[i*2] < xMin else xMin
            xMin = stringList[i*2] if stringList[i*2] > xMax else xMax
            yMin = stringList[(i*2) + 1] if stringList[(i*2) + 1] < yMin else yMin
            yMax = stringList[(i*2) + 1] if stringList[(i*2) + 1] > yMax else yMax

        self.rect = [xMin, yMin, xMac - xMin, yMax - yMin]

    def getRect(self):
        """
         Returns the rectangle as a list of x,y,w,h

         Considered SciPy, but is an unknown without all required funcitons
        """
        return(self.rect)

    def distance(self, coord):
        """
            How far away the given point is from the closest point of the obstacle

            @param coord = (x,y)

            @return the minimum distance from the coordinates to the obstacle
        """
        # Circles, all 4
        x = coord[0]
        y = coord[1]

        ownX = self.rect[0]
        ownY = self.rect[1]
        ownW = self.rect[2]
        ownH = self.rect[3]


        if coord in self:
            return(0)

        if (x > ownX and x < ownX + ownW):
            #If a perpendicular line is possible it is the shortest something something dot product
            return( min([ abs(y-ownY), abs(y-(ownY + ownH)) ]) )
        elif (y > ownY and y < ownY + ownH):
            return( min([ abs(x-ownX), abs(x-(ownX + ownW)) ]) )

        else:
            #If we are past a corner, return the pythagorean distance from said corner
            cornerX = min([ abs(x-ownX), abs(x-(ownX + ownW)) ])
            cornerY = min([ abs(y-ownY), abs(y-(ownY + ownH)) ])

            dx = abs(x-cornerX)
            dy = abs(y-cornerY)

            return( math.sqrt(dx**2 + dy**2) )

    def outcode(self, coord):
        """
            Gives the shortests vector from the obstacle to the coord

            @param coord = (x,y)

            @return the vector [x,y,dx,dy] from the closest point on the rectangle to the point coord
        """
        # Circles, all 4
        x = coord[0]
        y = coord[1]

        ownX = self.rect[0]
        ownY = self.rect[1]
        ownW = self.rect[2]
        ownH = self.rect[3]


        if coord in self:
            return(0)

        if (x > ownX and x < ownX + ownW):
            #If a perpendicular line is possible it is the shortest something something dot product

            sideY   = ownY if abs(y-ownY) < abs(y-(ownY + ownH)) else ownY + ownH
            dy      = min( [ abs(y-ownY), abs(y-(ownY + ownH)) ] )

            return( [x, sideY, 0, dy ] )

        elif (y > ownY and y < ownY + ownH):

            sideX   = ownX if abs(x-ownX) < abs(x-(ownX + ownW)) else ownX + ownW
            dx      = min( [ abs(x-ownX), abs(x-(ownX + ownW)) ] )

            return( [sideX, y, dx, 0] )

        else:
            #If we are past a corner, return the pythagorean distance from said corner
            cornerX = min([ abs(x-ownX), abs(x-(ownX + ownW)) ])
            cornerY = min([ abs(y-ownY), abs(y-(ownY + ownH)) ])

            dx = abs(x-cornerX)
            dy = abs(y-cornerY)

            return( [cornerX, cornerY, dx, dy] )
