import pandas as pd
import numpy as np
import pickle

# load movies data
cm = pd.read_csv('../../processed_data/cleaned_subsetted_movies.csv')

# load movie-id-map2
with open('movie-id-map2.pkl', 'rb') as f:
    mv2id2 = pickle.load(f)

# create matrix
rsim = np.zeros((len(mymv), len(mymv)), dtype='f4')
i = 0
for mv, rt in cm[['movieId', 'rating']].itertuples(index=False):
    # this results in the matrix being anti-symmetric
    rsim[mv2id2[mv], :] += rt
    rsim[:, mv2id2[mv]] -= rt
    i += 1
    if i%1000 == 0:
        print('done', i)
# save to file
np.savez_compressed('rating-similarity.npz', rsim)