def create_modal_dialog(user_num):
	#インポート
	import tkinter as tk
	#グローバル宣言
	global password
	global num
	
	#ファイルオープン(パスワード取得)
	filename = 'pass_' + str(user_num) + '.txt'
	f = open(filename,'r')
	password = f.read()
	f.close()
	
	#変数初期化
	num = 3
	
	#モーダルダイアログボックスの作成
	dlg_modal = tk.Toplevel()
	dlg_modal.title("パスワード認証") # ウィンドウタイトル
	dlg_modal.geometry("300x125")   # ウィンドウサイズ(幅x高さ)
	
	# モーダルにする設定
	dlg_modal.grab_set()        # モーダルにする
	dlg_modal.focus_set()       # フォーカスを新しいウィンドウをへ移す
	#dlg_modal.transient(master)   # タスクバーに表示しない
	
	#部品用意
	label = tk.Label(dlg_modal,relief=tk.SOLID,text="パスワードを入力してください",height=1,width=30,font=("Helvetica",13))
	label.grid(row=0, column=0, columnspan=2, padx=5, pady=20)
	global entry
	entry = tk.Entry(dlg_modal,font=("Helvetica",13))
	entry.grid(row=1, column=0, padx=5, pady=2)
	button = tk.Button(dlg_modal,text="決定",bg="LightSteelBlue2",width=10,height=1,command=check,font=("Helvetica",13))
	button.grid(row=1, column=1, padx=5, pady=2)
	#label.pack()
	#button.pack()
	#entry.pack()
	
#判定する(決定ボタンから)
def check():
	#インポート
	from tkinter import messagebox
	global num
	import processing
	
	#エントリー内のパスワード取得
	key = entry.get()
	#入力パスワード加工
	key = processing.password(key)
	
	#確認用(確認後コメントアウト)
	#print(key,type(key))
	#print(password,type(password))
	
	#承認処理
	if str(key) == str(password):
		messagebox.showinfo('承認', 'あなたは本人です！！アクセスを許可します！！')
		num = 3
	else:
		num = num - 1
		if num != 0:
			messagebox.showerror('承認失敗', 'あなたは本人ではありません！あと%d回認証可能です。'%num)
		elif num == 0:
			messagebox.showerror('認証失敗','ロックをかけます')
			import sys
			sys.exit()