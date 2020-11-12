import pandas as pd
import numpy as np
import pickle
import numba

cm = pd.read_csv('Movie_data_cleaned.csv')
with open('movie-id-map2.pkl', 'rb') as f:
    mv2id = pickle.load(f)

dist = set(cm.director)
print(f"ndir {len(dist)}")
dist = list(dist)
p2id = {dist[i]: i for i in range(len(dist))}
psim = np.zeros((len(dist), len(mv2id)), dtype='f4')
for mv, it in cm[['movieId', 'director']].dropna().itertuples(index=False):
	psim[p2id[it], mv2id[mv]] += 1
print('done psim')

@numba.jit(nopython=True, parallel=True)
def other_half_similarity(sim, start, end):
    print('Entered')
    nmv = sim.shape[1]
    msim = np.zeros(shape=(nmv, nmv), dtype=numba.float32)
    for i in range(start, end):
        col = sim[:, i]
        for j in range(i+1, nmv):
            msim[i, j] += np.linalg.norm(col-sim[:, j])
        print('done', i)
    return msim

print('Enter start index')
start = int(input())
print('Enter end index')
end = int(input())

np.savez_compressed('director-similarity.npz', other_half_similarity(psim, start, end))
