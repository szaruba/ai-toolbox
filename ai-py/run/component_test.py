from rx import operators as ops

from components.cpg import Cpg
from components.eval import Eval
from components.rpg import Rpg
from components.visual import Visual
import time
from core.env import Env
from core.logger import Logging
from core.timer import Timer

__author__ = "Stefan Zaruba"


"""
A demonstration for how some components can be assembled together, to build an agent, who interacts with an environment.

This agent uses a visual component to classify cat/dog images. Results are used by an evaluation component, to 
estimate the situation. The classification is also used by the Rpg component, to produce some randomness. Both results
are used by a Cpg component to generate a movement pattern.

The final goal is, for the agent, to "run away" from dogs and "run towards" cats. The running away and running towards
are simulated by the two different muscle activation patterns.

The outputs of every component are logged, by attaching a Logger to their output streams. The resulting CSV log file is
plotted in the log_visualization.py file.
"""

demo_mode = False  # set to true to produce a demonstrating log output that cycles through all images in order

# ========= create components ===========
vis = Visual()
eval = Eval()
cpg = Cpg()
rpg = Rpg(inv_chance=0) if demo_mode else Rpg()

env = Env(demo_mode=demo_mode)

# ==== wire the components together =====
env.visual_feedback.subscribe(lambda img: vis.input_image.on_next(img))
vis.output_predictions.subscribe(lambda preds: eval.input_encountered_object.on_next(preds))

eval.output_danger_level.subscribe(lambda d: cpg.input_danger.on_next(d))
eval.output_opportunity_level.subscribe(lambda o: cpg.input_opportunity.on_next(o))

eval.output_danger_level.subscribe((lambda d: rpg.input_danger.on_next(d)))
eval.output_opportunity_level.subscribe(lambda o: rpg.input_opportunity.on_next(o))
rpg.output_invert_movement.subscribe(lambda i: cpg.input_flip.on_next(i))

cpg.output_muscle_stimuli.subscribe(lambda ms: process_muscle_stimulus(ms))

# ========== configure logging ==========
log_path = "../log/demo.txt" if demo_mode else "../log/logfile.txt"
logging = Logging(log_path, 10)

logging.add_logger(Logging.Logger("vis_feedback", env.visual_feedback_label))
logging.add_logger(Logging.Logger("prediction", vis.output_prediction_label))
logging.add_logger(Logging.Logger("danger", eval.output_danger_level))
logging.add_logger(Logging.Logger("opportunity", eval.output_opportunity_level))
logging.add_logger(Logging.Logger("invert", rpg.output_invert_movement))
logging.add_logger(Logging.Logger("muscle_f_ant", cpg.output_muscle_stimuli.pipe(ops.map(lambda x: x[0]))))
logging.add_logger(Logging.Logger("muscle_f_post", cpg.output_muscle_stimuli.pipe(ops.map(lambda x: x[1]))))

logging.start_logging()

# ========= start timer ticks ===========
Timer().start()


def process_muscle_stimulus(ms):
    env.contract_anterior(ms[0])
    env.contract_posterior(ms[1])


# prevent termination of streams
while True:
    time.sleep(10)
