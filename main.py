import toml
import os
from src.constants import ROOT_DIR
from src.api.weather import Weather
from src.database.mysql_crud import insert_weather_data

config = toml.load(os.path.join(ROOT_DIR, 'conf', 'config.toml'))

if __name__ == '__main__':
    a = Weather(loc='Missisauga,Ontario,CA', date_start='2023-11-14')
    # _, weather_insert_data = a.fetch_weather_data()
    a.mysql_weather_insert_data()