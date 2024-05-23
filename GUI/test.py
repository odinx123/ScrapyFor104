import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window(themename='darkly')

for color in root.style.colors:
    b = ttk.Button(root, text=color, bootstyle=color)
    b.pack(side=LEFT, padx=5, pady=5)

root.mainloop()