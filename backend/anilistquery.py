import requests
import json
import re


def query_anime_id(id):
  # Queries a single anime by MAL ID

  query = '''
  query ($id: Int, $charPerPage: Int, $reviewPerPage: Int, $staffPerPage: Int){ 
    Media (idMal:$id){
      id
      idMal
      isAdult
      title {
        romaji
        english
        native
        userPreferred
      }
      coverImage {
        extraLarge
        large
        medium
      }
      bannerImage
      description
      episodes
      popularity
      genres
      meanScore
      type
      format
      source
      startDate{
        year
        month
        day
      }
      endDate{
        year
        month
        day
      }

      characters(page:1, perPage:$charPerPage, sort:FAVOURITES_DESC){
        edges{
          voiceActors{
            id
            name{
              full
              native
            }
            image{
              medium
              large
            }
          }
          node{
            id
            name{
              full
              native
            }
            image {
              large
              medium
            }
          }
        }
      }
      staff(page:1, perPage:$staffPerPage, sort:FAVOURITES_DESC){
        edges{
          role
          node{
            id
            name{
              full
              native
            }
            image{
              large
              medium
            }
          }
        }

      }
      
      studios{
        edges{
          node{
            id
            name
          }
        }
      }
      reviews(page:1, perPage:$reviewPerPage, sort:RATING_DESC) {
        edges {
          node {
            id
            score
            rating
            summary
          }
        }
      }
    }
  }
  '''

  # Define our query variables and values that will be used in the query request
  variables = {
      'id': id,
      'charPerPage': 5,
      'reviewPerPage':5,
      'staffPerPage':5
  }

  url = 'https://graphql.anilist.co'

  # Make the HTTP Api request
  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  #print(dict_response)
  return dict_response['data']['Media']


def query_anime_name(name):
  '''
  Takes an anime name and returns a single anime. Probably useful for instance pages
  '''

  query = '''
  query ($search: String, $perPage: Int) { # Define which variables will be used in the query (id)
    Media (search: $search, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
      id
      title {
        romaji
        english
        native
      }
      popularity
      coverImage {
        large
        extraLarge
      }
      bannerImage
      description
      episodes
      genres
      meanScore
      startDate{
        year
        month
        day
      }
      endDate {
        year 
        month
        day
      }

      characters(page:1, perPage:$perPage, sort:FAVOURITES_DESC){
        edges{ 
          node{
            id
            name {
              full
            }
            image {
              large
              medium
            }
          }
        }
      }
      studios {
        edges {
          node {
            name
          }
        }
      }

    }
    
  }
  '''

  # Define our query variables and values that will be used in the query request
  variables = {
      'search': name,
      'perPage':3
  }

  url = 'https://graphql.anilist.co'

  # Make the HTTP Api request
  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  dict_response_useful = dict_response['data']['Media']
  return dict_response_useful



def query_anime_character(name):
  '''
  Takes a character name and returns a single anime character. Probably useful for a character instance page
  '''

  query = '''
  query ($search: String, $perPage: Int) { # Define which variables will be used in the query (id)
    Character (search: $search) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
      id
      name {
        first
        last
        full
        native
      }
      image {
        large
        medium
      }
      description
      favourites
      media (page:1, perPage:$perPage, sort:POPULARITY_DESC, type:ANIME){
        edges{
          node{
            title{
              english
              userPreferred
            }
            coverImage {
              large
              medium
              extraLarge
            }
            description
            studios(isMain:true){
              nodes{
                name
              }
            }
          }
        }
      }
    }
  }
  '''

  # Define our query variables and values that will be used in the query request
  variables = {
      'search': name,
      'perPage': 3
  }

  url = 'https://graphql.anilist.co'

  # Make the HTTP Api request
  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  dict_response_useful = dict_response['data']['Character']
  return dict_response_useful

def query_anime_character_by_id(id):
  '''
  Takes a character name and returns a single anime character. Probably useful for a character instance page
  '''

  query = '''
  query ($id: Int, $animePerPage: Int) {
    Character (id:$id){
      id
      name {
        full
        native
      }
      image {
        large
        medium
      }
      description
      favourites
      media (page:1, perPage:$animePerPage, sort:POPULARITY_DESC, type:ANIME){
        edges{
          voiceActors(sort:FAVOURITES_DESC) {
            id
            name {
              full
              native
            }
            language
            image{
              large
              medium
            }
          }
          node{
            id
            idMal
            meanScore
            averageScore
            genres
            favourites
            title{
              english
              userPreferred
              native
            }
            coverImage{
              large
              medium
              extraLarge
            }
            description
            studios(isMain:true){
              nodes{
                id
                name
              }
            }
          }
        }

      }
    }
  }
  '''
  variables = {
      'id':id,
      'animePerPage': 5
  }

  url = 'https://graphql.anilist.co'

  # Make the HTTP Api request
  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  dict_response_useful = dict_response['data']['Character']
  return dict_response_useful

