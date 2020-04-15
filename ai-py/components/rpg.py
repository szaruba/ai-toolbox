# A random pattern generator component

from core.component import Component
import rx.subject
import random
import rx.operators as ops

__author__ = "Stefan Zaruba"


class Rpg(Component):
    """
    A random pattern generator component. It has a chance to send an inversion signal, which can be used to randomize
    decisions. In this case it is used to randomize the movement patterns of the CPG.

    :var input_danger: Feed it with danger levels between [0.0, 1.0]
    :var input_oppoprtunity: Feed it with opportunity levels between [0.0, 1.0]
    :var output_invert_movement: An inversion signal. Can be 0='no inversion' or 1='invert'
    """

    # inputs
    input_danger = rx.subject.Subject()
    input_opportunity = rx.subject.Subject()

    # outputs
    output_invert_movement = rx.subject.Subject()

    def __init__(self, inv_chance=0.2):
        super().__init__()
        self.inv_chance = inv_chance
        self.input_danger.pipe(
            ops.zip(self.input_opportunity),
            ops.map(lambda x: self.should_flip(x))
        ).subscribe(lambda x: self.output_invert_movement.on_next(x))

    def should_flip(self, x):
        """Probabilistically determines the inversion signal, based on the discrepancy between the input levels"""
        return random.random() < (1 - abs(x[0] - x[1])) * self.inv_chance  # max 10% chance to invert
