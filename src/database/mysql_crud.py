import toml
import os
import MySQLdb as mysql_db
from datetime import date, datetime, timedelta
from src.constants import ROOT_DIR
from src.database.sqlconn import DbFactory, MySqlDB, PostgreSqlDB

TPYE_DAY = 0
TYPE_HOUR = 1

config = toml.load(os.path.join(ROOT_DIR, 'conf', 'config.toml'))
mysql_param = {
    'host': config['database']['mysql']['host'],
    'user': config['database']['mysql']['user'],
    'password': config['database']['mysql']['password'],
    'port': config['database']['mysql']['port'],
    'database': config['database']['mysql']['db_name']
}

conn = DbFactory()
cnx = conn.get_database_connection(MySqlDB(**mysql_param))
cursor = cnx.cursor()

def insert_weather_data(weather_json:dict) -> None:
    conn = DbFactory()
    cnx = conn.get_database_connection(MySqlDB(**mysql_param))
    cursor = cnx.cursor()
    
    stations = weather_json['stations']
    days = weather_json['days']
    locations = {'timezone': weather_json['timezone'], 'latitude': weather_json['latitude'], 'longitude': weather_json['longitude'],
                 'resolved_addr': weather_json['resolvedAddress'], 'address': weather_json['address'], 'description': weather_json['description']}

    # insert locations
    loc_id = insert_weather_location(locations)

    # insert stations
    insert_weather_stations(stations)
    
    # insert weathers
    insert_weather_day_data(days, loc_id)

    cursor.close()
    cnx.close()

def insert_weather_location(location:dict) -> int:
    ins_stmt = ("INSERT INTO locations "
                     "(timezone, latitude, longitude, resolved_addr, address, description) "
                     "VALUES (%(timezone)s, %(latitude)s, %(longitude)s, %(resolved_addr)s, %(address)s, %(description)s)")
    get_stmt = ("SELECT id FROM locations WHERE latitude=%(latitude)s AND longitude=%(longitude)s ")
    cursor.execute(get_stmt, {'latitude': location['latitude'], 'longitude': location['longitude']})
    
    row = cursor.fetchone()
    if not row:
        try:
            id = cursor.execute(ins_stmt, location)
            # print(cursor._executed)
            # Make sure data is committed to the database
            cnx.commit()
        except (mysql_db.Error, mysql_db.Warning) as err:
            print(f'caught error: {err.args}')
            cnx.rollback()
    else:
        id = row[0]
        
    return id


def insert_weather_stations(stations:dict) -> None:
    # insert stations
    ins_stmt = ("INSERT INTO stations "
                    "(distance, latitude, longitude, use_count, name, name_abbr, quality, contribution) "
                    "VALUES (%(distance)s, %(latitude)s, %(longitude)s, %(useCount)s, %(name)s, %(id)s, %(quality)s, %(contribution)s)")
    for station, value in stations.items():
        get_stmt = ("SELECT id FROM stations WHERE name_abbr=%(name)s")
        cursor.execute(get_stmt, {'name': station})
        
        if not cursor.fetchone():
            try:
                id = cursor.execute(ins_stmt, value)
                # print(cursor._executed)
                # Make sure data is committed to the database
                cnx.commit()
            except (mysql_db.Error, mysql_db.Warning) as err:
                print(f'caught error: {err.args}')
                cnx.rollback()


def insert_weather_day_data(weather_data:dict, loc_id: int) -> None:
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
        day['type'] = TPYE_DAY
        day['preciptype'] = ','.join(day['preciptype']) if day['preciptype'] else None
        day['sunrise'] = day['datetime'] + ' ' + day['sunrise']
        day['sunrise_epoch'] = day['sunriseEpoch']
        day['sunset'] = day['datetime'] + ' ' + day['sunset']
        day['sunset_epoch'] = day['sunsetEpoch']
        day['stations'] = ','.join(day['stations']) if day['stations'] else None
        cursor.execute(get_stmt, {'date': day['date'], 'datetime_epoch': day['datetime_epoch'], 
                                  'datetime': day['datetime'], 'type': 0, 'location_id': loc_id})
        day_info = cursor.fetchone()
        if not day_info:
            try:
                cursor.execute(ins_stmt, day)
                # print(cursor._executed)
                # Make sure data is committed to the database
                cnx.commit()
            except (mysql_db.Error, mysql_db.Warning) as err:
                print(f'caught error: {err.args}')
                
        for hour in day['hours']:
            hour['location_id'] = loc_id
            hour['date'] = day['datetime']
            hour['datetime_epoch'] = hour['datetimeEpoch']
            hour['datetime'] = day['datetime'] + ' ' + hour['datetime']
            hour['type'] = TYPE_HOUR
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
            cursor.execute(get_stmt, {'date': hour['date'], 'datetime_epoch': hour['datetime_epoch'], 
                                      'datetime': hour['datetime'], 'type': 1, 'location_id': loc_id})
            hour_info = cursor.fetchone()
            if not hour_info:
                try:
                    cursor.execute(ins_stmt, hour)
                    # print(cursor._executed)
                    # Make sure data is committed to the database
                    cnx.commit()
                except (mysql_db.Error, mysql_db.Warning) as err:
                    print(f'caught error: {err.args}')
