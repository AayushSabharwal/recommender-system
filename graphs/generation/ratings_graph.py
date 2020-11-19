from os import path
import pandas as pd
import graph_tool.all as gt
from pathlib import Path

cur_dir = Path(__file__)

if not path.isfile(cur_dir.parent.parent / '../../ml-25m/new_ratings.csv'):
    print('new_ratings.csv not detected, creating file')
    mv = pd.read_csv(cur_dir.parent.parent / '../../processed_data/subsetted_movies.csv')
    mvIds = set(mv[mv.language.isin(['English', 'Hindi', 'Urdu', 'Punjabi'])].movieId.to_list())
    trat = pd.read_csv(cur_dir.parent.parent / '../../ml-25m/timeless_ratings.csv')
    trat = trat[trat.movieId.isin(mvIds)]
    trat = trat.assign(movieId=['m' + str(id) for id in trat.movieId],
                       userId=['u' + str(id) for id in trat.userId])
    trat.to_csv(cur_dir.parent.parent / '../../ml-25m/new_ratings.csv', index=False)
    del trat
    del mvIds
    del mv

df = pd.read_csv(cur_dir.parent.parent / '../../ml-25m/new_ratings.csv')
g = gt.Graph(directed=False)
g.ep.rating = g.new_ep('float')
g.vp.id = g.add_edge_list(df.values, hashed=True, eprops=[g.ep.rating])
g.save(cur_dir.parent / 'ratings_graph.gt.xz')
