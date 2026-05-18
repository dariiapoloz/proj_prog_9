import tkinter as tk
from logic import CheckersLogic
from gui import CheckersGUI

if __name__ == "__main__":
    root = tk.Tk()
    logic = CheckersLogic()
    app = CheckersGUI(root, logic)
    root.mainloop()