import toml
import os
from datetime import date, datetime, timedelta
from src.constants import ROOT_DIR
from src.database.sqlconn import DbFactory, MySqlDB, PostgreSqlDB

config = toml.load(os.path.join(ROOT_DIR, 'conf', 'config.toml'))

mysql_param = {
    'host': config['database']['mysql']['host'],
    'user': config['database']['mysql']['user'],
    'password': config['database']['mysql']['password'],
    'database': config['database']['mysql']['db_name']
}

def insert_employee():
    conn = DbFactory()
    cnx = conn.get_database_connection(MySqlDB(**mysql_param))
    cursor = cnx.cursor()

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