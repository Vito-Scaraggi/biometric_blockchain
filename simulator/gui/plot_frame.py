from tkinter import NW, Button, Frame, TOP, BOTH
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from numpy import zeros, arange

class plot_frame(Frame):

    '''Builds plots view'''
    
    def __init__(self, root, stats):
        super(plot_frame, self).__init__(root)
        self.titles = [ "Block mined", "Avg block creation time", "Avg clearing time", 
                        "Avg clearing time (detailed)","Avg PRNG/CRYPTO ratio","Avg cPoW time",
                        "Avg clearing attempts", "Avg cPoW attempts"] 
        
        self.ylabels = ["n°", "seconds", "seconds", "seconds", "times", "seconds", "n°", "n°"]

        self.matrixes = [ [stats.count_block], [stats.avg_cr_time], [stats.avg_tx_time], [stats.avg_tx_p_time, stats.avg_tx_c_time],
                          [stats.avg_p_c_ratio], [stats.avg_cpow_time], [stats.avg_tx_attempts], [stats.avg_cpow_attempts] ]
    
        self.colors = [ 
                    [  [["cornflowerblue"], ], [  ["mediumseagreen", "indianred"],]],
                    [  [["cornflowerblue"], ["orange"],], [["mediumseagreen", "indianred"], ["springgreen", "mistyrose"],]],
                ]
        
        self.legends = [ 
                    [  [[""], ], [  ["fair", "evil"],]],
                    [  [["PRNG time"], ["CRYPTO time"],], [["fair PRNG time", "evil PRNG time"], ["fair CRYPTO time", ""],]],
                ]
        
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 4)
        self.rowconfigure(0)
        self.rowconfigure(1)
        self.rowconfigure(2)

        self.side_menu()
        self.plot_axes()
    
    def side_menu(self):
        
        frame = Frame(master = self)
        self.combo_1 = ttk.Combobox(master = frame, width=25)
        self.combo_1['values'] = self.titles
        self.combo_1['state'] = "readonly"

        self.combo_2 = ttk.Combobox(master = frame, width=15)
        self.combo_2['values'] = [ "fair/evil", "transactions", "both"]
        self.combo_2['state'] = "readonly"
        
        button = Button(master = frame, text = "Plot", command = self.histo)

        self.combo_1.pack(padx=5, pady=5, anchor=NW)
        self.combo_2.pack(padx=5, pady=5, anchor=NW)
        button.pack(padx=5, pady=5)
        frame.grid(row = 0, column = 0, pady=5, padx = 3, sticky="NW")

    def plot_axes(self):
        self.plot_frame = Frame(master = self)
        self.plot_frame.grid(row = 0, column = 1)

    def histo(self):
        
        self.plot_frame.destroy()
        self.plot_axes()

        index = self.combo_1.current()
        mode = self.combo_2.current()

        if index > -1 and mode > -1:
            m = self.matrixes[index]
            dim_1 = len(m) #floor  
            dim_2 = m[0].shape[0] - 1 if mode == 2 else 1 #subcat
            dim_3 = m[0].shape[min(mode,1)] - 1 #subcat len

            arr = zeros([dim_1, dim_2, dim_3])        

            if mode == 0:
                labels = ["fair", "evil"]
                for i, m in enumerate(m):
                    arr[i, 0, :] = m[1:, 0]
            
            if mode == 1:
                labels = ["{} tx".format(i) for i in range(1, dim_3 + 1) ]
                for i, m in enumerate(m):
                    arr[i, 0, :] = m[0, 1:]

            if mode == 2:
                labels = ["{} tx".format(i) for i in range(1, dim_3 + 1) ]
                for i, m in enumerate(m):
                    arr[i, :, :] = m[1:, 1:]

            if self.ylabels[index] == "n°":
                arr = arr.astype(int)

            
            fig = Figure(figsize = (7, 5), dpi = 100)
            canvas = FigureCanvasTkAgg(fig, self.plot_frame)
            toolbar = NavigationToolbar2Tk( canvas, self.plot_frame)
            plot = fig.add_subplot()
            
            prec = zeros([dim_2, dim_3])
            
            for i in range(dim_1):
                for j in range(dim_2):
                    data = arr[i][j]
                    X = arange(dim_3)
                    plot.bar(X + j/4, data, bottom = prec[j], color= self.colors[dim_1-1][dim_2-1][i][j], 
                                    label = self.legends[dim_1-1][dim_2-1][i][j], width = 0.25)
                    plot.set_xticks(X+j/4, minor=False)
                    plot.set_xticklabels(labels, fontdict=None, minor=False)
                    
                    for k, v in enumerate(data):
                        plot.text(X[k]+j/4, v/2 + prec[j][k], v, ha = 'center', fontsize="x-small",
                                bbox = dict(facecolor = 'beige', edgecolor  ="yellow", pad=0.5))
                    
                    prec[j] = data

            plot.set_title(self.titles[index])
            plot.set_ylabel(self.ylabels[index])
            
            if dim_1 - 1 or dim_2 - 1:
                plot.legend(bbox_to_anchor=(0, 0.5, 1, 0.5), loc='best', fontsize = "x-small")
            
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)