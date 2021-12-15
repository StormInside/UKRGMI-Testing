import requests
import sqlite3
from datetime import datetime

cities = {
        'Kiev': [50.389259, 30.417332],
        'Zhitomir': [50.259169, 28.686406], 
        'Vinnitsa': [49.230266, 28.496265], 
        'Rivne': [50.624746, 26.263355], 
        'Kharkiv': [49.968944, 36.270284], 
        }

api_key = '563da9b3538f9c911a3e0076d5ef18ae'

database_name = 'sqlite_python.db'
connection = sqlite3.connect(database_name)
cursor = connection.cursor()


def connect_to_sqlite():
    for city in cities:
        try:
            cursor.execute(f'SELECT * FROM {city};')
            # print(f'{city} exist')

        except sqlite3.OperationalError as error:
            cursor.execute(f'''CREATE TABLE {city} (
                                w_date DATE,
                                w_temp REAL,
                                pcp REAL,
                                clouds INTEGER,
                                pressure INTEGER,
                                humidity INTEGER,
                                wind_speed REAL);''')

        except sqlite3.Error as error:
            print("Error connecting to sqlite", error)


def get_weather_data():
    for city in cities:
        lat = cities[city][0]
        lon = cities[city][1]

        res = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=current,minutely,hourly,alerts&appid={api_key}')
        res = res.json()['daily']

        for day in range(0,7):
            day_res = res[day]
            date = datetime.fromtimestamp(day_res['dt']).date()
            temp = day_res['temp']['day']

            try:
                pcp = day_res['rain']
            except KeyError:
                pcp = 0

            clouds = day_res['clouds']
            pressure = day_res['pressure']
            humidity = day_res['humidity']
            wind_speed = day_res['wind_speed']

            cursor.execute(f"INSERT INTO {city} VALUES ('{date}', {temp}, {pcp}, {clouds}, {pressure}, {humidity}, {wind_speed});")


def drop_tables():
    for city in cities:
        cursor.execute(f'DROP TABLE {city};')

# drop_tables()

connect_to_sqlite()
get_weather_data()

connection.commit()

cursor.close()