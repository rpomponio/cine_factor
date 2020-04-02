import imdb
from imdb import IMDb
import numpy as np
import pandas as pd

# load ratings
df_ratings = pd.read_csv('../data/Personal_Movie_Ratings_Updated.csv')

# drop movies missing ratings
df_ratings = df_ratings.loc[~df_ratings['My Rating'].isnull(), :].reset_index(drop=True)

# load UIDs for movies that do not match search results
df_uid = pd.read_csv('../data/Personal_Movies_Missing_UID_Updated.csv', dtype={'UID':str})
df_ratings = df_ratings.merge(df_uid, how='left', validate='1:1')

# create an instance of the IMDb class
ia = IMDb()

# initialize results container
results = {'UID':[], 'My_Rating':[],
           'Budget':[], 'Cumulative_Worldwide_Gross':[],
           'Production_Company1':[], 'Synopsis': [],
           'Top_250_Rank':[],
           'Country1':[], 'Director1':[], 'Genre1': [],
           'Genre2':[], 'Genre3':[], 'Rating':[],
           'Runtime':[], 'Title':[], 'Poster_URL': [], 'Votes':[],
           'Writer1':[], 'Writer2':[], 'Year':[]}
movies_missing_uid = {'Movie': []}

# iterate over movies
for i in range(0, df_ratings.shape[0]):
    print(i)
    my_movie_title = df_ratings.Movie[i]
    my_movie_year = df_ratings['Release Year'][i]
    my_movie_imdb = df_ratings['IMDb'][i] / 10
    my_movie_rating = df_ratings['My Rating'][i]
    my_movie_uid = df_ratings['UID'][i]
    if np.isnan(float(my_movie_uid)):
        # search by title first
        title_search = ia.search_movie(my_movie_title)
        # is the first item in search the correct movie?
        movie_guess = ia.get_movie(title_search[0].movieID)
        # does the first item in the search match the release year?
        if movie_guess['year']!=my_movie_year:
            print('Skipping movie due to mismatch in year: %s' % my_movie_title)
            movies_missing_uid['Movie'].append(my_movie_title)
            continue
        # does the first item in the search match the rating?
        if (np.abs(movie_guess['rating'] - my_movie_imdb) > 0.5):
            print('Skipping movie due to mismatch in rating: %s' % my_movie_title)
            movies_missing_uid['Movie'].append(my_movie_title)
            continue
    else:
        movie_guess = ia.get_movie(my_movie_uid)
    # for the movie object, try to obtain all features
    results['UID'].append(movie_guess.movieID)
    results['My_Rating'].append(my_movie_rating)
    try:
        results['Budget'].append(movie_guess['box office']['Budget'])
    except:
        results['Budget'].append('')
    try:
        results['Cumulative_Worldwide_Gross'].append(movie_guess['box office']['Cumulative Worldwide Gross'])
    except:
        results['Cumulative_Worldwide_Gross'].append('')
    try:
        results['Production_Company1'].append(movie_guess['production companies'][0]['name'])
    except:
        results['Production_Company1'].append('')
    try:
        results['Synopsis'].append(movie_guess['synopsis'][0])
    except:
        results['Synopsis'].append('')
    try:
        results['Top_250_Rank'].append(movie_guess['top 250 rank'])
    except:
        results['Top_250_Rank'].append('')
    try:
        results['Country1'].append(movie_guess['countries'][0])
    except:
        results['Country1'].append('')
    try:
        results['Director1'].append(movie_guess['directors'][0]['name'])
    except:
        results['Director1'].append('')
    try:
        results['Genre1'].append(movie_guess['genres'][0])
    except:
        results['Genre1'].append('')
    try:
        results['Genre2'].append(movie_guess['genres'][1])
    except:
        results['Genre2'].append('')
    try:
        results['Genre3'].append(movie_guess['genres'][2])
    except:
        results['Genre3'].append('')
    try:
        results['Rating'].append(movie_guess['rating'])
    except:
        results['Rating'].append('')
    try:
        results['Runtime'].append(movie_guess['runtimes'][0])
    except:
        results['Runtime'].append('')
    try:
        results['Title'].append(movie_guess['title'])
    except:
        results['Title'].append('')
    try:
        results['Poster_URL'].append(movie_guess['full-size cover url'])
    except:
        results['Poster_URL'].append('')
    try:
        results['Votes'].append(movie_guess['votes'])
    except:
        results['Votes'].append('')
    try:
        results['Writer1'].append(movie_guess['writer'][0]['name'])
    except:
        results['Writer1'].append('')
    try:
        results['Writer2'].append(movie_guess['writer'][1]['name'])
    except:
        results['Writer2'].append('')
    try:
        results['Year'].append(movie_guess['year'])
    except:
        results['Year'].append('')


# write to csv
df_results = pd.DataFrame(results)
df_results.to_csv('../data/Personal_Movies_Ratings_Features.csv', index=False)

# write missing movies to separate csv
df_missing = pd.DataFrame(movies_missing_uid)
df_missing.to_csv('../data/Personal_Movies_Missing_UID.csv', index=False)


