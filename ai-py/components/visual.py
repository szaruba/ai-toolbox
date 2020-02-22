# A visual classification component
from core.component import Component
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers
import numpy as np
import PIL.Image
import rx
from rx.subject import Subject
from rx import operators as ops


class Visual(Component):
    IMAGE_SHAPE = (224, 224)
    classifier_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2"  # @param {type:"string"}

    input_image = rx.subject.Subject()

    output_predictions = rx.subject.Subject()

    def __init__(self):
        super().__init__()

        self.classifier = tf.keras.Sequential([
            hub.KerasLayer(self.classifier_url, input_shape=self.IMAGE_SHAPE + (3,))
        ])

        labels_path = tf.keras.utils.get_file('ImageNetLabels.txt',
                                              'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
        self.imagenet_labels = np.array(open(labels_path).read().splitlines())

        self.input_image.pipe(ops.map(lambda image: self.classify(image)))\
            .subscribe(lambda preds: self.output_predictions.on_next(preds))



    def classify(self, image):
        """classifies the input image and returns the prediction values"""
        prediction = self.classifier.predict(image[np.newaxis, ...])
        predicted_class = np.argmax(prediction[0], axis=-1)
        predicted_class_name = self.imagenet_labels[predicted_class]
        print("spotted a " + predicted_class_name)
        return prediction[0]
