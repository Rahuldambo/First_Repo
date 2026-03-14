import tkinter as tk
from tkinter import ttk

class CircleGrid(tk.Frame):
    def __init__(self, parent, n, m, items):
        super().__init__(parent)
        self.n = n
        self.m = m
        self.items = items
        self.selected_indices = set()
        self.circles = []

        self.create_grid_circle()

    def create_grid_circle(self):
        for row in range(self.n):
            for col in range(self.m):
                index = row * self.m + col
                if index >= len(self.items):
                    break

                circle = tk.Canvas(self, width=40, height=40, bg='white', highlightthickness=0)
                circle.grid(row=row, column=col, padx=5, pady=5)

                circle.create_oval(5, 5, 35, 35, fill='grey', tags="circle")

                circle.bind("<Button-1>", lambda e, idx=index: self.toggle_select(idx))

                self.create_tooltip(circle, self.items[index])

                self.circles.append(circle)

    def toggle_select(self, index):
        circle = self.circles[index]

        if index in self.selected_indices:
            self.selected_indices.remove(index)
            circle.itemconfig("circle", fill='grey')
        else:
            self.selected_indices.add(index)
            circle.itemconfig("circle", fill='red')

    def highlight_from_list(self, index):
        self.toggle_select(index)

    def create_tooltip(self, widget, text):
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.overrideredirect(True)

        label = tk.Label(tooltip, text=text, bg='yellow', relief='solid', borderwidth=1, font=("Arial", 10))
        label.pack()

        def enter(event):
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + 20
            tooltip.geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def leave(event):
            tooltip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Circle Grid Selection")

        n = 4
        m = 5
        total = n * m

        items = [f"Item {i+1}" for i in range(total)]

        main_frame = tk.Frame(self)
        main_frame.pack(padx=20, pady=20)

        # Create Circle Grid
        self.grid_widget = CircleGrid(main_frame, n, m, items)
        self.grid_widget.grid(row=0, column=1, padx=20)

        # Create Treeview
        self.tree = ttk.Treeview(main_frame, columns=("Number",), show="headings", height=10)
        self.tree.heading("Number", text="Circle Number")
        self.tree.grid(row=0, column=0)

        for i in range(total):
            self.tree.insert("", "end", iid=i, values=(i+1,))

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            index = int(selected[0])
            self.grid_widget.highlight_from_list(index)


if __name__ == "__main__":
    app = App()
    app.mainloop()