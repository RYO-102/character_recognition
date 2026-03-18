def mk_dataset(i):
	import matplotlib.pyplot as plt
	import os
	import cv2
	import random
	import numpy as np
	
	CATEGORIES = ["0","1","2"]
	if i == 'train':
		DATADIR = "C:/python-39/sand/image/20231018train"
	else:
		DATADIR = "C:/python-39/sand/image/20231018test"
	IMG_SIZE_W = 250
	IMG_SIZE_H = 250
	training_data = []
	
	def create_training_data():
	    for class_num, category in enumerate(CATEGORIES):
	        path = os.path.join(DATADIR, category)
	        for image_name in os.listdir(path):
	            try:
	                img_array = cv2.imread(os.path.join(path, image_name), cv2.IMREAD_GRAYSCALE)
	                img_resize_array = cv2.resize(img_array, (IMG_SIZE_W, IMG_SIZE_H))
	                training_data.append([img_resize_array, CATEGORIES[class_num]])
	            except Exception as e:
	                pass
	create_training_data()
	random.shuffle(training_data)
	X_train = []
	y_train = []
	
	for feature, label in training_data:
	    X_train.append(feature)
	    y_train.append(label)
	
	X_train = np.array(X_train)
	y_train = np.array(y_train)
	y_train = y_train.astype('uint8')

	#for i in range(0, 4):
	#    print("学習データのラベル：", y_train[i])
	#    plt.subplot(2, 2, i+1)
	#    plt.axis('off')
	#    plt.title(label = 'Dog' if y_train[i] == 0 else 'Cat')
	#    plt.imshow(X_train[i], cmap='gray')
	#plt.show()

	return(X_train,y_train)

def mk_dataset_1(i):
	import matplotlib.pyplot as plt
	import os
	import cv2
	import random
	import numpy as np
	
	CATEGORIES = ["0"]
	if i == 'train':
		DATADIR = "C:/python-39/sand/image/20231012_2train"
	else:
		DATADIR = "C:/python-39/sand/image/20231012_2test"
	IMG_SIZE_W = 250
	IMG_SIZE_H = 250
	training_data = []
	
	def create_training_data():
	    for class_num, category in enumerate(CATEGORIES):
	        path = os.path.join(DATADIR, category)
	        for image_name in os.listdir(path):
	            try:
	                img_array = cv2.imread(os.path.join(path, image_name), cv2.IMREAD_GRAYSCALE)
	                img_resize_array = cv2.resize(img_array, (IMG_SIZE_W, IMG_SIZE_H))
	                training_data.append([img_resize_array, CATEGORIES[class_num]])
	            except Exception as e:
	                pass
	create_training_data()
	random.shuffle(training_data)
	X_train = []
	y_train = []
	
	for feature, label in training_data:
	    X_train.append(feature)
	    y_train.append(label)
	
	X_train = np.array(X_train)
	y_train = np.array(y_train)
	y_train = y_train.astype('uint8')

	#for i in range(0, 4):
	#    print("学習データのラベル：", y_train[i])
	#    plt.subplot(2, 2, i+1)
	#    plt.axis('off')
	#    plt.title(label = 'Dog' if y_train[i] == 0 else 'Cat')
	#    plt.imshow(X_train[i], cmap='gray')
	#plt.show()

	return(X_train,y_train)

def mk_dataset_2(i):
	import matplotlib.pyplot as plt
	import os
	import cv2
	import random
	import numpy as np
	
	CATEGORIES = ["1","2"]
	if i == 'train':
		DATADIR = "C:/python-39/sand/image/20231012_2train"
	else:
		DATADIR = "C:/python-39/sand/image/20231012_2test"
	IMG_SIZE_W = 250
	IMG_SIZE_H = 250
	training_data = []
	
	def create_training_data():
	    for class_num, category in enumerate(CATEGORIES):
	        path = os.path.join(DATADIR, category)
	        for image_name in os.listdir(path):
	            try:
	                img_array = cv2.imread(os.path.join(path, image_name), cv2.IMREAD_GRAYSCALE)
	                img_resize_array = cv2.resize(img_array, (IMG_SIZE_W, IMG_SIZE_H))
	                training_data.append([img_resize_array, CATEGORIES[class_num]])
	            except Exception as e:
	                pass
	create_training_data()
	random.shuffle(training_data)
	X_train = []
	y_train = []
	
	for feature, label in training_data:
	    X_train.append(feature)
	    y_train.append(label)
	
	X_train = np.array(X_train)
	y_train = np.array(y_train)
	y_train = y_train.astype('uint8')

	#for i in range(0, 4):
	#    print("学習データのラベル：", y_train[i])
	#    plt.subplot(2, 2, i+1)
	#    plt.axis('off')
	#    plt.title(label = 'Dog' if y_train[i] == 0 else 'Cat')
	#    plt.imshow(X_train[i], cmap='gray')
	#plt.show()

	return(X_train,y_train)