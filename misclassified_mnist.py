########################
#認識ミスをした画像出力#
########################

# coding: utf-8
import os
import sys
import time
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import list_get
import model_test

from tensorflow import config
from tensorflow.keras import layers,models,datasets
from keras.utils.np_utils import to_categorical
from keras import optimizers,regularizers
from sklearn.model_selection import StratifiedKFold
sys.path.append('deep-learning-from-scratch-master')
from dataset.mnist import load_mnist
from emnist import extract_training_samples,extract_test_samples

def affin(img, m):
    WID = np.max(img.shape)
    x = np.tile(np.linspace(-1, 1, WID).reshape(1, -1), (WID, 1))
    y = np.tile(np.linspace(-1, 1, WID).reshape(-1, 1), (1, WID))
    p = np.array([[x, y, np.ones(x.shape)]])
    dx, dy, _ = np.sum(p * m.reshape(*m.shape, 1, 1), axis=1)
    u = np.clip((dx + 1) * WID / 2, 0, WID-1).astype('i')
    v = np.clip((dy + 1) * WID / 2, 0, WID-1).astype('i')
    return img[v, u]

def rotation_matrix(a):
    return np.array([[np.cos(a), -np.sin(a), 0],
                     [np.sin(a),  np.cos(a), 0],
                     [        0,          0, 1]])

def translation_matrix(tx, ty):
    return np.array([[1, 0, -tx],
                     [0, 1, -ty],
                     [0, 0, 1]])

#GPU_preparation
os.environ["CUDA_VISIBLE_DEVICES"]="0"
os.environ["TF_ENABLE_ONEDNN_OPTS"]="0"
gpus = config.list_physical_devices(device_type = 'GPU')
if len(gpus)>0:
    print(f">> GPU detected. {gpus[0].name}")
    config.experimental.set_memory_growth(gpus[0], True)

#mnist_preparation
#(x_train, y_train), (x_test, y_test) = load_mnist(normalize=False)

#emnist_preparation
#['balanced', 'byclass', 'bymerge', 'digits', 'letters', 'mnist']
x_train, y_train = extract_training_samples("balanced")
x_test, y_test = extract_test_samples('balanced')

#rote_x = np.copy(x_train_temp)
#rote_y = np.copy(y_train_temp)
#rote_x2 = np.copy(x_train_temp)
#rote_y2 = np.copy(y_train_temp)
#move_x = np.copy(x_train_temp)
#move_y = np.copy(y_train_temp)


#角度の決定
m = rotation_matrix(np.pi / 12)
m2 = rotation_matrix(np.pi / -12)
#移動方向の決定
m3 = translation_matrix(0.3,0)

#回転したデータの作成
#for x in range(len(x_train_temp)):
#	rote_x[x] = affin(x_train_temp[x], m)
#for x in range(len(x_train_temp)):
#	rote_x2[x] = affin(x_train_temp[x], m2)
#移動したデータの作成
#for x in range(len(x_train_temp)):
#	move_x[x] = affin(x_train_temp[x], m3)

#データの結合
#x_train = np.concatenate([x_train_temp, rote_x, rote_x2,move_x])
#y_train = np.concatenate([y_train_temp, rote_y, rote_y2,move_y])












#network = DeepConvNet()
#network.load_params("deep_convnet_params.pkl")
model = tf.keras.models.load_model("emnist_model.h5")

print("calculating test accuracy ... ")
#sampled = 1000
#x_test = x_test[:sampled]
#t_test = t_test[:sampled]

classified_ids = []

acc = 0.0
batch_size = 100

for i in range(int(x_test.shape[0] / batch_size)):
    tx = x_test[i*batch_size:(i+1)*batch_size]
    tt = y_test[i*batch_size:(i+1)*batch_size]
    y = model.predict(tx)
	#y = model.predict(tx, train_flg=False)
    y = np.argmax(y, axis=1)
    classified_ids.append(y)
    acc += np.sum(y == tt)
    
acc = acc / x_test.shape[0]
print("test accuracy:" + str(acc))

classified_ids = np.array(classified_ids)
classified_ids = classified_ids.flatten()
 
max_view = 30
current_view = 1

fig = plt.figure(figsize=(8,7))
fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.2, wspace=0.2)

mis_pairs = {}

print("AAAAAAAAAAAAAAAAAAAAA")
print(classified_ids.dtype)
print("AAAAAAAAAAAAAAAAAAAAA")



for i, val in enumerate(classified_ids == y_test):
    if not val:
        ax = fig.add_subplot(6, 5, current_view, xticks=[], yticks=[])
        ax.imshow(x_test[i].reshape(28, 28), cmap=plt.cm.gray_r, interpolation='nearest')
        mis_pairs[current_view] = (y_test[i], classified_ids[i])
            
        current_view += 1
        if current_view > max_view:
            break

print("======= misclassified result =======")
print("{view index: (label, inference), ...}")
print(mis_pairs)

plt.show()