def query_studio_id(id):
  '''
  Takes a character name and returns a single anime studio. Probably useful for a character instance page
  '''

  query = '''
  query ($id: Int, $animePerPage: Int, $charsPerPage: Int) {
          Studio (id:$id){
            id
            name
            favourites
            media(page:1, perPage:$animePerPage, sort:POPULARITY_DESC){
              edges{
                node{
                  id
                  idMal
                  isAdult
                  episodes
                  meanScore
                  title{
                    english
                    native
                    userPreferred
                    romaji
                  }
                  coverImage{
                    large
                    medium
                  }
                  characters(perPage:$charsPerPage, sort:FAVOURITES_DESC){
                    nodes{
                      id
                      name{
                        full
                      }
                      image{
                        large
                        medium
                      }
                    }
                  }
                }
              }
            }
          }
  }
  '''

  # Define our query variables and values that will be used in the query request
  variables = {
      'id': id,
      'animePerPage':3,
      'charsPerPage':3
  }

  url = 'https://graphql.anilist.co'

  # Make the HTTP Api request
  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  dict_response_useful = dict_response['data']['Studio']
  #print(dict_response_useful)
  return dict_response_useful



def query_pageanime_name(animeName, numberResponses):
  '''
  Returns list of dicts of different anime related to given animeName

  animeName is the name searched for

  numberResponses is how many anime will be returned in list
  '''

  query = '''
  query ($id: Int, $page: Int, $perPage: Int, $search: String) {
      Page (page: $page, perPage: $perPage) {
          pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
          }
          media (id: $id, search: $search, type: ANIME) {
              id
              title {
                  romaji
                  english
                  native
              }
              coverImage {
                large
                medium
              }
              description
              episodes
              genres
              meanScore
              type
              bannerImage
              format
              source
              startDate {
                year
                month
                day
              }
              endDate {
                year
                month
                day
              }
          }
      }
  }
  '''
  variables = {
      'search': animeName,
      'page': 1,
      'perPage': numberResponses
  }

  url = 'https://graphql.anilist.co'

  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  animeList = dict_response['data']['Page']['media'] # gets list dicts of different anime
  return animeList


def query_pagecharacter_name(charName, numberResponses):
  '''
  Returns list of dicts of characters related to given charName

  charName is the name searched for

  numberResponses is how many characters will be returned in list
  '''

  query = '''
  query ($perPage: Int, $page: Int, $search: String) {
      Page (page: $page, perPage: $perPage) {
          pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
          }
          characters (search: $search) {
              id
              name {
                first
                last
                full
                native
              }
              image {
                large 
                medium
              }
              favourites
              description
          }
      }
  }
  '''
  variables = {
      'search': charName,
      'page': 1,
      'perPage': numberResponses
  }
  url = 'https://graphql.anilist.co'

  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  charList = dict_response['data']['Page']['characters'] # gets list dicts of different characters
  return charList


def query_pagestudio_name(studioName, numberResponses):
  '''
  Returns list of dicts of studios related to given studioName

  studioName is the name searched for

  numberResponses is how many characters will be returned in list
  '''

  query = '''
  query ($perPage: Int, $page: Int, $search: String) {
      Page (page: $page, perPage: $perPage) {
          pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
          }
          studios (search: $search) {
              id
              name
              favourites

              media(sort:POPULARITY_DESC, type:ANIME){
                edges{
                  node{
                    title{
                      romaji
                      english
                      native
                      userPreferred
                    }
                    coverImage {
                      extraLarge
                      large
                      medium
                    }
                    bannerImage
                  }
                }
              }
          }
      }
  }
  '''
  variables = {
      'search': studioName,
      'page': 1,
      'perPage': numberResponses
  }
  url = 'https://graphql.anilist.co'

  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  studioList = dict_response['data']['Page']['studios'] # gets list dicts of different characters
  return studioList


