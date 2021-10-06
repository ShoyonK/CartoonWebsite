import anilistquery
import mongoengine
from pymongo import MongoClient
import wikipedia
import time



''' 
This module uploads anilist stuff to anilist database
DO NOT RUN because it will mess up our database
'''

client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = client.anilist # use anilist database
anime_collection = db.anime # specify collection

anime_collection.aggregate({"indexStats":""})
'''
ANIME
Choose which pages you want data from
CURRENTLY: I have done 2 pages with 50 each to upload 100 anime
Can easily do more with start page 3, end page 10 or something
'''
anime_page_start = 1 
anime_page_end = 2
'''
for i in range(anime_page_start, anime_page_end+1):
    anime_list = anilistquery.query_pageanime_popularity(50, i)
    for anime in anime_list:
        print("inserting")
        anime_collection.insert_one(anime)
'''

char_collection = db.characters # change collection to characters

'''
CHARACTERS
Choose which pages you want data from
CURRENTLY: I have done 2 pages with 50 each to upload 100 characters
Can easily do more with start page 3, end page 10 or something
'''
char_page_start = 1 
char_page_end = 2

'''
for i in range(char_page_start, char_page_end+1):
    char_list = anilistquery.query_pagecharacter_popularity(50, i)
    for char in char_list:
        print("Inserting " + str(i) + ":" + char['name']['full'])
        char_collection.insert_one(char)
'''


studio_collection = db.studios # change collection to characters

'''
STUDIOS
Choose which pages you want data from
CURRENTLY: I have done 1 page with 40 studios
Can easily do more with 
'''
studio_page_start = 1 
studio_page_end = 1
'''
studio_popularity_rank = 1 # starting popularity rank
for i in range(studio_page_start, studio_page_end+1):
    studio_list = anilistquery.query_pagestudio_popularity(40,i)
    for studio in studio_list:
        #print("Inserting:" + studio['name'])

        stringToTry = "Studio " + studio['name']
        print(stringToTry)
        
        time.sleep(1) # need bc i think the wikipedia api doesn't like if you call it too much 
        page = wikipedia.page(stringToTry)

        studio['summary'] = page.summary # append dictionary with wikipedia info
        studio['images'] = page.images
        studio['popularityRank']= studio_popularity_rank
        studio_popularity_rank = studio_popularity_rank + 1

        print("intserting " + stringToTry)
        studio_collection.insert_one(studio)
'''

'''
STAFF
Choose which pages you want data from
CURRENTLY: I have done 1 page with 40 staff members
Can easily do more
'''
staff_collection = db.staff # change collection to characters

staff_page_start = 1 
staff_page_end = 1

'''
staff_popularity_rank = 1 # initial popularity as a rank
for i in range(studio_page_start, studio_page_end+1):
    staff_list = anilistquery.query_pagestaff_popularity(40, i)
    for staff in staff_list:
        print("Inserting:" + staff['name']['full'])

        staff['popularityRank'] = staff_popularity_rank # add new field of populairty rank
        staff_popularity_rank = staff_popularity_rank + 1

        staff_collection.insert_one(staff)
'''
'''
current_staff = list(staff_collection.find())

for i in range(0, len(current_staff)):
    staff = current_staff[i]

    characters_voiced = len(staff['characters']['edges'])
    production_roles = len(staff['staffMedia']['edges'])
    print(str(i) + ": " + staff['name']['full'] + " " + str(characters_voiced) + " " + str(production_roles))
    
    staff_collection.update_one(staff,{'$set':{
        "characters_voiced":characters_voiced,
        "production_roles":production_roles
        }})
'''


'''
search = wikipedia.search("Studio Trigger",results = 20, suggestion = True)
#print(search) # search, gives selated stuff
suggest = wikipedia.summary("Studio Bones")
#print(suggest) # gives summary, very useful
page = wikipedia.page("Studio SILVER")
print(page.title)
#print(page.summary) # gives same as previous summary
#print(page.content) # gives too much
#print(page.images)
print(page.__dict__)
print(page.sections)
print(page.section)
print(page.categories)
'''


