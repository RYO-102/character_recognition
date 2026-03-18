################################
# 入力パスワード加工プログラム #
################################

def password(data):
	#変数初期化
	ASCII_sum = 0
	ASCII_list = []
	
	#パスワードの長さ取得
	pass_len = len(data)
	
	#ASCIIコード変換、ASCII_sumの取得
	for i in range(pass_len):
		ord_s = ord(data[i])
		ASCII_sum += int(ord_s)
		ASCII_list.append(ord_s)
	
	#ASCII_sumの長さを取得
	ASCII_sumlen = len(str(ASCII_sum))
	
	#ASCII_listの各要素にASCII_sumを足し、255で割ったときの余りを求める
	for i in range(pass_len):
		ASCII_list[i] += ASCII_sum
		ASCII_list[i] = ASCII_list[i] % 255
	
	#ASCII_sumの値を255で割ったときの余りを求める
	ASCII_sum = ASCII_sum % 255
	
	#暗号化パスワードの作成
	password = str(ASCII_sumlen)
	for i in range(pass_len):
		password = str(password) + str(ASCII_list[i])
	password = str(password) + str(ASCII_sum)
	
	#確認用(動作確認後コメントアウト)
	#print(ASCII_sumlen)
	#print(ASCII_list)
	#print(ASCII_sum)
	
	#password(key)をcreate_modal_dialogに返す
	return password