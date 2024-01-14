import os
import requests
import toml
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from src.constants import ROOT_DIR
from src.database.mysql_crud import insert_weather_data


class Weather:
    def __init__(self, loc: str = 'Toronto,CA', 
                           date_start: str = '2023-12-01', 
                           date_end: str = ''):
        config = toml.load(os.path.join(ROOT_DIR, 'conf', 'config.toml'))
        self.weather_api = config['api']['visualcrossing']['api_server']
        self.key_api = config['api']['visualcrossing']['key']
        self.loc = loc
        date_tmp = list(map(int, date_start.split('-')))
        self.date_start = date_start
        self.date_end = date_end if date_end else str(date(date_tmp[0], date_tmp[1], date_tmp[2]) + relativedelta(months=1))


    def fetch_weather_data(self) -> tuple:
        api = os.path.join(self.weather_api, self.loc, self.date_start, self.date_end)
        try:
            resp = requests.get(api, params={'key': self.key_api})
            resp.raise_for_status() 
        except requests.exceptions.HTTPError as errh: 
            print(f"HTTP Error, {errh.args[0]}")
        except requests.exceptions.ReadTimeout as errrt: 
            print(f"Time out, {errrt}") 
        except requests.exceptions.ConnectionError as conerr: 
            print(f"Connection error, {conerr}")

        if resp.ok:
            return resp.status_code, resp.json()

        return resp.status_code, False
    
    def mysql_weather_insert_data(self, weather_json='') -> str:
        # get data from api
        if not weather_json:
            _, weather_json = self.fetch_weather_data()
        
        insert_weather_data(weather_json)

        return weather_json
