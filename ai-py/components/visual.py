from core.component import Component
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import rx
from rx.subject import Subject
from rx import operators as ops

__author__ = "Stefan Zaruba"


class Visual(Component):
    """
    A visual classification component.

    Receives images, sized (224, 224) pixels. Uses a pre-trained classifier, for predicting ImageNet labels.
    Google's Classifier: https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2
    ImageNet labels: https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt
    ImageNet challenge: http://www.image-net.org/challenges/LSVRC/

    :var input_image: Feed this stream with images in the form (224, 224, 3)
    :var output_predictions: The class confidences for the ImageNet labels.
    :var output_prediction_label: The class name of the argmax prediction.
    """

    # inputs
    input_image = rx.subject.Subject()

    # outputs
    output_predictions = rx.subject.Subject()
    output_prediction_label = rx.subject.Subject()  # maximum likelihood predicted class name for debugging

    IMAGE_SHAPE = (224, 224)
    classifier_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2"  # @param {type:"string"}

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
        self.output_prediction_label.on_next(predicted_class_name)
        return prediction[0]
