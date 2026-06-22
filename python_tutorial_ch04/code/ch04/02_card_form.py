"""A minimal learning-card form with Tkinter."""
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


def save_card():
    topic = topic_entry.get().strip() or "未命名主题"
    idea = idea_text.get("1.0", "end").strip()
    out = Path("cards")
    out.mkdir(exist_ok=True)
    file = out / f"{topic.replace(' ', '_')}_card.md"
    file.write_text(f"# {topic}\n\n{idea}\n", encoding="utf-8")
    messagebox.showinfo("已保存", f"卡片已写入：{file}")


root = tk.Tk()
root.title("学习卡片表单")
root.geometry("520x360")

tk.Label(root, text="主题").pack(anchor="w", padx=16, pady=(12, 4))
topic_entry = tk.Entry(root)
topic_entry.pack(fill="x", padx=16)

tk.Label(root, text="要点").pack(anchor="w", padx=16, pady=(12, 4))
idea_text = tk.Text(root, height=8)
idea_text.pack(fill="both", expand=True, padx=16)

tk.Button(root, text="保存卡片", command=save_card).pack(pady=14)
root.mainloop()
