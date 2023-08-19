from bs4 import BeautifulSoup
import pandas as pd
import os
import datetime
from datetime import datetime as dt
from datetime import date
import calendar
from sel_weather import sel


# def get_resources_path():
#     current_path = os.getcwd()
#     os.chdir('../..')
#     resources_path = os.getcwd() + '/HTML_files'
#     print(resources_path)
#     os.chdir(current_path)
#     return resources_path


def forecast(file_name):
    files = open(file_name, "r")

    # Reading the file and storing in a variable
    contents = files.read()

    soup = BeautifulSoup(contents, 'html.parser')

    a = soup.findAll('div', class_="date")
    b = soup.findAll('div', class_="high")
    c = soup.findAll('div', class_="low")
    d = soup.findAll('div', class_="map-dropdown-toggle")

    date = []
    max_temp = []
    min_temp = []
    month = str(d[0].text)
    year = d[1].text

    month_to_number = dict(January=1, February=2, March=3, April=4, May=5, June=6, July=7, August=8, September=9,
                           October=10, November=11, December=12)
    month_to_days = dict(January=31, February=29, March=31, April=30, May=31, June=30, July=31, August=31, September=30,
                         October=31, November=30, December=31)

    month_num = [v for k, v in month_to_number.items() if k.lower() in month.lower()]

    for i in range(0, len(a)):
        date.append((int(year), month_num[0], int(a[i].text)))

    for i in range(0, len(b)):
        max_temp.append((int((b[i].text[7:9]))))

    for i in range(0, len(c)):
        min_temp.append((int((c[i].text[7:9]))))

    df = pd.DataFrame(list(zip(date, min_temp, max_temp)), columns=["Date", "Min_Temp", "Max_Temp"])

    start_date = dt(int(year), int(month_num[0]), 1).date()
    res = calendar.monthrange(int(year), int(month_num[0]))
    day = res[1]
    end_date = datetime.datetime(int(year), int(month_num[0]), day)

    count = 0

    for i in range(0, len(df['Date'])):
        if df['Date'][i][2] == start_date.day:
            count = i
            break

    start_date_index = count
    end_date_index = start_date_index + int(day)

    df1 = df.iloc[start_date_index:end_date_index]
    df1.reset_index(inplace=True)

    c = pd.DataFrame(df1['Date'].values.tolist(), columns=['year', 'month', 'day'])
    df1.Date = pd.to_datetime(c)

    return df1[['Date', 'Min_Temp', 'Max_Temp']]


if __name__ == '__main__':

    todays_date = date.today()
    number_to_month = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'july', 8: 'august',
                       9: 'september', 10: 'october', 11: 'november', 12: 'december'}

    for k, v in number_to_month.items():
        if k == todays_date.month:
            month_name = v

    url = "https://www.accuweather.com/en/in/gadag-betigeri/2849071/{0}-weather/2849071".format(month_name)
    sel(url)
    forecast_table = forecast('/forecast.html')
    forecast_table['temp_diff'] = forecast_table['Max_Temp'] - forecast_table['Min_Temp']
    print(forecast_table)
    # get_resources_path()
