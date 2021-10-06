import urllib.request
from jikanpy import Jikan
import requests
import json, re



''' 
Functions to use the Jikan API
YOU MAY HAVE TO pip install jikanpy 
'''
def query_anime_name(name):
    jikan = Jikan()  
    results = jikan.search('anime', name) #get all anime
    allAnime =  results['results']
    animeID= allAnime[0]['mal_id']
    animeInformation = jikan.anime(animeID)
    #print(animeInformation)
    return(animeInformation)

def query_pageanime_name(name):
    jikan = Jikan()  
    results = jikan.search('anime', name) # is dict with lists
    allAnime = results['results'] #list of dicts
    return(allAnime)

    
def query_anime_character(name):
    jikan = Jikan()  
    results = jikan.search('character', name) # is dict with lists
    allChar = results['results'] #list of dicts
    charID = allChar[0]['mal_id'] #currently taking the most relevant one
    charInformation = jikan.character(charID)
    #print(charInformation)
    return(charInformation)

def query_anime_character_by_id(id):
    jikan = Jikan()  
    charInformation = jikan.character(id)
    #print(charInformation)
    return(charInformation)


def query_pagecharacter_name(name):
    jikan = Jikan()  
    results = jikan.search('character', name) # is dict with lists
    allChar = results['results'] #list of dicts
    return(allChar)

#doesn't work currently
def query_pagestudio_name(name):
    jikan = Jikan()  
    studio = jikan.producer('16')
    for x in studio['meta']['name']:
        print("")
        print(x)
    return(studio)



