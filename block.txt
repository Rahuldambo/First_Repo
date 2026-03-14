import tkinter as tk

class CircleGrid(tk.Frame):
    def __init__(self, parent, n, m, items):
        super().__init__(parent)
        self.n = n
        self.m = m
        self.items = items  # List of data items
        self.selected_indices = set()
        self.circles = []
        
        self.create_grid()
        
    def create_grid(self):
        for row in range(self.n):
            for col in range(self.m):
                index = row * self.m + col
                if index >= len(self.items):
                    break
                circle = tk.Canvas(self, width=40, height=40, bg='white', highlightthickness=0)
                circle.grid(row=row, column=col, padx=5, pady=5)
                
                # Draw the circle
                circle.create_oval(5, 5, 35, 35, fill='grey', tags="circle")
                
                # Bind click event, pass index with default arg trick
                circle.bind("<Button-1>", lambda e, idx=index: self.toggle_selection(idx))
                
                # Tooltip with item
                self.create_tooltip(circle, self.items[index])
                
                self.circles.append(circle)
                
    def toggle_selection(self, index):
        circle = self.circles[index]
        if index in self.selected_indices:
            self.selected_indices.remove(index)
            circle.itemconfig("circle", fill='grey')
        else:
            self.selected_indices.add(index)
            circle.itemconfig("circle", fill='red')
            
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

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Circle Grid Selection")
    
    n = 4  # rows
    m = 5  # columns
    total = n*m
    
    # Example list of items
    items = [f"Item {i+1}" for i in range(total)]
    
    grid = CircleGrid(root, n, m, items)
    grid.pack(padx=20, pady=20)
    
    root.mainloop()