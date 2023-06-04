import tkinter as tk


class CustomCircle(tk.Canvas):
    def __init__(self, master, size, width=1, custom_mark="?", **kwargs):
        super().__init__(master, width=size, height=size, **kwargs)

        self.custom_mark = custom_mark

        self.radius = size // 2
        self.canvas_width = self.canvas_height = size
        self.master = master
        self.width = width

        # Draw the circle
        self.create_oval(2, 2, self.canvas_width - 2, self.canvas_height - 2, outline='black',
                         width=self.width)  # Adjusted line thickness

        # Draw the question mark inside the circle
        text = self.custom_mark  # The symbol to display
        font = ("Arial", size // 2)  # Font settings
        text_x = self.canvas_width // 2  # x-coordinate of the text (centered horizontally)
        text_y = self.canvas_height // 2  # y-coordinate of the text (centered vertically)
        self.create_text(text_x, text_y, text=text, font=font)
