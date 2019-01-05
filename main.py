from tkinter import *
from tkinter import ttk

import numpy as np
import pandas as pd

import matplotlib.backends.backend_tkagg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TKAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style

#import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from statsmodels.tsa.stattools import coint, adfuller


from pipermodules import fetch_data, zscore, ticker_list

def run_pairs():
    
    symbol_list = [droplist1.get(), droplist2.get()]
        
    price = fetch_data(symbol_list, 'closing_price', start_date.get(), end_date.get())

    S1 = price[symbol_list[0]]
    S2 = price[symbol_list[1]]
    
    S1 = sm.add_constant(S1)
    results = sm.OLS(S2, S1).fit()
    S1 = S1[symbol_list[0]]
    b = results.params[symbol_list[0]]
    spread = S2 - b * S1
    
    S2 = sm.add_constant(S2)
    results = sm.OLS(S1, S2).fit()
    S2 = S2[symbol_list[1]]
    b = results.params[symbol_list[1]]
    spread_rev = S1 - b * S2
      
    zscore1 = zscore(spread)
    zscore1.plot(figsize=(16, 3))
    zscore2 = zscore(spread_rev)
    zscore2.plot(figsize=(16,3))
    
    plt.axhline(0.0, color='black')
    plt.axhline(1.0, color='red', linestyle='--')
    plt.axhline(-1.0, color='green', linestyle='--')
    plt.legend(['Spread ' + symbol_list[1], 'Spread ' + symbol_list[0]], bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=1, mode="expand", borderaxespad=0.);
   
    f = Figure(figsize=(16, 3), dpi=100)        
    canvas = FigureCanvasTKAgg(f, self)
    canvas.show()
    canvas.get_tk_widget().pack()
    
#Färgsättningsvariabler
header_color = '#31496b'
body_color = '#3d5c87'
font_color = 'white'

# Definiera huvudfönstret
mainWindow = Tk()
mainWindow.title('Pair Piper v.0.0.2')
mainWindow.iconbitmap('Graphics\Trader.ico')
mainWindow.configure(background=body_color)

# Definiera frames för olika innehåll
topFrame = Frame(mainWindow, background=header_color)
bottomFrame = Frame(mainWindow)

# Definiera widgets
label_1 = Label(topFrame, text='Start Date', fg=font_color, background=header_color)
label_2 = Label(topFrame, text='End Date', fg=font_color, background=header_color)
label_3 = Label(topFrame, text='Ticker 1', fg=font_color, background=header_color)
label_4 = Label(topFrame, text='Ticker 2', fg=font_color, background=header_color)
start_date = Entry(topFrame)
end_date = Entry(topFrame)
droplist1 = ttk.Combobox(topFrame, values=ticker_list)
droplist2 = ttk.Combobox(topFrame, values=ticker_list)
refresh = Button(topFrame, text='Refresh', command=run_pairs)

# Placera ut frames
bottomFrame.grid(row=1)
topFrame.grid(row=0, pady=10)

# Placera ut widgets
label_1.grid(row=0, column=0, padx=5, pady=8)
label_2.grid(row=0, column=1, padx=5, pady=8)
label_3.grid(row=0, column=2, padx=5, pady=8)
label_4.grid(row=0, column=3, padx=5, pady=8)
start_date.grid(row=1, column=0, padx=5, pady=8)
end_date.grid(row=1, column=1, padx=5, pady=8)
droplist1.grid(row=1, column=2, padx=5, pady=8)
droplist2.grid(row=1, column=3, padx=5, pady=8)
refresh.grid(row=1, column=4, padx=5, pady=8)

mainWindow.mainloop()