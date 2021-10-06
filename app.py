from flask import Flask, render_template
from flask import request, redirect
from jikanpy import Jikan
import backend
from backend import anilistquery, jikanquery, pytrendsquery
from backend import anilistdatabase, jikandatabase, pytrendsdatabase
from static.desc import about
import mongoengine
from pymongo import MongoClient
import re

'''
Creates a webpage that allows searching through the AniList and Jikan APIs by anime name
You may have to pip install jikanpy to be able to use the jikan API
'''

app = Flask(__name__)
client = MongoClient('mongodb+srv://teame14:teame14website@cluster0.dtlaf.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority')

@app.route("/")
def splash():
    return render_template('splash.html')

@app.route("/test")
def test():
    return render_template('testpage.html')   

@app.route("/about")
def about_page():
    team = about.about_page
    return render_template('about.html', team=team)

@app.route('/animes', methods=['POST', 'GET'])
def animemodel():

    genres = ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mahou Shoujo", "Mecha", "Music", "Mystery", "Psychological", "Romance", "Sci-Fi", "Slice of Life", "Sports", "Supernatural", "Thriller"]
    media_formats = [("TV", "TV"), ("TV_SHORT","TV Short"), ("MOVIE","Movie"), ("SPECIAL", "Special"), ("OVA","OVA"), ("ONA","ONA"), ("MUSIC", "Music")]
    media_sources = [("ORIGINAL", "Original"), ("MANGA","Manga"), ("LIGHT_NOVEL","Light Novel"), ("VISUAL_NOVEL","Visual Novel"), ("VIDEO_GAME", "Video Game"), ("OTHER", "Other")]
    sorts = [("popularity dec", "Popularity Decreasing"), ("popularity inc", "Popularity Increasing"), ("alphabetical", "Alphabetical"), ("rev alphabetical", "Reverse Alphabetical"), ("score dec", "Score Decreasing"), ("score inc", "Score Increasing"), ("newest to oldest", "Newest to Oldest"), ("oldest to newest", "Oldest to Newest")]

    if request.method == 'POST':
        # get content from form
        anime_to_search = request.form.get('search_string')  # get content type as string
        sort_method = request.form.get('sort', 'popularity dec')
        genre_filter = request.form.getlist('genre[]') #('filter')
        score_filter = request.form.get('score', 0)
        media_format_filter = request.form.getlist('media_formats')
        media_source_filter = request.form.getlist('media_sources')

        # print("anime to search is " + anime_to_search)
        # print("sort method is " + sort_method)
        # print("filters are " + str(genre_filter))
        # print("score filter is " + score_filter)
        # print("media formats are " + str(media_format_filter))
        # print("media formats are " + str(media_source_filter))

        anilist_popular_anime = anilistdatabase.databasesearch_anime_title(client, anime_to_search, sort_method, genre_filter, score_filter, media_format_filter, media_source_filter) # search results
        
        for anime in anilist_popular_anime:
            anime['genres'] = ", ".join(anime['genres'])

        genre_remember = [1 if genre in genre_filter else 0 for genre in genres]

        media_sources_first_elems = [i[0] for i in media_sources] #get the first element of all tuples
        media_sources_remember = [1 if media_source in media_source_filter else 0 for media_source in media_sources_first_elems]

        media_formats_first_elems = [i[0] for i in media_formats] #get the first element of all tuples
        media_formats_remember = [1 if media_format in media_format_filter else 0 for media_format in media_formats_first_elems]

        return render_template('animemodel.html', popularList=anilist_popular_anime, genres=zip(genres,genre_remember), media_formats=zip(media_formats, media_formats_remember),media_sources=zip(media_sources, media_sources_remember),
            search_string=anime_to_search, sorts=sorts, sort_method=sort_method, score_filter=score_filter)
    else:
        #anilist_popular_anime = anilistquery.query_pageanime_popularity(30,1) # list of popular animes from API (phase 1)
        anilist_popular_anime = anilistdatabase.databasequery_pageanime_popularity(client, 100) # get popular animes from our database
        for anime in anilist_popular_anime:
            anime['genres'] = ", ".join(anime['genres'])

        genre_remember = [0 for genre in genres]
        media_formats_remember = [0 for media_format in media_formats]
        media_sources_remember = [0 for media_source in media_sources]

        return render_template('animemodel.html', popularList=anilist_popular_anime, genres=zip(genres, genre_remember), media_formats=zip(media_formats, media_formats_remember),media_sources=zip(media_sources, media_sources_remember),
            search_string="", sorts=sorts, sort_method="popularity dec", score_filter="0") # put zero as default value and check in index.html

