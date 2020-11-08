import pandas as pd
import numpy as np
import pickle
import numba

cm = pd.read_csv('final.csv')
cm['genres'] = cm.genres.str.split('/')
cm['tags'] = cm.tags.str.split('\|\|')
mymv = set(cm.movieId)
with open('movie-id-map.pkl', 'rb') as f:
    mv2id = pickle.load(f)

def other_calculate_similarity(cname: str):
    dist = set()
    for it in cm[cname].dropna():
        dist |= set(it)
    print(f"len {len(dist)}")
    dist = list(dist)
    p2id = {dist[i]: i for i in range(len(dist))}
    psim = np.zeros((len(dist), len(mymv)), dtype='f4')
    for mv, it in cm[['movieId', cname]].dropna().itertuples(index=False):
        psim[[p2id[i] for i in it], mv2id[mv]] += 1
    print('done psim')
    return psim

@numba.jit(nopython=True, parallel=True)
def other_half_similarity(sim, nmv, start, end):
    print('Enter')
    msim = np.zeros(shape=(nmv, nmv), dtype=numba.float32)
    for i in range(start, end):
        col = sim[:, i]
        for j in range(i+1, nmv):
            msim[i, j] += np.linalg.norm(col-sim[:, j])
        print('done', i)
    return msim

print('Enter name of parameter')
cname = input()
print('Enter start index')
start = int(input())
print('Enter end index')
end = int(input())

psim = other_calculate_similarity('tags')
np.savez_compressed(cname+'-similarity.npz', other_half_similarity(psim, len(mymv), start, end))
