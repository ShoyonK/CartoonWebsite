import mongoengine
from pymongo import MongoClient
import wikipedia
import time


client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = client.CRUD # use anilist database
CRUD_TESTS = db.CRUD_TESTS # specify collection


def create(client : MongoClient, test_doc):
    ''' Creates a document '''
    collection = client.CRUD.crud
    collection.insert_one(test_doc)


def create_many(client : MongoClient, test_doc):
    collection = client.CRUD.crud
    collection.insert_many(test_doc,test_doc,test_doc,test_doc)

def read(client : MongoClient, test_doc):
    ''' Remove a document '''
    collection = client.CRUD.crud
    found_doc = collection.find_one(test_doc)
    return found_doc


def update(client : MongoClient, test_doc, key_to_update, value):
    ''' Update a document '''
    collection = client.CRUD.crud
    collection.update_one(test_doc,{'$set':{key_to_update:value}})
    
    collection.update_one

def delete(client : MongoClient, test_doc):
    ''' Delete a document '''
    collection = client.CRUD.crud
    collection.delete_one(test_doc)

def delete_many(client: MongoClient, test_doc):
    ''' Delete many documents '''
    collection = client.CRUD.crud
    collection.delete_many(test_doc)

