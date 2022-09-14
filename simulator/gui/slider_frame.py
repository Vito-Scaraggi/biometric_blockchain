from tkinter import LEFT, Button, Frame, Text, Label
from tkinter import ttk

class slider_frame(Frame):

    '''Builds simple explorer view'''

    def __init__(self, root, iterable : list) -> None:
        super(slider_frame, self).__init__(root)
        self.iterable = iterable
        self.num_item = len(iterable)
    
    def build(self, num_row=1):
        self.grid_configure()
        self.counter = 0
        self.bottom_menu(num_row)
        self.show(0)

    def grid_configure(self):
        self.columnconfigure(0, weight=10)
        self.rowconfigure(0, weight=6)
        self.rowconfigure(1, weight=1)

    def goto(self):
        value = self.spinbox.get()
        if value.isdigit():
            cur = int(value)
            if 0 <= cur < self.num_item:
                self.counter = cur
                self.show(cur)

    def next(self):
        next = min(self.counter+1, self.num_item-1)
        self.spinbox.set(next)
        self.counter = next
        self.show(next)

    def prev(self):
        prev = max(0, self.counter - 1)
        self.spinbox.set(prev)
        self.counter = prev
        self.show(prev)

    def show(self, index):
        info = str(self.iterable[index])
        t  = Text(master = self)
        t.insert(1.0, info)
        t.configure(state = "disabled")
        t.grid(row = 0, column=0, sticky="news")

    def bottom_menu(self, num_row):
        frame = Frame(master = self)
        frame.grid(row = num_row, column = 0, columnspan=2)
        goto = Button(master = frame, text = "Go to", command = self.goto)
        self.spinbox = ttk.Spinbox(master = frame, from_=0, to=self.num_item-1, width=10)
        self.spinbox.set(0)
        total = Label(master = frame, text = "out of {}".format(self.num_item-1))
        prev = Button(master = frame, text = "prev", command = self.prev)
        next = Button(master = frame, text = "next", command = self.next)
        goto.pack(padx=5, pady=5, side = LEFT)
        self.spinbox.pack(padx=5, pady=5, side = LEFT)
        total.pack(padx=5, pady=5, side = LEFT)
        prev.pack(padx=5, pady=5, side = LEFT)
        next.pack(padx=5, pady=5, side = LEFT)