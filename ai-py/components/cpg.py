# A central pattern generator component
from core.component import Component
from rx.subject import Subject
from rx import operators as ops


class Cpg(Component):

    # inputs
    input_danger = Subject()
    input_opportunity = Subject()
    input_flip = Subject()

    # outputs
    output_muscle_stimulus = Subject()  # outputs the muscle stimulus for each muscle between [0,1] (1 = maximum force)

    def __init__(self):
        super().__init__()
        self.input_danger.pipe(ops.zip(self.input_opportunity, self.input_flip))\
            .subscribe(lambda x: self.process_input(x))

    def process_input(self, x):
        print(f"danger: {x[0]:.2f}, opp: {x[1]:.2f}, invert: {x[2]}")
        forward = x[1] > x[0]

        if x[2]:
            forward = not forward

        if forward:
            print("move forward")
            return 'move forward'
        else:
            print("move backward")
            return 'move backward'
