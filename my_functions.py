import pandas as pd
from DB_mapping import engine
from geopy.geocoders import Nominatim
from geopy.distance import distance
import folium
import matplotlib.pyplot as plt

# połączenie SQLAlchemy 
cnx = engine.connect()

# wywołanie wyników dla konkretnej stacji pomiarowej

#średnie wartości w rozpatrywanym okresie
def sensor_results_mean(station_id):

    df1 = pd.read_sql_table('stanowiska_pomiarowe', cnx)
    df2 = pd.read_sql_table('pomiary', cnx)

    df = df1.merge(df2, left_on='id', right_on='sensor_id')
    df = df[df['station_id'] == station_id]

    mean_df = pd.pivot_table(df, values='value', index=None, columns='key', aggfunc='mean')
    return mean_df



#najmniejsze wartości w rozpatrywanym okresie
def sensor_results_min(station_id):

    df1 = pd.read_sql_table('stanowiska_pomiarowe', cnx)
    df2 = pd.read_sql_table('pomiary', cnx)

    df = df1.merge(df2, left_on='id', right_on='sensor_id')
    df = df[df['station_id'] == station_id]

    min_df = pd.pivot_table(df, values='value', index=None, columns='key', aggfunc='min')
    return min_df

#największe wartości w rozpatrywanym okresie
def sensor_results_max(station_id):

    df1 = pd.read_sql_table('stanowiska_pomiarowe', cnx)
    df2 = pd.read_sql_table('pomiary', cnx)

    df = df1.merge(df2, left_on='id', right_on='sensor_id')
    df = df[df['station_id'] == station_id]

    max_df = pd.pivot_table(df, values='value', index=None, columns='key', aggfunc='max')
    return max_df



###########################################################################

#lokalizowanie wyszukiwania
def lokalizator(loc, promien):

    geolocator = Nominatim(user_agent="my_request")
    location = geolocator.geocode(loc)
    location2 = location.latitude, location.longitude

# zwraca listę stacji(gegrLat, gegrLon, stationName) w podanym promieniu[km] od podanej lokalizacji w lokalizatorze

    df2 = pd.read_sql_table('stacje_pomiarowe', cnx)
    df2 = df2[['gegrLat','gegrLon','stationName']]
    dict_of_loc = df2.to_dict('records')
    list_of_loc = []
    bliskie_loc = []

    for item in dict_of_loc:
        one_loc = item['gegrLat'], item['gegrLon'], item['stationName']
        list_of_loc.append(one_loc)
    
    for item in list_of_loc:
        item2 = item[0], item[1]
        km = distance(location2, item2)
        if km <= promien:
            bliskie_loc.append(item)

   
    m = folium.Map(location=location2, width=800, height=400)
    folium.Marker(location2, popup="Twój adres").add_to(m)
    for item in bliskie_loc:
        locationx = item[0], item[1]
        folium.Marker(locationx, popup=item[2]).add_to(m)
    # wyświetla punkty na mapie
        
    return m


##############################################################################

#wykres z pomiarami dla danej stacji

def diagram(station_id):

    cnx = engine.connect()
    df1 = pd.read_sql_table('stanowiska_pomiarowe', cnx)
    df2 = pd.read_sql_table('pomiary', cnx)

    df = df1.merge(df2, left_on='id', right_on='sensor_id')
    df = df[df['station_id'] == station_id]


    df = df[['key', 'date', 'value']]
    df = pd.pivot_table(df, values='value', index='date', columns='key')

    df.plot()
    return plt.show()