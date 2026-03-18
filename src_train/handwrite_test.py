#########################################
#			メインプログラム			#
#########################################

##import
import os
import sys
import time
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import list_get
import model_test
#import mk_data
import mk_dataset

##from_import
from tensorflow import config
from tensorflow.keras import layers,models,datasets
from keras.utils.np_utils import to_categorical
from keras import optimizers,regularizers
from sklearn.model_selection import StratifiedKFold
sys.path.append('deep-learning-from-scratch-master')
#from dataset.mnist import load_mnist
from emnist import extract_training_samples,extract_test_samples

##関数
##アフィン変換用関数
def affin(img, m):
    WID = np.max(img.shape)
    x = np.tile(np.linspace(-1, 1, WID).reshape(1, -1), (WID, 1))
    y = np.tile(np.linspace(-1, 1, WID).reshape(-1, 1), (1, WID))
    p = np.array([[x, y, np.ones(x.shape)]])
    dx, dy, _ = np.sum(p * m.reshape(*m.shape, 1, 1), axis=1)
    u = np.clip((dx + 1) * WID / 2, 0, WID-1).astype('i')
    v = np.clip((dy + 1) * WID / 2, 0, WID-1).astype('i')
    return img[v, u]
##回転角度取得用関数
def rotation_matrix(a):
    return np.array([[np.cos(a), -np.sin(a), 0],
                     [np.sin(a),  np.cos(a), 0],
                     [        0,          0, 1]])
##移動方向取得用関数
def translation_matrix(tx, ty):
    return np.array([[1, 0, -tx],
                     [0, 1, -ty],
                     [0, 0, 1]])

##GPUの準備
os.environ["CUDA_VISIBLE_DEVICES"]="0"
os.environ["TF_ENABLE_ONEDNN_OPTS"]="0"
gpus = config.list_physical_devices(device_type = 'GPU')
if len(gpus)>0:
    print(f">> GPU detected. {gpus[0].name}")
    config.experimental.set_memory_growth(gpus[0], True)

##mnistの準備
#(x_train, y_train), (x_test, y_test) = load_mnist(normalize=False)

##emnistの準備
##['balanced', 'byclass', 'bymerge', 'digits', 'letters', 'mnist']
#x_train_norm, y_train_norm = mk_dataset.mk_dataset_1('train')
x_train_temp, y_train_temp = mk_dataset.mk_dataset('train')
#x_train, y_train = mk_dataset.mk_dataset('train')
x_test, y_test = mk_dataset.mk_dataset('test')
#x_train, y_train = extract_training_samples("balanced")
#x_test_temp, y_test_temp = extract_test_samples('balanced')
#x_test, y_test = extract_test_samples('balanced')

#print(len(x_train_temp))

##アフィン変換用変数宣言
rote_x = np.copy(x_train_temp)
rote_y = np.copy(y_train_temp)
rote_x2 = np.copy(x_train_temp)
rote_y2 = np.copy(y_train_temp)
move_x = np.copy(x_train_temp)
move_y = np.copy(y_train_temp)
move_x2 = np.copy(x_train_temp)
move_y2 = np.copy(y_train_temp)
move_x3 = np.copy(x_train_temp)
move_y3 = np.copy(y_train_temp)
move_x4 = np.copy(x_train_temp)
move_y4 = np.copy(y_train_temp)
move_x5 = np.copy(x_train_temp)
move_y5 = np.copy(y_train_temp)
move_x6 = np.copy(x_train_temp)
move_y6 = np.copy(y_train_temp)
move_x7 = np.copy(x_train_temp)
move_y7 = np.copy(y_train_temp)
move_x8 = np.copy(x_train_temp)
move_y8 = np.copy(y_train_temp)

##角度の決定
r1 = rotation_matrix(np.pi / 12)
r2 = rotation_matrix(np.pi / -12)
##移動方向の決定
m1 = translation_matrix(0.1,0)
m2 = translation_matrix(0.1,0.1)
m3 = translation_matrix(0,0.1)
m4 = translation_matrix(-0.1,0.1)
m5 = translation_matrix(-0.1,0)
m6 = translation_matrix(-0.1,-0.1)
m7 = translation_matrix(0,-0.1)
m8 = translation_matrix(0.1,-0.1)

##回転したデータの作成
for x in range(len(x_train_temp)):
	rote_x[x] = affin(x_train_temp[x], r1)
