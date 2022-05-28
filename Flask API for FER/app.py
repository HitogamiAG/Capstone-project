from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
import dlib
import cv2
import base64

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

from tensorflow.keras.models import Model,Sequential, load_model,model_from_json
from tensorflow.compat.v1.keras.backend import set_session
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
sess=tf.compat.v1.Session(config=config)
set_session(sess)

detector = dlib.get_frontal_face_detector()
model=load_model('mobilenet_7.h5')

def mobilenet_preprocess_input(x,**kwargs):
    x[..., 0] -= 103.939
    x[..., 1] -= 116.779
    x[..., 2] -= 123.68
    return x

preprocessing_function=mobilenet_preprocess_input
INPUT_SIZE = (224, 224)

idx_to_class={0: 'Anger', 1: 'Disgust', 2: 'Fear', 3: 'Happiness', 4: 'Neutral', 5: 'Sadness', 6: 'Surprise'}

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST'])
#@cross_origin()
def predict():

    response = jsonify({'some': 'data'})
    data = request.data

    tensor = tf.io.decode_raw(data, np.int32)
    #tensor = tf.convert_to_tensor(tensor, dtype=np.int32)
    tensor = tensor.numpy().reshape(400, 600, 3).astype(np.uint8)

    tensor = cv2.cvtColor(tensor, cv2.COLOR_BGR2RGB)
    faces = detector(tensor)

    if len(faces) != 0:
        face = faces[0]

        top = max(0, face.top()) # -50
        bottom = min(face.bottom(), tensor.shape[0]) # +50
        left = max(0, face.left()) # -50
        right = min(face.right(), tensor.shape[1]) # +50

        cropped_img = tensor[top:bottom, left:right, :]

        # препроцессинг
        face_img=cv2.resize(cropped_img,INPUT_SIZE)
        inp=face_img.astype(np.float32)
        inp[..., 0] -= 103.939
        inp[..., 1] -= 116.779
        inp[..., 2] -= 123.68
        inp = np.expand_dims(inp, axis=0)

        # определить эмоцию
        scores=model.predict(inp)[0]
        result = idx_to_class[np.argmax(scores)]

    else: # если не найдено - No face
        result = 'No face'

    response.headers.add('Access-Control-Allow-Origin', '*')

    return result

if __name__ == '__main__':
    app.run(debug=True)

#%%
