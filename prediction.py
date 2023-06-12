import tensorflow as tf
import numpy as np
from io import BytesIO
import urllib.request
from tensorflow.keras.utils import load_img, img_to_array

model = tf.keras.models.load_model('fresh_fruit_alpha_v41.h5')

def loadImage(image_url):
    print("In load iamge")

    req = urllib.request.Request(
        url= image_url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as url:
        img = load_img(BytesIO(url.read()), target_size=(150, 150))
    return img_to_array(img)

def model_predict(url):
    print("In model predict")
    x = loadImage(url)
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    classes = model.predict(images)
    idx_classes = np.argmax(classes)
    result = str(idx_classes)
    return result