def query_pageanime_popularity(numberResponses, page):
  '''
  Returns list of dicts of animes sorted by popularity

  numberResponses is how many animes will be returned in list
  '''

  query = '''
  query ($perPage: Int, $page: Int, $charPerPage: Int, $reviewPerPage: Int, $staffPerPage: Int) {
      Page (page: $page, perPage: $perPage) {
          pageInfo {
              total
              currentPage
              lastPage
              hasNextPage
              perPage
          }
          media (sort:POPULARITY_DESC){
            id
            idMal
            isAdult
            title {
              romaji
              english
              native
              userPreferred
            }
            coverImage {
              extraLarge
              large
              medium
            }
            bannerImage
            description
            episodes
            popularity
            genres
            meanScore
            type
            format
            source
            startDate{
              year
              month
              day
            }
            endDate{
              year
              month
              day
            }

            characters(page:1, perPage:$charPerPage, sort:FAVOURITES_DESC){
              edges{
                voiceActors{
                  id
                  name{
                    full
                    native
                  }
                  image{
                    medium
                    large
                  }
                }
                node{
                  id
                  name{
                    full
                    native
                  }
                  image {
                    large
                    medium
                  }
                }
              }
            }
            staff(page:1, perPage:$staffPerPage, sort:FAVOURITES_DESC){
              edges{
                role
                node{
                  id
                  name{
                    full
                    native
                  }
                  image{
                    large
                    medium
                  }
                }
              }

            }
            
            studios{
              edges{
                node{
                  id
                  name
                }
              }
            }
            reviews(page:1, perPage:$reviewPerPage, sort:RATING_DESC) {
              edges {
                node {
                  id
                  score
                  rating
                  summary
                }
              }
            }
          }
      }
  }
  '''
  variables = {
      'page': page,
      'perPage': numberResponses,
      'charPerPage':5,
      'reviewPerPage':5,
      'staffPerPage':5
  }
  url = 'https://graphql.anilist.co'

  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  animeList = dict_response['data']['Page']['media'] # gets list dicts of different characters
  return animeList

def query_pagecharacter_popularity(numberResponses, page):
  '''
  Returns list of dicts of characters sorted by popularity

  numberResponses is how many animes will be returned in list
  '''

  query = '''
  query ($perPage: Int, $page: Int, $animePerPage: Int) {
      Page (page: $page, perPage: $perPage) {
          characters (sort:FAVOURITES_DESC){
            id
            name {
              full
              native
            }
            image {
              large
              medium
            }
            description
            favourites
            media (page:1, perPage:$animePerPage, sort:POPULARITY_DESC, type:ANIME){
              edges{
                voiceActors(sort:FAVOURITES_DESC) {
                  id
                  name {
                    full
                    native
                  }
                  language
                  image{
                    large
                    medium
                  }
                }
                node{
                  id
                  idMal
                  meanScore
                  averageScore
                  genres
                  favourites
                  title{
                    english
                    userPreferred
                    native
                  }
                  coverImage{
                    large
                    medium
                    extraLarge
                  }
                  description
                  studios(isMain:true){
                    nodes{
                      id
                      name
                    }
                  }
                }
              }

            }
          }
      }
  }
  '''
  variables = {
      'page': page,
      'perPage': numberResponses,
      'animePerPage': 5
  }
  url = 'https://graphql.anilist.co'

  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  animeList = dict_response['data']['Page']['characters'] # gets list dicts of different characters
  return animeList


def query_pagestudio_popularity(numberResponses, page):
  '''
  Returns list of dicts of animes sorted by popularity

  numberResponses is how many animes will be returned in list
  '''

  query = '''
  query ($perPage: Int, $page: Int, $animePerPage: Int, $charsPerPage: Int) {
      Page (page: $page, perPage: $perPage) {
          studios (sort:FAVOURITES_DESC){
            id
            name
            favourites
            media(page:1, perPage:$animePerPage, sort:POPULARITY_DESC){
              edges{
                node{
                  id
                  idMal
                  isAdult
                  episodes
                  meanScore
                  title{
                    english
                    native
                    userPreferred
                    romaji
                  }
                  coverImage{
                    large
                    medium
                  }
                  characters(perPage:$charsPerPage, sort:FAVOURITES_DESC){
                    nodes{
                      id
                      name{
                        full
                      }
                      image{
                        large
                        medium
                      }
                    }
                  }
                }
              }
            }
          }
      }
  }
  '''
  variables = {
      'page': page,
      'perPage': numberResponses,
      'animePerPage':3,
      'charsPerPage':3
  }
  url = 'https://graphql.anilist.co'

  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  animeList = dict_response['data']['Page']['studios'] # gets list dicts of different characters
  return animeList


