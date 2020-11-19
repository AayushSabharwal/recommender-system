import pandas as pd
import numpy as np
import pickle
import numba
from pathlib import Path

cur_dir = Path(__file__)
cm = pd.read_csv(cur_dir.parent.parent / '../../processed_data/cleaned_subsetted_movies.csv')
with open(cur_dir.parent / 'movie-id-map2.pkl', 'rb') as f:
    mv2id = pickle.load(f)

a = np.zeros((23843), dtype='<U35')
for mv, it in cm[['movieId', 'director']].dropna().itertuples(index=False):
	a[mv2id[mv]] = it
print('done psim')

@numba.jit(nopython=True, parallel=True)
def other_half_similarity(sim, start, end):
    print('Entered')
    nmv = 23843
    msim = np.zeros(shape=(nmv, nmv), dtype=numba.float32)
    for i in range(start, end):
        for j in range(i+1, nmv):
            msim[i, j] = sim[i] == sim[j]
        print('done', i)
    return msim

print('Enter start index')
start = int(input())
print('Enter end index')
end = int(input())

np.savez_compressed('director-similarity.npz', other_half_similarity(a, start, end))
