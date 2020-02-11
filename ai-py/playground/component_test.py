from components.cpg import Cpg
from components.rng import Rng
import time

rng = Rng()
cpg = Cpg()

# wire the rng and cpg component together
# based on the generated number of the rng, the cpg should output 'move forward' or 'move backwards'
rng.outputs['o1'].subscribe(lambda x: cpg.inputs['i1'].on_next(x))
cpg.outputs['pattern'].subscribe(lambda value: print(value))

# prevent termination of streams
while True:
    time.sleep(10)
