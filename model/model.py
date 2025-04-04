import tensorflow as tf
from keras import layers as L

import pickle, librosa, numpy as np

def zcr(data, fl, hl):
    return np.squeeze(librosa.feature.zero_crossing_rate(y=data, frame_length=fl, hop_length=hl))

def rms(data, fl, hl):
    return np.squeeze(librosa.feature.rms(y=data, frame_length=fl, hop_length=hl))

def mfcc(data, sr): 
    return np.ravel(librosa.feature.mfcc(y=data, sr=sr).T)

def extract_features(data, sr=22050, fl=2048, hl=512):
    features = np.hstack((np.array([]), zcr(data, fl, hl), rms(data, fl, hl), mfcc(data, sr)))
    target_size = 2376
    
    if features.shape[0] < target_size:
        features = np.pad(features, (0, target_size - features.shape[0]), 'constant')
    elif features.shape[0] > target_size:
        features = features[:target_size]

    return features

def get_features(path):
    data, sr = librosa.load(path); res = np.array(extract_features(data, sr))
    return np.expand_dims(scaler.transform(np.reshape(res, newshape=(1, res.shape[0]))), axis=2)

def prediction(path): return encoder.inverse_transform(model.predict(get_features(path)))

with open('./model/helper/scaler.pickle', 'rb') as f: scaler = pickle.load(f)
with open('./model/helper/encoder.pickle', 'rb') as f: encoder = pickle.load(f)

model = tf.keras.Sequential(
    [
        L.Conv1D(512,kernel_size=5, strides=1,padding='same', activation='relu',input_shape=(2376,1)),
        L.BatchNormalization(), L.MaxPool1D(pool_size=5,strides=2,padding='same'),
    
        L.Conv1D(512,kernel_size=5,strides=1,padding='same',activation='relu'),
        L.BatchNormalization(), L.MaxPool1D(pool_size=5,strides=2,padding='same'), L.Dropout(0.2),
    
        L.Conv1D(256,kernel_size=5,strides=1,padding='same',activation='relu'),
        L.BatchNormalization(), L.MaxPool1D(pool_size=5,strides=2,padding='same'),
    
        L.Conv1D(256,kernel_size=3,strides=1,padding='same',activation='relu'),
        L.BatchNormalization(), L.MaxPool1D(pool_size=5,strides=2,padding='same'), L.Dropout(0.2),
    
        L.Conv1D(128,kernel_size=3,strides=1,padding='same',activation='relu'),
        L.BatchNormalization(), L.MaxPool1D(pool_size=3,strides=2,padding='same'), L.Dropout(0.2),
    
        L.Flatten(), L.Dense(512,activation='relu'), L.BatchNormalization(), L.Dense(7,activation='softmax')
    ]
)

model.load_weights('./model/helper/weights.h5')