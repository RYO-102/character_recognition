def load_imgset(filename):
	#インポート
	import tensorflow as tf
	import numpy as np
	import cv2
	
	#データ読み込み
	img_array = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
	#リサイズ
	img_resize_array = cv2.resize(img_array, (250, 250))
	#何やってるかわからん
	img_expand = img_resize_array[np.newaxis, ...]
	
	
#	img = tf.io.decode_image(tf.io.read_file(filename))
#	img = tf.image.rgb_to_grayscale(img)
#	img = cv2.resize(img, dsize=(250, 250))
#	img = np.reshape(img, (250, 250))
#	img / 255.0
#	img_set = np.expand_dims(img,0) # Create dataset from one image
	return img_expand

#tk_GUIから呼び出される
def Appraisal(arg_name):
	#インポート
	import tensorflow as tf
	import numpy as np
	import cv2
	
	#モデル読み込み
	model = tf.keras.models.load_model("handwrite_model_Ac.h5")
	
	#print(arg_name)
	#img = cv2.imread(arg_name)
	
	#データ取得・加工
	img = load_imgset(arg_name)
	
	#img2 = cv2.resize(img,dsize=(250, 250))
	#img3 = cv2.cvtColor(img2,cv2.COLOR_RGB2GRAY)
	#img3 = tf.image.rgb_to_grayscale(img2)
	#print(img.shape)
	#print(img2.shape)
	#print(img3.shape)
	
	#cv2.imshow("moge3",img3)
	#img4 = np.reshape(img3, (250, 250,1))
	#img = np.reshape(img, (250, 250))
	#img5 = img4 / 255.0
	#print(img5.shape)
	#print(img5.dtype)
	
	#img6 = img5.astype(np.float32)
	#img7 = np.array(img6)
	#print(img7.shape)
	#print(img7.dtype)
	
	#予測
	pred = model.predict(img)
	pred_num = pred.argmax()
	#print("-->", pred_num)
	
	return pred_num