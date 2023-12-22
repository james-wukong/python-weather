import MySQLdb
import psycopg
from abc import ABC, abstractmethod

class Database(ABC):
   conn_params = {}

   def __init__(self, **kwargs):
       if kwargs['host'] is not None:
           self.conn_params['host'] = kwargs['host']
       if kwargs['user'] is not None:
           self.conn_params['user'] = kwargs['user']
       if kwargs['password'] is not None:
           self.conn_params['password'] = kwargs['password']
       if kwargs['database'] is not None:
           self.conn_params['database'] = kwargs['database']

   @abstractmethod
   def connection(self):
        pass

class PostgreSqlDB(Database):
    def connection(self):
        cnx = psycopg.connect(**self.conn_params)
        return cnx


class MySqlDB(Database):
    def connection(self):
        cnx = MySQLdb.connect(**self.conn_params)
        return cnx
    
class DbFactory:
    '''
    database: PostgreSqlDB() | MySqlDB()
    Usage:
        factory = DbFactory()
        factory.get_database_connection(PostgreSqlDB())
    '''
    def get_database_connection(self, database):
        return database.connection()