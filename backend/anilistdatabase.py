import mongoengine
import string
from pymongo import MongoClient


def databasequery_pageanime_popularity(client : MongoClient, numResults):
    ''' Gets a list of numResults size of popular anime from our database '''
    anime_collection = client.anilist.anime
    #popular_list = anime_collection.find().limit(numResults)
    popular_list = anime_collection.find({}).sort('popularity',-1).limit(100)
    popular_list = list(popular_list)
    return popular_list


def databasequery_anime_name(client : MongoClient, name):
    ''' Searches our database for a singular anime by its name. Probably should switch to searching by IDs for everything soon '''
    anime_collection = client.anilist.anime
    anime = anime_collection.find({'title.english':name}).limit(1)
    return anime[0]


def databasequery_anime_idMal(client : MongoClient, idMal):
    ''' Searches our database for a singular anime by its id '''
    anime_collection = client.anilist.anime
    anime = anime_collection.find({'idMal':idMal}).limit(1)
    return anime[0]


def databasequery_pagechar_popularity(client : MongoClient, numResults):
    ''' Gets a list of numResults size of popular characters from our database '''
    char_collection = client.anilist.characters
    popular_list = char_collection.find().sort('favourites',-1).limit(numResults)
    popular_list = list(popular_list) # for some reason has to be made a list to show descriptions?
    return popular_list


def databasequery_char_name(client : MongoClient, name):
    ''' Searches our database for a singular character by its name '''
    char_collection = client.anilist.characters
    char = char_collection.find({'name.full':name}).limit(1)
    return char[0]


def databasequery_char_id(client : MongoClient, id):
    ''' Searches our database for a singular character by its id '''
    char_collection = client.anilist.characters
    char = char_collection.find({'id':id}).limit(1)
    return char[0]


def databasequery_pagestudio_popularity(client : MongoClient, numResults):
    ''' Gets a list of numResults size of popular studios from our database '''
    studio_collection = client.anilist.studios
    popular_list = studio_collection.find().sort('favourites',-1).limit(numResults)
    popular_list = list(popular_list) # for some reason studios only works if made a list???
    return popular_list

def databasequery_studio_name(client : MongoClient, name):
    ''' Searches our database for a singular studio by its name '''
    studio_collection = client.anilist.studios
    studio = studio_collection.find({'name':name}).limit(1)
    return studio[0]

def databasequery_studio_id(client : MongoClient, id):
    ''' Searches our database for a singular studio by its id '''
    studio_collection = client.anilist.studios
    studio = studio_collection.find({'id':id}).limit(1)
    return studio[0]


def databasequery_pagestaff_popularity(client : MongoClient, numResults):
    ''' Gets a list of numResults size of popular staff from our database '''
    staff_collection = client.anilist.staff
    popular_list = staff_collection.find().sort('favourites',-1).limit(numResults)
    popular_list = list(popular_list) # for some reason studios only works if made a list???
    return popular_list

def databasequery_staff_id(client : MongoClient, id):
    ''' Searches our database for a singular staff by its id '''
    staff_collection = client.anilist.staff
    staff = staff_collection.find({'id':id}).limit(1)
    return staff[0]


''' Phase 3 atlas search stuff starts here '''

