class ASVConfig:
    """
        Represents a configuration of the ASVs, in python. This class doesn't do
        validity checking, so see the code in tester for this...

        TODO: translate tester?
        TODO: iterator, generator, or access function

        @author Loreith
    """
    def __init__(self, coords):
        """
            Implements either constructor from the java 'cause you don't need lend

            @param coords either a list of tuples (x,y)
                or a space-separated string containing x y coords
                doing it with a list of [x,y,x,y] seems silly, if you need it just use the string method except check if the list contains tuples or floats
                I don't understand what the cfg thing is, some Java object? If you need it, use the same method!
        """
        if isinstance(coords, str):
            coordsList = coords.split(' ')
            coords = []
            for i in range(len(coordsList)/2):
                coords.append(( coordsList[i*2], coordsList[(i*2)+1] ))

        #Now that input is homogenised, we can continue

        self.asvPositions = coords

    def __str__(self):
        """
            Enables using str(asvConfig) to return the space-separated string

            @return a space-separated string x y x y for all asv units
        """
        string = ""
        for i in self.asvPositions:
            string += i[0] + " " + i[1]
        return(string)

    def __add__(self, coord):
        """
            Enables using += point to add a point to the asvConfig

            @param coord a tuple coordinate (x,y)
        """
        self.asvPositions.append(coord)

    def __len__(self):
        """
            Enables the use of len(asvConfig) to get the number of asvs

            @return the length of the asvPositions list
        """
        return(len(self.asvPositions))

    def getPos(self, asvNo):
        """
            Returns the position of the ASV with the given index

            @param asvNo the index of the asv to return

            @return the position of the asv with the given index
        """
        return(self.asvPositions[asvNo])

    def getAllPos(self):
        """
            Returns the positions of all of the ASVs. Analogous to printing.

            @return the list of (x,y) tuples representing ASVs
        """
        return(self.asvPositions[:]) #Slice to actually copy the list as opposed to unsafe access

    def maxDistance(self, otherState):
        """
            Returns the maximum straight-line distance between this state
            and another state, or -1 if the asv counts don't match

            @param otherState The other state to compare with. Type = ASVConfig

            @return the maximum straight-line distance for any ASV
        """
        if len(self.asvPositions) != len(otherState):
            return(-1)

        maxDistance = 0
        for i in range(len(self.asvPositions)):
            p1 = self.asvPositions[i]
            p2 = otherState.getPos(i)
            distance = sqrt( abs(p2[0] - p1[0])**2 + abs(p2[1] - p1[1])**2 )

            maxDistance = max([distance, maxDistance])

        return(maxDistance)

    def totalDistance(self, otherState):
        """
            Returns the total straight-line distance over all the ASVs between this
      	    state and the other state, or -1 if the ASV counts don't match.

            @param otherState The other state to compare with. Type = ASVConfig

            @return the total straight-line distance over all ASVs.
        """
        if len(self.asvPositions) != len(otherState):
            return(-1)

        totalDistance = 0
        for i in range(len(self.asvPositions)):
            p1 = self.asvPositions[i]
            p2 = otherState.getPos(i)
            distance = sqrt( abs(p2[0] - p1[0])**2 + abs(p2[1] - p1[1])**2 )
            #TODO: remove unnecesary variable when tested
            totalDistance += distance

        return(totalDistance)
