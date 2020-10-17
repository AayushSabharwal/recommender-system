from csv import reader
import scraper
import pandas as pd
data=open('links.csv')
data=reader(data)
data=list(data)
imdb_id=[]
for ids in data:
    imdb_id.append((ids[1],ids[0]))
a=int(input("Enter the starting index of the movie (this index is included) "))
b=int(input("Enter the ending index of the movie (this index is excluded) "))
id_format="tt{}"
# 0th index is not the id, omit that 
final={'IMDB':[],'ID':[],'Title':[],'Genre':[],'Tags':[],'Director':[],'Cast':[],'Language':[],'Rating':[]}
i=a
for ids in imdb_id[a:b]:
    try:
        test=id_format.format(ids[0])
        titles,genres,keywords,c,d,e,f=scraper.credentials(test)
        final['IMDB'].append(ids[0])
        final['ID'].append(ids[1])
        final['Title'].append(titles)
        final['Genre'].append(genres)
        final['Tags'].append(keywords)
        final['Director'].append(c)
        final['Cast'].append(d)
        final['Language'].append(e)
        final['Rating'].append(f)
        print(i, "Scraped out",titles)
    except:
        print(test,"is throwing an error")
    i+=1
pd1=pd.DataFrame(final)
compression_opts = dict(method='zip',
                        archive_name='out.csv') 
pd1.to_csv('out.zip', index=False,
          compression=compression_opts)