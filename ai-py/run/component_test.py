from rx import operators as ops

from components.cpg import Cpg
from components.eval import Eval
from components.rng import Rng
from components.rpg import Rpg
from components.visual import Visual
import time
from core.env import Env
from core.logger import Logging
from core.timer import Timer

demo_mode = True  # set to true to produce a demonstrating log output that cycles through all images in order

# ========= create components ===========
vis = Visual()
eval = Eval()
rng = Rng()
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
