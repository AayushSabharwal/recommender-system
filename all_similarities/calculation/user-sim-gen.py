import numpy as np
import numba
import pickle
import pandas as pd
from pathlib import Path

cur_dir = Path(__file__)

with open(cur_dir.parent / 'movie-id-map2.pkl', 'rb') as f:
    mv2id2 = pickle.load(f)
uids = pickle.load(open(cur_dir.parent / 'most-active-users.pkl', 'rb'))
us = pd.read_csv(cur_dir.parent.parent.parent / '../../ml-25m/timeless_ratings.csv')
us = us[us.userId.isin(uids)]
us = us[us.movieId.isin(mv2id2)]
uids = np.array(list(uids))
rtu = np.array(us.userId)
rtm = np.array(us.movieId)
rtr = np.array(us.rating)
del us, pd, pickle
uu = np.zeros((uids.shape[0], len(mv2id2)))
u2id = {uids[i]:i for i in range(len(uids))}
for i in range(len(rtu)):
    uu[u2id[rtu[i]], mv2id2[rtm[i]]] = rtr[i]

@numba.njit()
def makeumat(uu, nmv, start, end):
    msim = np.zeros((nmv, nmv))
    for i in range(start, end):
        col = uu[:, i]
        for j in range(i+1, nmv):
            msim[i, j] += np.linalg.norm(col-uu[:, j])
        print('done', i)
    return msim

print('done uu mat')
print(uu.shape)
print('Enter start')
st = int(input())
print('Enter end')
en = int(input())

np.savez_compressed('user_sim.npz', makeumat(uu, len(mv2id2), st, en))
