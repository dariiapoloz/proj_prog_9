import tkinter as tk
from tkinter import messagebox

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
            self._check_and_show_winner()

    def _update_label(self):
        if self.logic.winner:
            w_text = "Чорні" if self.logic.winner == 'b' else "Білі"
            self.label.config(text=f"Перемогли {w_text}!", fg="green")
        else:
            turn_text = "Чорні" if self.logic.turn == 'b' else "Білі"
            self.label.config(text=f"Хід: {turn_text}", fg="black")
    def _check_and_show_winner(self):
        #Показує спливаюче вікно, якщо є переможець
        if self.logic.winner:
            winner_text = "Чорні" if self.logic.winner == 'b' else "Білі"
            messagebox.showinfo("Кінець гри", f"Вітаємо! Перемогли {winner_text}!")

    def draw(self):
        self.canvas.delete("all")
        for r in range(8):
            for c in range(8):
                # Малюємо клітинку
                color = "gray" if (r + c) % 2 != 0 else "white"
                if self.logic.selected == (r, c):
                    color = "green"

                x1, y1 = c * self.CELL_SIZE, r * self.CELL_SIZE
                x2, y2 = x1 + self.CELL_SIZE, y1 + self.CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                # Малюємо шашку
                p = self.logic.board[r][c]
                if p:
                    p_color = "black" if p.lower() == 'b' else "white"
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=p_color)
                    if p.isupper():  # Дамка
                        self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="#FFD700", width=4) 
