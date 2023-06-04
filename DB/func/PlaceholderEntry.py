import tkinter as tk

class PlaceholderEntry(tk.Entry):
    """PlaceholderEntry widget which will detect if entry is selected or not"""
    def __init__(self, master=None, placeholder="placeholder text", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)
        self.insert_placeholder()


    def focus_in(self, event):
        """
        If entry is selected and has the same value as @self.placeholder it will delete @self.placeholder and sets
        the color as black
        """
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(fg="black")

    def focus_out(self, event):
        """If the entry is emtpy it will do @self.insert_placeholder()"""
        if self.get() == "":
            self.insert_placeholder()

    def insert_placeholder(self):
        """Sets the entry text as @self.placeholder and color as gray"""
        self.insert(0, self.placeholder)
        self.config(fg="gray")