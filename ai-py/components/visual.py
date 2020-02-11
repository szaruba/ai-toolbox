# A visual classification component
from core.component import Component
import tensorflow_hub as hub

class Visual(Component):

    def __init__(self):
        super().__init__()

        module = hub.Module("https://tfhub.dev/google/efficientnet/b0/classification/1")
        height, width = hub.get_expected_image_size(module)

