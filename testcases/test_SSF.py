import unittest
import CRUD
import mongoengine
from pymongo import MongoClient
import wikipedia
import SSF
import string
import warnings
import re


class TestSSF(unittest.TestCase): 

    # def test_search_anime_name_Naruto(self): 
    #     '''Tests if search entry is a substring of all search results'''

    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = "naruto" 
    #     sort_method = "popularity dec"
    #     genre_filter = ""
    #     score_filter = 0
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for anime in searches:
    #         titleAnimeSearched = anime['title']['userPreferred'].lower()
    #         description = anime['description'].lower()
    #         if title not in titleAnimeSearched and title not in description:
    #             result = False

    #     self.assertEqual(True, result)


    # def test_search_anime_name_special_char(self): 
    #     '''Tests if search entry with a special character is a substring of all search results'''

    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
    #     database = client.anilist.anime
    #     title = "fate/" 
    #     sort_method = "popularity dec"
    #     genre_filter = ""
    #     score_filter = 0
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for anime in searches:
    #         titleAnimeSearched = anime['title']['userPreferred'].lower()
    #         description = anime['description'].lower()
    #         if title not in titleAnimeSearched and title not in description.lower():
    #             result = False
    #     self.assertEqual(True, result)


    # def test_search_anime_name_find_all_instances(self): 
    #     '''Checks to see if all instances searched by name are found'''

    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.CRUD.crud
    #     test_doc = {
    #         'title': { 'userPreferred': 'animetest' },
    #         'meanScore': 0
    #     }
    #     test_doc2 = {
    #         'title': { 'userPreferred': 'animetestcase substring' },
    #         'meanScore': 0
    #     }

    #     database.insert_one(test_doc.copy())
    #     database.insert_one(test_doc.copy())
    #     database.insert_one(test_doc.copy())
    #     database.insert_one(test_doc2)

    #     title = "animetest" 
    #     sort_method = "popularity dec"
    #     genre_filter = ""
    #     score_filter = 0
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)
    #     lengthResult = 4

    #     CRUD.delete_many(client,test_doc)
    #     CRUD.delete(client,test_doc2)

    #     self.assertEqual(4,lengthResult)


    # def test_search_one_anime_genre(self): 
    #     ''' Searches only by 1 genre and checks if only documents with that genre are returned'''
    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "popularity dec"
    #     genre_filter = ["Action"]
    #     score_filter = 0
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for anime in searches:
    #             if genre_filter[0] not in anime['genres']:
    #                 result = False
    #     self.assertEqual(True, result)


    # def test_search_multiple_selected_anime_genre(self): 
    #     ''' Searches by several selected genres and checks if only documents with that genre are returned'''
    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.CRUD.crud

    #     test_doc = {
    #         'title': { 'userPreferred': 'animetest' },
    #         'meanScore': 0,
    #         'genres':["Action"]
    #     }

    #     test_doc2 = { #same name different genre
    #         'title': { 'userPreferred': 'animetest' },
    #         'meanScore': 0,
    #         'genres':["Action","Comedy"]
    #     }

    #     database.insert_one(test_doc)
    #     database.insert_one(test_doc2)

    #     title = "" 
    #     sort = "popularity"
    #     direction = -1
    #     genre_filter = ["Action", "Comedy"]
    #     score_filter = 0
    #     searches = SSF.search_anime_name_all(database, title, sort, direction, genre_filter, score_filter)
    #     lengthResult = searches.count()
        
    #     CRUD.delete(client,test_doc)
    #     CRUD.delete(client,test_doc2)
        
    #     self.assertEqual(1,lengthResult)


    # def test_search_anime_genre_find_all_instances(self): 
    #     '''Checks to see if all instances searched by genre are found'''

    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.CRUD.crud

    #     test_doc = {
    #         'title': { 'userPreferred': 'animetest' },
    #         'meanScore': 0,
    #         'genres':["Action"]
    #     }

    #     test_doc2 = { #same name different genre
    #         'title': { 'userPreferred': 'animetest' },
    #         'meanScore': 0,
    #         'genres':["Drama"]
    #     }

    #     test_doc3 = { #different genre
    #         'title': { 'userPreferred': 'animetestcase substring' },
    #         'meanScore': 0,
    #         'genres': ["Comedy"]
    #     }

    #     test_doc4 = { 
    #         'title': { 'userPreferred': 'animetestcase' },
    #         'meanScore': 0,
    #         'genres': ["Comedy","Action"]
    #     }

    #     database.insert_one(test_doc.copy())
    #     database.insert_one(test_doc.copy())
    #     database.insert_one(test_doc2)
    #     database.insert_one(test_doc3)
    #     database.insert_one(test_doc4)

    #     title = "" 
    #     sort = "popularity"
    #     direction = -1
    #     genre_filter = ["Action"]
    #     score_filter = 0
    #     searches = SSF.search_anime_name_all(database, title, sort, direction, genre_filter, score_filter)
    #     lengthResult = searches.count()
        
    #     CRUD.delete_many(client,test_doc)
    #     CRUD.delete(client,test_doc2)
    #     CRUD.delete(client,test_doc3)
    #     CRUD.delete(client,test_doc4)
        
    #     self.assertEqual(3,lengthResult)


    # def test_search_anime_media_format(self):
    #     '''Searches only by score and checks if returned anime have greater score'''

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "popularity dec"
    #     genre_filter = ""
    #     score_filter = 0
    #     media_format_filter = ["TV"]
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)
        
    #     result = True
    #     if not searches:
    #         result = False
    #     for anime in searches:
    #         if anime['format'] != media_format_filter[0]:
    #             result = False
    #     self.assertEqual(True, result)


    # def test_search_anime_source(self):
    #     '''Searches only by score and checks if returned anime have greater score'''

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "popularity dec"
    #     genre_filter = ""
    #     score_filter = 0
    #     media_format_filter = []
    #     media_source_filter = ["MANGA"]
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)
        
    #     result = True
    #     if not searches:
    #         result = False
    #     for anime in searches:
    #         if anime['source'] != media_source_filter[0]:
    #             result = False
    #     self.assertEqual(True, result)


    # def test_search_anime_score(self):
    #     '''Searches only by score and checks if returned anime have greater score'''

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "popularity dec"
    #     genre_filter = ""
    #     score_filter = 50
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)
        
    #     result = True
    #     if not searches:
    #         result = False
    #     for anime in searches:
    #             if anime['meanScore'] <= score_filter:
    #                 result = False
    #     self.assertEqual(True, result)

    
    # def test_search_anime_genre_and_score(self):
    #     '''Tests to see if genre filter and score filter work together'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "popularity dec"
    #     genre_filter = ["Action"]
    #     score_filter = 50
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for anime in searches:
    #             if genre_filter[0] not in anime['genres'] or anime['meanScore'] <= score_filter:
    #                 result = False
    #     self.assertEqual(True, result)


    # def test_search_anime_name_and_genre(self):
    #     '''Tests to see if search and genre filter work together, should return nothing'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = "Death Note"
    #     sort_method = "popularity dec"
    #     genre_filter = ["Action"]
    #     score_filter = 50
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)
    #     result = True
    #     for anime in searches:
    #             if genre_filter[0] not in anime['genres'] or title not in anime['title']['userPreferred'] or title not in anime['description']:
    #                 result = False
    #     self.assertEqual(True, result)


    # def test_search_anime_name_and_genre_and_score(self):
    #     '''Tests to see if search, genre, and score filter work together'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = "Death Note"
    #     sort_method = "popularity dec"
    #     genre_filter = ["Mystery"]
    #     score_filter = 50
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)       
    #     result = True
    #     if not searches:
    #         result = False
    #     for anime in searches:
    #             if title not in anime['title']['userPreferred'] or genre_filter[0] not in anime['genres'] or anime['meanScore'] < score_filter:
    #                 result = False
    #     self.assertEqual(True, result)


    # def test_sort_anime_pop_decreasing(self):
    #     '''Tests to see if returned result is sorted by decreasing popularity'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "popularity dec"
    #     genre_filter = ""
    #     media_format_filter = []
    #     media_source_filter = []
    #     score_filter = 0
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)       
    #     animelist = []
    #     for anime in searches:
    #         animelist.append(anime)
    #     result = False

    #     if(all(animelist[i]['popularity'] >= animelist[i + 1]['popularity'] for i in range(len(animelist) - 1))):
    #         result = True
    #     if not searches:
    #         result = False
    #     self.assertEqual(True, result)


    # def test_sort_anime_pop_increasing(self):
    #     '''Tests to see if returned result is sorted by increasing popularity'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "popularity inc"
    #     genre_filter = ""
    #     score_filter = 0
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)       
    #     animelist = []
    #     for anime in searches:
    #         animelist.append(anime)
    #     result = False

    #     if(all(animelist[i]['popularity'] <= animelist[i + 1]['popularity'] for i in range(len(animelist)-1))):
    #         result = True

    #     if not searches:
    #         result = False
    #     self.assertEqual(True, result)


    # def test_sort_anime_alphabetical(self):
    #     '''Tests to see if returned result is sorted alphabetically'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "alphabetical"
    #     genre_filter = ""
    #     score_filter = 0
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)       
    #     animelist = []
    #     for anime in searches:
    #         animelist.append(anime)
    #     result = False
        
    #     if(all(animelist[i]['title']['userPreferred'].lower() <= animelist[i + 1]['title']['userPreferred'].lower() for i in range(len(animelist)-1))):
    #         result = True
    #     if not searches:
    #         result = False
    #     self.assertEqual(True, result)


    # def test_sort_anime_reverse_alphabetical(self):
    #     '''Tests to see if returned result is sorted in reverse alphabetical order'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "rev alphabetical"
    #     genre_filter = ""
    #     score_filter = 0
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)       
    #     animelist = []
    #     for anime in searches:
    #         animelist.append(anime)
        
    #     result = True
    #     if(all(animelist[i]['title']['userPreferred'].lower() >= animelist[i + 1]['title']['userPreferred'].lower() for i in range(len(animelist)-1))):
    #         result = True
    #     if not searches:
    #         result = False
    #     self.assertEqual(True, result)


    # def test_sort_anime_score_decreasing(self):
    #     '''Test to see if returned result is sorted by decreasing score'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "score dec"
    #     genre_filter = ""
    #     score_filter = 0
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)       
    #     animelist = []
    #     for anime in searches:
    #         animelist.append(anime)
        
    #     result = False
    #     if(all(animelist[i]['meanScore'] >= animelist[i + 1]['meanScore'] for i in range(len(animelist)-1))):
    #         result = True
    #     if not searches:
    #         result = False
    #     self.assertEqual(True, result)


    # def test_sort_anime_score_increasing(self):
    #     '''Test to see if returned result is sorted by increasing score'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "score inc"
    #     genre_filter = ""
    #     score_filter = 0
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)       
    #     animelist = []
    #     for anime in searches:
    #         animelist.append(anime)
        
    #     result = False
    #     if(all(animelist[i]['meanScore'] <= animelist[i + 1]['meanScore'] for i in range(len(animelist)-1))):
    #         result = True
    #     if not searches:
    #         result = False
    #     self.assertEqual(True, result)

    # def test_sort_anime_score_increasing_and_genre(self):
    #     '''Test to see if returned result is sorted by increasing score'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "score inc"
    #     genre_filter = ["Action"]
    #     score_filter = 0
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)       
    #     animelist = []
    #     for anime in searches:
    #         animelist.append(anime)
        
    #     result = False
    #     if(all(animelist[i]['meanScore'] <= animelist[i + 1]['meanScore'] and genre_filter[0] in animelist[i]['genres']for i in range(len(animelist)-1))):
    #         result = True
    #     if not searches:
    #         result = False
    #     self.assertEqual(True, result)

    
    # def test_sort_anime_score_decreasing_and_genre(self):
    #     '''Test to see if returned result is sorted by increasing score'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.anime
    #     title = ""
    #     sort_method = "score dec"
    #     genre_filter = ["Action"]
    #     score_filter = 0
    #     media_format_filter = []
    #     media_source_filter = []
    #     searches = SSF.search_anime_name(database, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter)       
    #     animelist = []
    #     for anime in searches:
    #         animelist.append(anime)
        
    #     result = False
    #     if(all(animelist[i]['meanScore'] >= animelist[i + 1]['meanScore'] and genre_filter[0] in animelist[i]['genres'] for i in range(len(animelist)-1))):
    #         result = True
    #     if not searches:
    #         result = False
    #     self.assertEqual(True, result)


    # def test_search_character_name(self):
    #     '''Tests if search entry is a substring of all search results'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
    #     database = client.anilist.characters
    #     title = "Kakashi" 
    #     sort_method = "popularity dec (char)"
    #     direction = "Greater than"
    #     field_filter = []
    #     score_filter = 0
    #     language_filter = []
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #         titleCharSearched = char['name']['full'].lower()
    #         if title not in titleCharSearched:
    #             result = False
    #     self.assertEqual(True, result)


    # def test_search_character_animeography_less_than(self):
    #     ''' Searches by animeography less than score of 7 '''

    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length"]
    #     score_filter = 7
    #     language_filter = ""
    #     direction = "Less than"
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #             if char['animeography_length'] > score_filter:
    #                 result = False
    #     self.assertEqual(True, result)

    
    # def test_search_character_animeography_greater_than(self):
    #     ''' Searches by animeography, greater than score of 7'''

    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length"]
    #     score_filter = 7
    #     language_filter = []
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #             if char['animeography_length'] < score_filter:
    #                 result = False
    #     self.assertEqual(True, result)


    # def test_search_character_mangaography_less_than(self):
    #     ''' Searches by mangaography less than score of 7 '''

    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["mangaography_length"]
    #     score_filter = 7
    #     language_filter = ""
    #     direction = "Less than"
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #             if char['mangaography_length'] > score_filter:
    #                 result = False
    #     self.assertEqual(True, result)

    
    # def test_search_character_mangaography_greater_than(self):
    #     ''' Searches by mangaography greater than score of 7'''

    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["mangaography_length"]
    #     score_filter = 7
    #     language_filter = ""
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #             if char['mangaography_length'] < score_filter:
    #                 result = False
    #     self.assertEqual(True, result)

    
    # def test_search_character_language(self):
    #     '''Tests to see if returned results are filtered by provided language properly'''
 
    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = []
    #     score_filter = 0
    #     language_filter = ["JAPANESE"]
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #             if char['voiceActor_language'] not in language_filter:
    #                 result = False
    #     self.assertEqual(True, result)


    # def test_search_character_language_2(self):
    #     '''Tests to see if returned results are filtered by provided language properly'''
 
    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = [""]
    #     score_filter = 0
    #     language_filter = ["ENGLISH"]
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #             if char['voiceActor_language'] not in language_filter:
    #                 result = False
    #     self.assertEqual(True, result)


    # def test_search_character_animeography_and_mangaography_less_than(self):
        
    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length","mangaography_length"]
    #     score_filter = 4
    #     language_filter = ""
    #     direction = "Less than"
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #             if char['mangaography_length'] > score_filter or char['animeography_length'] > score_filter:
    #                 result = False
    #     self.assertEqual(True, result)        


    # def test_search_character_animeography_and_mangaography_greater_than(self):
        
    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length","mangaography_length"]
    #     score_filter = 0
    #     language_filter = ""
    #     direction = "Greater than"
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     if not searches:
    #         result = False
    #     result = True
    #     for char in searches:
    #             if char['mangaography_length'] < score_filter or char['animeography_length'] < score_filter:
    #                 result = False
    #     self.assertEqual(True, result)        

   
    # def test_search_character_language_and_animeography_greater_than(self):
    #     '''Tests to see if language and animegraphy filters work together with score of 7'''
 
    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length"]
    #     score_filter = 7
    #     language_filter = ["JAPANESE"]
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #             if char['voiceActor_language'] not in language_filter or char['animeography_length'] < score_filter:
    #                 result = False
    #     self.assertEqual(True, result)


    # def test_search_character_language_and_animeography_less_than(self):
    #     '''Tests to see if language and animegraphy filters work together with score of 7'''
 
    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length"]
    #     score_filter = 7
    #     language_filter = ["JAPANESE"]
    #     direction = "Less than"
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #             if char['voiceActor_language'] not in language_filter or char['animeography_length'] > score_filter:
    #                 result = False
    #     self.assertEqual(True, result)


    # def test_search_character_language_and_mangaography_greater_than(self):
    #     '''Tests to see if language and animegraphy filters work together with score of 7'''
 
    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["mangaography_length"]
    #     score_filter = 7
    #     language_filter = ["JAPANESE"]
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     for char in searches:
    #             if char['voiceActor_language'] not in language_filter or char['mangaography_length'] < score_filter:
    #                 result = False
    #     self.assertEqual(True, result)


    # def test_search_character_language_and_mangaography_less_than(self):
    #     '''Tests to see if language and animegraphy filters work together with score of 7'''
 
    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["mangaography_length"]
    #     score_filter = 7
    #     language_filter = ["JAPANESE"]
    #     direction = "Less than"
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #             if char['voiceActor_language'] not in language_filter or char['mangaography_length'] > score_filter:
    #                 result = False
    #     self.assertEqual(True, result)


    # def test_search_character_language_and_animeography_and_mangaography_less_than(self):
    #     '''Tests to see if language, animeography, and mangaography filters work together with score of 5'''
 
    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length","mangaography_length"]
    #     score_filter = 5
    #     language_filter = ["JAPANESE"]
    #     direction = "Less than"
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #             if char['voiceActor_language'] not in language_filter or char['mangaography_length'] > score_filter or char['animeography_length'] > score_filter:
    #                 result = False
    #     self.assertEqual(True, result)

        
    # def test_search_character_language_and_animeography_and_mangaography_greater_than(self):
    #     '''Tests to see if language, animeography, and mangaography filters work together with score of 9'''
 
    #     warnings.filterwarnings("ignore")
    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length","mangaography_length"]
    #     score_filter = 9
    #     language_filter = ["JAPANESE"]
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     result = True
    #     if not searches:
    #         result = False
    #     for char in searches:
    #             if char['voiceActor_language'] not in language_filter or char['mangaography_length'] < score_filter or char['animeography_length'] < score_filter:
    #                 result = False
    #     self.assertEqual(True, result)


    # def test_sort_character_pop_decreasing(self):
    #     '''Tests to see if returned result is sorted by decreasing popularity'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = []
    #     score_filter = 0
    #     language_filter = []
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     charlist = []
    #     for char in searches:
    #         charlist.append(char)
        
    #     result = False
    #     if(all(charlist[i]['favourites'] >= charlist[i + 1]['favourites'] for i in range(len(charlist) - 1))):
    #         result = True

    #     if not searches:
    #         result = False

    #     self.assertEqual(True, result)


    # def test_sort_character_pop_increasing(self):
    #     '''Tests to see if returned result is sorted by increasing popularity'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity inc (char)"
    #     field_filter = []
    #     score_filter = 0
    #     language_filter = []
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     charlist = []
    #     for char in searches:
    #         charlist.append(char)
        
    #     result = False
    #     if(all(charlist[i]['favourites'] <= charlist[i + 1]['favourites'] for i in range(len(charlist) - 1))):
    #         result = True

    #     if not searches:
    #         result = False
    #     self.assertEqual(True, result)


    # def test_sort_character_alphabetical(self):
    #     '''Tests to see if returned result is sorted alphabetically'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "alphabetical (char)"
    #     field_filter = []
    #     score_filter = 0
    #     language_filter = []
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     charlist = []
    #     for char in searches:
    #         charlist.append(char)
        
    #     result = False
    #     if(all(charlist[i]['name']['full'].lower() <= charlist[i + 1]['name']['full'].lower() for i in range(len(charlist) - 1))):
    #         result = True

    #     if not searches:
    #         result = False
    #     self.assertEqual(True, result)


    # def test_sort_character_reverse_alphabetical(self):
    #     '''Tests to see if returned result is sorted reverse alphabetically'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "rev alphabetical (char)"
    #     field_filter = []
    #     score_filter = 0
    #     language_filter = []
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     charlist = []
    #     for char in searches:
    #         charlist.append(char)
        
    #     result = False
    #     if(all(charlist[i]['name']['full'].lower() >= charlist[i + 1]['name']['full'].lower() for i in range(len(charlist) - 1))):
    #         result = True

    #     if not searches:
    #         result = False

    #     self.assertEqual(True, result)

        
    # def test_character_sort_and_language(self):
    #     '''Tests to see if returned result is sorted by decreasing popularity and filtered by language'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = []
    #     score_filter = 0
    #     language_filter = ["JAPANESE"]
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     charlist = []
    #     for char in searches:
    #         charlist.append(char)
        
    #     result = False
    #     if(all(charlist[i]['favourites'] >= charlist[i + 1]['favourites'] for i in range(len(charlist) - 1))):
    #         result = True
    #     for char in searches:
    #         if char['voiceActor_language'] not in language_filter:
    #             result = False

    #     if not searches:
    #         result = False

    #     self.assertEqual(True, result)


    # def test_character_sort_and_field_greater_than(self):
    #     '''Tests to see if returned result is sorted by decreasing popularity and filtered by fields'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length"]
    #     score_filter = 11
    #     language_filter = []
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     charlist = []
    #     for char in searches:
    #         charlist.append(char)
        
    #     result = False
    #     if(all(charlist[i]['favourites'] >= charlist[i + 1]['favourites'] for i in range(len(charlist) - 1))):
    #         result = True
    #     for char in searches:
    #         if char['animeography_length'] < score_filter:
    #             result = False

    #     if not searches:
    #         result = False

    #     self.assertEqual(True, result)


    # def test_character_sort_and_field_less_than(self):
    #     '''Tests to see if returned result is sorted by decreasing popularity and filtered by fields'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length"]
    #     score_filter = 11
    #     language_filter = []
    #     direction = "Less than"
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     charlist = []
    #     for char in searches:
    #         charlist.append(char)
        
    #     result = False
    #     if(all(charlist[i]['favourites'] >= charlist[i + 1]['favourites'] for i in range(len(charlist) - 1))):
    #         result = True
    #     for char in searches:
    #         if char['animeography_length'] > score_filter:
    #             result = False
    #     if not searches:
    #         result = False

    #     self.assertEqual(True, result)


    # def test_character_sort_and_field_and_language_greater_than(self):
    #     '''Tests to see if returned result is sorted by decreasing popularity and filtered by fields and language'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length"]
    #     score_filter = 11
    #     language_filter = ["ENGLISH"]
    #     direction = "Greater than"
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     charlist = []
    #     for char in searches:
    #         charlist.append(char)
        
    #     result = False
    #     if(all(charlist[i]['favourites'] >= charlist[i + 1]['favourites'] for i in range(len(charlist) - 1))):
    #         result = True
    #     for char in searches:
    #         if char['animeography_length'] < score_filter or char['voiceActor_language'] not in language_filter:
    #             result = False
    #     if not searches:
    #         result = False
    
    #     self.assertEqual(True, result)


    # def test_character_sort_and_field_and_language_less_than(self):
    #     '''Tests to see if returned result is sorted by decreasing popularity and filtered by fields and language'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = ""
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length"]
    #     score_filter = 11
    #     language_filter = ["ENGLISH"]
    #     direction = ['Less than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     charlist = []
    #     for char in searches:
    #         charlist.append(char)
    #     result = False
    #     if(all(charlist[i]['favourites'] >= charlist[i + 1]['favourites'] for i in range(len(charlist) - 1))):
    #         result = True
    #     for char in searches:
    #         if char['animeography_length'] > score_filter or char['voiceActor_language'] not in language_filter:
    #             result = False

    #     self.assertEqual(True, result)


    # def test_search_character_sort_and_field_and_language_greater_than(self):
    #     '''Tests to see if returned result is sorted by decreasing popularity and filtered by fields and language'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = "as"
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length"]
    #     score_filter = 11
    #     language_filter = ["ENGLISH"]
    #     direction = ['Greater than']
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     if not searches:
    #         result = False
    #     charlist = []
    #     for char in searches:
    #         charlist.append(char)
        
    #     result = False
    #     if(all(charlist[i]['favourites'] >= charlist[i + 1]['favourites'] for i in range(len(charlist) - 1))):
    #         result = True
    #     for char in searches:
    #         if title not in char['name']['full'] or char['animeography_length'] < score_filter or char['voiceActor_language'] not in language_filter:
    #             result = False

    #     self.assertEqual(True, result)


    # def test_search_character_sort_and_field_and_language_less_than(self):
    #     '''Tests to see if search works with all the filters'''
    #     warnings.filterwarnings("ignore")

    #     client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
    #     database = client.anilist.characters
    #     title = "kakashi"
    #     sort_method = "popularity dec (char)"
    #     field_filter = ["animeography_length"]
    #     score_filter = 11
    #     language_filter = ["ENGLISH"]
    #     direction = "Less than"
    #     searches = SSF.search_char_name(database, title, sort_method, direction, field_filter, score_filter, language_filter)
    #     if not searches:
    #         result = False        
    #     charlist = []
    #     for char in searches:
    #         charlist.append(char)
        
    #     result = False
    #     if(all(charlist[i]['favourites'] >= charlist[i + 1]['favourites'] for i in range(len(charlist) - 1))):
    #         result = True
    #     for char in searches:
    #         if title not in char['name']['full'] or char['animeography_length'] > score_filter or char['voiceActor_language'] not in language_filter:
    #             result = False

    #     self.assertEqual(True, result)


    def test_search_staff_name(self):
        '''Tests if search entry is a substring of all search results'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "hi" 
        sort_method = "popularity dec (staff)"
        direction = "Greater than"
        field_filter = []
        score_filter = 0
        language_filter = []
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            titleStaffSearched = staff['name']['full'].lower()
            if title not in titleStaffSearched:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_char_voiced_less_than(self):
        '''Tests if filter by less than 10 haracters voiced returns correct results'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Less than"
        field_filter = ["characters_voiced"]
        score_filter = 10
        language_filter = []
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['characters_voiced'] > score_filter:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_char_voiced_greater_than(self):
        '''Tests if filter by less than 10 haracters voiced returns correct results'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Greater than"
        field_filter = ["characters_voiced"]
        score_filter = 10
        language_filter = []
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['characters_voiced'] < score_filter:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_productions_less_than(self):
        '''Tests if filter by less than production roles works'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Less than"
        field_filter = ["production_roles"]
        score_filter = 10
        language_filter = []
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['production_roles'] > score_filter:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_productions_greater_than(self):
        '''Tests if filter by less than production roles works'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Greater than"
        field_filter = ["production_roles"]
        score_filter = 10
        language_filter = []
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['production_roles'] < score_filter:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_language(self):
        '''Tests if filter by less than production roles works'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Greater than"
        field_filter = []
        score_filter = 0
        language_filter = ["ENGLISH"]
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['language'] != language_filter[0]:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_char_voiced_and_productions_less_than(self):
        '''Tests if filter by less than production roles works'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Less than"
        field_filter = ["characters_voiced","production_roles"]
        score_filter = 10
        language_filter = []
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['production_roles'] > score_filter or staff['characters_voiced'] > score_filter:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_char_voiced_and_productions_greater_than(self):
        '''Tests if filter by less than production roles works'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "greater than"
        field_filter = ["characters_voiced","production_roles"]
        score_filter = 10
        language_filter = []
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['production_roles'] < score_filter or staff['characters_voiced'] < score_filter:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_language_and_char_voiced_greater_than(self):
        '''Tests if filter by less than production roles works'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Less than"
        field_filter = ["characters_voiced"]
        score_filter = 10
        language_filter = ["ENGLISH"]
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['language'] != language_filter[0] or staff['characters_voiced'] > score_filter:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_language_and_char_voiced_less_than(self):
        '''Tests if filter by less than production roles works'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Greater than"
        field_filter = ["characters_voiced"]
        score_filter = 10
        language_filter = ["ENGLISH"]
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['language'] != language_filter[0] or staff['characters_voiced'] < score_filter:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_language_and_char_voiced_greater_than(self):
        '''Tests if filter by less than production roles works'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Greater than"
        field_filter = ["characters_voiced"]
        score_filter = 10
        language_filter = ["ENGLISH"]
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['language'] != language_filter[0] or staff['characters_voiced'] < score_filter:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_language_and_production_less_than(self):
        '''Tests if filter by less than production roles works'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Less than"
        field_filter = ["production_roles"]
        score_filter = 10
        language_filter = ["ENGLISH"]
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['language'] != language_filter[0] or staff['production_roles'] > score_filter:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_language_and_production_greater_than(self):
        '''Tests if filter by less than production roles works'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Greater than"
        field_filter = ["production_roles"]
        score_filter = 10
        language_filter = ["ENGLISH"]
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['language'] != language_filter[0] or staff['production_roles'] < score_filter:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_language_and_char_voiced_and_production_greater_than(self):
        '''Tests if filter by less than production roles works'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Greater than"
        field_filter = ["characters_voiced","production_roles"]
        score_filter = 10
        language_filter = ["ENGLISH"]
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['language'] != language_filter[0] or staff['production_roles'] < score_filter or staff['characters_voiced'] < score_filter:
                result = False
        self.assertEqual(True, result)

    
    def test_search_staff_language_and_char_voiced_and_production_less_than(self):
        '''Tests if filter by less than production roles works'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        
        database = client.anilist.staff
        title = "" 
        sort_method = "popularity dec (staff)"
        direction = "Less than"
        field_filter = ["characters_voiced","production_roles"]
        score_filter = 10
        language_filter = ["ENGLISH"]
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        result = True
        if not searches:
            result = False
        for staff in searches:
            if staff['language'] != language_filter[0] or staff['production_roles'] > score_filter or staff['characters_voiced'] > score_filter:
                result = False
        self.assertEqual(True, result)
        

    def test_sort_staff_pop_decreasing(self):
        '''Tests to see if returned result is sorted by decreasing popularity'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        database = client.anilist.staff
        title = ""
        sort_method = "popularity dec (staff)"
        field_filter = []
        score_filter = 0
        language_filter = []
        direction = ""
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        stafflist = []
        for staff in searches:
            stafflist.append(staff)
        
        result = False
        if(all(stafflist[i]['favourites'] >= stafflist[i + 1]['favourites'] for i in range(len(stafflist) - 1))):
            result = True

        if not searches:
            result = False

        self.assertEqual(True, result)


    def test_sort_staff_pop_increasing(self):
        '''Tests to see if returned result is sorted by decreasing popularity'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        database = client.anilist.staff
        title = ""
        sort_method = "popularity inc (staff)"
        field_filter = []
        score_filter = 0
        language_filter = []
        direction = "Greater than"
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        stafflist = []
        for staff in searches:
            stafflist.append(staff)
        
        result = False
        if(all(stafflist[i]['favourites'] <= stafflist[i + 1]['favourites'] for i in range(len(stafflist) - 1))):
            result = True

        if not searches:
            result = False

        self.assertEqual(True, result)


    def test_sort_staff_alphabetical(self):
        '''Tests to see if returned result is sorted by decreasing popularity'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        database = client.anilist.staff
        title = ""
        sort_method = "alphabetical (staff)"
        field_filter = []
        score_filter = 0
        language_filter = []
        direction = "Greater than"
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        stafflist = []
        for staff in searches:
            stafflist.append(staff)
        
        result = True
        if(all(stafflist[i]['name']['full'].lower() <= stafflist[i + 1]['name']['full'].lower() for i in range(len(stafflist) - 2))):
            result = True


        self.assertEqual(True, result)


    def test_sort_staff_reverse_alphabetical(self):
        '''Tests to see if returned result is sorted by decreasing popularity'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        database = client.anilist.staff
        title = ""
        sort_method = "rev alphabetical (staff)"
        field_filter = []
        score_filter = 0
        language_filter = []
        direction = "Greater than"
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        stafflist = []
        for staff in searches:
            stafflist.append(staff)
        
        result = False
        if(all(stafflist[i]['name']['full'].lower() >= stafflist[i + 1]['name']['full'].lower() for i in range(len(stafflist) - 1))):
            result = True

        if not searches:
            result = False

        self.assertEqual(True, result)


    def test_staff_sort_and_language(self):
        '''Tests to see if returned result is sorted by decreasing popularity'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        database = client.anilist.staff
        title = ""
        sort_method = "popularity dec (staff)"
        field_filter = []
        score_filter = 0
        language_filter = ["ENGLISH"]
        direction = ""
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        stafflist = []
        for staff in searches:
            stafflist.append(staff)
        
        result = False
        if(all(stafflist[i]['favourites'] >= stafflist[i + 1]['favourites'] and stafflist[i]['language'] == language_filter[0] for i in range(len(stafflist) - 1))):
            result = True

        if not searches:
            result = False

        self.assertEqual(True, result)

    
    def test_staff_sort_and_field_less_than(self):
        '''Tests to see if returned result is sorted by decreasing popularity'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        database = client.anilist.staff
        title = ""
        sort_method = "popularity dec (staff)"
        field_filter = ["characters_voiced"]
        score_filter = 10
        language_filter = []
        direction = "Less than"
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        stafflist = []
        for staff in searches:
            stafflist.append(staff)
        
        result = False
        if(all(stafflist[i]['favourites'] >= stafflist[i + 1]['favourites'] and stafflist[i]['characters_voiced'] <= score_filter 
            for i in range(len(stafflist) - 1))):
            result = True

        if not searches:
            result = False

        self.assertEqual(True, result)


    def test_staff_sort_and_field_greater_than(self):
        '''Tests to see if returned result is sorted by decreasing popularity'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        database = client.anilist.staff
        title = ""
        sort_method = "popularity dec (staff)"
        field_filter = ["characters_voiced"]
        score_filter = 10
        language_filter = []
        direction = "Greater than"
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        stafflist = []
        for staff in searches:
            stafflist.append(staff)
        
        result = False
        if(all(stafflist[i]['favourites'] >= stafflist[i + 1]['favourites'] and stafflist[i]['characters_voiced'] >= score_filter 
            for i in range(len(stafflist) - 1))):
            result = True

        if not searches:
            result = False

        self.assertEqual(True, result)


    def test_staff_sort_and_field_and_language_less_than(self):
        '''Tests to see if returned result is sorted by decreasing popularity'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        database = client.anilist.staff
        title = ""
        sort_method = "popularity dec (staff)"
        field_filter = ["characters_voiced"]
        score_filter = 10
        language_filter = ["ENGLISH"]
        direction = "Less than"
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        stafflist = []
        for staff in searches:
            stafflist.append(staff)
        
        result = False
        if(all(stafflist[i]['favourites'] >= stafflist[i + 1]['favourites'] and stafflist[i]['characters_voiced'] <= score_filter 
            and stafflist[i]['language'] == language_filter[0] for i in range(len(stafflist) - 1))):
            result = True

        if not searches:
            result = False

        self.assertEqual(True, result)


    def test_staff_sort_and_field_and_language_greater_than(self):
        '''Tests to see if returned result is sorted by decreasing popularity'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        database = client.anilist.staff
        title = ""
        sort_method = "popularity dec (staff)"
        field_filter = ["characters_voiced"]
        score_filter = 10
        language_filter = ["ENGLISH"]
        direction = "Greater than"
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        stafflist = []
        for staff in searches:
            stafflist.append(staff)
        
        result = False
        if(all(stafflist[i]['favourites'] >= stafflist[i + 1]['favourites'] and stafflist[i]['characters_voiced'] >= score_filter 
            and stafflist[i]['language'] == language_filter[0] for i in range(len(stafflist) - 1))):
            result = True

        if not searches:
            result = False

        self.assertEqual(True, result)


    def test_search_staff_sort_and_field_and_language_less_than(self):
        '''Tests to see if returned result is sorted by decreasing popularity'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        database = client.anilist.staff
        title = ""
        sort_method = "popularity dec (staff)"
        field_filter = ["characters_voiced"]
        score_filter = 10
        language_filter = ["ENGLISH"]
        direction = "Less than"
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        stafflist = []
        for staff in searches:
            stafflist.append(staff)
        
        result = False
        if(all(stafflist[i]['favourites'] >= stafflist[i + 1]['favourites'] for i in range(len(stafflist) - 1))):
            result = True

        if not searches:
            result = False

        for staff in searches:
            if staff['language'] != language_filter[0] or title not in staff['name']['full'].lower() or staff['characters_voiced'] > score_filter:
                result = False
        self.assertEqual(True, result)


    def test_search_staff_sort_and_field_and_language_greater_than(self):
        '''Tests to see if returned result is sorted by decreasing popularity'''
        warnings.filterwarnings("ignore")

        client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
        database = client.anilist.staff
        title = ""
        sort_method = "popularity dec (staff)"
        field_filter = ["characters_voiced"]
        score_filter = 10
        language_filter = ["ENGLISH"]
        direction = "Greater"
        searches = SSF.search_staff_name(database, title, sort_method, language_filter, field_filter, score_filter, direction)
        stafflist = []
        for staff in searches:
            stafflist.append(staff)
        
        result = False
        if(all(stafflist[i]['favourites'] >= stafflist[i + 1]['favourites'] for i in range(len(stafflist) - 1))):
            result = True

        if not searches:
            result = False

        for staff in searches:
            if staff['language'] != language_filter[0] or title not in staff['name']['full'].lower() or staff['characters_voiced'] < score_filter:
                result = False
        self.assertEqual(True, result)


if __name__ == '__main__':
    unittest.main()