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


from pipermodules import fetch_data, zscore

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
    
ticker_list = [
    'ABB',
    'ALFA',
    'ALIV-SDB',
    'ASSA-B',
    'ATCO-A',
    'ATCO-B',
    'AXFO',
    'BOL',
    'DAX',
    'ELUX-A',
    'ELUX-B',
    'EURSEK',
    'GLD',
    'HOLM-B',
    'HUSQ-B',
    'ICA',
    'NCC-B',
    'NDA-SEK',
    'NIBE-B',
    'OMX',
    'PEAB-B',
    'SAAB-B',
    'SAND',
    'SCA-B',
    'SEB-A',
    'SECU-B',
    'SHB-A',
    'SKA-B',
    'SKF-A',
    'SKF-B',
    'SLV',
    'SP500',
    'SSAB-A',
    'SSAB-B',
    'STE-R',
    'SWED-A',
    'TEL2-B',
    'TELIA',
    'TREL-B',
    'USDSEK',
    'VIX',
    'VOLV-A',
    'VOLV-B'
]

#Färgsättningsvariabler
header_color = '#31496b'
body_color = '#3d5c87'
font_color = 'white'

mainWindow = Tk()
mainWindow.title('Pair Piper v.0.0.1')

w = 1200 # mainWindow width
h = 600 # mainWindow height

# get screen width and height
ws = mainWindow.winfo_screenwidth() # width of the screen
hs = mainWindow.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the mainWindow
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen and where it is placed
mainWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
mainWindow.configure(background='#31496b')

# Skapa frames för olika innehåll
topFrame = Frame(mainWindow, background=header_color)
topFrame.grid(row=0)
bottomFrame = Frame(mainWindow)
bottomFrame.grid(row=1)

label_1 = Label(topFrame, text='Start Date', fg=font_color, background=header_color)
label_2 = Label(topFrame, text='End Date', fg=font_color, background=header_color)
start_date = Entry(topFrame)
end_date = Entry(topFrame)

label_1.grid(row=0, column=0, sticky=W)
label_2.grid(row=0, column=1, sticky=E)
start_date.grid(row=1, column=0, sticky=W)
end_date.grid(row=1, column=1, sticky=E)


droplist1 = ttk.Combobox(topFrame, values=ticker_list)
droplist2 = ttk.Combobox(topFrame, values=ticker_list)
droplist1.grid(row=2, column=0)
droplist2.grid(row=2, column=1)

refresh = Button(topFrame, text='Refresh', command=run_pairs)
refresh.grid(columnspan=2)

mainWindow.mainloop()