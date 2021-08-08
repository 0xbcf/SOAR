#!/usr/bin/env python
import pymongo

class mydb(object):
    def __init__(self):
        # Initial the database connection
        self._db_connection = pymongo.MongoClient("mongodb://localhost:27017")
        self._db_database = self._db_connection["db"]
    def query(self, query, collection):
        # Run a database search
        return self._db_database[collection].find(query)
    def insert(self, doc, collection):
        # insert a document into the collection
        return self._db_database[collection].insert_one(doc)
    def mark_read(self, myid, collection):
        # Mark a document as read
        self._db_database[collection].update({"_id": myid}, {"$set": {"read": 1}}, upsert=False)
    def __del__(self):
        # Close down the database
        self._db_connection.close()
