import re
import pandas as pd


def get_year(title):
    matches = re.findall(r'\([0-2][0-9][0-9][0-9]\)$', title)
    if len(matches) > 0:
        try:
            return int(matches[-1][1:-1])
        except:
            return 0
    return 0


def fix_the(title):
    has_the = len(re.findall(r', The$', title)) > 0
    if has_the:
        return 'The ' + re.sub(r', The$', '', title).strip()
    else:
        return title


raw_mv = pd.read_csv('./ml-25m/movies.csv')
# just some unicode things, to resolve spaces. Then, strip all whitespace from ends
raw_mv.title = raw_mv.title.str.replace('\xa0', ' ').str.strip()
# get the year and remove all content in parentheses from title
raw_mv = raw_mv.assign(year=[get_year(t) for t in raw_mv.title])\
    .assign(title=[re.sub(r'\(.*?\)', '', t).strip() for t in raw_mv.title])
# special case of this movie having parentheses in it's name
raw_mv.at[15292, 'title'] = '(Untitled)'
# movies beginning with "The" are stored as <Name>, The
# this should be fixed, since it is now how people specify movies
raw_mv = raw_mv.assign(title=[fix_the(t) for t in raw_mv.title])
# makes more sense for missing values to be represented this way
raw_mv.genres = raw_mv.genres.astype('string').str.replace('(no genres listed)', 'NA')

links = pd.read_csv('links.csv')
# tmdb Id is not necessary
links = links.drop('tmdbId', axis=1)
# final merged dataset
cleaned_mv = links.merge(raw_mv, left_on='movieId', right_on='movieId')
# save to file
cleaned_mv.to_csv('./ml-25m/cleaned_movies.csv', index=False)
