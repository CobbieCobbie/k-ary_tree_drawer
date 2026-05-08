class Vertex:
    def __init__(self, x, y, h, id):
        self.coordinates = (x, y)
        self.height = h
        self.id = id

    def __repr__(self):
        return "coordinates are: " \
               + str(self.coordinates[0]) + "," + str(self.coordinates[1]) + \
               "\n Height equals: " + str(self.height)