for x in range(len(x_train_temp)):
	rote_x2[x] = affin(x_train_temp[x], r2)
##移動したデータの作成
for x in range(len(x_train_temp)):
	move_x[x] = affin(x_train_temp[x], m1)
	move_x2[x] = affin(x_train_temp[x], m2)
	move_x3[x] = affin(x_train_temp[x], m3)
	move_x4[x] = affin(x_train_temp[x], m4)
	move_x5[x] = affin(x_train_temp[x], m5)
	move_x6[x] = affin(x_train_temp[x], m6)
	move_x7[x] = affin(x_train_temp[x], m7)
	move_x8[x] = affin(x_train_temp[x], m8)

##データの結合
x_train = np.concatenate([x_train_temp, rote_x, rote_x2, move_x, move_x2, move_x3, move_x4, move_x5, move_x6, move_x7, move_x8])
y_train = np.concatenate([y_train_temp, rote_y, rote_y2, move_y, move_y2, move_y3, move_y4, move_y5, move_y6, move_y7, move_y8])

#x_train = np.concatenate([x_train_temp, rote_x, rote_x2])
#y_train = np.concatenate([y_train_temp, rote_y, rote_y2])

##データの用意
#x_train,y_train = mk_data.mk_data(x_train_temp,y_train_temp)
#x_test,y_test = mk_data.mk_data(x_test_temp,y_test_temp)
x_train,x_test = x_train/255.0,x_test/255.0
print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
print(len(x_train))
print(len(x_test))

#print(x_train.dtype,x_test.dtype)
print("aaaaaaaaaaaaaaaaaaaaaaaa")
print(y_train.dtype,y_test.dtype)
print(y_train.dtype)
print(y_test.dtype)
print("aaaaaaaaaaaaaaaaaaaaaaaa")


plt.figure(figsize=(1,1))
plt.subplots_adjust(hspace=0.5)
i=0
for n in range(112800):
  if y_test[n] == 1:
    if i==1:
      break
    plt.subplot(1, 1, i+1)
    i = i+1
    plt.imshow(x_test[n], cmap="Greys")
    plt.title(y_test[n])
  plt.axis('off')
plt.show()


##データセットが'letter'の時に入れる
#y_train = to_categorical(y_train,47)
#y_test = to_categorical(y_test,47)

##分割処理
#skf = StratifiedKFold(n_splits=1)
#for train_index, test_index in skf.split(x_train,y_train):
#	x_train_59000 = x_train[train_index]
#	y_train_59000 = y_train[train_index]
#	x_train_1000 = x_train[test_index]
#	y_train_1000 = y_train[test_index] 

#*******************************************************************************************************************************#
##パラメーター設定
NEURONS = 128									#ニューロン数
ACTIVATION = 'relu'							#活性化関数
OPTIMIZER = optimizers.Adagrad()					#最適化アルゴリズム
LOSS = 'sparse_categorical_crossentropy'		#損失関数
BATCH = 40									#バッチサイズ
RATIO = 0.7										#Dropout層の割合
INITIALIZER = 'RandomNormal'					#重みの初期化
L2 = 0.0005									#Weight decayのL2ノルム
file_name = 'test_handwrite(20231018_Ac2).txt'				#historyを保存するファイル名
row = 1											#ファイル内の何番目を参照するか
title = 'test_handwrite(20231018_Ac2)'						#グラフの名前
subtitle = '(20231018_Ac2)2rote+8move'					#グラフ内のタイトル

##CNNのパラメーター設定
PADDING = 'same'								#パディングを行うか
STRIDES = 3										#ストライドの数

#時間測定開始
time_start = time.perf_counter()

##モデルのパーツ
##layers.Conv2D(NEURONS,(3,3),activation=ACTIVATION,padding=PADDING,strides=STRIDES,input_shape=(28,28,1))
##layers.Activation(ACTIVATION)
##layers.MaxPooling2D(pool_size=(2,2))
##layers.Flatten(input_shape=(28,28,1))
##layers.Dense(NEURONS,activation = ACTIVATION,kernel_regularizer=regularizers.l2(L2),kernel_initializer=INITIALIZER)
##layers.BatchNormalization()
##layers.Dropout(RATIO)

