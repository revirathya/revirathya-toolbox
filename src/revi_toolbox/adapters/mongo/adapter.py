from pydantic import SecretStr
from pymongo import MongoClient
from pymongo.collection import Collection

from revi_toolbox.adapters.mongo.schema import MongoAuth


class MongoAdapter:
    __auth_params: MongoAuth
    
    def __init__(
        self,
        username: str,
        password: SecretStr,
        hostname: str,
        port: int,
        db_name: str
    ):
        self.__db_name = db_name
        self.__auth_params = MongoAuth(
            username = username,
            password = password,
            hostname = hostname,
            port = port
        )


    # Public
    def get_collection(self, collection_name: str) -> Collection:
        client = MongoClient(self.__auth_params.uri.get_secret_value())
        db = client[self.__db_name]
        collection = db[collection_name]
        return collection
