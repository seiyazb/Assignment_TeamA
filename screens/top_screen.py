import tkinter as tk
from tkinter import ttk

class TopScreen(tk.Frame):
    def __init__(self, master, show_screen_callback, new_screen, list_screen, search_screen):
        super().__init__(master, bg="#FFFDD0") # 背景色変更
        self.place(relwidth=1, relheight=1)
        self.show_screen = show_screen_callback
        self.new_screen = new_screen
        self.list_screen = list_screen
        self.search_screen = search_screen

        # ttkスタイル設定
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton',
                        font=('Helvetica', 14),
                        padding=10,
                        background='white',     # ボタン背景白
                        foreground='black',     # 文字黒
                        borderwidth=1,
                        relief='flat')
        style.map('TButton',
                  background=[('active', '#e0e0e0'), ('pressed', '#d0d0d0')],
                  foreground=[('disabled', '#a3a3a3')])
        
        # タイトル
        title_label = ttk.Label(self, text="引継ぎ・日報 管理アプリ", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=(60, 40))

        # ボタンフレーム（背景をフレーム色に統一、グレーなし）
        button_frame = tk.Frame(self, bg="#FFFDD0")  # フレームもクリーム色
        button_frame.pack(padx=60, pady=20, fill='x')

        # 列幅を均等にする
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        # 新規登録ボタン
        new_button = ttk.Button(button_frame, text="新規登録", command=lambda: self.show_screen(self.new_screen))
        new_button.pack(side='left', expand=True, fill='x', padx=15)

        # 検索ボタン
        search_button = ttk.Button(button_frame, text="検索", command=lambda: self.show_screen(self.search_screen))
        search_button.pack(side='left', expand=True, fill='x', padx=15)
