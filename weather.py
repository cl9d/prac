#!/usr/bin/env python

import sys
import os
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime

arg = sys.argv[1:]

def Main():
    if not arg or arg[0].startswith('-'):
        print(f"Please enter a valid city")
        return
    if '--h' in arg:
        print(f"usage: weather [city] \noptional arguments: \n\t--h : returns this help message \n\t-c : current weather \n\t-d : 7 day weather forecast \n\t-h : 24 hour forecast")
        return
    if len(arg) > 2:
        print("Please choose one forecast timeframe : -c, -h, or -d")
        
    session = Session()
    try:
        response = session.get(f"https://geocode.xyz/{arg[0]}?json=1", verify=True)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    lng = json.loads(response.text)['longt']
    lat = json.loads(response.text)['latt']
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}"
    url += "&windspeed_unit=ms&timezone=Europe%2FBerlin"
    
    if '-h' in arg:
        url += "&hourly=temperature_2m,relativehumidity_2m,precipitation,cloudcover"
    if '-d' in arg:
        url += "&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,precipitation_hours"
    if '-c' in arg:
        url += "&current_weather=true"
    try:
        response = session.get(url, verify=True)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    finally:
        output(response)

def output(response):   
    if '-h' in arg:
        hourlyTemp = []
        hourlyHum = []
        hourlyPrc = []
        hourlyCld = []
        times = []
        for x in range(24):
            hourlyTemp.append(json.loads(response.text)['hourly']['temperature_2m'][x])
            hourlyHum.append(json.loads(response.text)['hourly']['relativehumidity_2m'][x])
            hourlyPrc.append(json.loads(response.text)['hourly']['precipitation'][x])
            hourlyCld.append(json.loads(response.text)['hourly']['cloudcover'][x])
            times.append(json.loads(response.text)['hourly']['time'][x])
        print("TIME  |  TEMPERATURE\tHUMIDITY\tPRECIPITATION\tCLOUD COVERAGE")
        for x in range(24):
            print(f"{times[x][11:]} | {str(hourlyTemp[x]).rjust(5)} °C\t{hourlyHum[x]}%\t\t{str(hourlyPrc[x]).rjust(5)} mm\t{hourlyCld[x]}%")
            
    if '-d' in arg:
        dailyTempMin = []
        dailyTempMax = []
        dailySunrise = []
        dailySunset = []
        hourlyHum = []
        dailyPrc = []
        dailyPrcH = []
        times = []
        for x in range(7):
            dailyTempMin.append(json.loads(response.text)['daily']['temperature_2m_min'][x])
            dailyTempMax.append(json.loads(response.text)['daily']['temperature_2m_max'][x])
            dailySunrise.append(json.loads(response.text)['daily']['sunrise'][x])
            dailySunset.append(json.loads(response.text)['daily']['sunset'][x])
            dailyPrc.append(json.loads(response.text)['daily']['precipitation_sum'][x])
            dailyPrcH.append(json.loads(response.text)['daily']['precipitation_hours'][x])
            times.append(json.loads(response.text)['daily']['time'][x])
        for x in range(7):
            print(f"{times[x]} | {str(round(dailyTempMin[x])).rjust(2)} - {str(round(dailyTempMax[x])).ljust(2)} °C | sunrise {dailySunrise[x][11:]} | sunset {dailySunset[x][11:]} | {dailyPrc[x]} mm in {dailyPrcH[x]} hours")
            
    if '-c' in arg:
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        temp = json.loads(response.text)['current_weather']['temperature']
        speed = json.loads(response.text)['current_weather']['windspeed']
        direction = json.loads(response.text)['current_weather']['winddirection']
        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        ix = round(direction / (360. / len(dirs)))
        dir = dirs[ix % len(dirs)]
        print(f"{time} | {temp} °C | {speed} m/s {dir} wind")
    
    
    
Main()