# A central pattern generator component
from core.component import Component
import rx
from rx.subject import Subject
from rx import operators as ops


class Cpg(Component):

    def __init__(self):
        super().__init__()

        input1 = Subject()
        self.inputs['i1'] = input1

        pattern = Subject()
        self.outputs['pattern'] = pattern

        input1.pipe(ops.map(lambda x: self.process_input(x))).subscribe(lambda x: pattern.on_next(x))

    def process_input(self, x):
        if x > 0.5:
            return 'move forward'
        else:
            return 'move backwards'
