import pandas as pd
import re
import unicodedata
from os import listdir, path

print('NOTE: This script should not be moved to another directory')
mv = pd.read_csv('./ml-25m/clean_movies.csv')

print('Enter path to folder containing (only) all scraped files')
path_to_scraped_folder = input()

files = [path.join(path_to_scraped_folder, f) for f in listdir(
    path_to_scraped_folder) if path.isfile(path.join(path_to_scraped_folder, f))]

bigdf = None
for file in files:
    df = pd.read_csv(file)
    df = df.merge(mv, left_on='ID', right_on='movieId').drop(['IMDB', 'ID', 'Title'], axis=1)
    df = df.astype({col: 'string' for col in df.columns if df.dtypes[col] == 'object'})[
        ['movieId', 'imdbId', 'title', 'Language', 'year', 'Director', 'Tags', 'Cast', 'genres', 'Genre', 'Rating']]
    df = df[df.year >= 1990]
    df = df.assign(genres=[[x[1:-1] for x in re.findall(r'\'.*?\'', y)] for y in df.genres],
                   Genre=[[x[1:-1] for x in re.findall(r'\'.*?\'', y)] for y in df.Genre],
                   Cast=[[x[1:-1] for x in re.findall(r'\'.*?\'', y)] for y in df.Cast],
                   Tags=[[x[1:-1] for x in re.findall(r'\'.*?\'', y)] for y in df.Tags])
    df = df.assign(genres=[list(set(x) | set(y)) for x, y in zip(df.genres, df.Genre)])\
        .drop('Genre', axis=1)
    df = df.assign(genres=['/'.join(x) for x in df.genres],
                   Cast=['|'.join(x) for x in df.Cast],
                   Tags=['|'.join(x) for x in df.Tags])\
        .rename(columns={
            'Cast': 'cast',
            'Tags': 'tags',
            'Language': 'language',
            'Director': 'director',
            'Rating': 'rating'
        })\
        .astype({
            'genres': 'string',
            'cast': 'string',
            'tags': 'string'
        })

    if bigdf is None:
        bigdf = df
    else:
        bigdf = pd.concat([bigdf, df])

bigdf.to_csv('final.csv', index=False)
