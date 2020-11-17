from beam import Beam
from load import Load
from support import Support
import matplotlib.pyplot as plt


supports = []
loads = []

supports.append(Support("fixed", 5))
loads.append(Load("point", 3, -5))
#loads.append(Load("distributed", [0,2],-1))
loads.append(Load("triangle", [0,3],[-2,-6]))
for load in loads:
    if (load.need_to_split()):
        loads.append(load.split())
beam = Beam(5, supports, loads)

beam.calculate_reaction_loads()
beam.calc_shear_force()
beam.calc_bending_moment()
plt.show()
