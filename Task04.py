import json
import urllib.request
import csv
import datetime
import math

req = urllib.request.Request("http://api.open-notify.org/iss-now.json")
response = urllib.request.urlopen(req)
obj = json.loads(response.read())

lat = float(obj['iss_position']['latitude'])
lon = float(obj['iss_position']['longitude'])

def dec2dms(dec):       #Convert decimal to Degree, Minute, Second
    D = round(math.floor(abs(dec)) * dec/abs(dec))
    M = round(math.floor(abs(dec - D)*60))
    S = round((abs(dec) - (abs(D)+M/60))*3600,2)
    DMS = str(D) + ' ' + str(M) + ' ' + str(S)
    return DMS

fieldnames = ['Timestamp', 'Time','Latitude','Longitude']
temp_dict = {'Timestamp':obj['timestamp'],
    'Time':str(datetime.datetime.now().strftime("%d.%m.%Y, %H:%M:%S")),
    'Latitude':dec2dms(lat),
    'Longitude':dec2dms(lon)}       #Create a temporary dictionary to write to csv

try:
    print('try')
    with open('ISS_Pos_Logger.csv','a+') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        reader = csv.DictReader(open('ISS_Pos_Logger.csv'))
        if not reader.fieldnames:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            csv_writer.writerow(temp.values())
        else:
            csv_writer.writerow(temp.values())
except FileNotFoundError:       #For some reason, after 2 runs, it creates a file automatically, so try always satisfied
    print("File Not Found. A new file has been created in the active directory: ISS_Pos_Logger.csv")
    with open('ISS_Pos_Logger.csv','w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(temp)