def databasesearch_anime_title(client : MongoClient, title, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter):
    ''' Searches by inputted anime title '''
    anime_collection = client.anilist.anime

    sort_and_dir = find_sort_method(sort_method)
    sort = sort_and_dir[0]
    direction = sort_and_dir[1]

    # make case if no genre filters selected, then just return everything
    if len(genre_filter) != 0: 
        genre_filter_type = '$all'
    else:
        genre_filter_type = '$ne'

    if len(media_format_filter) != 0: 
        media_format_filter_type = '$in'
    else:
        media_format_filter_type = '$ne'

    if len(media_source_filter) != 0: 
        media_source_filter_type = '$in'
    else:
        media_source_filter_type = '$ne'
        
    try:
        if sort_method == "newest to oldest" or sort_method == "oldest to newest": # case when sort by date    
            search_and_filter = anime_collection.find({
                "meanScore": {'$gte':int(score_filter)}, # filter greater than or equal to selected score
                "genres": {genre_filter_type: genre_filter}, # filter generes
                "format": {media_format_filter_type:media_format_filter}, # filter by media type
                "source": {media_source_filter_type:media_source_filter}, # filter by source type}
                '$or': [ # query from different title fields, EX: attack on titan and shingeki no kyojin should return same animes
                {"title.english": {"$regex": title,"$options":"i"}}, 
                {"title.romaji": {"$regex": title,"$options":"i"}},
                {"title.userPreferred": {"$regex": title,"$options":"i"}},
                #{"description": {"$regex": title,"$options":"i"}}
                ]}).sort([
                    (sort[0],direction), # year
                    (sort[1],direction), # month
                    (sort[2],direction) # day
                ]).limit(100)
        else:
            search_and_filter = anime_collection.find({
                "meanScore": {'$gte':int(score_filter)}, # filter greater than or equal to selected score
                "genres": {genre_filter_type: genre_filter}, # filter generes
                "format": {media_format_filter_type:media_format_filter}, # filter by media type
                "source": {media_source_filter_type:media_source_filter}, # filter by source type}
                '$or': [ # query from different title fields, EX: attack on titan and shingeki no kyojin should return same animes
                {"title.english": {"$regex": title,"$options":"i"}}, 
                {"title.romaji": {"$regex": title,"$options":"i"}},
                {"title.userPreferred": {"$regex": title,"$options":"i"}},
                #{"description": {"$regex": title,"$options":"i"}}
                ]}).collation({'locale':'en'}).sort(sort,direction).limit(100)

        list_search_and_filter = list(search_and_filter)
        len_list = len(list_search_and_filter)
        #print(len_list)
        if len_list != 0:
            return list_search_and_filter

    
        # RETRY QUERY SEARCHING DESCRIPTIONS THIS TIME
        if sort_method == "newest to oldest" or sort_method == "oldest to newest": # case when sort by date    
            search_and_filter = anime_collection.find({
                "meanScore": {'$gte':int(score_filter)}, # filter greater than or equal to selected score
                "genres": {genre_filter_type: genre_filter}, # filter generes
                "format": {media_format_filter_type:media_format_filter}, # filter by media type
                "source": {media_source_filter_type:media_source_filter}, # filter by source type}
                '$or': [ # query from different title fields, EX: attack on titan and shingeki no kyojin should return same animes
                #{"title.english": {"$regex": title,"$options":"i"}}, 
                #{"title.romaji": {"$regex": title,"$options":"i"}},
                #{"title.userPreferred": {"$regex": title,"$options":"i"}},
                {"description": {"$regex": title,"$options":"i"}}
                ]}).sort([
                    (sort[0],direction), # year
                    (sort[1],direction), # month
                    (sort[2],direction) # day
                ]).limit(100)
        else:
            search_and_filter = anime_collection.find({
                "meanScore": {'$gte':int(score_filter)}, # filter greater than or equal to selected score
                "genres": {genre_filter_type: genre_filter}, # filter generes
                "format": {media_format_filter_type:media_format_filter}, # filter by media type
                "source": {media_source_filter_type:media_source_filter}, # filter by source type}
                '$or': [ # query from different title fields, EX: attack on titan and shingeki no kyojin should return same animes
                #{"title.english": {"$regex": title,"$options":"i"}}, 
                #{"title.romaji": {"$regex": title,"$options":"i"}},
                #{"title.userPreferred": {"$regex": title,"$options":"i"}},
                {"description": {"$regex": title,"$options":"i"}}
                ]}).collation({'locale':'en'}).sort(sort,direction).limit(100)

        return list(search_and_filter)
    except:
        return []

def databasesearch_char_name(client : MongoClient, name, sort_method, directional_filter, field_filter, score_filter, language_filter):
    ''' Searches by inputted char name '''
    char_collection = client.anilist.characters

    sort_and_dir = find_sort_method(sort_method)
    sort = sort_and_dir[0]
    direction = sort_and_dir[1]
    filterTitle = ""

    if len(language_filter) != 0: 
        language_filter_type = '$all'
    else:
        language_filter_type = '$ne'

    if directional_filter == 'Less than':
        animeography_filterMethod = "$lte"
        mangaography_filterMethod = "$lte"
    else:
        animeography_filterMethod = "$gte"
        mangaography_filterMethod = "$gte"

    animeScore = 0
    mangaScore = 0
    if "animeography_length" in field_filter:
        animeScore = score_filter
    else:
        animeography_filterMethod = "$gte"
    if "mangaography_length" in field_filter:
        mangaScore = score_filter
    else:
        mangaography_filterMethod = "$gte"

    try:
        search_and_filter = char_collection.find({
            "animeography_length": {animeography_filterMethod: int(animeScore)},
            "mangaography_length": {mangaography_filterMethod: int(mangaScore)},
            "voiceActor_language":{language_filter_type : language_filter},
            '$or': [ # query from different fields
            {"name.full": {"$regex": name,"$options":"i"}},
            #{"description": {"$regex": name,"$options":"i"}}
            ]}).collation({'locale':'en'}).sort(sort,direction).limit(100)

        list_search_and_filter = list(search_and_filter)
        len_list = len(list_search_and_filter)
        #print(len_list)
        if len_list != 0:
            return list_search_and_filter
        
        # TRY AGAIN WITH DESCRIPTIONS THIS TIME
        search_and_filter = char_collection.find({
            "animeography_length": {animeography_filterMethod: int(animeScore)},
            "mangaography_length": {mangaography_filterMethod: int(mangaScore)},
            "voiceActor_language":{language_filter_type : language_filter},
            '$or': [ # query from different fields
            #{"name.full": {"$regex": name,"$options":"i"}},
            {"description": {"$regex": name,"$options":"i"}}
            ]}).collation({'locale':'en'}).sort(sort,direction).limit(100)

        return list(search_and_filter)
    except:
        return []

