from multiprocessing import Pool
import random
import time
import graph_tool.all as gt
import numpy as np
# import matplotlib.cm as cm
# import pandas as pd


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

# create_edges()
# g.save("random.gt")
# gt.random_rewire(g, model='erdos', n_iter=nedges)
# print(f"did erdos renyi{time.time()}")
# n = 10   # number of walks
g = gt.load_graph("random.gt")
# movies = pd.read_csv("ml-25m/movies.csv")

# names = g.new_vertex_property("string", vals=movies['title'].to_numpy())
# g.vertex_properties["name"] = names
# g.save("random.gt")


def walk(vertex):
    reset_probability = 0.2
    # creating the vertex property map for frequency
    fvp = g.new_vertex_property('int', val=0)
    vert = g.vertex(vertex)

    for _ in range(100000):
        fvp[vert] += 1
        # with reset_probability we go back to origin vertex
        if random.uniform(0, 1) < reset_probability:
            vert = g.vertex(vertex)
        else:
            # otherwise just go to a random neighbour
            vert = random.choice(g.get_out_neighbors(vert))
    return fvp.a


def run_walk(n):

    with Pool(n) as p:
        # walk from node 1 n times
        print(f"start walks {time.time()}")
        maps = p.map(walk, [1 for i in range(n)])
        # add the resultant frequency arrays into one
        print(f"after walks{time.time()}")
        result = np.ndarray(g.num_vertices(), dtype=int)
        for vmap in maps:
            result += vmap

        # set the frequency into a map
        # freq = g.new_vertex_property('int', vals=result)
        # labels = g.new_vertex_property('string', vals=list(range(100)))

        # drawing
        # pos = gt.radial_tree_layout(g, 1)
        # gt.graph_draw(g, pos, vertex_fill_color=freq, vcmap=cm.viridis, vprops={'text': labels})
        idx = np.argpartition(result, -5)[-5:]
        print([g.vertex_properties["name"][x] for x in idx[np.argsort((-result)[idx])]])
