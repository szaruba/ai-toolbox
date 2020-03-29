#  Simulates the environment in which the organism lives
#  Allows the organism to interact and provides feedback
import random
import PIL
import rx
import rx.subject
import numpy as np
from rx import operators as ops
__author__ = "Stefan Zaruba"

from core.timer import Timer


class Env:
    #  sends an image of shape (224, 224, 3) whenever the organism sees something different
    visual_feedback = rx.subject.Subject()
    # a name of the image for debugging purposes
    visual_feedback_label = rx.subject.Subject()

    # provides feedback to the organism
    pain_receptor = rx.subject.Subject()
    pleasure_receptor = rx.subject.Subject()

    # specify how many ticks before a new image gets shown
    image_tick_rate = 50

    i = 0

    def __init__(self, demo_mode=False):
        self.demo_mode = demo_mode
        # set up visual feedback, by periodically providing random cat/dog image
        Timer().ticks\
            .pipe(
                ops.filter(lambda x: x % self.image_tick_rate == 0),
                ops.map(lambda x: self.read_random_image())
            )\
            .subscribe(lambda img: self.visual_feedback.on_next(img))

    def contract_anterior(self, force):
        print(f"contracting anterior muscle with force {force}")

    def contract_posterior(self, force):
        print(f"contracting posterior muscle with force {force}")

    def read_random_image(self):
        IMAGE_SHAPE = (224, 224)
        if self.demo_mode:
            self.i = self.i % 10
            catdog = "cat" if self.i < 5 else "dog"
            i = self.i if self.i < 5 else self.i - 5
            self.i += 1
        else:
            catdog = "cat" if random.random() < 0.5 else "dog"
            i = random.randint(0, 4)

        img_name = f"{catdog}.{i}.jpg"

        image = PIL.Image.open(f"../data/{img_name}").resize(IMAGE_SHAPE)
        image = np.array(image)
        image = image / 255.0  # norm rgb values to [0,1]

        self.visual_feedback_label.on_next(img_name)
        return image
