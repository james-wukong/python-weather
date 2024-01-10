import toml
import os
import json
import MySQLdb as mysql_db
from datetime import date, datetime, timedelta
from src.constants import ROOT_DIR
from src.database.sqlconn import DbFactory, MySqlDB, PostgreSqlDB

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


def insert_employee_test():
    tomorrow = datetime.now().date() + timedelta(days=1)

    add_employee = ("INSERT INTO employees "
                "(emp_no, first_name, last_name, hire_date, gender, birth_date) "
                "VALUES (%s, %s, %s, %s, %s, %s)")
    add_salary = ("INSERT INTO salaries "
                "(emp_no, salary, from_date, to_date) "
                "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

    emp_no = 1111
    data_employee = (emp_no, 'Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

    # Insert new employee
    cursor.execute(add_employee, data_employee)
    # emp_no = cursor.lastrowid

    # Insert salary information
    data_salary = {
        'emp_no': emp_no,
        'salary': 50000,
        'from_date': tomorrow,
        'to_date': date(9999, 1, 1),
    }
    try:
        cursor.execute(add_salary, data_salary)

        # Make sure data is committed to the database
        cnx.commit()
    except Exception as e:
        cnx.rollback()

    cursor.close()
    cnx.close()


def insert_weather_data(weather_json):
    conn = DbFactory()
    cnx = conn.get_database_connection(MySqlDB(**mysql_param))
    cursor = cnx.cursor()
    
    stations = weather_json['stations']
    days = weather_json['days']
    # insert stations
    insert_weather_stations(stations)
    
    # insert weathers
    insert_weather_day_data(days)


    cursor.close()
    cnx.close()


def insert_weather_stations(stations):
    # insert stations
    for station, value in stations.items():
        get_stmt = ("SELECT id FROM stations WHERE name_abbr = %(name)s")
        cursor.execute(get_stmt, {'name': station})
        
        ins_stmt = ("INSERT INTO stations "
                     "(distance, latitude, longitude, useCount, name, name_abbr, quality, contribution) "
                     "VALUES (%(distance)s, %(latitude)s, %(longitude)s, %(useCount)s, %(name)s, %(id)s, %(quality)s, %(contribution)s)")
        # print(value)
        # return
        if not cursor.fetchone():
            try:
                cursor.execute(ins_stmt, value)
                # print(cursor._executed)
                # Make sure data is committed to the database
                cnx.commit()
            except (mysql_db.Error, mysql_db.Warning) as err:
                print(f'caught error: {err.args}')
                cnx.rollback()


def insert_weather_day_data(weather_data):
    ins_stmt = ("INSERT INTO stations "
                     "(`date`, `datetime_epoch`, `datetime`, `type`, `tempmax`, "
                     "`tempmin`, `temp`, `feelslikemax`, `feelslikemin`, `feelslike`, "
                     "`dew`, `humidity`, `precip`, `precipprob`, `precipcover`, "
                     "`preciptype`, `snow`, `snowdepth`, `windgust`, `windspeed`, `winddir`, "
                     "`pressure`, `cloudcover`, `visibility`, `solarradiation`, `solarenergy`, "
                     "`uvindex`, `severerisk`, `sunrise`, `sunrise_epoch`, `sunset`, "
                     "`sunset_epoch`, `moonphase`, `conditions`, `description`, `icon`, `stations`, `source`) "
                     "VALUES (%(date)s, %(datetime_epoch)s, %(datetime)s, %(type)s, %(tempmax)s, "
                     "%(tempmin)s, %(temp)s, %(feelslikemax)s, %(feelslikemin)s, %(feelslike)s, "
                     "%(dew)s, %(humidity)s, %(precip)s, %(precipprob)s, %(precipcover)s, "
                     "%(preciptype)s, %(snow)s, %(snowdepth)s, %(windgust)s, %(windspeed)s, "
                     "%(winddir)s, %(pressure)s, %(cloudcover)s, %(visibility)s, %(solarradiation)s, "
                     "%(solarenergy)s, %(uvindex)s, %(severerisk)s, %(sunrise)s, %(sunrise_epoch)s, "
                     "%(sunset)s, %(sunset_epoch)s, %(moonphase)s, %(conditions)s, %(description)s, "
                     "%(icon)s, %(stations)s, %(source)s)")
                     
    # insert weather data
    for day in weather_data:
        for hour in day['hours']:
            hour['datetime'] = day['datetime'] + ' ' + hour['datetime']
            print(hour)
            break
            # try:
            #     cursor.execute(ins_stmt, hour)
            #     # print(cursor._executed)
            #     # Make sure data is committed to the database
            #     cnx.commit()
            # except (mysql_db.Error, mysql_db.Warning) as err:
            #     print(f'caught error: {err.args}')
            #     cnx.rollback()
        break
    