def query_pagestaff_popularity(numberResponses, page):
  '''
  Returns list of dicts of animes sorted by popularity

  numberResponses is how many animes will be returned in list
  '''

  query = '''
  query ($perPage: Int, $page: Int, $animePerPage: Int) {
      Page (page: $page, perPage: $perPage) {
        staff(sort:FAVOURITES_DESC){
          id
          language
          name{
            full
            native
          }
          language
          image{
            large
            medium
          }
          description
          favourites

          staffMedia(sort:POPULARITY_DESC){
            edges{
              staffRole
              node{
                id
                idMal
                title{
                  romaji
                  english
                  native
                  userPreferred
                }
                coverImage{
                  extraLarge
                  large
                  medium
                }
              }
            }
          }

          characters(sort:FAVOURITES_DESC){
            edges{
              node{
                id
                name {
                  full
                  native
                }
                image{
                  large
                  medium
                }

                media(perPage:$animePerPage, sort:POPULARITY_DESC){
                  nodes{
                    id
                    idMal
                    title{
                      romaji
                      english
                      native
                      userPreferred
                    }
                    coverImage{
                      extraLarge
                      large
                      medium
                    }
                  }
                }
                
              }
            }
          }
        }
          
      }
  }
  '''
  variables = {
      'page': page,
      'perPage': numberResponses,
      'animePerPage':3,
  }
  url = 'https://graphql.anilist.co'

  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  #print(dict_response)
  animeList = dict_response['data']['Page']['staff'] # gets list dicts of different characters
  return animeList

def query_staff_id(id):
  # Queries a single staff member by anilist ID

  query = '''
  query ($id: Int, $animePerPage: Int) {
        Staff(id:$id){
          id
          language
          name{
            full
            native
          }
          language
          image{
            large
            medium
          }
          description
          favourites

          staffMedia(sort:POPULARITY_DESC){
            edges{
              staffRole
              node{
                id
                idMal
                title{
                  romaji
                  english
                  native
                  userPreferred
                }
                coverImage{
                  extraLarge
                  large
                  medium
                }
              }
            }
          }

          characters(sort:FAVOURITES_DESC){
            edges{
              node{
                id
                name {
                  full
                  native
                }
                image{
                  large
                  medium
                }

                media(perPage:$animePerPage, sort:POPULARITY_DESC){
                  nodes{
                    id
                    idMal
                    title{
                      romaji
                      english
                      native
                      userPreferred
                    }
                    coverImage{
                      extraLarge
                      large
                      medium
                    }
                  }
                }
                
              }
            }
          }
        }
  }
  '''

  # Define our query variables and values that will be used in the query request
  variables = {
      'id': id,
      'animePerPage':5
  }

  url = 'https://graphql.anilist.co'

  # Make the HTTP Api request
  response = requests.post(url, json={'query': query, 'variables': variables})
  dict_response = response.json() # turns the response into a dict
  #print(dict_response)
  return dict_response['data']['Staff']

def char_desc_parser(desc):
  mylist = re.split("__", desc)
  tuplesList = []
  for i in range(1,len(mylist), 2):
      if (i+1 < len(mylist)):
          tuplesList.append((mylist[i],mylist[i+1]))
  return tuplesList

def parentheses_remover(desc):
  return re.sub(r'\([^)]*\)', '', desc)

def tilde_remover(desc):
  return re.sub(r'\~~~[^~~~]*\~~~', '', desc)

def tag_remover(desc):
  return re.sub(r'<.*?.>', '', desc)

def square_brackets_remover(desc):
  return desc.replace('[','').replace(']','')

def links_remover(desc):
  desc_no_links = re.sub(r"<a href=\"https:\/\/anilist\.co[^>]*>([\s\S]*?)<\/a>", r"\1", desc)
  return desc_no_links

def find_spoiler(desc):
  spoiler = re.search(r'\~![^)]*\!~', desc)
  if spoiler is not None:
    spoiler = spoiler.group(0).replace('!~','').replace('~!','')
  no_spoiler = re.sub(r'\~![^)]*\!~', '', desc)
  return no_spoiler, spoiler

def find_HTML_spoiler(desc):
  spoiler = re.search(r"<span class='markdown_spoiler'>[^)]*</span>", desc)
  if spoiler is not None:
    spoiler = spoiler.group(0).replace('<p>','').replace('</p>','')

  no_spoiler = re.sub(r"<span class='markdown_spoiler'>[^)]*</span>", '', desc)
  return no_spoiler, spoiler