
from DB_mapping import engine
from tkinter import *
import pandas as pd
from my_functions import *
import tkinter as tk 
from tkinter import ttk, messagebox
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

dates1 = []
dates2 = []

def cal1_func(event):
    dates1.clear()
    start_date = event.widget.get()
    dates1.append(start_date)

def cal2_func(event):
    dates2.clear()
    end_date = event.widget.get()
    dates2.append(end_date)
  


def diagram(station_id, start, end):

    cnx = engine.connect()
    df1 = pd.read_sql_table('stanowiska_pomiarowe', cnx)
    df2 = pd.read_sql_table('pomiary', cnx)

    df = df1.merge(df2, left_on='id', right_on='sensor_id')
    df = df[df['station_id'] == station_id]

    df = df[['key', 'date', 'value']]
    df['date']= pd.to_datetime(df['date'])


    df = df.loc[df['date'] >= start]
    df = df.loc[df['date'] <= end ]


    df = pd.pivot_table(df, values='value', index='date', columns='key')

    df.plot()
    
    return plt.show()

#średnie wartości w rozpatrywanym okresie
def sensor_results_mean(station_id, start, end):

    df1 = pd.read_sql_table('stanowiska_pomiarowe', cnx)
    df2 = pd.read_sql_table('pomiary', cnx)

    df2['date']= pd.to_datetime(df2['date'])

    df2 = df2.loc[df2['date'] >= start]
    df2 = df2.loc[df2['date'] <= end ]

    df = df1.merge(df2, left_on='id', right_on='sensor_id')
    df = df[df['station_id'] == station_id]

    mean_df = pd.pivot_table(df, values='value', index=None, columns='key', aggfunc='mean')
    mean_df = mean_df.round(2)

    txt_mean.delete("1.0", "end") 
    txt_mean.insert(tk.END,"\n" + "\t" + "Średnie wartości:" + "\n" + "\n")
    return txt_mean.insert(END, mean_df)



#najmniejsze wartości w rozpatrywanym okresie
def sensor_results_min(station_id, start, end):

    df1 = pd.read_sql_table('stanowiska_pomiarowe', cnx)
    df2 = pd.read_sql_table('pomiary', cnx)

    df2['date']= pd.to_datetime(df2['date'])

    df2 = df2.loc[df2['date'] >= start]
    df2 = df2.loc[df2['date'] <= end ]

    df = df1.merge(df2, left_on='id', right_on='sensor_id')
    df = df[df['station_id'] == station_id]

    min_df = pd.pivot_table(df, values='value', index=None, columns='key', aggfunc='min')
    min_df = min_df.round(2)

    txt_min.delete("1.0", "end") 
    txt_min.insert(tk.END,"\n" + "\t" + "Najmniejsze wartości:" + "\n" + "\n")
    return txt_min.insert(END, min_df)



#największe wartości w rozpatrywanym okresie
def sensor_results_max(station_id, start, end):

    df1 = pd.read_sql_table('stanowiska_pomiarowe', cnx)
    df2 = pd.read_sql_table('pomiary', cnx)

    df2['date']= pd.to_datetime(df2['date'])

    df2 = df2.loc[df2['date'] >= start]
    df2 = df2.loc[df2['date'] <= end ]

    df = df1.merge(df2, left_on='id', right_on='sensor_id')
    df = df[df['station_id'] == station_id]

    max_df = pd.pivot_table(df, values='value', index=None, columns='key', aggfunc='max')
    max_df = max_df.round(2)

    txt_max.delete("1.0", "end") 
    txt_max.insert(tk.END,"\n" + "\t" + "Największe wartości:" + "\n" + "\n")
    return txt_max.insert(END, max_df)

def callbackFunc(event):
    chosen_station = event.widget.get() #pobierz dane z przycisku wybierz
    cnx = engine.connect()
    df0 = pd.read_sql_table('stacje_pomiarowe', cnx)
    df2 = df0[['station', 'stationName']]
    df2 = df2[df2['stationName'] == chosen_station]
    station_id = df2['station'].unique() #zamień nazwę stacji na id
    station_id = station_id[0]
    
    sensor_results_mean(station_id, dates1[0], dates2[0])
    sensor_results_min(station_id, dates1[0], dates2[0])
    sensor_results_max(station_id, dates1[0], dates2[0])
    diagram(station_id, dates1[0], dates2[0])
    
   

     

# Set label 
ttk.Label(window, text = "Wybierz stację pomiarową").grid(column = 1, 
          row = 8, sticky = W, pady = 2)

  
# Create Combobox
n = tk.StringVar() 
select_station = ttk.Combobox(window, width = 27, textvariable = n) 


  
# Adding combobox drop down list 
select_station['values'] = loc_listdf1
  
select_station.grid(column = 2, row = 8, sticky = W, pady = 10, columnspan = 2, padx = 5) 
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



def clicked():   
    try:  
        txt_output.delete("1.0", "end")         # definiuje funkcję
        address = place.get()   # to co pwisaliśmy imie tu się wyświetla
        km2 = int(km.get())
        locations = lokalizator(address, km2)
        for item in locations:
            txt_output.insert(END, item + "\n")
    except:
        tk.messagebox.showerror(title="GeocoderUnavailable", message="Aktualnie pobranie danych nie jest możliwe. Wybierz stację pomiarową z listy.")

przycisk = Button(window, text="Szukaj", command=clicked)
# naciśnij przycisk a uruchomi się funkcja
przycisk.grid(column=7, row=3, padx = 10) # położenie przycisku

#time pickers

cal_label = Label(window, text="Wybierz datę początkową i końcową")   # wprowadza napis do okna
cal_label.grid(column=1, row=5, sticky = W, pady = 30)    # zdefiniowanie gdzie ten napis ma sie znajdować

cal1=DateEntry(window,selectmode='day')
cal1.grid(row=5,column=2,padx=15)
cal1.delete(0, "end")
cal1.bind("<<DateEntrySelected>>", cal1_func)

cal2=DateEntry(window,selectmode='day')
cal2.grid(row=5,column=3,padx=15)
cal2.delete(0, "end")
cal2.bind("<<DateEntrySelected>>", cal2_func)

#odświeżanie danych

def refresh(): 
    try:
        return db_insert()
    except:
        tk.messagebox.showerror(title="Błąd pobierania danych", message="Aktualnie pobranie danych nie jest możliwe. Skorzystaj z danych historycznych.")

    

refresh_click = Button(window, text="Odśwież dane", command=refresh)
# naciśnij przycisk a uruchomi się funkcja
refresh_click.grid(column=9, row=3, padx=20) # położenie przycisku

#statistics textboxes
txt_mean = Text(window, height=8, width=80)
txt_mean.grid(column=8, row = 11, sticky = W, pady = 2)
txt_mean.insert(tk.END,"\n" + "\t" + "Średnie wartości:" + "\n" + "\n")

txt_min = Text(window, height=8, width=80)
txt_min.grid(column=8, row = 12, sticky = W, pady = 2)
txt_min.insert(tk.END, "\n" + "\t" + "Najmniejsze wartości:" + "\n" + "\n")

txt_max = Text(window, height=8, width=80)
txt_max.grid(column=8, row = 13, sticky = W, pady = 2)
txt_max.insert(tk.END, "\n" + "\t" + "Największe wartości:" + "\n" + "\n")

window.mainloop()
