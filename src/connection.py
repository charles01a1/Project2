from pymongo.mongo_client import MongoClient

from config import *


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class Connection(metaclass=Singleton):

    def __init__(self):
        self.__client = MongoClient(connection_string)
        self.__db = self.__client[dbname]

        self.__collections = {name: self.__db[name.replace(".", "_")] for name in collection_names}

    def get_collection(self):
        return self.__collections


collections = Connection().get_collection()