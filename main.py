import tkinter as tk
from screens.top_screen import TopScreen
from screens.new_screen import NewScreen
from screens.search_screen_temp import SearchScreen

def show_screen(frame):
    frame.tkraise()

# メニュー画面
root = tk.Tk()
root.title("TOP画面")
root.geometry("800x600")

top_frame = TopScreen(root, show_screen, None, None, None)
new_screen = NewScreen(root, show_screen, top_frame)
search_screen = SearchScreen(root, show_screen, top_frame)

top_frame.new_screen = new_screen
top_frame.search_screen = search_screen

for frame in (top_frame, new_screen, search_screen):
    frame.place(relwidth=1, relheight=1)

# 初期画面表示
show_screen(top_frame)

root.mainloop()