@app.route("/characters", methods=['POST', 'GET'])
def characterModel():
    languages = ["JAPANESE","ENGLISH","PORTUGUESE","ITALIAN", "GERMAN", "KOREAN"]
    fields = [("animeography_length","Animeography"),("mangaography_length","Mangaography")]
    directional = ["Less than", "Greater than"]
    sorts = [("popularity dec (char)", "Popularity Decreasing"),
    ("popularity inc (char)","Popularity Increasing"), ("alphabetical (char)", "Alphabetical"), ("rev alphabetical (char)","Reverse Alphabetical")]
    if request.method == 'POST':
        # get content from form
        char_to_search = request.form.get('search_string')  # get content type as string
        sort_method = request.form.get('sort', 'popularity dec (char)')
        directional_filter = request.form.get('directional', 'Greater than')#('filters')#
        score_filter = request.form.get('score', 0)
        field_filter = request.form.getlist('fieldfilter') #('filter')
        language_filter = request.form.getlist('languages')
        # print('field filter is', end=" ")
        # for x in field_filter:
        #     print(x, end=" ")
        # print()
        # print("char to search is " + char_to_search)
        # print("sort method is " + sort_method)
        # print("directional filters are ", end=" ")
        # for x in directional_filter:
        #     print(x, end=" ")
        # print()
        anilist_searched_chars = anilistdatabase.databasesearch_char_name(client, char_to_search, sort_method, directional_filter, field_filter, score_filter, language_filter)
       
        for anilist_char in anilist_searched_chars:
            if anilist_char['description'] is not None:
                anilist_char['parsed_description'] = anilistquery.char_desc_parser(anilist_char['description'])
                if (len(anilist_char['parsed_description'])>0 and '.' in anilist_char['parsed_description']):
                    anilist_char['description'] = anilist_char['parsed_description'][-1][1].split(".", 1)[1]

        fields_first_elems = [i[0] for i in fields] #get the first element of all tuples
        fields_remember = [1 if field in field_filter else 0 for field in fields_first_elems]

        directional_remember = [1 if direction in directional_filter else 0 for direction in directional]
        language_remember = [1 if language in language_filter else 0 for language in languages]
        return render_template('charactermodel.html', popularList=anilist_searched_chars, search_string=char_to_search, fields = zip(fields, fields_remember), score_filter = score_filter, directional = zip(directional, directional_remember), languages = zip(languages,language_remember), sorts=sorts, sort_method=sort_method)
    else:
        #anilist_popular_chars = anilistquery.query_pagecharacter_popularity(27, 1) # list of popular chars from API (phase 1)
        anilist_popular_chars = anilistdatabase.databasequery_pagechar_popularity(client, 100)

        for anilist_char in anilist_popular_chars:
            anilist_char['parsed_description'] = anilistquery.char_desc_parser(anilist_char['description'])
            if (len(anilist_char['parsed_description'])>0):
                anilist_char['description'] = anilist_char['parsed_description'][-1][1].split(".", 1)[1]

        fields_remember = [0 for field in fields]  
        directional_remember = [0,1] #'greater than' default selected
        language_remember = [0 for language in languages]
        return render_template('charactermodel.html', popularList=anilist_popular_chars, search_string="", fields = zip(fields, fields_remember), directional = zip(directional, directional_remember), languages = zip(languages,language_remember), score_filter = "0", sorts=sorts, sort_method="popularity dec (char)") 

@app.route("/studios", methods=['POST', 'GET'])
def studiomodel():
    if request.method == 'POST':
        # get content from form
        studio_to_search = request.form.get('content')  # get content type as string
        # search for what they typed in AniList API
        anilist_studio_page = anilistquery.query_pagestudio_name(studio_to_search, 10)

        anilist_popular_studios = anilistquery.query_pagestudio_popularity(5, 1) # get popular studios

        return render_template('studiomodel.html', search=1,studioList=anilist_studio_page, popularList=anilist_popular_studios)
    else:
        #anilist_popular_studios = anilistquery.query_pagestudio_popularity(27, 1) # get popular studios from API (phase 1)
        anilist_popular_studios = anilistdatabase.databasequery_pagestudio_popularity(client, 40)
        return render_template('studiomodel.html', search=0, popularList=anilist_popular_studios) # put zero as default value and check in index.html

