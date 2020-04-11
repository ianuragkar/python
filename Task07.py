#Select country
country = 'China'
province = 'Hubei'

#How long prediction (in days)
pred = 1

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import datetime

timestring = str(datetime.datetime.now().strftime("%d.%m.%Y, %H:%M:%S"))
df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
headers = list(df.columns.values)

if df[(df['Province/State']==province) & (df['Country/Region']==country)].empty:
    index = df.index[df['Country/Region']==country].values[0]
    prov = ''
else:
    index = df.index[(df['Province/State']==province) & (df['Country/Region']==country)].values[0]
    prov = df.iloc[index, 0]

day = list(range(1,len(list(df.columns.values)[3:])))
inf = list(df.iloc[index,4:])
tot_inf = inf[len(inf)-1]

#Using y = ab^x exponential model
b = []
for i in range(1,len(inf)):
    if (str(inf[i]/inf[i-1]) == 'nan') or (str(inf[i]/inf[i-1]) == 'inf'):
        b.append(0)
    else:
        b.append(inf[i]/inf[i-1])
bmean = np.average(b)

yexp = []
for i in range(1,len(inf)):
    yexp.append(bmean*inf[i-1])

#Prediction
pred0 = inf[len(inf)-1]
day_exp = []
for each in day:
    day_exp.append(each)

for p in range(0,pred):
    day_exp.append((len(day))+p+1)
    day_pred = bmean * pred0
    yexp.append(day_pred)
    pred0 = day_pred

plt.figure(1)
#Scatter plot
plt.scatter(day,inf,label="Real data",color="k")

#Exponential plot
plt.plot(day_exp[1:],yexp, color = [1,0.25,0.25], linewidth = 2.5, label="Exponential model")
plt.title(prov + ' ' + country + ': Cases by time, using approximation model ' + '$x(t) = x_0 * b^t, b_{mean} = $' + str(round(bmean,3)) + ' as of ' + timestring)
plt.legend()
plt.xlabel("Days since 22 January 2020")
plt.ylabel("Total number of infected people")
plt.ylim((0,1.1*yexp[len(yexp)-1]))

total_cases = []
country_list = []
lats = []
lons = []
for index, row in df.iterrows():
    country_list.append(df.iloc[index,1])
    lats.append(df.iloc[index,2].item())
    lons.append(df.iloc[index,3].item())
    total_cases.append(df.iloc[index,len(headers)-1])
max_total = max(total_cases)


plt.figure(2)
max_dot_size = 750
m = Basemap(projection='mill',resolution=None)

for country in range(0,len(country_list)):
    lat = lats[country]
    lon = lons[country]
    x, y = m(lon,lat)
    marker_size = max_dot_size*total_cases[country]/max_total
    color_density = 1 - (total_cases[country]/max_total)
    scat = m.scatter(x,y,marker_size,marker='o',color=[color_density,0,0])
    plt.title('Total cases in the world as of ' + timestring + str(headers[len(headers)-1]))

m.etopo()
plt.show()
