import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers
import numpy as np
import PIL.Image


classifier_url ="https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2" #@param {type:"string"}

IMAGE_SHAPE = (224, 224)

classifier = tf.keras.Sequential([
    hub.KerasLayer(classifier_url, input_shape=IMAGE_SHAPE+(3,))
])

inputs = np.empty((10, 224, 224, 3))

for i in range(0,5):
    cat = PIL.Image.open(f'../data/cat.{i}.jpg').resize(IMAGE_SHAPE)
    dog = PIL.Image.open(f'../data/dog.{i}.jpg').resize(IMAGE_SHAPE)

    cat = np.array(cat) / 255.0
    dog = np.array(dog) / 255.0

    inputs[i] = cat
    inputs[i+5] = dog


results = classifier.predict(inputs)

pred_classes = []
pred_labels = []

labels_path = tf.keras.utils.get_file('ImageNetLabels.txt','https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
imagenet_labels = np.array(open(labels_path).read().splitlines())

for r in results:
    print(r)
    argmax = np.argmax(r)
    pred_classes.append(argmax)
    pred_labels.append(imagenet_labels[argmax])

# predicted_class = np.argmax(results[0], axis=-1)


# predicted_class_name = imagenet_labels[predicted_class]
print(pred_labels)