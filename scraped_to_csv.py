import pandas as pd
import re
import unicodedata
from os import listdir, path

print('NOTE: This script should not be moved to another directory')

mv = pd.read_csv('./ml-25m/clean_movies.csv')
mv = mv.astype({'title': 'string', 'genres': 'string'})

print('Enter path to folder containing (only) all scraped files')
path_to_scraped_folder = input()
files = [path.join(path_to_scraped_folder, f) for f in listdir(
    path_to_scraped_folder) if path.isfile(path.join(path_to_scraped_folder, f))]
bigdf = None
for file in files:
    df = pd.read_csv(file)
    df = df.astype({col: 'string' for col in df.columns[~df.columns.str.contains('Rating')]})\
        .rename(columns={col: col.lower() for col in df.columns})
    df.title = pd.Series([re.sub(r'\([0-2][0-9][0-9][0-9]\)$', '', unicodedata.normalize("NFKD", x)
                                 .strip()).strip() for x in df.title]).astype('string')
    df = df.query('language == "English" | language == "Hindi"').merge(mv, left_on='id',
                                                                       right_on='movieId')
    if bigdf is None:
        bigdf = df
    else:
        bigdf = pd.concat([bigdf, df])

bigdf.to_csv('final.csv')
