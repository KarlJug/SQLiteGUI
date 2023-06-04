import tkinter as tk


class ToolTip:
    def __init__(self, widget, tooltip_text="placeholder", bg="white", fg="black"):
        self.widget = widget
        self.tooltip_text = tooltip_text
        self.label_bg = bg
        self.label_fg = fg

        self.tooltip = None

        self.widget.bind("<Enter>", self.on_hover)
        self.widget.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty()

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"+{x}+{y}")

        tooltip_label = tk.Label(self.tooltip, text=self.tooltip_text, bg=self.label_bg, fg=self.label_fg)
        tooltip_label.pack()

    def on_leave(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
