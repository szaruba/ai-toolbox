# A random number generator component

from core.component import *
import rx
from rx import operators as ops
import random


class Rng(Component):

    def __init__(self):
        super().__init__()

        # every second emit a uniformly distributed random float between [0,1)
        rng_stream = rx.timer(0, 1).pipe(ops.map(lambda s: random.random()))

        self.outputs['o1'] = rng_stream
        self.meta['o1'] = {'desc': 'Emits a uniformly distributed random float between [0,1) every second'}
