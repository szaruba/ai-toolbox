# an evaluator component. Evaluates a situation
import numpy as np
import rx
import rx.subject

from core.component import Component


class Eval(Component):

    # inputs
    input_encountered_object = rx.subject.Subject()

    # outputs
    output_danger_level = rx.subject.Subject()
    output_opportunity_level = rx.subject.Subject()

    def __init__(self):
        super().__init__()
        self.input_encountered_object.subscribe(lambda x: self.process_inputs(x))

    def process_inputs(self, object_confidences):
        max = np.max(object_confidences)
        min = np.min(object_confidences)

        object_confidences = (object_confidences + np.abs(min)) / (np.abs(min) + np.abs(max))  # scale to [0,1]

        # cats
        cat_i = np.argmax(object_confidences[282:287])
        self.output_opportunity_level.on_next(object_confidences[cat_i+282])

        # dogs
        dog_i = np.argmax(object_confidences[152:270])
        self.output_danger_level.on_next(object_confidences[dog_i+152])