from multiprocessing import Pool
import random
import graph_tool.all as gt
import numpy as np
import matplotlib.cm as cm

g = gt.Graph(directed=False)
g.add_vertex(100)
for it in range(1000):
    a, b = random.sample(range(100), 2)
    g.add_edge(a, b)
gt.random_rewire(g, model='erdos', n_iter=1000)

n = 10   # number of walks


def walk(vertex):
    reset_probability = 0.2
    fvp = g.new_vertex_property('int', val=0)
    vert = g.vertex(vertex)

    for _ in range(100000):
        fvp[vert] += 1
        if random.uniform(0, 1) < reset_probability:
            vert = g.vertex(vertex)
        else:
            vert = random.choice(g.get_out_neighbors(vert))
    return fvp.a


with Pool(n) as p:
    maps = p.map(walk, [1 for i in range(n)])
    result = np.ndarray(100, dtype=int)
    for vmap in maps:
        result += vmap

    freq = g.new_vertex_property('int', vals=result)
    labels = g.new_vertex_property('string', vals=[i for i in range(100)])
    pos = gt.radial_tree_layout(g, 1)
    gt.graph_draw(g, pos, vertex_fill_color=freq, vcmap=cm.viridis, vprops={'text': labels})
