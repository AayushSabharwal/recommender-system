import numpy as np
from scipy import optimize as op

similarity_files = ['all_similarities/director-similarity', 'all_similarities/genre-similarity', 
                    'all_similarities/tags-similarity', 'all_similarities/language-similarity']
with np.load('all_similarities/user-similarity.npz', 'r') as npf:
    usim = npf['arr_0']
adj_mat = np.zeros((23843, 23843), dtype='f4')

def weightfn(x, *args):
    print(x, x/x.sum(), end=' ')
    adj_mat = args[0]
    adj_mat -= adj_mat
    for param, weight in zip(similarity_files, x):
        with np.load(param+'.npz', 'r') as npf:
            adj_mat += npf['arr_0'] * weight
    adj_mat /= x.sum()
    adj_mat -= usim
    # uncomment this line for norm similarity. If this is used, make sure to remove hess=hessfn from the op.minimize call below
#    ret = np.linalg.norm(adj_mat)
    #uncomment below two lines for absolute difference similarity
    np.abs(adj_mat, out=adj_mat)
    ret = adj_mat.sum()
    print(ret, ret/(23843*23843))
    return ret

def hessfn(x, *args):
    return np.zeros(shape=x.shape, dtype='f4')

print(f'Enter weights {len(similarity_files)} space separated float values')
inp = [float(x) for x in input().split(' ')]
weights = np.array(inp, dtype='f4')
# only uncomment one of the below lines

# standard BFGS, no contstraints on the weights
res = op.minimize(weightfn, weights, method='BFGS', options={'disp': True}, args=(adj_mat, ))
# L-BFGS-B, constrains values to be > 0
#res = op.minimize(weightfn, weights, hess=hessfn, method='L-BFGS-B', options={'disp': True}, args=(adj_mat, ), bounds=op.Bounds([0., 0., 0., 0.], [np.inf, np.inf, np.inf, np.inf]))
print('final fn value', res.fun)
print('final x value', res.x)
np.save('final_weights.npy', res.x)
