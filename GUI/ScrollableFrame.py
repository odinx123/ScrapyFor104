import tkinter as tk
from tkinter import ttk

class ScrollableFrame:
    def __init__(self, parent_frame, data_list, *args, **kwargs):
        self.parent_frame = parent_frame
        self.canvas = tk.Canvas(parent_frame)
        self.scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind the mouse wheel to the canvas for scrolling
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        # Display the data list on the scrollable frame
        self.display_data(data_list)

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def display_data(self, data_list):
        for item in data_list:
            ttk.Label(self.scrollable_frame, text=item).pack()

def main():
    root = tk.Tk()
    root.title("Scrollable Frame with Data Example")

    # Create a parent frame
    parent_frame = ttk.Frame(root)
    parent_frame.pack(expand=1, fill='both')

    # Sample data list
    data_list = [f"Sample data item {i}" for i in range(50)]

    # Create an instance of ScrollableFrame with the data list
    scrollable_frame_instance = ScrollableFrame(parent_frame, data_list)

    root.mainloop()

if __name__ == "__main__":
    main()