model = models.Sequential([
#  layers.Conv2D(256,(5,5),activation=ACTIVATION,padding=PADDING,input_shape=(100,250,1)),
  layers.Conv2D(256,(5,5),activation=ACTIVATION,padding=PADDING,input_shape=(250,250,1)),
  layers.Conv2D(256,(5,5),activation=ACTIVATION,padding=PADDING),
  layers.Conv2D(NEURONS,(5,5),activation=ACTIVATION),
  layers.Conv2D(NEURONS,(5,5),activation=ACTIVATION),
  layers.MaxPooling2D(pool_size=(2,2)),
  layers.Dropout(RATIO),
  layers.Conv2D(NEURONS,(3,3),activation=ACTIVATION,padding=PADDING),
  layers.Conv2D(NEURONS,(3,3),activation=ACTIVATION,padding=PADDING),
  layers.Conv2D(64,(3,3),activation=ACTIVATION),
  layers.Conv2D(64,(3,3),activation=ACTIVATION),
  layers.MaxPooling2D(pool_size=(2,2)),
  layers.Flatten(),
  layers.Dense(NEURONS,activation = ACTIVATION,kernel_regularizer=regularizers.l2(L2)),
  layers.Dropout(RATIO),
  layers.Dense(3, activation='softmax')
])

##モデルの概要表示
model.summary()

##モデルのコンパイル
model.compile(optimizer = OPTIMIZER,
              loss = LOSS,
              metrics=['accuracy'])

##実行
history = model.fit(x_train, y_train,batch_size = BATCH,validation_split=0.1,epochs=20)

##時間計測終了
time_end = time.perf_counter()
time = time_end - time_start

#*******************************************************************************************************************************

##評価関数の取得
metrics=['loss','accuracy']

##グラフ全体のサイズ
plt.figure(figsize=(13,6))

##グラフの描画
for i in range(len(metrics)):
	
	plt_train_ax1 = history.history['loss']
	plt_test_ax1 = history.history['val_loss']
	plt_train_ax2 = history.history['accuracy']
	plt_test_ax2 = history.history['val_accuracy']

	##損失関数グラフ
	ax1=plt.subplot(1,2,1)
	ax1.set_xlim(0,20)
	#ax1.set_ylim(0.09,1)
	ax1.set_yscale('log')
	ax1.plot(plt_train_ax1,label='training',color='blue')
	#ax1.plot(plt_train_ax1,label='training',marker='p',color='blue')
	ax1.plot(plt_test_ax1,label='test',color='orange')
	#ax1.plot(plt_test_ax1,label='test',marker='*',color='orange')
	ax1.set_xlabel('epochs',fontsize=10)
	ax1.set_ylabel('loss',fontsize=10)
	ax1.grid(color='b',linestyle=':',linewidth=0.3,which='both')
	ax1.legend(['training','test'])

	##正解率グラフ
	ax2=plt.subplot(1,2,2)
	ax2.set_xlim(0,20)
	#ax2.set_ylim(0.60,1)
	ax2.plot(plt_train_ax2,label='training',color='blue')
	#ax2.plot(plt_train_ax2,label='training',marker='p',color='blue')
	ax2.plot(plt_test_ax2, label='test',color='orange')
	#ax2.plot(plt_test_ax2, label='test',marker='*',color='orange')
	ax2.set_xlabel('epochs',fontsize=10)
	ax2.set_ylabel('accuracy',fontsize=10)
	ax2.grid(color='b',linestyle=':',linewidth=0.3,which='both')
	ax2.legend(['training','test'])
	
	plt.subplots_adjust(wspace=0.3)

##タイトルの出力
plt.suptitle(subtitle)
print(subtitle)

print('\a')

plt.savefig(title + ".png")
#plt.show()

##historyをファイルに書き込み
with open(file_name,'a') as f:
	print('loss_train_' + subtitle,file=f)
	print(history.history['loss'],file=f)
	print('loss_test_' + subtitle,file=f)
	print(history.history['val_loss'],file=f)
	print('accuracy_train_' + subtitle,file=f)
	print(history.history['accuracy'],file=f)
	print('accuracy_test_' + subtitle,file=f)
	print(history.history['val_accuracy'],file=f)

model.save("handwrite_model_Ac2.h5")

##損失関数：増加前の値を取得
##正解率：減少前の値を取得
list_get.loss_get(row,file_name)
list_get.accuracy_get(row,file_name)

##損失関数増加前の値,正解率減少前の値,学習時間を記載
print(str(time),end=',')
with open ('resurt.txt','a') as f:
	print(str(time),end=',',file = f)
f.close()

##モデルのテスト
model_test.model_test(x_test,y_test)
