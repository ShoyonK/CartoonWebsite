import mongoengine
from pymongo import MongoClient


def databasequery_anime_idMal(client : MongoClient, idMal):
    ''' Searches our database for a singular anime by its id '''
    anime_collection = client.jikan.anime
    anime = anime_collection.find({'mal_id':idMal}).limit(1)
    return anime[0]

def databasequery_char_id(client : MongoClient, idMal):
    character_collection = client.jikan.characters
    character = character_collection.find({'anilistID':idMal}).limit(1)
    return character[0]