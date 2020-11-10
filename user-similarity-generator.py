import pandas as pd
import numpy as np
import pickle
import numba

with open('movie-id-map2.pkl', 'rb') as f:
    mv2id2 = pickle.load(f)
with open('Test_Set_users_list.csv', 'r') as f:
    uids = [int(x) for x in f.readlines()]
us = pd.read_csv('ml-25m/timeless_ratings.csv')
us = us[us.userId.isin(uids)]
us = us[us.movieId.isin(mv2id2)]
uids = np.array(uids)
rtu = np.array(us.userId)
rtm = np.array(us.movieId)
rtr = np.array(us.rating)
del us
del pd

@numba.njit(parallel=True)
def makeumat(uu, nmv, start, end):
    msim = np.zeros((nmv, nmv))
    for i in range(start, end):
        col = uu[:, i]
        for j in range(i+1, nmv):
            msim[i, j] += np.linalg.norm(col-uu[:, j])
        print('done', i)
    return msim

uu = np.zeros((len(uids), len(mv2id2)))
u2id = {uids[i]:i for i in range(len(uids))}
for i in range(len(rtu)):
    uu[u2id[rtu[i]], mv2id2[rtm[i]]] = rtr[i]

print('Enter starting index')
st = int(input())
print('Enter ending index')
en = int(input())

msim = makeumat(uu, len(mv2id2), st, en)
np.savez_compressed('user-similarity.npz', msim)
