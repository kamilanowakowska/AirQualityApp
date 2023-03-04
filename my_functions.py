import pandas as pd
from DB_mapping import engine
from geopy.geocoders import Nominatim
from geopy.distance import distance

# połączenie SQLAlchemy 
cnx = engine.connect()

# wywołanie wyników dla konkretnej stacji pomiarowej
def sensor_results(sensor_id):
    df = pd.read_sql_table('pomiary', cnx)
    df['sensor_id'] = sensor_id
    return df


#średnie wartości w rozpatrywanym okresie
def sensor_results_mean(df):
    mean_df = pd.pivot_table(df, values='value', index=None, columns='key', aggfunc='mean')
    return mean_df

def sensor_results_min(df):
#najmniejsze wartości w rozpatrywanym okresie
    min_df = pd.pivot_table(df, values='value', index=None, columns='key', aggfunc='min')
    return min_df

def sensor_results_max(df):
#największe wartości w rozpatrywanym okresie
    max_df = pd.pivot_table(df, values='value', index=None, columns='key', aggfunc='max')
    return max_df



###########################################################################

#lokalizowanie wyszukiwania
def lokalizator(loc):
    geolocator = Nominatim(user_agent="my_request")
    location = geolocator.geocode(loc)
    gegrLat = location.latitude
    gegrLon = location.longitude
    location2 = gegrLat, gegrLon
    return location2

# zwraca listę stacji w podanym promieniu[km] od podanej lokalizacji w lokalizatorze
def najblizsze_stacje(location2, promien):

    df2 = pd.read_sql_table('stacje_pomiarowe', cnx)
    df2 = df2[['gegrLat','gegrLon']]
    dict_of_loc = df2.to_dict('records')
    list_of_loc = []
    bliskie_loc = []

    for item in dict_of_loc:
        one_loc = item['gegrLat'], item['gegrLon']
        list_of_loc.append(one_loc)
    
    for item in list_of_loc:
        km = distance(location2, item)
        if km <= promien:
            bliskie_loc.append(item)

    return bliskie_loc