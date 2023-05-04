import tkinter as tk
from tkinter import ttk

def on_select(event):
    item = event.widget.focus()
    values = event.widget.item(item)['values']
    print(values)

root = tk.Tk()

# Create the Treeview widget
columns = ('Name', 'Age', 'Country')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)

# Insert some sample data
data = [('John', 25, 'USA'), ('Emily', 30, 'Canada'), ('Mark', 20, 'UK')]
for i, row in enumerate(data):
    tree.insert('', 'end', iid=i, values=row)

# Bind the on_select function to the TreeviewSelect event
tree.bind('<<TreeviewSelect>>', on_select)

tree.pack(expand=True, fill='both')

root.mainloop()
