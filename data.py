import requests

res = requests.get("https://api.gios.gov.pl/pjp-api/rest/station/findAll").json()

for station in res:
    res2 = requests.get("https://api.gios.gov.pl/pjp-api/rest/station/sensors/{}".format(station['id'])).json()
    for sensor in res2:

        res3 = requests.get("https://api.gios.gov.pl/pjp-api/rest/data/getData/{}".format(sensor['id'])).json()
        for dana in res3['values']:
            print(sensor['id'], res3['key'], dana['date'], dana['value'])