import logging
import threading
from pymongo import MongoClient, errors


class Store:
    def __init__(self, db_path):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['bookstore']
        self.init_tables()

    def init_tables(self):
        try:
            self.db.create_collection("user", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["user_id", "password", "balance"],
                    "properties": {
                        "user_id": {"bsonType": "string"},
                        "password": {"bsonType": "string"},
                        "balance": {"bsonType": "int"},
                        "token": {"bsonType": "string"},
                        "terminal": {"bsonType": "string"}
                    }
                }
            })

            self.db.create_collection("user_store", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["user_id", "store_id"],
                    "properties": {
                        "user_id": {"bsonType": "string"},
                        "store_id": {"bsonType": "string"}
                    }
                }
            })

            self.db.create_collection("store", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["store_id", "book_id", "book_info", "stock_level"],
                    "properties": {
                        "store_id": {"bsonType": "string"},
                        "book_id": {"bsonType": "string"},
                        "book_info": {"bsonType": "string"},
                        "stock_level": {"bsonType": "int"}
                    }
                }
            })

            self.db.create_collection("new_order", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["order_id", "user_id", "store_id"],
                    "properties": {
                        "order_id": {"bsonType": "string"},
                        "user_id": {"bsonType": "string"},
                        "store_id": {"bsonType": "string"}
                    }
                }
            })

            self.db.create_collection("new_order_detail", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["order_id", "book_id", "count", "price"],
                    "properties": {
                        "order_id": {"bsonType": "string"},
                        "book_id": {"bsonType": "string"},
                        "count": {"bsonType": "int"},
                        "price": {"bsonType": "int"}
                    }
                }
            })
        except errors.PyMongoError as e:
            logging.error(e)

    def get_db_conn(self):
        return self.db


database_instance: Store = None
# global variable for database sync
init_completed_event = threading.Event()


def init_database(db_path):
    global database_instance
    database_instance = Store(db_path)


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()
