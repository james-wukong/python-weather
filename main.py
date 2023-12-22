import toml
import os
from datetime import date, datetime, timedelta
from src.constants import ROOT_DIR
from src.database.sqlconn import DbFactory, MySqlDB, PostgreSqlDB

config = toml.load(os.path.join(ROOT_DIR, 'conf', 'config.toml'))

if __name__ == '__main__':
    mysql_param = {
        'host': config['database']['mysql']['host'],
        'user': config['database']['mysql']['user'],
        'password': config['database']['mysql']['password'],
        'database': config['database']['mysql']['db_name']
    }

    postgres_param = {
        'host': config['database']['postgres']['host'],
        'user': config['database']['postgres']['user'],
        'password': config['database']['postgres']['password'],
        'database': config['database']['postgres']['db_name']
    }

    