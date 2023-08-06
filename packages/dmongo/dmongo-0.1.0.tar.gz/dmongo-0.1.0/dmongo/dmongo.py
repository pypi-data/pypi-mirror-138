import collections
from pymongo import MongoClient

from bson.objectid import ObjectId


class mongoQuery:
    def __init__(self, MONGO_URI=None, Database=None, collections=None):
        self.collect = collections
        self.mongoClient = MongoClient(MONGO_URI)
        self.collections = self.mongoClient[Database]
        self.collections[self.collect]
        return

    def create(self, data):
        userData = self.collections[self.collect].insert_one(data)
        return

    def getAll(self):
        array = []
        userData = self.collections[self.collect].find({})
        for usr in userData:
            array.append(usr)
        return array

    def getOne(self, ID):
        userData = self.collections[self.collect].find_one(
            {'_id': ObjectId(ID)})
        if userData:
            return userData

    def update(self, ID, data):
        userData = self.collections[self.collect].find_one(
            {'_id': ObjectId(ID)})

        if userData:
            for key, value in data.items():
                userData[key] = value
            _userData = userData
            self.collections[self.collect].replace_one(
                {"_id": ObjectId(ID)}, _userData, upsert=True)
            return _userData

    def delete(self, ID):
        userData = self.collections[self.collect].delete_one(
            {'_id': ObjectId(ID)})
        return

    def filterBy(self, data):
        array = []
        userData = self.collections[self.collect].find(data)
        for usr in userData:
            array.append(usr)
        return array
