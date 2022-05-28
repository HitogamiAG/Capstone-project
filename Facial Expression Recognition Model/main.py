import cv2
import dlib
import numpy as np

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

import tensorflow as tf
from tensorflow.keras.models import Model,Sequential, load_model,model_from_json
from tensorflow.compat.v1.keras.backend import set_session
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
sess=tf.compat.v1.Session(config=config)
set_session(sess)

# найти самый частый элемент в списке
def most_frequent(List):
    return max(set(List), key = List.count)

# захват видео и объект face recognition
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()

# загрузить веса модели
model=load_model('mobilenet_7.h5')

# препроцессинг
def mobilenet_preprocess_input(x,**kwargs):
    x[..., 0] -= 103.939
    x[..., 1] -= 116.779
    x[..., 2] -= 123.68
    return x

# Размер изображения на вход
preprocessing_function=mobilenet_preprocess_input
INPUT_SIZE = (224, 224)

# список эмоций
idx_to_class={0: 'Anger', 1: 'Disgust', 2: 'Fear', 3: 'Happiness', 4: 'Neutral', 5: 'Sadness', 6: 'Surprise'}

# сче
c = 0 # %30
dominant_emo = 'None'
store_emo = []


while True:
    _, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    cropped_img = img
    faces = detector(img)
    if len(faces) != 0:
        face = faces[0]

        top = max(0, face.top()) # -50
        bottom = min(face.bottom(), img.shape[0]) # +50
        left = max(0, face.left()) # -50
        right = min(face.right(), img.shape[1]) # +50

        cropped_img = img[top:bottom, left:right, :]

        face_img=cv2.resize(cropped_img,INPUT_SIZE)
        inp=face_img.astype(np.float32)
        inp[..., 0] -= 103.939
        inp[..., 1] -= 116.779
        inp[..., 2] -= 123.68
        inp = np.expand_dims(inp, axis=0)

        scores=model.predict(inp)[0]
        print(np.round(scores, 3))
        result = idx_to_class[np.argmax(scores)]
        store_emo.append(result)
    else:
        result = 'No face'
        face_img=cv2.resize(img,INPUT_SIZE)
        store_emo.append(result)




    c += 1

    if c % 15 == 0:
        dominant_emo = most_frequent(store_emo)
        store_emo = []
        c = 1

    cv2.putText(img, str(dominant_emo), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    #cv2.imshow('Emotion Detector', cropped_img)
    cv2.imshow('Face', img)
    cv2.imshow('Face2', face_img)
    cv2.waitKey(1)
#%%
