import tensorflow as tf
import numpy as np
from io import BytesIO
import urllib.request
from tensorflow.keras.utils import load_img, img_to_array

model = tf.keras.models.load_model('fresh_fruit_alpha_v3.h5')
path = "https://firebasestorage.googleapis.com/v0/b/bidtrade-710bf.appspot.com/o/banana-rotten.jpg?alt=media&token=1ef7e0fd-0dab-4b2e-967d-54f028462b28"

def loadImage(image_url):
    print("In load iamge")

    req = urllib.request.Request(
        url= image_url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as url:
        img = load_img(BytesIO(url.read()), target_size=(150, 150))
    return img_to_array(img)
# def model_predict():
#     img = load_img(path, target_size=(150, 150))
#     x = img_to_array(img)
#     x = np.expand_dims(x, axis=0)

#     images = np.vstack([x])
#     classes = model.predict(images)
#     idx_classes = np.argmax(classes)
#     return idx_classes

# result = model_predict()
# stringV = str(result)
# print(stringV)

def model_predict(url):
    print("In model predict")
    x = loadImage(url)
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    classes = model.predict(images)
    idx_classes = np.argmax(classes)
    result = str(idx_classes)
    return result