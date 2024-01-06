import MySQLdb
import psycopg
from pymongo import MongoClient
from abc import ABC, abstractmethod

class Database(ABC):
    """
    Singleton class for managing database connections.
    """

    conn_params = {}
    cnx = None
    _instance = None

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
    
    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
            cls._instance.cnx = None
        return cls._instance
    
    @abstractmethod
    def connection(self):
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