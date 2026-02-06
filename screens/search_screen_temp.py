import pymysql
import tkinter as tk
from tkinter import ttk, scrolledtext

class SearchScreen(tk.Frame):
    def __init__(self, master, show_screen_callback, top_frame):
        super().__init__(master)
        self.show_screen = show_screen_callback
        self.top_frame = top_frame

        # データベース接続取得
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='0728',
            database='app_assiggnment',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
		
        tk.Label(self, text="検索一覧画面", font=("Arial", 14)).pack(pady=20)
        tk.Button(self, text="TOPへ戻る", command=lambda: self.show_screen(self.top_frame)).pack(pady=10)
        
        # 検索条件フレーム
        cond_frame = tk.Frame(self, bg="#FFFDD0")
        cond_frame.pack(pady=10, padx=20, fill='x')
        
        # record_typeラジオボタン
        self.record_type_var = tk.StringVar(value="日報")
        types = [("日報", "日報"), ("引継ぎ", "引継ぎ"), ("障害/問い合わせ", "障害/問い合わせ")]
        for text, val in types:
            tk.Radiobutton(cond_frame, text=text, variable=self.record_type_var,
                           value=val, bg="#FFFDD0").pack(side='left', padx=10)
            
        tk.Label(cond_frame, text="本文キーワード:", bg="#FFFDD0").pack(side='left', padx=10)
        self.body_entry = tk.Entry(cond_frame, width=30)
        self.body_entry.pack(side='left', padx=5)

        # 検索ボタン
        tk.Button(cond_frame, text="検索", command=self._search_records).pack(side='left', padx=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                background="white",
                foreground="black",
                fieldbackground="white",
                rowheight=25,
                bordercolor="gray",
                borderwidth=1)
        style.map("Treeview", background=[("selected", "#a4cbf5")])

        # 結果表示
        self.tree = ttk.Treeview(self, columns=("record_type", "body", "created_at"), show="headings")
        self.tree.heading("record_type", text="種類")
        self.tree.heading("body", text="本文")
        self.tree.heading("created_at", text="日付")
        self.tree.pack(padx=20, pady=20, fill='both', expand=True)

        # スクロールバー
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.tree.pack(padx=20, pady=20, fill="both", expand=True)

        # 交互行の背景色
        self.tree.tag_configure('oddrow', background='white')
        self.tree.tag_configure('evenrow', background="#e6e6e6")
              
    def _search_records(self):
        record_type = self.record_type_var.get()
        keyword = self.body_entry.get().strip()

        sql = "SELECT id, record_type, body, created_at FROM records WHERE record_type = %s AND body LIKE %s"
        params = (record_type, f"%{keyword}%")

        with self.conn.cursor() as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()

        # Treeviewに表示
        for i in self.tree.get_children():
            self.tree.delete(i)
        #for row in results:
        #    self.tree.insert("", "end", values=(row['record_type'], row['body'],row['created_at']))

        # Treeview に表示（交互色）
        for idx, row in enumerate(results):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert("", "end",
                             values=(row['record_type'], row['body'], row['created_at']),
                             tags=(tag,))