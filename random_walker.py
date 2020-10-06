from multiprocessing import Pool
import random
import json
import graph_tool.all as gt
import numpy as np
import pandas as pd
from fuzzywuzzy import process

"""
# creating random graph
print(f"initial{time.time()}")
movies = pd.read_csv('ml-25m/movies.csv')
print(f"read{time.time()}")
print(len(movies))

g = gt.Graph(directed=False)
g.add_vertex(len(movies) // 2)
print(f"made graph{time.time()}")
nedges = int(len(movies)**2 * 0.01 * 0.25)

print(f"nedges {nedges}")


def make_edge(_):
    return random.sample(range(len(movies)), 2)


def create_edges():
    print("here")
    edges = []
    with Pool(16) as p:
        edges = p.map(make_edge, range(nedges))
    g.add_edge_list(edges)
    print(f"added edges{time.time()}")
"""

# load the graph
g = gt.load_graph("random.gt")
# load the titles
titles = pd.read_csv("ml-25m/movies.csv")['title'].to_numpy()
# load the reverse mapping from title to vertex index. This is faster than calculating from title
with open('reverse_mapping.json') as infile:
    reverse_mapping = json.load(infile)

# how many iterations to walk for
walk_length = 100000


def walk(vertex: int):
    """
    Does a random walk from starting vertex
    """
    reset_probability = 0.2
    # creating the vertex property map for frequency
    fvp = g.new_vertex_property('int', val=0)
    # getting the corresponding vertex
    vert = g.vertex(vertex)

    for _ in range(walk_length):
        # increment the frequency of this vertex
        fvp[vert] += 1
        if random.uniform(0, 1) < reset_probability:
            # with reset_probability we go back to origin vertex
            vert = g.vertex(vertex)
        else:
            # otherwise just go to a random neighbour
            vert = random.choice(g.get_out_neighbors(vert))
    # returns the frequency map as a np.ndarray
    return fvp.a


def names_to_indices(names: list):
    # this is just QoL, allows passing a single string instead of a list
    if not isinstance(names, list):
        names = [names]
    # make sure the names are all strings
    assert all(isinstance(name, str) for name in names)
    # get the corresponding best match
    return [process.extractOne(name, titles) for name in names]


def run_walk(movies, weights):
    # value sanity checks
    assert len(movies) == len(weights)
    assert all(isinstance(w, float) for w in weights)

    # get the vertex indices for the movie names
    indices = [reverse_mapping[n[0]] for n in names_to_indices(movies)]

    with Pool(16) as pool:
        # walk from node 1 n times
        maps = pool.map(walk, indices)
        # add the resultant frequency arrays into one
        result = np.ndarray(g.num_vertices(), dtype=float)

        # add the correponsing freuquencies, multiplied by respective weights
        for i in range(len(movies)):
            result += maps[i] * weights[i]

        # just fancy stuff necessary to get 5 maximum indices from results, and display their
        # corresponding movie names
        idx = np.argpartition(result, -5)[-5:]
        return [g.vertex_properties["name"][x] for x in idx[np.argsort((-result)[idx])]]
