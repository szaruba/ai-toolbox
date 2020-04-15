# A random number generator component

from core.component import *
import rx
from rx import operators as ops, Observable
import random

__author__ = "Stefan Zaruba"


class Rng(Component):
    """
    A random number generator component. Produces uniformly distributed random floats between [0,1)

    :var output_random_number: A stream of the generated random numbers.
    """

    output_random_number = Observable()

    def __init__(self):
        super().__init__()

        # every second emit a uniformly distributed random float between [0,1)
        self.output_random_number = rx.timer(0, 1).pipe(ops.map(lambda s: random.random()))
