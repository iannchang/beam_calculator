from beam import Beam
from load import Load
from support import Support
import matplotlib.pyplot as plt

#Init array of supports and loads
supports = []
loads = []
#This is where you add supports For supports, there are two
#parameters. The first is type. It can be either "fixed" or "roller"
#Note: that the only possible configurations are one fixed support, or two roller supports.
#Other configurations are not solvable.
supports.append(Support("fixed", 5))
#This is where you add loads. For loads there are 3 parameters. The first is type.
#it can be either "point", "distributed", or "triangle". The next is the location along the beam.
#For distributed loads, you enter in a length 2 array where the first value is the start location
#and the second value is the end locaiton. The third parameter is the load. The load does need to be
#signed. For unevenly distributed loads, you have to enter in a length 2 array where the first value
#is the starting force and the second value is the ending force.
loads.append(Load("point", 3, -5))
#loads.append(Load("distributed", [0,2],-1))
loads.append(Load("triangle", [0,3],[-2,-6]))
#Checks to see if there are any uneven loads that need to be split
for load in loads:
    if (load.need_to_split()):
        loads.append(load.split())

#Initialize the beam
#Parameters are length, support array, loads array
beam = Beam(5, supports, loads)

#Runs the calculations and shows the plots
beam.calculate_reaction_loads()
beam.calc_shear_force()
beam.calc_bending_moment()
plt.show()
