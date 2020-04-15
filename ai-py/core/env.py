import random
import PIL
import rx.subject
import numpy as np
from rx import operators as ops
from core.timer import Timer

__author__ = "Stefan Zaruba"


class Env:
    """
    Simulates the environment in which the organism lives. Allows the organism to interact and provides feedback.

    This particular demo environment provides the agent with two functions (contract_anterior, contract_posterior) to
    which it can use to activate two muscles. The environment also provides the agent with a random image periodically
    from a selection of 5 cat and 5 dog images.

    The pain and pleasure receptor could be used by the agent, as additional sources of feedback, to train itself or
    make decisions.
    """

    # sends an image of shape (224, 224, 3) whenever the organism sees something different
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
        """
        Sets up the environment.

        :param demo_mode: activate demo_mode to cycle through the images in a set order instead of randomly. Useful for
        plotting an initial demo graph, for verifying correctness of decisions made by the agent.
        """

        self.demo_mode = demo_mode
        # set up visual feedback, by periodically providing random cat/dog image
        Timer().ticks\
            .pipe(
                ops.filter(lambda x: x % self.image_tick_rate == 0),
                ops.map(lambda x: self.read_random_image())
            )\
            .subscribe(lambda img: self.visual_feedback.on_next(img))

    def contract_anterior(self, force):
        """Simulates contracting the muscle"""

        print(f"contracting anterior muscle with force {force}")

    def contract_posterior(self, force):
        """Simulates contracting the muscle"""

        print(f"contracting posterior muscle with force {force}")

    def read_random_image(self):
        """Reads a random cat or dog image from the hard disk"""

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
