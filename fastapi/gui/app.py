import tkinter as tk
from tkinter import messagebox
import subprocess
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def map_hash():
    h = entry.get()
    try:
        out = subprocess.check_output(
            ["../cuda_core/rainbow_app.exe", h],
            text=True
        )
        result.set(out)
    except:
        messagebox.showerror("Error", "CUDA GPU not detected")

root = tk.Tk()
root.title("CUDA Hash–Plaintext Mapper")

tk.Label(root, text="Enter MD5 Hash").pack()
entry = tk.Entry(root, width=50)
entry.pack()

tk.Button(root, text="Map Plaintext (CUDA)", command=map_hash).pack()

result = tk.StringVar()
tk.Label(root, textvariable=result, fg="green").pack()

# Graph
fig = Figure(figsize=(4,3))
ax = fig.add_subplot(111)
ax.plot([100,200,300],[1.1,0.6,0.3])
ax.set_title("CUDA Lookup Time")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

root.mainloop()
