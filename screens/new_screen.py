import pymysql
import json
import tkinter as tk
from tkinter import scrolledtext,messagebox
from .scroll_frame import ScrollableFrame


class NewScreen(tk.Frame):
	def __init__(self, master, show_screen_callback, top_frame):
		super().__init__(master)
		self.show_screen = show_screen_callback
		self.top_frame = top_frame  # set_top_frame() で後から設定⇒OK
		
		#DB設定
		#connection = pymysql.connect(
		#	host="localhost",
		#	user="root",
		#	password="root",
		#	database="app_assiggnment",
		#	charset="utf8mb4",
		#	cursorclass=pymysql.cursors.DictCursor,
		#)
		### リストに設定 ###
		standup_title  = ["standup","日付","昨日やったこと","今日やったこと","困っていること","チケット番号"]
		standup_items  = ["frame_standup","date","done","today","blocker","ticket"]
		handover_title = ["handover","タイトル","背景","現状","次アクション","注意点","参考リンク"]
		handover_items = ["frame_handover","title","context","current","next","notes","link"]
		incident_title = ["incident","現象","影響範囲","環境","再現手順","確認済みログ","仮説"]
		incident_items = ["frame_incident","summary","impact","env","repro","chkedlog","hypo"]

		### GUI作成 ###
		scroll = ScrollableFrame(self)
		scroll.pack(fill="both", expand=True, padx=10, pady=10)

		##ヘッダー部分
		#選択
		frame_top = tk.Frame(scroll.scrollable_frame, pady=5)
		self.var = tk.StringVar(value="1")
		tk.Label(frame_top, text="種類:").pack(pady=5)
		#中央揃えにしたい
		tk.Radiobutton(frame_top, command=self.switchDisp, text="日報", variable=self.var, value="1").pack(side=tk.LEFT)
		tk.Radiobutton(frame_top, command=self.switchDisp, text="引継ぎ", variable=self.var, value="2").pack(side=tk.LEFT)
		tk.Radiobutton(frame_top, command=self.switchDisp, text="障害/問合せ", variable=self.var, value="3").pack(side=tk.LEFT)
		frame_top.pack(fill=tk.X, anchor=tk.CENTER)

		#戻るボタンと登録ボタン
		#ここも綺麗に揃えたい
		btn_frame = tk.Frame(scroll.scrollable_frame)
		tk.Button(btn_frame, text="戻る", command=lambda: self.show_screen(self.top_frame)).pack(side=tk.LEFT, pady=10, padx=40)
		tk.Button(btn_frame, text="登録", command=lambda: self.regData()).pack(side=tk.LEFT, pady=10, padx=40)
		btn_frame.pack(fill=tk.X)

		#各パターンの情報を辞書型で保持
		self.entries = {}
		self.sections = {}
		#日報
		self.entries["standup"],  self.sections["standup"]  = self.dispEachItems(standup_title, standup_items, scroll)
		#引継ぎ
		self.entries["handover"], self.sections["handover"] = self.dispEachItems(handover_title, handover_items, scroll)
		#障害
		self.entries["incident"], self.sections["incident"] = self.dispEachItems(incident_title, incident_items, scroll)

		#下部の登録ボタン⇒いらないかも
		self.btn_bottom = tk.Button(scroll.scrollable_frame, text="登録", command=lambda: self.regData())
		self.btn_bottom.pack(pady=10)

		# 初期表示（日報のみ表示）
		self.switchDisp()
		#connection.close()

	#def setTopFrame(self, top_frame):
	#	self.top_frame = top_frame

	def switchDisp(self):
		type_map = {"1": "standup", "2": "handover", "3": "incident"}
		selected = type_map.get(self.var.get())
		for section_frame in self.sections.values():
			section_frame.pack_forget()
		self.btn_bottom.pack_forget()
		if selected and selected in self.sections:
			self.sections[selected].pack(fill=tk.X, anchor=tk.CENTER)
		self.btn_bottom.pack(pady=10)

	def regData(self):
		connection = pymysql.connect(
			host="localhost",
			user="root",
			password="0728",
			database="app_assiggnment",
			charset="utf8mb4",
			cursorclass=pymysql.cursors.DictCursor,
		)
		type_map = {"1": "standup", "2": "handover", "3": "incident"}
		selected = type_map.get(self.var.get())
		#print(selected)
		if selected is None:
			return
		result = {}
		for key, widget in self.entries[selected].items():
			result[key] = widget.get("1.0", "end-1c")
		#print(selected)
		#print(result)
		#print(result['date'])

		title = ""
		body = ""
		meta_json = json.dumps(result, ensure_ascii=False)
		with connection.cursor() as cursor:
			insSQL = "INSERT INTO records (record_type, title, body, meta_json) VALUES ('" + selected + "','"
			insSQL = insSQL + title + "','" + body + "','" + meta_json + "')"
			cursor.execute(insSQL)
			connection.commit() 
		connection.close()
		self.finReg()

	def dispEachItems(self, titles, items, scroll):
		section_frame = tk.Frame(scroll.scrollable_frame, pady=5)
		entry_dict = {}
		for i in range(1, len(titles)):
			tk.Label(section_frame, text=titles[i]+":").pack(pady=5)
			entry = scrolledtext.ScrolledText(section_frame, width=50, height=5)
			entry.pack(pady=5)
			entry_dict[items[i]] = entry
		return entry_dict, section_frame

	def finReg(self):
		for section in self.entries.values():
			for widget in section.values():
				widget.delete("1.0", "end")
		messagebox.showinfo("登録完了","登録が完了しました")
		self.show_screen(self.top_frame)
		
		