@app.route("/staff", methods=['POST', 'GET'])
def staffmodel():
    languages = ["JAPANESE", "ENGLISH", "KOREAN", "ITALIAN", "SPANISH", "PORTUGUESE", "GERMAN"]
    fields = [("characters_voiced", "Characters Voiced"), ("production_roles", "Production Roles")]
    directional = ["Less than", "Greater than"]
    sorts = [("popularity dec (staff)", "Popularity Decreasing"),
    ("popularity inc (staff)","Popularity Increasing"), ("alphabetical (staff)", "Alphabetical"), ("rev alphabetical (staff)","Reverse Alphabetical")]
    if request.method == 'POST':
        # get content from form
        staff_to_search = request.form.get('search_string')  # get content type as string
        sort_method = request.form.get('sort', 'popularity dec (staff)')
        language_filter = request.form.getlist('languages')
        field_filter = request.form.getlist('fieldfilter')
        score_filter = request.form.get('score', 0)
        directional_filter = request.form.get('directional', 'Greater than') #('filters')#

        # print("staff to search is " + staff_to_search)
        # print("sort method is " + sort_method)
        # print("languages are " + str(language_filter))
        # print("fields are " + str(field_filter))
        # print("voice/production roles is " + str(score_filter))
        # print("direction is " + str(directional_filter))

        anilist_searched_staff = anilistdatabase.databasesearch_staff_name(client, staff_to_search, sort_method, language_filter, field_filter, score_filter, directional_filter)

        fields_first_elems = [i[0] for i in fields] #get the first element of all tuples
        fields_remember = [1 if field in field_filter else 0 for field in fields_first_elems]

        directional_remember = [1 if direction in directional_filter else 0 for direction in directional]
        language_remember = [1 if language in language_filter else 0 for language in languages]

        return render_template('staffmodel.html', popularList=anilist_searched_staff, search_string=staff_to_search, languages = zip(languages,language_remember), fields = zip(fields, fields_remember), directional = zip(directional, directional_remember),
            language_filter=language_filter, field_filter=field_filter, score_filter=score_filter, sorts=sorts, sort_method=sort_method)
    else:
        #anilist_popular_staff = anilistquery.query_pagestaff_popularity(40, 1) # from api
        anilist_popular_staff =  anilistdatabase.databasequery_pagestaff_popularity(client, 40)

        fields_remember = [0 for field in fields]
        directional_remember = [0,1] #'greater than' default selected
        language_remember = [0 for language in languages]

        return render_template('staffmodel.html', popularList=anilist_popular_staff, search_string="", languages = zip(languages,language_remember), fields = zip(fields, fields_remember), directional = zip(directional, directional_remember),
            language_filter=[], field_filter=[], score_filter="0", sorts=sorts, sort_method="popularity dec (staff)") # put zero as default value and check in index.html


@app.route('/animes/<int:id>', methods=['POST', 'GET'])
def animeinstance_by_id(id):
    media_formats = {"TV": "TV", "TV_SHORT":"TV Short", "MOVIE":"Movie", "SPECIAL": "Special", "OVA":"OVA", "ONA":"ONA", "MUSIC": "Music"}
    media_sources = {"ORIGINAL": "Original", "MANGA":"Manga", "LIGHT_NOVEL":"Light Novel", "VISUAL_NOVEL":"Visual Novel", "VIDEO_GAME": "Video Game", "OTHER": "Other"}
    try:
        #anilist_anime = anilistquery.query_anime_id(id) # by api (phase 1)
        anilist_anime = anilistdatabase.databasequery_anime_idMal(client, id) # search our database for anime

        anilist_anime['description'] = anilistquery.tag_remover(anilist_anime['description'])
        for review in anilist_anime['reviews']['edges']:
            review['node']['body'] = anilistquery.tilde_remover(review['node']['body'])
            review['node']['body'] = anilistquery.parentheses_remover(review['node']['body'])
            review['node']['body'] = anilistquery.tag_remover(review['node']['body'])
        jikan_anime = jikandatabase.databasequery_anime_idMal(client,id)
        #print(jikan_anime)
        related_char_list = anilist_anime['characters']['edges'] # get list of related characters
        related_studio_list = anilist_anime['studios']['edges']
        related_staff_list = anilist_anime['staff']['edges']

        newList = sorted(related_char_list, key=lambda x: x['node']['id'])

        for key in media_formats.keys():
            if key == anilist_anime['format']:
                anilist_anime['format'] = media_formats[key]

        for key in media_sources.keys():
            if key == anilist_anime['source']:
                anilist_anime['source'] = media_sources[key]

        suggestions_trend = pytrendsdatabase.databasequery_anime_keywordSuggestions(client, re.sub('[^A-Za-z0-9]+', ' ', anilist_anime['title']['userPreferred']))

        return render_template('animeinstance.html', search=1,anilist_anime=anilist_anime, related_chars=newList, related_studios=related_studio_list,jikan_anime = jikan_anime, suggestions_trend=suggestions_trend)
    except Exception as e:
        print(e)
        return render_template('errorPage.html')

