# A random pattern generator component
from rx import Observable

from core.component import Component
import rx.subject
import random
import rx.operators as ops


class Rpg(Component):

    # inputs
    input_danger = rx.subject.Subject()
    input_opportunity = rx.subject.Subject()

    # outputs
    output_invert_movement = rx.subject.Subject()

    def __init__(self):
        super().__init__()
        self.input_danger.pipe(
            ops.zip(self.input_opportunity),
            ops.map(lambda x: self.should_flip(x))
        ).subscribe(lambda x: self.output_invert_movement.on_next(x))

    def should_flip(self, x):
        return random.random() < (1 - abs(x[0] - x[1])) * 0.1  # max 10% chance to invert
