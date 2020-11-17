import numpy as np
import matplotlib.pyplot as plt

class Beam:

    def __init__(self, length, supports, loads):
        self.length = length
        self.supports = supports
        self.loads = loads

    def calculate_reaction_loads(self):
        load_force = 0
        load_moments = 0
        for load in self.loads:
            if load.type == "point":
                load_force+=load.load_force
            else:
                load_force+=load.get_resultant(load.location[0],load.location[1])
        for load in self.loads:
            if load.type == "point":
                load_moments += load.load_force*load.location
            else:
                load_moments += load.get_resultant(load.location[0],load.location[1])*load.get_centroid(load.location[0], load.location[1])
        if len(self.supports) > 1:
            left_hand = [[1, 1],[self.supports[0].location, self.supports[1].location]]
            left_hand = np.asarray(left_hand)
            right_hand = np.asarray([-load_force, -load_moments])
            reaction_forces = np.linalg.solve(left_hand, right_hand)
            self.supports[0].reaction_force = reaction_forces[0]
            self.supports[1].reaction_force = reaction_forces[1]
            print("Reaction forces (N)")
            print(reaction_forces)
        else:
            left_hand = np.asarray([[1,0],[self.supports[0].location, 1]])
            right_hand = np.asarray([-load_force, -load_moments])
            reactions = np.linalg.solve(left_hand, right_hand)
            self.supports[0].reaction_force = reactions[0]
            self.supports[0].reaction_moment = reactions[1]
            print("Reaction force (N) and moment (Nm)")
            print(reactions)

    def calc_shear_force(self):
        x = []
        i = 0
        while i<=self.length:
            x.append(i)
            i+=.01
        y = []
        for loc in x:
            force_sum = 0
            for load in self.loads:
                if load.type == "point":
                    if load.location < loc:
                        force_sum += load.load_force
                else:
                    if (load.location[0] < loc) & (load.location[1] < loc):
                        force_sum += load.get_resultant(load.location[0],load.location[1])
                    elif (load.location[0] < loc):
                        force_sum += load.get_resultant(load.location[0],loc)
            for support in self.supports:
                if support.location < loc:
                    force_sum += support.reaction_force
            y.append(force_sum)
        plot1 = plt.figure(1)
        plt.title("Shear Force Diagram")
        plt.plot(x,y)
        plt.xlabel("Distance (m)")
        plt.ylabel("Shear Force (N)")

    def calc_bending_moment(self):
        x = []
        i = 0
        while i <= self.length:
            x.append(i)
            i+=.01
        x.append(self.length)
        y = []
        for loc in x:
            moment_sum = 0
            for load in self.loads:
                if load.type == "point":
                    if load.location < loc:
                        moment_sum += load.load_force*(loc-load.location)
                else:
                    if (load.location[0] < loc) & (load.location[1] < loc):
                        moment_sum += load.get_resultant(load.location[0],load.location[1])*(loc-load.get_centroid(load.location[0], load.location[1]))
                    elif(load.location[0] < loc):
                        moment_sum += load.get_resultant(load.location[0],loc)*(loc-(load.get_centroid(load.location[0], loc)))
            for support in self.supports:
                if support.location < loc:
                    moment_sum += support.reaction_force*(loc-support.location)
                    moment_sum -= support.reaction_moment
            y.append(moment_sum)
        plot2 = plt.figure(2)
        plt.plot(x,y)
        plt.title("Bending Moment Diagram")
        plt.xlabel("Distance (m)")
        plt.ylabel("Bending Moment (Nm)")
