import toml
import os
import MySQLdb as mysql_db
from src.constants import ROOT_DIR
from src.database.sqlconn import DbFactory, MySqlDB


class WeatherDataToMysql:

    # weather type indicator
    TPYE_DAY = 0
    TYPE_HOUR = 1

    def __init__(self):
        """
        initialize mysql connection
        """
        self.config = toml.load(os.path.join(ROOT_DIR, 'conf', 'config.toml'))
        self.mysql_param = {
            'host': self.config['database']['mysql']['host'],
            'user': self.config['database']['mysql']['user'],
            'password': self.config['database']['mysql']['password'],
            'port': self.config['database']['mysql']['port'],
            'database': self.config['database']['mysql']['db_name']
        }

        print('initializing the connection')
        self.conn = DbFactory()
        self.cnx = self.conn.get_database_connection(MySqlDB(**self.mysql_param))
        self.cursor = self.cnx.cursor()
    
    def __del__(self) -> None:
        """
        close mysql connection
        """
        print('closing the connection')
        self.cursor.close()
        self.cnx.close()

    def insert_weather_data(self, weather_json:dict) -> None:
        """
        insert data fetched from weather api
        Args:
            weather_json: dict, data returned from weather api
        Returns:
            None
        """
        stations = weather_json['stations']
        days = weather_json['days']
        locations = {'timezone': weather_json['timezone'], 'latitude': weather_json['latitude'], 'longitude': weather_json['longitude'],
                    'resolved_addr': weather_json['resolvedAddress'], 'address': weather_json['address'], 'description': weather_json['description']}

        # insert locations
        loc_id = self.__insert_weather_location(locations)

        # insert stations
        self.__insert_weather_stations(stations)
        
        # insert weathers
        self.__insert_weather_day_data(days, loc_id)

        # cursor.close()
        # cnx.close()

    def __insert_weather_location(self, location:dict) -> int:
        """
        insert weather location information into locations table
        Args:
            location: dict, includes location information
        Return:
            int: inserted id or already existing id
        """
        ins_stmt = ("INSERT INTO locations "
                        "(timezone, latitude, longitude, resolved_addr, address, description) "
                        "VALUES (%(timezone)s, %(latitude)s, %(longitude)s, %(resolved_addr)s, %(address)s, %(description)s)")
        get_stmt = ("SELECT id FROM locations WHERE latitude=%(latitude)s AND longitude=%(longitude)s ")
        self.cursor.execute(get_stmt, {'latitude': location['latitude'], 'longitude': location['longitude']})
        
        row = self.cursor.fetchone()
        if not row:
            try:
                print(f'inserting location...')
                id = self.cursor.execute(ins_stmt, location)
                # print(cursor._executed)
                # Make sure data is committed to the database
                self.cnx.commit()
            except (mysql_db.Error, mysql_db.Warning) as err:
                print(f'caught error: {err.args}')
                self.cnx.rollback()
        else:
            id = row[0]
            
        return id


    def __insert_weather_stations(self, stations:dict) -> None:
        """
        insert weather station information into stations table
        Args:
            stations: dict, includes stations information
        Return:
            None
        """
        ins_stmt = ("INSERT INTO stations "
                        "(distance, latitude, longitude, use_count, name, name_abbr, quality, contribution) "
                        "VALUES (%(distance)s, %(latitude)s, %(longitude)s, %(useCount)s, %(name)s, %(id)s, %(quality)s, %(contribution)s)")
        for station, value in stations.items():
            get_stmt = ("SELECT id FROM stations WHERE name_abbr=%(name)s")
            self.cursor.execute(get_stmt, {'name': station})
            row = self.cursor.fetchone()
            if not row:
                try:
                    print(f'inserting station...')
                    self.cursor.execute(ins_stmt, value)
                    # print(cursor._executed)
                    # Make sure data is committed to the database
                    self.cnx.commit()
                except (mysql_db.Error, mysql_db.Warning) as err:
                    print(f'caught error: {err.args}')
                    self.cnx.rollback()


    def __insert_weather_day_data(self, weather_data:dict, loc_id: int) -> None:
        """
        insert weather data information into weather_details table
        TODO: implement with multi-threading or multi-processing
        Args:
            weather_data: dict, includes weather_data information
            loc_id: int, location id for the weather_data
        Return:
            None
        """
        ins_stmt = ("INSERT INTO weather_details "
                        "(`location_id`, `date`, `datetime_epoch`, `datetime`, `type`, `tempmax`, "
                        "`tempmin`, `temp`, `feelslikemax`, `feelslikemin`, `feelslike`, "
                        "`dew`, `humidity`, `precip`, `precipprob`, `precipcover`, "
                        "`preciptype`, `snow`, `snowdepth`, `windgust`, `windspeed`, `winddir`, "
                        "`pressure`, `cloudcover`, `visibility`, `solarradiation`, `solarenergy`, "
                        "`uvindex`, `severerisk`, `sunrise`, `sunrise_epoch`, `sunset`, "
                        "`sunset_epoch`, `moonphase`, `conditions`, `description`, `icon`, `stations`, `source`) "
                        "VALUES (%(location_id)s, %(date)s, %(datetime_epoch)s, %(datetime)s, %(type)s, %(tempmax)s, "
                        "%(tempmin)s, %(temp)s, %(feelslikemax)s, %(feelslikemin)s, %(feelslike)s, "
                        "%(dew)s, %(humidity)s, %(precip)s, %(precipprob)s, %(precipcover)s, "
                        "%(preciptype)s, %(snow)s, %(snowdepth)s, %(windgust)s, %(windspeed)s, "
                        "%(winddir)s, %(pressure)s, %(cloudcover)s, %(visibility)s, %(solarradiation)s, "
                        "%(solarenergy)s, %(uvindex)s, %(severerisk)s, %(sunrise)s, %(sunrise_epoch)s, "
                        "%(sunset)s, %(sunset_epoch)s, %(moonphase)s, %(conditions)s, %(description)s, "
                        "%(icon)s, %(stations)s, %(source)s)")
        get_stmt = ("SELECT id FROM weather_details WHERE date=%(date)s AND datetime_epoch=%(datetime_epoch)s " 
                        "AND datetime=%(datetime)s AND type=%(type)s AND location_id=%(location_id)s")                 
        # insert weather data
        # TODO multi-threading
        for day in weather_data:
            day['location_id'] = loc_id
            day['datetime_epoch'] = day['datetimeEpoch']
            day['date'] = day['datetime']
            day['type'] = self.TPYE_DAY
            day['preciptype'] = ','.join(day['preciptype']) if day['preciptype'] else None
            day['sunrise'] = day['datetime'] + ' ' + day['sunrise']
            day['sunrise_epoch'] = day['sunriseEpoch']
            day['sunset'] = day['datetime'] + ' ' + day['sunset']
            day['sunset_epoch'] = day['sunsetEpoch']
            day['stations'] = ','.join(day['stations']) if day['stations'] else None
            self.cursor.execute(get_stmt, {'date': day['date'], 'datetime_epoch': day['datetime_epoch'], 
                                    'datetime': day['datetime'], 'type': 0, 'location_id': loc_id})
            day_info = self.cursor.fetchone()
            if not day_info:
                try:

                    print(f'inserting day info...')
                    self.cursor.execute(ins_stmt, day)
                    # print(cursor._executed)
                    # Make sure data is committed to the database
                    self.cnx.commit()
                except (mysql_db.Error, mysql_db.Warning) as err:
                    print(f'caught error: {err.args}')
                    
            for hour in day['hours']:
                hour['location_id'] = loc_id
                hour['date'] = day['datetime']
                hour['datetime_epoch'] = hour['datetimeEpoch']
                hour['datetime'] = day['datetime'] + ' ' + hour['datetime']
                hour['type'] = self.TYPE_HOUR
                hour['tempmax'] = day['tempmax']
                hour['tempmin'] = day['tempmin']
                hour['feelslikemax'] = day['feelslikemax']
                hour['feelslikemin'] = day['feelslikemin']
                hour['precipcover'] = day['precipcover']
                hour['precipcover'] = day['precipcover']
                hour['sunrise'] = day['sunrise']
                hour['sunrise_epoch'] = day['sunriseEpoch']
                hour['sunset'] = day['sunset']
                hour['sunset_epoch'] = day['sunsetEpoch']
                hour['description'] = None
                hour['moonphase'] = day['moonphase']
                hour['preciptype'] = ','.join(hour['preciptype']) if hour['preciptype'] else None
                hour['stations'] = ','.join(hour['stations']) if hour['stations'] else None
                self.cursor.execute(get_stmt, {'date': hour['date'], 'datetime_epoch': hour['datetime_epoch'], 
                                        'datetime': hour['datetime'], 'type': 1, 'location_id': loc_id})
                hour_info = self.cursor.fetchone()
                if not hour_info:
                    try:

                        print(f'inserting hour infol...')
                        self.cursor.execute(ins_stmt, hour)
                        # print(cursor._executed)
                        # Make sure data is committed to the database
                        self.cnx.commit()
                    except (mysql_db.Error, mysql_db.Warning) as err:
                        print(f'caught error: {err.args}')
