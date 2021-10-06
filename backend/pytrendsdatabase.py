import mongoengine
from pymongo import MongoClient

def databasequery_anime_keywordSuggestions(client: MongoClient, name):
    ' searches anime by name '
    anime_collection = client.pytrends.anime
    suggestions = list(anime_collection.find({'fromSearch:': name}))
    return(suggestions)
    
def databasequery_studio_keywordSuggestions(client: MongoClient, name):
    ' searches studio by name '
    studio_collection = client.pytrends.studios
    suggestions = list(studio_collection.find({'fromSearch:': name}))
    return(suggestions)

def databasequery_staff_keywordSuggestions(client: MongoClient, name):
    ' searches staff by name '
    studio_collection = client.pytrends.staff
    suggestions = list(studio_collection.find({'fromSearch:': name}))
    print(suggestions)
    return(suggestions)