def databasesearch_staff_name(client : MongoClient, name, sort_method, language_filter, field_filter, score_filter, directional_filter):
    ''' Searches by inputted staff name '''
    staff_collection = client.anilist.staff

    sort_and_dir = find_sort_method(sort_method)
    sort = sort_and_dir[0]
    direction = sort_and_dir[1]

    # make cases if nothing selected
    if len(language_filter) != 0: 
        language_filter_type = '$in'
    else:
        language_filter_type = '$ne'

    if directional_filter == "Less than":
        char_directional_filter_type = "$lte"
        prod_directional_filter_type = "$lte"
    else:
        char_directional_filter_type = "$gte"
        prod_directional_filter_type = "$gte"

    chars_voiced_input = "0"
    prod_roles_input = "0"
    if "characters_voiced" in field_filter:
        chars_voiced_input = score_filter
    else:
        char_directional_filter_type = "$gte"
    if "production_roles" in field_filter:
        prod_roles_input = score_filter
    else:
        prod_directional_filter_type = "$gte"
    
    try:
        search_and_filter = staff_collection.find({
            "language": {language_filter_type:language_filter}, # filter greater than or equal to selected score
            "characters_voiced": {char_directional_filter_type: int(chars_voiced_input)},
            "production_roles": {prod_directional_filter_type: int(prod_roles_input)},
            '$or': [ # query from different fields
            {"name.full": {"$regex": name,"$options":"i"}},
            #{"description": {"$regex": name,"$options":"i"}},
            ]}).collation({'locale':'en'}).sort(sort,direction).limit(40)
        
        list_search_and_filter = list(search_and_filter)
        len_list = len(list_search_and_filter)
        #print(len_list)
        if len_list != 0:
            return list_search_and_filter
        
        # TRY AGAIN WITH DECRIPTIONS THIS TIME
        search_and_filter = staff_collection.find({
            "language": {language_filter_type:language_filter}, # filter greater than or equal to selected score
            "characters_voiced": {char_directional_filter_type: int(chars_voiced_input)},
            "production_roles": {prod_directional_filter_type: int(prod_roles_input)},
            '$or': [ # query from different fields
            #{"name.full": {"$regex": name,"$options":"i"}},
            {"description": {"$regex": name,"$options":"i"}},
            ]}).collation({'locale':'en'}).sort(sort,direction).limit(40)
        
        return list(search_and_filter)
    except:
        return []

def find_sort_method(sort_method):
    ''' Used to take string given from model page and convert to sort method and direction '''

    # ANIME SORTS
    if sort_method == "popularity dec":
        sort = "popularity"
        direction = -1
    if sort_method == "popularity inc":
        sort = "popularity"
        direction = 1
    if sort_method == "alphabetical":
        sort = "title.userPreferred"
        direction = 1
    if sort_method == "rev alphabetical":
        sort = "title.userPreferred"
        direction = -1
    if sort_method == "score dec":
        sort = "meanScore"
        direction = -1
    if sort_method == "score inc":
        sort = "meanScore"
        direction = 1
    if sort_method == "newest to oldest":
        sort = ["startDate.year", "startDate.month", "startDate.day"]
        direction = -1
    if sort_method == "oldest to newest":
        sort = ["startDate.year", "startDate.month", "startDate.day"]
        direction = 1

    # CHARACTER
    if sort_method == "popularity dec (char)":
        sort = "favourites"
        direction = -1
    if sort_method == "popularity inc (char)":
        sort = "favourites"
        direction = 1   
    if sort_method == "alphabetical (char)":
        sort = "name.full"
        direction = 1
    if sort_method == "rev alphabetical (char)":
        sort = "name.full"
        direction = -1

    # STAFF
    if sort_method == "popularity dec (staff)":
        sort = "favourites"
        direction = -1
    if sort_method == "popularity inc (staff)":
        sort = "favourites"
        direction = 1   
    if sort_method == "alphabetical (staff)":
        sort = "name.full"
        direction = 1
    if sort_method == "rev alphabetical (staff)":
        sort = "name.full"
        direction = -1

    sort_and_dir = []
    sort_and_dir.append(sort)
    sort_and_dir.append(direction)
    return sort_and_dir