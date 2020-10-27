from os import path
import pandas as pd
import graph_tool.all as gt


if not path.isfile('../../ml-25m/new_ratings.csv'):
    print('new_ratings.csv not detected, creating file')
    if not path.isfile('../../ml-25m/timeless_ratings.csv'):
        raise FileNotFoundError('File timeless_ratings.csv not found in ../../ml-25m/')

    with open('../../ml-25m/timeless_ratings.csv', 'r') as infile:
        with open('../../ml-25m/new_ratings.csv', 'w') as outfile:
            for line in infile:
                l = line.split(',')
                l[0] = l[0] + 'u'
                l[1] = l[1] + 'm'
                outfile.write(','.join(l))

df = pd.read_csv('../../ml-25m/new_ratings.csv')
g = gt.Graph(directed=False)
g.ep.rating = g.new_ep('float')
g.vp.id = g.add_edge_list(df.values, hashed=True, eprops=[g.ep.rating])
g.save('../ratings_graph.gt.xz')
