import tkinter as tk
from tkinter import ttk

class ScrollableCheckboxFrame:
    def __init__(self, master, frame_width, frame_height):
        self.master = master
        self.frame_width = frame_width
        self.frame_height = frame_height

        self.scrollbar = ttk.Scrollbar(master, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.frame = tk.Frame(master, width=frame_width, height=frame_height)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, yscrollcommand=self.scrollbar.set, width=frame_width, height=frame_height)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        #self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.canvas.bind("<Enter>", self.bind_mousewheel)
        self.canvas.bind("<Leave>", self.unbind_mousewheel)

        # Dictionary to store checkbox states
        self.checkbox_states = {}

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.inner_frame_id, width=event.width)

    def bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")

    def add_checkbox(self, text):
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(self.inner_frame, text=text, variable=var)
        checkbox.pack(anchor="w")
        self.checkbox_states[text] = var  # Store the BooleanVar
        # Update scroll region after adding checkbox
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def get_selected_checkboxes(self):
        selected_checkboxes = []
        for text, var in self.checkbox_states.items():
            if var.get():  # If the checkbox is checked
                selected_checkboxes.append(text)
       # print(selected_checkboxes)
        return selected_checkboxes

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scrollable Checkbox Frame")

    frame_width = 200
    frame_height = 100

    scrollable_frame = ScrollableCheckboxFrame(root, frame_width, frame_height)

    for i in range(20):
        scrollable_frame.add_checkbox(f"Checkbox {i+1}")

    btn = tk.Button(root, text="Show Selected", command=scrollable_frame.get_selected_checkboxes)
    btn.pack()

    root.mainloop()
