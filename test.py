import tkinter as tk

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Window")

        # create a list to hold the Entry widgets
        self.entries = []

        # create a label and pack it
        self.label = tk.Label(self.root, text="Enter some text:")
        self.label.pack()

        # create the Entry widgets using a for loop and pack them
        for i in range(5):
            entry = tk.Entry(self.root)
            entry.pack()
            self.entries.append(entry)

        # create a button to submit the Entry values
        self.button = tk.Button(self.root, text="Submit", command=self.submit_entries)
        self.button.pack()

        # start the main event loop
        self.root.mainloop()

    def submit_entries(self):
        # print the value of each Entry widget
        for entry in self.entries:
            print(entry.get())

if __name__ == '__main__':
    main_window = MainWindow()
