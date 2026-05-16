import tkinter as tk

class CheckersGUI:
    def __init__(self, root, logic):
        self.root = root
        self.logic = logic
        self.CELL_SIZE = 70

        self.root.title("Шашки")

        self.label = tk.Label(root, text="Хід: Білі", font=("Arial", 16, "bold"))
        self.label.pack()

        self.canvas = tk.Canvas(root, width=8 * self.CELL_SIZE, height=8 * self.CELL_SIZE)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_click)

        self.draw()

    def _on_click(self, event):
        c, r = event.x // self.CELL_SIZE, event.y // self.CELL_SIZE
        if self.logic.handle_click(r, c):
            self.draw()
            self._update_label()

    def _update_label(self):
        turn_text = "Чорні" if self.logic.turn == 'b' else "Білі"
        self.label.config(text=f"Хід: {turn_text}")
