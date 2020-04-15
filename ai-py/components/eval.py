import numpy as np
import rx.subject

from core.component import Component

__author__ = "Stefan Zaruba"


class Eval(Component):
    """
    An evaluator component. Evaluates a situation.

    Receives classification confidences as inputs for the classes of the http://www.image-net.org/ challenge. Outputs
    opportunity and danger levels, based on whether it thinks the input image is a cat/dog. Cats are seen as
    opportunities for the agent, whereas dogs are considered dangerous.

    :var input_encountered_object: Input is the prediction confidence for each image class. View the link for a list
    of classes: https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt
    :var output_danger_level: A float between [0,1] describing how dangerous the encountered object is.
    :var output_opportunity_level: A float between [0,1] describing how much opportunity the encountered object promises
    """

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
