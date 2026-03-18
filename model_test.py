########################################
#テストデータから正解率、損失関数の算出#
########################################

def model_test(x_test,y_test):
	import time
	import tensorflow as tf
	from tensorflow.keras import layers,models,datasets

	time_start = time.perf_counter()	#Time measurement start

	model=models.load_model('emnist_model.h5')
	test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

	time_end = time.perf_counter()	#Time measurement end
	time = time_end - time_start

	print(str(test_loss),end=',')
	print(str(test_accuracy),end=',')
	print(str(time))

	with open ('resurt.txt','a') as f:
		print(str(test_loss) + ',' + str(test_accuracy) + ',' + str(time),file=f)
	f.close()

