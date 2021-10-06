import pandas as pd
from pytrends.request import TrendReq

'''
# anime cat=317
pytrend.build_payload(kw_list=['Studio MADHOUSE'],cat=317)

df = pytrend.interest_by_region(resolution='united_states')
print(df.head)
'''

def query_keywordSuggestions(keyword):
    ''' Queries suggestions for a keyword. Returns a list of dicts of keyword suggestions '''
    pytrend = TrendReq()
    keywords = pytrend.suggestions(keyword=keyword)
    return keywords


def query_keywordRelated(keyword):
    ''' Queries word and returns dict of related queries.'''

    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[keyword],cat=317) # cat=317 filters to anime/manga
    related_queries = pytrend.related_queries()
    #rel_values = related_queries.values()
    top_related = related_queries[keyword]['top'] # gives a pandas data frame of top stuf
    top_related_dict = {}
    if top_related is not None:
        top_related_dict = top_related.to_dict()

    return(top_related_dict) # return a string version of top related