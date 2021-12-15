import requests
import random
from tabulate import tabulate
from datetime import datetime, time, timedelta
import time

params = ['temp', 'pcp', 'clouds', 'pressure', 'humidity', 'wind_speed']

host = 'http://localhost'
port = 5000


def get_random_params():
    param = random.choice(params)
    city = random.choice(cities)

    return param, city


def main_requests():
    average = requests.get(f'{host}:{port}/mean?value_type={r_value}&city={r_city}').json()
    print(f'\nAverage "{r_value}" for {r_city} is {average[0]}')

    date = datetime.now().date()
    records = requests.get(f'{host}:{port}/records?city={r_city}&start_dt={date}&end_dt={date+timedelta(days=2)}').json()
    print(f'\nToday and next 2 days weather in {r_city} will be:')
    print(tabulate(records, headers='keys', tablefmt='fancy_grid'))

    moving_average = requests.get(f'{host}:{port}/moving_mean?city={r_city}&value_type={r_value}').json()
    print(f'\nMoving_average of "{r_value}" in {r_city} is:')
    print(moving_average)

    broken_request = requests.get(f'{host}:{port}/moving_mean?city=NoCity&value_type=NoValue')
    print(f'\nIf wrong parameters it will be {broken_request.status_code} status code with description:')
    print(broken_request.json()['error'])


cities = requests.get(f'{host}:{port}/cities').json()
print('\nCities:')
print(cities)

r_value, r_city = get_random_params()
main_requests()

time.sleep(1)

r_value, r_city = get_random_params()
main_requests()

