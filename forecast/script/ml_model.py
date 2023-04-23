from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pandas as pd
from weather_forecast import forecast, get_resources_path
import requests
from datetime import datetime as dt
from datetime import timedelta
import mysql.connector


def my_sql_conn(table, date_, actual_generation, forecast_generation):
    mydb = mysql.connector.connect(
        host="localhost",
        password="*****",
        user="root",
        database="XYZ",
        port="*****"
    )

    print(table, date_, round(actual_generation,3), round(forecast_generation,3))

    my_cursor = mydb.cursor()

    sql = """INSERT INTO {0} (_date, actual_generation,forecast_generation) VALUES('{1}',{2},{3})""".format(table,
                                                                                                            date_,
                                                                                                            round(actual_generation,3),
                                                                                                            round(forecast_generation,3))

    my_cursor.execute(sql)

    mydb.commit()

    return


def api_data(url, plant):
    current_date = (dt.today()).date()
    yesterday = current_date - timedelta(days=1)
    start_date = (dt.today().replace(day=1)).date()
    date_range = [(start_date + timedelta(n)) for n in range(int((current_date - start_date).days) - 1)]

    actual_generation = [['date', 'actual_generation']]

    params = {'date__gte': start_date, 'date__lte': yesterday, 'parameter': 'generation', 'plant': plant}
    header = {'Authorization': 'Token ******'}
    response = requests.get(url, params=params, headers=header)
    data = response.json()
    for i in range(len(data)):
        actual_generation.append([data[i].get('date'), data[i].get('value')])

    return actual_generation


def model(sample, sheet_name):
    Training_Data = pd.read_excel(
        r"C:\Users\Kumar Shubham\PycharmProjects\generation_forecast\Training_dataset\Forecast_Training_Data.xlsx",
        sheet_name=sheet_name)
    Training_Data['date'] = pd.to_datetime(Training_Data['Date'])
    Training_Data['month'] = Training_Data['date'].dt.month
    Training_Data['day'] = Training_Data['date'].dt.day
    Training_Data['year'] = Training_Data['date'].dt.year
    Training_Data['temp squared'] = Training_Data['Temp Difference '].pow(2)

    x_array = Training_Data[['day', 'month', 'temp squared', 'Temp Difference ']]

    y_array = Training_Data['Actual Generation (kWh)']

    x_train, x_test, y_train, y_test = train_test_split(x_array, y_array, test_size=0.05)

    lr_model = LinearRegression()

    y = lr_model.fit(x_train, y_train)

    sample_predict = lr_model.predict(sample[['day', 'month', 'temp squared', 'Temp Difference ']])

    pd.options.mode.chained_assignment = None
    sample['generation_forecast'] = sample_predict

    return sample[['Date', 'day', 'month', 'year', 'generation_forecast']]


if __name__ == '__main__':
    url = "******"

    # Fetching Scrapped Data from weather_forecast.py
    forecast_value = forecast(get_resources_path() + '/forecast.html')
    forecast_value['Temp Difference '] = forecast_value['Max_Temp'] - forecast_value['Min_Temp']
    forecast_value['Date'] = pd.to_datetime(forecast_value['Date'])
    forecast_value['day'] = forecast_value['Date'].dt.day
    forecast_value['month'] = forecast_value['Date'].dt.month
    forecast_value['year'] = forecast_value['Date'].dt.year
    forecast_value['temp squared'] = forecast_value['Temp Difference '].pow(2)

    # Calculating Forecast generation using ML model
    x_test = forecast_value[['Date', 'day', 'month', 'year', 'temp squared', 'Temp Difference ']]
    forecast_data = model(x_test, "XYZ")

    # Calling API function for actual generation
    plant__ = '10127'
    generation = api_data(url, plant__)
    actual_generation = pd.DataFrame(generation[1:], columns=generation[0])

    # Final generation forecast and actual generation table
    final__table = pd.concat([forecast_data, actual_generation], axis=1)
    final_table_data = final__table[['Date', 'generation_forecast', 'actual_generation']]

    # Analysis Table

    Today = dt.now().date()

    actual_generation__sum = final_table_data['actual_generation'].loc[
        final_table_data['Date'] < str(Today)].sum()
    forecast_generation__sum = final_table_data['generation_forecast'].loc[
        final_table_data['Date'] >= str(Today)].sum()

    Estimated_generation_ = actual_generation__sum + forecast_generation__sum

    # Updating in Database

    my_sql_conn("veera_forecast", Today, actual_generation__sum, Estimated_generation_)

