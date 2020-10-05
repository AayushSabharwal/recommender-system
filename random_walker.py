from multiprocessing import Pool
import random
import graph_tool.all as gt
import numpy as np
import matplotlib.cm as cm

# creating random graph
g = gt.Graph(directed=False)
g.add_vertex(100)
for it in range(1000):
    a, b = random.sample(range(100), 2)
    g.add_edge(a, b)
gt.random_rewire(g, model='erdos', n_iter=1000)

n = 10   # number of walks


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


with Pool(n) as p:
    # walk from node 1 n times
    maps = p.map(walk, [1 for i in range(n)])
    # add the resultant frequency arrays into one
    result = np.ndarray(100, dtype=int)
    for vmap in maps:
        result += vmap

    # set the frequency into a map
    freq = g.new_vertex_property('int', vals=result)
    labels = g.new_vertex_property('string', vals=list(range(100)))

    # drawing
    pos = gt.radial_tree_layout(g, 1)
    gt.graph_draw(g, pos, vertex_fill_color=freq, vcmap=cm.viridis, vprops={'text': labels})
