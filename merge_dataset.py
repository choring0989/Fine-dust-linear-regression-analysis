import pandas as pd
import numpy as np
import random as rd
import warnings
warnings.filterwarnings(action='ignore')

samples = []
date_ = 2010

#load file
for i in range(0, 6):
    file_Name = 'SURFACE_ASOS_108_HR_'+str(date_)+'_'+str(date_)+'_2018.xlsx'
    sample = pd.read_excel(file_Name, encoding='utf-8')
    samples.append(sample[['일시', '강수량(mm)', '풍속(m/s)', '풍향(16방위)', '습도(%)']])
    samples[i]['강수량(mm)'] = samples[i]['강수량(mm)'].fillna(0.0)
    date_ = date_ + 1

#initialization
temp = {'Date': (['NaN' for i in range(2191)]),
        'Rainfall(mm/hour)' : (['NaN' for i in range(2191)]),
        'Rainfall(mm/day)' : (['NaN' for i in range(2191)]),
        'Wind velocity(m/s)': (['NaN' for i in range(2191)]),
        'Wind direction': (['NaN' for i in range(2191)]),
        'Humidity': (['NaN' for i in range(2191)])}

new_data_rain = pd.DataFrame(temp, columns=['Date', 'Rainfall(mm/hour)', 'Rainfall(mm/day)', 'Wind velocity(m/s)', 'Wind direction', 'Humidity'])

temp_mm=0
temp_ms=0
temp_16=0
temp_percent = 0

new_data_rain['Date'] = pd.date_range("20100101", periods=2191)

k=0;

for j in range(0, 6):
    for i in range(len(samples[j])):
        temp_mm = temp_mm + samples[j]['강수량(mm)'].loc[i]
        temp_ms = temp_ms + samples[j]['풍속(m/s)'].loc[i]
        ttemp = samples[j]['풍향(16방위)'].loc[i]
        if(ttemp == 0): samples[j]['풍향(16방위)'].loc[i] = 360
        temp_16 = temp_16 + samples[j]['풍향(16방위)'].loc[i]
        temp_percent = temp_percent + samples[j]['습도(%)'].loc[i]
        if ((i != 0) and (i % 23 == 0)):
            new_data_rain['Rainfall(mm/hour)'].loc[k] = temp_mm/24
            new_data_rain['Rainfall(mm/day)'].loc[k] = temp_mm
            new_data_rain['Wind velocity(m/s)'].loc[k] = temp_ms/24
            temp_16to8 = temp_16/24
            if(temp_16to8 <= 22.5 and temp_16to8 > 337.5) :new_data_rain['Wind direction'].loc[k] = "N"
            elif(temp_16to8 <= 67.5 and temp_16to8 > 22.5) :new_data_rain['Wind direction'].loc[k] = "NE"
            elif(temp_16to8 <= 112.5 and temp_16to8 > 67.5) :new_data_rain['Wind direction'].loc[k] = "E"
            elif(temp_16to8 <= 157.5 and temp_16to8 > 112.5) :new_data_rain['Wind direction'].loc[k] = "SE"
            elif(temp_16to8 <= 202.5 and temp_16to8 > 157.5) :new_data_rain['Wind direction'].loc[k] = "S"
            elif(temp_16to8 <= 247.5 and temp_16to8 > 202.5) :new_data_rain['Wind direction'].loc[k] = "SW"
            elif(temp_16to8 <= 292.5 and temp_16to8 > 247.5) :new_data_rain['Wind direction'].loc[k] = "W"
            elif(temp_16to8 <= 337.5 and temp_16to8 > 292.5) :new_data_rain['Wind direction'].loc[k] = "NW"
            new_data_rain['Humidity'].loc[k] = temp_percent/24
            temp_mm=0
            temp_ms=0
            temp_16=0
            temp_percent = 0
            k = k+1

new_data_rain = new_data_rain.dropna()
print(new_data_rain)

new_data_rain.to_csv("Meteorological_merge.csv", mode='w')
