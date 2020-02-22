import numpy as np
import PIL.Image
import tensorflow as tf

model_loaded = tf.keras.models.load_model('../model/catsdogs1.h5')


# grace_hopper = tf.keras.utils.get_file('../data/cat.0.jpg')

inputs = np.empty((10, 150, 150, 3))

for i in range(0,5):
    cat = PIL.Image.open(f'../data/cat.{i}.jpg').resize((150, 150))
    dog = PIL.Image.open(f'../data/dog.{i}.jpg').resize((150, 150))

    cat = np.array(cat) / 255.0
    dog = np.array(dog) / 255.0

    inputs[i] = cat
    inputs[i+5] = dog

predictions = model_loaded.predict(inputs)
print(predictions)