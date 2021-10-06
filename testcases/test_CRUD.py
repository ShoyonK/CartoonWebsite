import unittest
import CRUD
import mongoengine
from pymongo import MongoClient
import wikipedia
import time

class TestCRUD(unittest.TestCase): # inherit from unittst.TestCase

    def test_create(self):
        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        name = 'create'
        id = 1
        test_doc = {
            'name':name,
            'id':id
        }
        
        CRUD.create(client, test_doc)
        
        found_doc = client.CRUD.crud.find_one({'name':name, 'id':id})
        self.assertEqual(test_doc,found_doc)

        client.CRUD.crud.delete_one({'name':name,'id':id})
        
    
    def test_read(self):
        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        name = 'read'
        id = 1
        test_doc = {
            'name':name,
            'id':id
        }
        
        client.CRUD.crud.insert_one(test_doc)
        found_doc = CRUD.read(client, test_doc)
        self.assertEqual(test_doc,found_doc)

        client.CRUD.crud.delete_one(test_doc)
        

    def test_update(self):
        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        name = 'delete'
        id = 1
        test_doc = {
            'name':name,
            'id':id
        }

        client.CRUD.crud.insert_one(test_doc)

        key_to_update = 'name'
        value = 'new_update'
        CRUD.update(client,test_doc,key_to_update,value)

        found_doc = client.CRUD.crud.find_one({key_to_update:value})

        self.assertEqual(found_doc[key_to_update], value)

        client.CRUD.crud.delete_one(found_doc)


    def test_delete(self):
        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        name = 'delete'
        id = 1
        test_doc = {
            'name':name,
            'id':id
        }
        client.CRUD.crud.insert_one(test_doc)
        
        CRUD.delete(client, test_doc)

        count = client.CRUD.crud.count_documents(test_doc)
        
        self.assertEqual(0, count)
        
       


if __name__ == '__main__':
    unittest.main()