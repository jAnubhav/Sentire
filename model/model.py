import tensorflow as tf
from keras import layers as L

import pickle, librosa, numpy as np

def zcr(data, fl, hl):
    return np.squeeze(librosa.feature.zero_crossing_rate(y=data, frame_length=fl, hop_length=hl))

def rms(data, fl, hl):
    return np.squeeze(librosa.feature.rms(y=data, frame_length=fl, hop_length=hl))

def mfcc(data, sr): return np.ravel(librosa.feature.mfcc(y=data, sr=sr).T)

def extract_features(data, sr=22050, fl=2048, hl=512):
    return np.hstack((np.array([]), zcr(data,fl,hl), rms(data, fl, hl), mfcc(data, sr)))

def get_features(path):
    data, _ = librosa.load(path, duration=2.5, offset=0.6)
    result = np.array(extract_features(data))

    result = np.reshape(result, newshape=(1, result.shape[0]))
    return np.expand_dims(scaler.transform(result), axis=2)

def prediction(path):
    predictions=model.predict(get_features(path))
    return encoder.inverse_transform(predictions)

with open('./helper/scaler.pickle', 'rb') as f: scaler = pickle.load(f)
with open('./helper/encoder.pickle', 'rb') as f: encoder = pickle.load(f)

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
); model.load_weights('./helper/weights.h5')