import tkinter as tk
from curveBezierApp import CurveBezierApp
import logging
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="logs.log",
    )
    root = tk.Tk()
    app = CurveBezierApp(root)
    root.mainloop()
