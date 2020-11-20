import numpy as np

similarity_files = ['all_similarities/director-similarity', 'all_similarities/genre-similarity', 'all_similarities/rating-similarity', 'all_similarities/tags-similarity']
print('Include rating similarity? (y/n)')
if input() == 'n':
    del similarity_files[2]

print(similarity_files)
print(f'Enter {len(similarity_files)} weights, space separated')
wts = np.array([float(x) for x in input().split(' ')], dtype='f4')
wts /= wts.sum()
adj_mat = np.zeros((23843, 23843), dtype='f4')
for p, w in zip(similarity_files, wts):
    with np.load(p + '.npz', 'r') as npf:
        adj_mat += npf['arr_0'] * w
print(adj_mat)
np.savez_compressed('final_adj_mat.npz', adj_mat)
