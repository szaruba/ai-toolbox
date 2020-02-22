#  Simulates the environment in which the organism lives
#  Allows the organism to interact and provides feedback
import random
import PIL
import rx
import rx.subject
import numpy as np
from rx import operators as ops


class Env:
    #  sends an image of shape (224, 224, 3) whenever the organism sees something different
    visual_feedback = rx.subject.Subject()

    # provides feedback to the organism
    pain_receptor = rx.subject.Subject()
    pleasure_receptor = rx.subject.Subject()

    def __init__(self):
        # set up visual feedback, by periodically providing random cat/dog image
        rx.timer(0, 1)\
            .pipe(ops.map(lambda x: self.read_random_image()))\
            .subscribe(lambda img: self.visual_feedback.on_next(img))

    def contract_anterior(self, force):
        print(f"contracting anterior muscle with force {force}")

    def contract_posterior(self, force):
        print(f"contracting posterior muscle with force {force}")

    @staticmethod
    def read_random_image():
        IMAGE_SHAPE = (224, 224)
        catdog = "cat" if random.random() < 0.5 else "dog"
        i = random.randint(0, 4)

        image = PIL.Image.open(f"../data/{catdog}.{i}.jpg").resize(IMAGE_SHAPE)
        image = np.array(image)
        image = image / 255.0  # norm rgb values to [0,1]
        return image
