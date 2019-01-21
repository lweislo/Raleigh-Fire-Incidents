import pandas as pd
import requests
import time
import json
import csv
import Config
import datetime

def weatherout(dframe):

    timestr = time.strftime('%Y%m%d-%H%M%S')
    outfile = './output/weather_' + timestr + '.csv'
    try:
        dframe.to_csv(outfile, index=False, header=True)
        print(f'Your weather data is now available in {outfile}')
    except:
        print(f"Problem outputting dataframe:.")

def wwrite(weather_data):
    # Create lists to accept parsed json data
    wdate = []
    maxtempF = []
    mintempF = []
    hum = []
    precip = []
    w_type = []
    # Parse the json data
    print(f'Getting data for {len(weather_data)} records...')
    for item in weather_data:
        try:
            wdate.append(item['data']['weather'][0]['date'])
            maxtempF.append(item['data']['weather'][0]['maxtempF'])
            mintempF.append(item['data']['weather'][0]['mintempF'])
            hum.append(item['data']['weather'][0]['hourly'][0]['humidity'])
            precip.append(item['data']['weather'][0]['hourly'][0]['precipMM'])
            w_type.append(item['data']['weather'][0]['hourly'][0]['weatherDesc'][0]['value'])
        except KeyError:
            wdate.append('')
            maxtempF.append('')
            mintempF.append('')
            hum.append('')
            precip.append('')
            w_type.append('')

    clean_weather = pd.DataFrame({'Date': wdate, 'Max Temp (f)': maxtempF, 'Min Temp (f)': mintempF, 'Humidity': hum, 'Precipitation': precip, 'Weather Conditions': w_type,})
    weatherout(clean_weather)


def wwapi(final_dates):
    weather_data = []
    for day in final_dates:
        date = day
        try:
            # print(f'Getting weather for {date}')
            url =  "https://api.worldweatheronline.com/premium/v1/past-weather.ashx?"
            key = Config.w_key   # Check ConfigEnv.py
            city = "Raleigh"
            f= "json" #sets format to json
            tp = "24" #pull daily average
            query_url = f"{url}key={key}&q={city}&format={f}&date={date}&includelocation=yes&tp={tp}"
            weather_data.append(requests.get(query_url).json())
        except:
            pass
    wwrite(weather_data)

def getdates(base, numdays):
    # numdays = 5 #this is for testing
    base = datetime.datetime.strptime(base, '%Y-%m-%d').date()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
    final_dates = []

    for date in date_list:
        final_dates.append(str(date))
    print(f'Getting {numdays} days of weather data counting back from {base}')
    wwapi(final_dates)
