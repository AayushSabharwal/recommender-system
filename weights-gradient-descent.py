import numpy as np
from scipy import optimize as op
import numba

similarity_files = ['all_similarities/director-similarity', 'all_similarities/genre-similarity', 'all_similarities/rating-similarity', 'all_similarities/tags-similarity']
with np.load('all_similarities/user-similarity.npz', 'r') as npf:
    usim = npf['arr_0']
adj_mat = np.zeros((23843, 23843), dtype='f4')

def weightfn(x, *args):
    print(x, x/x.sum(), end=' ')
    adj_mat = args[0]
    adj_mat -= adj_mat
    for param, weight in zip(similarity_files, x):
        with np.load(param+'.npz', 'r') as npf:
        #npf = np.memmap(param+'.npy', mode='r', shape=adj_mat.shape, dtype='f4')
            adj_mat += npf['arr_0'] * weight
    adj_mat /= x.sum()
    adj_mat -= usim
    np.abs(adj_mat, out=adj_mat)
    ret = adj_mat.sum()
    print(ret)
    return ret


print(f'Enter weights {len(similarity_files)} space separated float values')
inp = [float(x) for x in input().split(' ')]
weights = np.array(inp, dtype='f4')

res = op.minimize(weightfn, weights, method='BFGS', options={'disp': True}, args=(adj_mat, ))

print('final fn value', res.fun)
print('final x value', res.x)
np.save('final_weights.npy', res.x)
