from itertools import combinations
import graph_tool.all as gt


def calculate_score(source, target):
    score = 0
    n_paths = 0
    n_edges = 0
    for sp in gt.all_shortest_paths(g, source, target, edges=True):
        n_edges = len(sp)
        n_paths += 1
        if is_weighted:
            for e in sp:
                score += g.ep.rating[e]
    if not is_weighted:
        score = n_edges
    return score * n_paths / (n_edges * n_edges)


print('Name of graph data file in parent directory')
gpath = input()
g = gt.load_graph('../' + gpath)
is_weighted = 'rating' in g.ep
movies = [v for v in g.get_vertices() if g.vp.id[v][0] == 'm']
for u, v in combinations(movies, 2):
    calculate_score(u, v)
