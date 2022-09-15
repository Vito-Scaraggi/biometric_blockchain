from tkinter import BOTH, Text, NS, EW
from tkinter.ttk import LabelFrame, Scrollbar

from gui.slider_frame import slider_frame

class block_frame(slider_frame):
    
    '''Builds blocks explorer view'''

    def __init__(self, root, iterable : list) -> None:
        super(block_frame, self).__init__(root, iterable)

    def grid_configure(self) -> None:
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=7)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=6)
        self.rowconfigure(2, weight=1)

    def show(self) -> None:

        info = self.iterable[self.counter].get_info(self.counter+1)
        lb1 = LabelFrame(master = self, text = "Info")
        general  = Text(master = lb1, height=5, width = 40)
        general.insert(1.0, info)
        general.configure(state = "disabled")
        general.pack(fill=BOTH, expand=1)

        logs = self.iterable[self.counter].get_logs()
        lb2 = LabelFrame(master = self, text = "Logs")
        history  = Text(master = lb2, height=20, width = 40)
        history.insert(1.0, logs)
        history.configure(state = "disabled")
        history.grid(row=0, column=0, sticky=EW)#,fill=BOTH, expand=1)

        scrollbar_1 = Scrollbar(
            lb2,
            orient='vertical',
            command=history.yview
        )
        scrollbar_1.grid(row=0, column=1, sticky = NS)
        history['yscrollcommand'] = scrollbar_1.set

        json = self.iterable[self.counter].raw_block
        lb3 = LabelFrame(master = self, text = "JSON block")
        block  = Text(master = lb3, height=35, width = 80, font=("Helvetica", 9))
        block.insert(1.0, json)
        block.configure(state = "disabled")
        block.grid(row=0, column=0, sticky=EW)#fill=BOTH, expand=1)
        
        scrollbar_2 = Scrollbar(
            lb3,
            orient='vertical',
            command=block.yview
        )

        scrollbar_2.grid(row=0, column=1, sticky = NS)
        block['yscrollcommand'] = scrollbar_2.set

        lb1.grid(row = 0, column = 0, sticky=NS)
        lb2.grid(row = 1, column = 0, sticky=NS)
        lb3.grid(row = 0, column = 1, rowspan=2, sticky=NS)