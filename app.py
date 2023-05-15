
from DB_mapping import engine
from tkinter import *
import pandas as pd
from my_functions import *
import tkinter as tk 
from tkinter import ttk 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from my_functions import *
import matplotlib.pyplot as plt
from tkcalendar import DateEntry

  
# Creating tkinter window and set dimensions
window = tk.Tk() 
window.title('AirQualityApp') 
window.geometry('1800x1250')

bg = PhotoImage(file = "airquality.png")
label1 = Label( window, image = bg)
label1.place(x = 0,y = 0)

cnx = engine.connect()
df0 = pd.read_sql_table('stacje_pomiarowe', cnx)
loc_listdf1 = df0['stationName'].unique().tolist()
loc_listdf1.sort()

def callbackFunc(event):
    chosen_station = event.widget.get() #pobierz dane z przycisku wybierz
    df2 = df0[['station', 'stationName']]
    df2 = df2[df2['stationName'] == chosen_station]
    station_id = df2['station'].unique() #zamień nazwę stacji na id
    station_id = station_id[0]
    diagram(station_id)
    
 
     

# Set label 
ttk.Label(window, text = "Wybierz stację pomiarową").grid(column = 1, 
          row = 5, sticky = W, pady = 2)

  
# Create Combobox
n = tk.StringVar() 
select_station = ttk.Combobox(window, width = 27, textvariable = n) 


  
# Adding combobox drop down list 
select_station['values'] = loc_listdf1
  
select_station.grid(column = 2, row = 5, sticky = W, pady = 10, columnspan = 2, padx = 5) 
select_station.current()
select_station.bind("<<ComboboxSelected>>", callbackFunc)

 
# search for the nearest

search_label = Label(window, text="Znajdź najbliższe stacje")   # wprowadza napis do okna
search_label.grid(column=1, row=3, sticky = W, pady = 30)    # zdefiniowanie gdzie ten napis ma sie znajdować

place = Entry(window,width=50)   # wycięcie do wpisania swojego imienia
place.grid(column=2, row=3, sticky = W, pady = 2, columnspan=2)    # zdefiniowanie gdzie te wcięcie ma się znajdować

km_label = Label(window, text="+km", width=10)   # wprowadza napis do okna
km_label.grid(column=3, row=3, sticky = E, pady = 2)    # zdefiniowanie gdzie ten napis ma sie znajdować

km = Entry(window,width=10)   # wycięcie do wpisania swojego imienia
km.grid(column=4, row=3, sticky = W, pady = 2)    # zdefiniowanie gdzie te wcięcie ma się znajdować

txt_output = Text(window, height=50, width=50)
txt_output.grid(column=0, row = 11, sticky = W, pady = 2, rowspan = 4)



def clicked():              # definiuje funkcję
    address = place.get()   # to co pwisaliśmy imie tu się wyświetla
    km2 = int(km.get())
    locations = lokalizator(address, km2)
    for item in locations:
        txt_output.insert(END, item + "\n")

przycisk = Button(window, text="Szukaj", command=clicked)
# naciśnij przycisk a uruchomi się funkcja
przycisk.grid(column=7, row=3, padx = 10) # położenie przycisku

#time pickers

cal_label = Label(window, text="Wybierz datę początkową i końcową")   # wprowadza napis do okna
cal_label.grid(column=1, row=8, sticky = W, pady = 30)    # zdefiniowanie gdzie ten napis ma sie znajdować

cal1=DateEntry(window,selectmode='day')
cal1.grid(row=8,column=2,padx=15)

cal2=DateEntry(window,selectmode='day')
cal2.grid(row=8,column=3,padx=15)

#odświeżanie danych

def refresh():              # definiuje funkcję
    return db_insert()
    

refresh_click = Button(window, text="Odśwież dane", command=refresh)
# naciśnij przycisk a uruchomi się funkcja
refresh_click.grid(column=9, row=3, padx=20) # położenie przycisku

#statistics textboxes
txt_mean = Text(window, height=10, width=50)
txt_mean.grid(column=10, row = 11, sticky = W, pady = 2)
txt_mean.insert(tk.END, "Średnie wartości:")

txt_min = Text(window, height=10, width=50)
txt_min.grid(column=10, row = 12, sticky = W, pady = 2)
txt_min.insert(tk.END, "Najmniejsze wartości:")

txt_max = Text(window, height=10, width=50)
txt_max.grid(column=10, row = 13, sticky = W, pady = 2)
txt_max.insert(tk.END, "Największe wartości:")

window.mainloop()
