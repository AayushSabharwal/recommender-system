import numpy as np
import pandas as pd
import user_id
from typing import List
from fuzzywuzzy import process
import pickle

# list of all movies, for fuzzy matching
all_movies_info=pd.read_csv('processed_data/cleaned_subsetted_movies.csv')
all_movies = list(all_movies_info.title)
all_movies_info=all_movies_info.set_index('movieId')
# map of movie name to it's movieId
title_to_id = pickle.load(open('movie_name_map.pkl', 'rb'))
# map of movieId to title
id_to_title = pickle.load(open('id_title_map.pkl', 'rb'))
# map of movieId to it's index in the dictionary
id_to_index = pickle.load(open('all_similarities/calculation/movie-id-map2.pkl', 'rb'))
# map of userId to the list of movies they have rated
user_to_movies = pickle.load(open('user_movies_map.pkl', 'rb'))

def pagerank(movie_ids: List[int], input_ids: List[int], epsilon: float = 1e-4, maxiterations: int = 1000, reset_chance: float = 0.15):
    """
    Calculates pagerank values for a given set of movies

    Parameters
    ----------
        movie_ids:
            List of movie_ids to run pagerank on
        epsilon:
            Maximum delta between interations for convergence to have been achieved
        maxiterations:
            Maximum number of iterations pagerank will be run for
    
    Returns
    -------
        pr: Dict[int, float]
            Map of movieId to it's pagerank value
    """
    # get indices of movies in matrix
    inds = np.array([id_to_index[i] for i in movie_ids])
    input_inds = np.array([movie_ids.index(i) for i in input_ids])
    # load and subset matrix
    with np.load('final_adj_mat.npz', 'r') as npf:
        mat = npf['arr_0'][np.vstack(inds), inds]*(1-reset_chance)
    # handle reset probability
    mat[:, input_inds] += reset_chance
    # initial vector is [1 0 0 0 ...]
    v = np.zeros(mat.shape[0], dtype='<f4')
    # old vector, to keep track of convergence
    oldv = v.copy()
    v[0] = 1
    # number of iterations
    i = 0
    # runs while v hasn't converged and iterations limit is not reached
    while np.amax(np.abs(oldv-v)) > epsilon and i < maxiterations:
        # copy v to oldv
        oldv = v.copy()
        # multiply with matrix
        v = np.matmul(v, mat)
        # normalize
        v /= np.linalg.norm(v)
        i += 1
    # construct map of movieId to pagerank value
    pr = {movie_ids[i]: v[i] for i in range(len(movie_ids))}
    return pr

def get_recommendations(movie_names: List[str]):
    """
    Takes movies inputted by user, and calculates recommended movies

    Parameters
    ----------
        movie_names:
            List of movie names the user likes. Fuzzy matched to names in dataset
    
    Returns
    -------
        recommendations: List[int]
            MovieID and rating for top 5 recommended movies
    """
    # for each movie name provided, find the closest match in list of movies through fuzzy searching
    movie_names = [process.extractOne(name, all_movies)[0] for name in movie_names]
    # movieId for each movie
    movie_ids = [title_to_id[mv] for mv in movie_names]
    # userIds whose movies to iterate through
    user_ids = user_id.subset(movie_ids)
    # get movies of those users
    chosen_movies = set()
    for uid in user_ids:
        chosen_movies|= set(user_to_movies[uid])
    chosen_movies |= set(movie_ids)
    # run pagerank
    pr = pagerank(list(chosen_movies), movie_ids)
    # remove user input movies from pagerank, since they will always have high values
    for mv in movie_ids:
        del pr[mv]
    maxval = max(pr.values())
    # sort the pairs by pagerank and return the 5 largest values, along with their percentage recommendation
    movie_tuples = [(pr[mv], mv) for mv in pr]
    movie_tuples = [(id_to_title[id], int(rt/maxval * 10000.)/100.) for rt, id in sorted(movie_tuples)[-5:]]
    
    return movie_tuples

def get_info(name: str):
    """
    Gathers the info. of the movie entered by the user

    Parameters
    ----------
    name:
        Name of a movie. Fuzzy Matched to the dataset.

    Returns
    -------
    String of relevant information
    """

    # for each movie name provided, find the closest match in list of movies through fuzzy searching
    movie_name = process.extractOne(name, all_movies)[0]
    # movieId for each movie
    movie_ids = title_to_id[movie_name]
    # Organize the data in a printable format
    movie_detail=list(all_movies_info.loc[movie_ids, ['imdbId','title','year','rating','language','genres','director','cast','tags'] ])
    template="Title : {}\nIMDB ID : {}\nYear : {}\nRating : {}\nLanguage : {}\nGenres : {}\nDirector : {}\nCast : {}\nTags : {}"
    final=template.format(movie_detail[1],movie_detail[0],movie_detail[2],movie_detail[3],movie_detail[4],movie_detail[5].replace("/",", "),movie_detail[6],movie_detail[7].replace("/",", "),movie_detail[8].replace("/",", "))

    return final