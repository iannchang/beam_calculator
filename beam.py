import numpy as np
import matplotlib.pyplot as plt

class Beam:

    def __init__(self, length, supports, loads):
        self.length = length
        self.supports = supports
        self.loads = loads

    def calculate_reaction_loads(self):
        """
        This function calculates the reaction forces from the given supports and loads
        """
        load_force = 0
        load_moments = 0
        #This segment of code adds up all of the known forces and moments to put them into our equilibrium equation
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
        #This if statement checks for the two different cases: one fixed support or two roller supports
        if len(self.supports) > 1:
            #This if statement sets up, solves, and stores the system of equilibrium equations for two rollers (two forces are stored)
            left_hand = [[1, 1],[self.supports[0].location, self.supports[1].location]]
            left_hand = np.asarray(left_hand)
            right_hand = np.asarray([-load_force, -load_moments])
            reaction_forces = np.linalg.solve(left_hand, right_hand)
            self.supports[0].reaction_force = reaction_forces[0]
            self.supports[1].reaction_force = reaction_forces[1]
            print("Reaction forces (N)")
            print(reaction_forces)
        else:
            #This if statement sets up, solves, and stores the system of equilibrium equations for one fixed support (one force and one moment are stored)
            left_hand = np.asarray([[1,0],[self.supports[0].location, 1]])
            right_hand = np.asarray([-load_force, -load_moments])
            reactions = np.linalg.solve(left_hand, right_hand)
            self.supports[0].reaction_force = reactions[0]
            self.supports[0].reaction_moment = reactions[1]
            print("Reaction force (N) and moment (Nm)")
            print(reactions)

    def calc_shear_force(self):
        """
        This function calculates the shear forces for the beam
        """
        x = []
        i = 0
        while i<=self.length:
            x.append(i)
            i+=.01
        y = []
        #This for loop traverses along the beam and calculates the shear force at each .01 m interval
        for loc in x:
            force_sum = 0
            for load in self.loads:
                if load.type == "point":
                    #If the load is a point load, just add the forces
                    if load.location < loc:
                        force_sum += load.load_force
                else:
                    if (load.location[0] < loc) & (load.location[1] < loc):
                        #This if statement uses the resultant force from the distributed load
                        #if the distributed load is fully inside length we are looking at
                        force_sum += load.get_resultant(load.location[0],load.location[1])
                    elif (load.location[0] < loc):
                        #This if statement is for cases when we are slicing the beam in the middle of a distributed load
                        force_sum += load.get_resultant(load.location[0],loc)
            for support in self.supports:
                if support.location < loc:
                    force_sum += support.reaction_force
            y.append(force_sum)
        #using matplotlib to plot the length versus shear force
        plot1 = plt.figure(1)
        plt.title("Shear Force Diagram")
        plt.plot(x,y)
        plt.xlabel("Distance (m)")
        plt.ylabel("Shear Force (N)")

    def calc_bending_moment(self):
        """
        This function calculates the bending moments for the beam
        """
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
                    #Calculates and adds moment to total for each load if load is within the length of the beam we are looking at
                    if load.location < loc:
                        moment_sum += load.load_force*(loc-load.location)
                else:
                    #Calculates and adds moment to total for each distributed load if load is within the length of the beam we are looking at
                    #Using centroid and resultant means we can treat the uneven and even distributed loads the same here
                    if (load.location[0] < loc) & (load.location[1] < loc):
                        moment_sum += load.get_resultant(load.location[0],load.location[1])*(loc-load.get_centroid(load.location[0], load.location[1]))
                    #Case for where we are slicing in the middle of the distributed load
                    elif(load.location[0] < loc):
                        moment_sum += load.get_resultant(load.location[0],loc)*(loc-(load.get_centroid(load.location[0], loc)))
            for support in self.supports:
                if support.location < loc:
                    moment_sum += support.reaction_force*(loc-support.location)
                    moment_sum -= support.reaction_moment
            y.append(moment_sum)
        #Plot the moments
        plot2 = plt.figure(2)
        plt.plot(x,y)
        plt.title("Bending Moment Diagram")
        plt.xlabel("Distance (m)")
        plt.ylabel("Bending Moment (Nm)")
