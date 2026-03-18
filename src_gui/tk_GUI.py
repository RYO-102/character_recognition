###############
# 筆跡鑑定GUI #
###############

def GUI_show():
	#インポート
	import tkinter as tk
	import num_test01
	#グローバル宣言
	global name
	global num
	#変数の初期化
	name = "null"
	num = 3
	
	#rootメインウィンドウ設定
	root = tk.Tk()
	root.title("Hand Write_Appraisal")
	root.geometry("975x525")
	
	#右側（画像表示、終了ボタン）
	frame_right = tk.Frame(root,pady=80,padx=50,bg="ivory2")
	global canvas_right
	canvas_right = tk.Canvas(frame_right,relief=tk.GROOVE,height=278,width=450,bg="gainsboro")
	button1_right = tk.Button(frame_right,text="終了",bg="LightSteelBlue2",width=10,command=end,font=("Helvetica",14))
	
	#左側（選択ボタン、取り消しボタン、結果表示、判定）
	frame_left = tk.Frame(root,pady=50, padx=5,bg="ivory2")
	button1_left = tk.Button(frame_left,text="選択",bg="LightSteelBlue2",width=50,command=file_open,font=("Helvetica",14))
	button2_left = tk.Button(frame_left,text="取り消し",bg="LightSteelBlue2",width=50,command=cancel,font=("Helvetica",14))
	global label_left
	label_left = tk.Label(frame_left,relief=tk.SOLID,text="画像を選択してください",bg="aliceblue",height=10,width=50,font=("Helvetica",17))
	button3_left = tk.Button(frame_left,text="判定",bg="LightSteelBlue2",width=50,command=judge,font=("Helvetica",14))
	
	#ウィジェットの配置(それぞれのフレーム、右側、左側)
	frame_right.pack(side=tk.RIGHT, fill=tk.Y)
	frame_left.pack(side=tk.LEFT, fill=tk.Y)
	
	canvas_right.pack(pady=5,padx=5)
	button1_right.pack(pady=5,padx=5,anchor=tk.E)
	
	button1_left.pack(pady=5,padx=5)
	button2_left.pack(pady=5,padx=5)
	label_left.pack(pady=5,padx=5)
	button3_left.pack(pady=5,padx=5)
	
	#rootループ実行
	root.mainloop()

#以下ボタンから呼び出す関数一覧

#ファイルオープン（選択ボタンから）
def file_open():
	#インポート
	import tkinter as tk
	import tkinter.filedialog
	from PIL import Image, ImageTk
	#グローバル変数
	global image
	global name
	global canvas_right
	
	#画像名取得、画像ロード、キャンバス表示
	name = tk.filedialog.askopenfilename(title="ファイル選択", initialdir="C:/python/GUI", filetypes=[("Image File","*.png")])
	
	#画像の取得・リサイズ・型変更？？
	image = Image.open(name)
	image = image.resize((450,278))
	image = ImageTk.PhotoImage(image)
	
	#image = tk.PhotoImage(file=name)
	
	#canvasに画像表示
	canvas_right.create_image(450/2, 278/2, image=image,tag="img_tag")

#キャンバス内の画像とラベルの取り消し（取り消しボタンから）
def cancel():
	#グローバル変数宣言
	global label_left
	global canvas_right
	global name
	
	#ラベル取り消し
	label_left["text"] = "取り消しました。"
	#画像取り消し
	canvas_right.delete("img_tag")
	#nameをnullに変更
	name = "null"

#判定（判定ボタンから）
def judge():
	#インポート
	import num_test01
	import create_modal_dialog
	from tkinter import messagebox
	#グローバル変数宣言
	global name
	global label_left
	global num
	
	#名前がnullの時処理を行わない
	if name == "null":
		label_left["text"] = "画像を選択してください。"
		return
	
	#予測関数に飛ばす
	result = num_test01.Appraisal(name)
	
	#ラベルに記入
	if result == 0:
		label_left["text"] = "この筆跡は本人のもの\nではありません。"
		#メッセージボックスの表示
		num = num - 1
		if num != 0:
			messagebox.showerror('認証失敗','あと% d 回認証可能です。'% num)
		elif num == 0:
			messagebox.showerror('認証失敗','ロックをかけます')
			import sys
			sys.exit()
	
	elif result == 1:
		label_left["text"] = "この筆跡は”柴田優希”さん\n本人のものです。"
		#変数の初期化
		num = 3
		create_modal_dialog.create_modal_dialog(1)
	
	elif result == 2:
		label_left["text"] = "この筆跡は”柴山美千夏”さん\n本人のものです。"
		#変数の初期化
		num = 3
		create_modal_dialog.create_modal_dialog(2)

#終了（終了ボタンから）
def end():
	import sys
	sys.exit()