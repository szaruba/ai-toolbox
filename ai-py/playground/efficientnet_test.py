import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers
import numpy as np
import PIL.Image as Image
import matplotlib.pylab as plt

tf.compat.v1.disable_eager_execution()
module = hub.Module("https://tfhub.dev/google/efficientnet/b0/classification/1")
height, width = hub.get_expected_image_size(module)

IMAGE_SHAPE = (224, 224)
grace_hopper = tf.keras.utils.get_file('image2.jpg','https://upload.wikimedia.org/wikipedia/commons/b/ba/Flower_jtca001.jpg')
grace_hopper = Image.open(grace_hopper).resize(IMAGE_SHAPE)
print(grace_hopper)

grace_hopper = np.array(grace_hopper)
grace_hopper = grace_hopper/255.0  # norm to [0,1]

images = np.expand_dims(grace_hopper, axis=0) # A batch of images with shape [batch_size, height, width, 3].
logits = module(images)  # Logits with shape [batch_size, num_classes].

print(logits)

outputs = module(dict(images=images), signature="image_classification",
                 as_dict=True)
logits = outputs["default"]

print(logits)
