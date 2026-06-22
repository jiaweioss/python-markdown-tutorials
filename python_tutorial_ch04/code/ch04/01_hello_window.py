"""Create a tiny Tkinter window."""
import tkinter as tk

root = tk.Tk()
root.title("科研卡片工厂控制台")
root.geometry("360x180")

label = tk.Label(root, text="第一块 GUI 面板已经亮灯", font=("Microsoft YaHei", 14))
label.pack(pady=30)

button = tk.Button(root, text="收到", command=root.destroy)
button.pack()

root.mainloop()
