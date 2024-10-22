from pymongo import MongoClient


class DBConn:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['bookstore']

    def user_id_exist(self, user_id):
        user = self.db.user.find_one({"user_id": user_id})
        if user is None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        book = self.db.store.find_one({"store_id": store_id, "book_id": book_id})
        if book is None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        store = self.db.user_store.find_one({"store_id": store_id})
        if store is None:
            return False
        else:
            return True
