import MySQLdb
import psycopg
from pymongo import MongoClient
from abc import ABC, abstractmethod

class Database(ABC):
   conn_params = {}
   cnx = None

   def __init__(self, **kwargs):
        if kwargs['host']:
            self.conn_params['host'] = kwargs['host']
        if kwargs['user']:
            self.conn_params['user'] = kwargs['user']
        if kwargs['password']:
            self.conn_params['password'] = kwargs['password']
        if kwargs['database']:
           self.conn_params['database'] = kwargs['database']
        if kwargs['port']:
            self.conn_params['port'] = kwargs['port']
        

   @abstractmethod
   def connection(self):
        pass
   
   def __del__(self):
        try:
            self.cnx.close()
        finally:
            pass
  

class PostgreSqlDB(Database):
    def connection(self):
        self.cnx = psycopg.connect(**self.conn_params)
        return self.cnx


class MySqlDB(Database):
    def connection(self):
        self.cnx = MySQLdb.connect(**self.conn_params)
        return self.cnx

class MongoDB(Database):
    def connection(self):
        self.cnx = MongoClient(**self.conn_params)
        return self.cnx

class DbFactory:
    '''
    database: PostgreSqlDB() | MySqlDB() | MongoDB
    Usage:
        factory = DbFactory()
        factory.get_database_connection(PostgreSqlDB())
    '''
    def get_database_connection(self, database):
        return database.connection()