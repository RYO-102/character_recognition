#############################################
#			ファイルから値を取得			#
#############################################
##損失関数
def loss_get(row,file_name):
	row = (row-1)*8
	n = row + 3

	with open (file_name,'r') as f:
		datalist = f.readlines()
		plt_test_ax1 = datalist[n]
	f.close()

	plt_test_ax1 = plt_test_ax1.replace('\n','')
	plt_test_ax1 = eval(plt_test_ax1)

	i = 0

	for i in range(999):
		if plt_test_ax1[i] < plt_test_ax1[i+1]:
			num = i + 1
			loss = plt_test_ax1[i]
			break
		elif i == 998:
			num = 1000
			loss = plt_test_ax1[999]
			break
	print(str(loss) + '(' + str(num) + ')',end=',')

	with open ('resurt.txt','a') as f:
		print(str(loss) + '(' + str(num) + ')',end=',',file=f)
	f.close()

##正解率
def accuracy_get(row,file_name):
	row = (row-1)*8
	n = row + 7

	with open (file_name,'r') as f:
		datalist = f.readlines()
		plt_test_ax2 = datalist[n]
	f.close()

	plt_test_ax2 = plt_test_ax2.replace('\n','')
	plt_test_ax2 = eval(plt_test_ax2)

	i = 0

	for i in range(999):
		if plt_test_ax2[i] > plt_test_ax2[i+1]:
			num = i + 1
			accuracy = plt_test_ax2[i]
			break
		elif i == 998:
			num = 100
			accuracy = plt_test_ax2[999]
			break
	print(str(accuracy) + '(' + str(num) + ')',end=',')

	with open ('resurt.txt','a') as f:
		print(str(accuracy) + '(' + str(num) + ')',end=',',file=f)
	f.close()

#row=17
#loss_get(row,'progress_test_ver1.2.txt')
#accuracy_get(row,'progress_test_ver1.2.txt')
