import imdb
from imdb import IMDb
import numpy as np
import pandas as pd

# read list of ratings
df_ratings = pd.read_csv('../data/IMDB_Top250_UID_title_rating.csv')

# define list of high-level features
features_hl = ['aspect ratio', 'box office', 'countries', 'directors', 'genres',
    'rating', 'runtimes', 'title', 'votes', 'writers', 'year']

# define list of low-level features
features_ll = {'box office':['Budget', 'Cumulative Worldwide Gross'],
    'countries': [0], 'directors':[0], 'genres': [0, 1, 2],
    'runtimes':[0], 'writers': [0, 1, 2]}

# define function to acquire features
def acquire_features(movie_id, features_hl=features_hl, features_ll=features_ll):
    """returns named list of desired features"""
    # create an instance of the IMDb class
    ia = IMDb()
    movie = ia.get_movie(movie_id)
    result = [movie.movieID]
    names = ['UID']
    # check existence of each high-level feature
    for feature_hl in features_hl:
        if not feature_hl in movie.keys():
            raise ValueError('Feature: %s not found in movie: %s' % (feature_hl, movie_id))

        if not feature_hl in features_ll.keys():
            result.append(movie[feature_hl])
            names.append(feature_hl)
    # obtain low-level features and append to list
    for feature_hl in features_ll:
        feature_object = movie[feature_hl]
        feature_keys = features_ll[feature_hl]
        for key in feature_keys:
            if isinstance(feature_object, dict):
                if not key in feature_object.keys():
                    result.append(np.nan)
                else:
                    result.append(feature_object[key])
                names.append(key)
            else:
                if key>=len(feature_object):
                    result.append(np.nan)
                    names.append(feature_hl)
                elif isinstance(feature_object[key], imdb.Person.Person):
                    if 'name' in feature_object[key].keys():
                        result.append(feature_object[key]['name'])
                    else:
                        result.append(np.nan)
                    names.append(feature_hl)
                else:
                    result.append(feature_object[key])
                    names.append(feature_hl)
    result = pd.Series(result)
    result.index = names
    return result

# iterate over movie list
for i in range(0, df_ratings.shape[0]):
    print(i)
    try:
        result = acquire_features(df_ratings.UID[i])
    except:
        print('exception occurred for: %s, skipping movie!' % df_ratings.Title[i])
    if i==0:
        df_results = result.to_frame().T
    else:
        df_result = result.to_frame().T
        df_results = pd.concat((df_results, df_result), sort=False, ignore_index=True)

# write to csv
df_results.to_csv('../data/IMDB_Top250_features_raw.csv', index=False)
