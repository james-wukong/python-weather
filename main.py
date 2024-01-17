import toml
import os
from src.constants import ROOT_DIR
from src.api.weather import Weather

# import json

config = toml.load(os.path.join(ROOT_DIR, 'conf', 'config.toml'))

if __name__ == '__main__':
    # initialize Weather Api class
    weather = Weather(loc='Missisauga,Ontario,CA', date_start='2024-01-14', date_end='2024-01-15')
    # insert weather data into mysql tables
    # weather_data = json.loads('')
    weather.mysql_weather_insert_data()