################
#アフィン変換用#
################

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
					 [		  0,		  0, 1]])

def translation_matrix(tx, ty):
	return np.array([[1, 0, -tx],
					 [0, 1, -ty],
					 [0, 0, 1]])

def scaling_matrix(sx, sy):
	return np.array([[1/sx, 0, 0],
					 [0, 1/sy, 0],
					 [0,  0, 1]])

def mk_data(x_train_temp,y_train_temp):
	x_train = np.copy(x_train_temp)
	y_train = np.copy(y_train_temp)

	count = 0
	move_x = [-0.1,0,0.1]
	move_y = [-0.1,0,0.1]
	scale = [0.8,1.2]
	rote = [-60,60]

	count = len(move_x) * len(move_y) * len(scale) * len(rote)

	#for i in range(length(move_x) * len(move_y) * len(scale) * len(rote)):
	x_train_2 = np.concatenate([x_train,x_train])
	y_train_2 = np.concatenate([y_train,y_train])

	x_train_4 = np.concatenate([x_train_2,x_train_2])
	y_train_4 = np.concatenate([y_train_2,y_train_2])

	x_train_8 = np.concatenate([x_train_4,x_train_4])
	y_train_8 = np.concatenate([y_train_4,y_train_4])

	x_train_16 = np.concatenate([x_train_8,x_train_8])
	y_train_16 = np.concatenate([y_train_8,y_train_8])

	x_train_32 = np.concatenate([x_train_16,x_train_16])
	y_train_32 = np.concatenate([y_train_16,y_train_16])

#	 x_train_64 = np.concatenate([x_train,x_train])
#	 y_train_64 = np.concatenate([y_train,y_train])

	x_train = np.concatenate([x_train_32,x_train_4])
	y_train = np.concatenate([y_train_32,y_train_4])  

#コピー
	x_t = np.copy(x_train)
	y_t = np.copy(y_train)

	# 初期化対策用
	m_ex = np.zeros((3, 3))

	for mx in move_x:
		for my in move_y:
			for s in scale:
				for r in rote:
#					train_x = np.copy(x_train_temp)
#					train_y = np.copy(y_train_temp)
					m1 = rotation_matrix(np.pi / r)
					m2 = translation_matrix(mx,my)
					m3 = scaling_matrix(s,s)
					m = np.dot(np.dot(m1, m2), m3)

					m_ex = np.concatenate([m_ex,m])

#					for x in range(len(x_train_temp)):
#						train_x[x] = affin(x_train_temp[x], m)
#
#					## 連結処理
#					x_train = np.concatenate([x_train,train_x])
#					y_train = np.concatenate([y_train,train_y])
#

	mm_ex = m_ex.reshape(count+1, 3, 3)

	for ii in range(1,count + 1):
		kk = 1
		for jj in range( 0, count ):
			
			tm = len(x_train_temp) * jj + ii - 1
			x_train[ tm ] = affin(x_t[ tm ], mm_ex[kk])
			kk = kk + 1

	plt.figure(figsize=(10, 9))
	plt.subplots_adjust(hspace=0.5)

	for n in range(1,len(x_train),len(x_train_temp)):
		plt.subplot(10,11 , int( n/len(x_train_temp)) + 1 )
		plt.imshow(x_train[n], cmap="Greys")
		plt.title(n)
		plt.axis('off')
#	plt.show()


	return(x_train,y_train)

def mk_data_add(x_train_temp,y_train_temp):
	x_train = np.copy(x_train_temp)
	y_train = np.copy(y_train_temp)

	count = 0
	move_x = [0]
	move_y = [0]
	scale = [1]
	rote = [360]

	count = len(move_x) * len(move_y) * len(scale) * len(rote)

	x_tmp = np.zeros([112800, 32, 32],dtype='uint8')

# 拡張処理
#	for i in range(0,len(x_train)):
#		x_tmp[i] = np.pad(x_train[i], [0, 0,], "constant")

	#for i in range(length(move_x) * len(move_y) * len(scale) * len(rote)):
	x_train_2 = np.concatenate([x_tmp,x_tmp])
	y_train_2 = np.concatenate([y_train,y_train])

	x_train_4 = np.concatenate([x_train_2,x_train_2])
	y_train_4 = np.concatenate([y_train_2,y_train_2])

	x_train_8 = np.concatenate([x_train_4,x_train_4])
	y_train_8 = np.concatenate([y_train_4,y_train_4])

	x_train_16 = np.concatenate([x_train_8,x_train_8])
	y_train_16 = np.concatenate([y_train_8,y_train_8])

	x_train_32 = np.concatenate([x_train_16,x_train_16])
	y_train_32 = np.concatenate([y_train_16,y_train_16])

#	 x_train_64 = np.concatenate([x_train,x_train])
#	 y_train_64 = np.concatenate([y_train,y_train])

	#x_tmp = np.concatenate([x_train_32,x_train_4])
	#y_train = np.concatenate([y_train_32,y_train_4])  

#コピー
	x_t = np.copy(x_tmp)
	y_t = np.copy(y_train)


	print("nununuunununun")


	# 初期化対策用
	m_ex = np.zeros((3, 3))

	for mx in move_x:
		for my in move_y:
			for s in scale:
				for r in rote:
#					train_x = np.copy(x_train_temp)
#					train_y = np.copy(y_train_temp)
					m1 = rotation_matrix(np.pi / r)
					m2 = translation_matrix(mx,my)
					m3 = scaling_matrix(s,s)
					m = np.dot(np.dot(m1, m2), m3)

					m_ex = np.concatenate([m_ex,m])

#					for x in range(len(x_train_temp)):
#						train_x[x] = affin(x_train_temp[x], m)
#
#					## 連結処理
#					x_train = np.concatenate([x_train,train_x])
#					y_train = np.concatenate([y_train,train_y])
#

	mm_ex = m_ex.reshape(count+1, 3, 3)

# アフィン変換

	for ii in range(1,count + 1):
		kk = 1
		for jj in range( 0, count ):
			
			tm = len(x_train_temp) * jj + ii - 1
			x_tmp[ tm ] = affin(x_t[ tm ], mm_ex[kk])
			kk = kk + 1



	return(x_tmp,y_train)

# 拡張処理
os.environ["CUDA_VISIBLE_DEVICES"]="0"
os.environ["TF_ENABLE_ONEDNN_OPTS"]="0"
gpus = config.list_physical_devices(device_type = 'GPU')
if len(gpus)>0:
	print(f">> GPU detected. {gpus[0].name}")
	config.experimental.set_memory_growth(gpus[0], True)

x_train_train, y_train_train = extract_training_samples("balanced")
x_test, y_test = extract_test_samples('balanced')

x_train,y_train = mk_data_add(x_train_train,y_train_train)
#x_train,y_train = mk_data(x_train_train,y_train_train)
