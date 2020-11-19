import numpy as np
from scipy import optimize as op
import numba

similarity_files = ['all_similarities/director-similarity', 'all_similarities/genre-similarity', 'all_similarities/rating-similarity', 'all_similarities/tags-similarity']
with np.load('all_similarities/user_similarity.npz', 'r') as npf:
    usim = npf['arr_0']

@numba.jit(forceobj=True, parallel=True, fastmath=True)
def calc_adj_mat(wts):
    adj_mat_t = np.zeros((23843, 23843), dtype='<f2')
    for param, weight in zip(similarity_files, wts):
        npf = np.memmap(param+'.npy', mode='r', shape=adj_mat_t.shape, dtype='<f2')
        adj_mat_t += npf * weight
    return adj_mat_t

@numba.jit(forceobj=True, cache=True, parallel=True, fastmath=True)
def weightfn(x):
    print(x)
    adj_mat = calc_adj_mat(x)
    adj_mat -= usim
    np.abs(adj_mat, out=adj_mat)
    return adj_mat.sum(dtype='f4')

print(f'Enter weights {len(similarity_files)} space separated float values')
inp = [float(x) for x in input().split(' ')]
weights = np.array(inp, dtype='f2')
res = op.minimize(weightfn, weights, method='BFGS', options={'disp': True})

print('final fn value', res.fun)
print('final x value', res.x)
np.save('final_weights.npy', res.x)