@app.route('/characters/<int:id>', methods=['POST', 'GET'])
def chracterinstance_by_id(id):
    try:
        #anilist_char= anilistquery.query_anime_character_by_id(id) # search anilist api (phase 1)
        anilist_char = anilistdatabase.databasequery_char_id(client, id) # get char by id from database
        #print(anilist_char)
        nameAnime = anilist_char['name']['full']
        #print(nameAnime)
        jikan_char = jikandatabase.databasequery_char_id(client, id)
        # anilist_char['parsed_description'] = anilistquery.char_desc_parser(anilist_char['description'])
        # if (len(anilist_char['parsed_description'])>0 and '.' in anilist_char['parsed_description']):
        #     anilist_char['description'] = anilist_char['parsed_description'][-1][1].split(".", 1)[1]

        # anilist_char['description'] = anilistquery.parentheses_remover(anilist_char['description'])
        # anilist_char['description'] = anilistquery.square_brackets_remover(anilist_char['description'])

        anilist_char['HTMLdescription'] = anilistquery.links_remover(anilist_char['HTMLdescription'])

        anilist_char['description'], anilist_char['spoiler_description'] = anilistquery.find_HTML_spoiler(anilist_char['HTMLdescription'])

        anilist_char['description'] = anilist_char['description'].replace("<p>","",1)

        # print(anilist_char['spoiler_description'])
        
        jikan_char['nicknames'] = ", ".join(jikan_char['nicknames']) if (len(jikan_char['nicknames']) > 0) else "None"

        related_anime_list = anilist_char['media']['edges']

        return render_template('characterinstance.html', search=1,anilist_char=anilist_char, related_animes=related_anime_list, jikan_char=jikan_char)
    except Exception as e:
        print(e)
        return render_template('errorPage.html')
            

@app.route('/studios/<int:id>', methods=['POST', 'GET'])
def studioinstance_by_id(id):   
    try:
        #anilist_studio = anilistquery.query_studio_id(id) # from api (phase 1)
        anilist_studio = anilistdatabase.databasequery_studio_id(client, id)
        related_anime_list = anilist_studio['media']['edges']

        suggestions_trend = pytrendsdatabase.databasequery_studio_keywordSuggestions(client, anilist_studio['name'])
        return render_template('studioinstance.html', search=1,anilist_studio=anilist_studio, related_animes=related_anime_list, suggestions_trend=suggestions_trend)
    except Exception as e:
        print(e)
        return render_template('errorPage.html')


@app.route('/staff/<int:id>', methods=['POST', 'GET'])
def staffinstance_by_id(id):   
    try:
        #anilist_staff = anilistquery.query_staff_id(id) # from api
        anilist_staff = anilistdatabase.databasequery_staff_id(client, id)
        related_media_list = anilist_staff['staffMedia']['edges'][:5]
        related_chars_list = anilist_staff['characters']['edges'][:5]

        #Extracting attributes from and cleaning up raw descriptions
        # anilist_staff['description'] = anilistquery.parentheses_remover(anilist_staff['description'])
        # anilist_staff['description'] = anilistquery.square_brackets_remover(anilist_staff['description'])
        # anilist_staff['parsed_description'] = anilistquery.char_desc_parser(anilist_staff['description'])
        # if (len(anilist_staff['parsed_description'])>0):
        #     anilist_staff['description'] = anilist_staff['parsed_description'][-1][1].split(".", 1)[1] if ("." in anilist_staff['parsed_description'][-1][1]) else ""

        suggestions_trend = pytrendsdatabase.databasequery_staff_keywordSuggestions(client, anilist_staff['name']['full'])

        anilist_staff['HTMLdescription'] = anilistquery.links_remover(anilist_staff['HTMLdescription'])

        return render_template('staffinstance.html', search=1,anilist_staff=anilist_staff, related_media = related_media_list,related_chars=related_chars_list, suggestions_trend=suggestions_trend)
    except Exception as e:
        #print(e)
        return render_template('errorPage.html')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':
    app.run(debug=True)

