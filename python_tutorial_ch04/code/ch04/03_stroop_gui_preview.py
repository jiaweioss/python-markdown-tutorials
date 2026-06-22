"""A tiny Stroop-like GUI preview."""
import time
import tkinter as tk

TRIAL = {"word": "RED", "ink": "blue", "correct": "j"}


def start_trial():
    global start
    prompt.config(text="判断墨水颜色：红色按 F，蓝色按 J")
    stimulus.config(text=TRIAL["word"], fg=TRIAL["ink"])
    start = time.perf_counter()


def respond(key: str):
    rt = round((time.perf_counter() - start) * 1000, 2)
    ok = key == TRIAL["correct"]
    result.config(text=f"反应：{key}  正确：{ok}  反应时：{rt} ms")


root = tk.Tk()
root.title("Stroop GUI 预告")
root.geometry("520x300")
start = time.perf_counter()

prompt = tk.Label(root, text="点击开始后看刺激", font=("Microsoft YaHei", 13))
prompt.pack(pady=16)
stimulus = tk.Label(root, text="", font=("Arial", 36, "bold"))
stimulus.pack(pady=18)
result = tk.Label(root, text="")
result.pack(pady=12)
tk.Button(root, text="开始", command=start_trial).pack()
root.bind("f", lambda event: respond("f"))
root.bind("j", lambda event: respond("j"))
root.mainloop()
