from components.cpg import Cpg
from components.eval import Eval
from components.rng import Rng
from components.rpg import Rpg
from components.visual import Visual
import time

from core.env import Env

vis = Visual()
eval = Eval()
rng = Rng()
cpg = Cpg()
rpg = Rpg()

env = Env()

# wire the components together
env.visual_feedback.subscribe(lambda img: vis.input_image.on_next(img))
vis.output_predictions.subscribe(lambda preds: eval.input_encountered_object.on_next(preds))

eval.output_danger_level.subscribe(lambda d: cpg.input_danger.on_next(d))
eval.output_opportunity_level.subscribe(lambda o: cpg.input_opportunity.on_next(o))

eval.output_danger_level.subscribe((lambda d: rpg.input_danger.on_next(d)))
eval.output_opportunity_level.subscribe(lambda o: rpg.input_opportunity.on_next(o))
rpg.output_invert_movement.subscribe(lambda i: cpg.input_flip.on_next(i))

cpg.output_muscle_stimulus.subscribe(lambda ms: process_muscle_stimulus(ms))


def process_muscle_stimulus(ms):
    env.contract_anterior(ms[0])
    env.contract_posterior(ms[1])


# prevent termination of streams
while True:
    time.sleep(10)
