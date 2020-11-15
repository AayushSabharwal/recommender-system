import pandas as pd

''' 
Takes as input a list of movieIDs and exports list of USER IDs
'''
# Tutorial
'''
import user_id
c=user_id.subset([180079,180075])
'''


def subset(movieID):
    count=pd.read_csv('Len_movies.csv',index_col=False)
    genre=pd.read_csv('Movie_data_cleaned.csv')
    genre=genre.set_index('movieId')
    genres=[]
    for x in movieID:
        genress=genre._get_value(x,'genres').split("/")
        genres.extend(genress)
    normalized=pd.read_csv("Scores_Normalized.csv",index_col=False)
    subdataframe=normalized[genres]
    subdataframe=subdataframe.copy()
    subdataframe['sum'] = subdataframe[list(subdataframe.columns)].sum(axis=1)
    subdataframe=subdataframe.nlargest(50,'sum')
    semi_final=subdataframe.index.values.tolist()
    final=[]
    counter=0
    for x in semi_final:
        a=count._get_value(x,'Total')
        if(a>3000):
            continue
        elif(counter>3000):
            break
        final.append(x+1)
        counter+=count._get_value(x,'Total')
    return final