class ASVConfig:
    """
        Represents a configuration of the ASVs, in python. This class doesn't do
        validity checking, so see the code in tester for this...

        TODO: translate tester

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
