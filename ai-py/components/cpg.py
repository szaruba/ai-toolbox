# A central pattern generator component
import numpy as np
from tensorflow import keras

from core.component import Component
from rx.subject import Subject
from rx import operators as ops

from core.timer import Timer


class Cpg(Component):

    # inputs
    input_danger = Subject()
    input_opportunity = Subject()
    input_flip = Subject()

    # outputs
    output_muscle_stimuli = Subject()  # outputs the muscle stimulus for each muscle between [0,1] (1 = maximum force)

    history_length = 20
    prediction_history = np.random.rand(history_length)
    last_input = [0, 0, 0]  # last zipped input of danger, opportunity and flip

    # specify how many ticks per muscle force update
    muscle_tick_rate = 1

    def __init__(self):
        super().__init__()
        self.forward_model = keras.models.load_model("../model/sine.h5")
        self.backward_model = keras.models.load_model("../model/spiked.h5")

        self.input_danger.pipe(ops.zip(self.input_opportunity, self.input_flip))\
            .subscribe(lambda x: setattr(self, "last_input", x))

        Timer().ticks.pipe(
                ops.filter(lambda x: x % self.muscle_tick_rate == 0),
                ops.map(lambda x: self.input_to_prediction(self.last_input)),
                ops.map(lambda x: self.prediction_to_stimuli(x)))\
            .subscribe(lambda x: self.output_muscle_stimuli.on_next(x))

    def input_to_prediction(self, x):
        print(f"danger: {x[0]:.2f}, opp: {x[1]:.2f}, invert: {x[2]}")
        forward = x[1] > x[0]

        if x[2]:
            forward = not forward

        if forward:
            print("move forward")
            y = self.forward_model.predict(self.prediction_history.reshape((1, self.history_length, 1)))
            self.prediction_history = np.append(self.prediction_history[1:], y)
            return y[0][0]
        else:
            print("move backward")
            y = self.backward_model.predict(self.prediction_history.reshape((1, self.history_length, 1)))
            self.prediction_history = np.append(self.prediction_history[1:], y)
            return y[0][0]

    def prediction_to_stimuli(self, prediction):
        """prediction is a float between -1 and +1"""
        stimuli = np.array([0.0, 0.0])
        if prediction > 0:
            stimuli[0] = prediction
        else:
            stimuli[1] = abs(prediction)

        print(f"prediction: {prediction:.2f} stimuli: [{stimuli[0]:.2f}, {stimuli[1]:.2f}]")
        return stimuli
