from tkinter import BOTH, TOP, ttk, Tk, Text, Frame
from turtle import width

from core.stats.report import report
from gui.plot_frame import plot_frame
from gui.slider_frame import slider_frame
from gui.block_frame import block_frame

class Gui(Tk):
    
    '''Builds tab group view'''

    def __init__(self, report : report):
        super(Gui, self).__init__()
        width = 960
        height =  576
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight() # Height of the screen
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.resizable(0,0)
        self.title("Blockchain Simulator ver. 1.0")
        self.report = report
        self.build()
        self.mainloop()

    def build(self) ->None:
        self.tabControl = ttk.Notebook(self)
        self.info_tab()
        self.user_tab()
        self.block_tab()
        self.histo_tab()
        self.tabControl.pack(expand = 1, fill ="both")

    def info_tab(self) ->None:
        info = self.report.get_info()
        tab = Frame(self.tabControl)
        self.tabControl.add(tab, text ='General')
        t  = Text(master = tab)
        t.insert(1.0, info)
        t.configure(state = "disabled")
        t.pack(fill=BOTH, side = TOP, expand=1)

    def user_tab(self) ->None:
        users  = self.report.user_pool.users
        tab = slider_frame(self.tabControl, users)
        tab.build()
        self.tabControl.add(tab, text ='Users')

    def block_tab(self) ->None:
        blocks = self.report.stats_f.block_stats
        tab = block_frame(self.tabControl, blocks)
        tab.build(2)
        self.tabControl.add(tab, text ='Blocks')

    def histo_tab(self) ->None:
        stats = self.report.stats
        tab = plot_frame(self.tabControl, stats)
        self.tabControl.add(tab, text ='Stats')