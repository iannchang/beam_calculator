class Load:

    def __init__(self, type, location, load):
          self.type = type
          self.location = location
          self.load_force = load


    def get_centroid(self, start, end):
        if self.type == "distributed":
            return (start+end)/2
        else:
            if abs(self.load_force[0]) < abs(self.load_force[1]):
                return (self.location[1]-self.location[0])*(2/3)+self.location[0]
            else:
                return (self.location[0]-self.location[1])*(2/3)+self.location[1]

    def get_resultant(self, start, end):
        if self.type == "distributed":
            return self.load_force*(end-start)
        else:
            if abs(self.load_force[0]) < abs(self.load_force[1]):
                return ((1/2)*self.load_force[1])*(end-start)
            else:
                return ((1/2)*self.load_force[0])*(end-start)


    def need_to_split(self):
        if self.type == "triangle":
            if (self.load_force[0] != 0) & (self.load_force[1] != 0):
                return True
            else:
                return False
        return False

    def split(self):
        if (abs(self.load_force[0]) < abs(self.load_force[1])):
            load = Load("distributed", self.location, self.load_force[0])
            self.load_force[1] = self.load_force[1] - self.load_force[0]
            self.load_force[0] = 0
        else:
            load = Load("distributed", self.location, self.load_force[1])
            self.load_force[0] = self.load_force[0] - self.load_force[1]
            self.load_force[1] = 0
        return load
