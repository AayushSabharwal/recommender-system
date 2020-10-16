from csv import reader
import scraper
import pandas as pd
data=open('links.csv')
data=reader(data)
data=list(data)
imdb_id=[]
for ids in data:
    imdb_id.append(ids[1])
a=int(input("Enter the starting index of the movie (this index is included) "))
b=int(input("Enter the ending index of the movie (this index is excluded) "))
id_format="tt{}"
# 0th index is not the id, omit that 
final={'Title':[],'Genre':[],'Tags':[],'Director':[],'Cast':[],'Language':[],'Rating':[]}
for ids in imdb_id[a:b]:
    test=id_format.format(ids)
    titles,genres,keywords,c,d,e,f=scraper.credentials(test)
    final['Title'].append(titles)
    final['Genre'].append(genres)
    final['Tags'].append(keywords)
    final['Director'].append(c)
    final['Cast'].append(d)
    final['Language'].append(e)
    final['Rating'].append(f)
    print("Scraped out",titles)
pd1=pd.DataFrame(final)
compression_opts = dict(method='zip',
                        archive_name='out.csv') 
pd1.to_csv('out.zip', index=False,
          compression=compression_opts)