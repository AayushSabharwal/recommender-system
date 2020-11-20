import requests
import lxml
import bs4
def credentials(movie_id):
    ''' Takes as input movie_id
        Returns list of genres, keywords, cast
        Returns title,director, language, rating'''
    
    # Initial lists and values to return
    genre_final=[]
    keywords_final=[]
    cast_final=[]
    director=''
    language=''
    rating=0
    title=''

    
    # Requesting page URL of the given movie id
    web_link="https://www.imdb.com/title/{}/"
    web_link=web_link.format(movie_id)
    req=requests.get(web_link)
    soup=bs4.BeautifulSoup(req.text,'lxml')

    # Find the title of the movie
    title=soup.find('div',{'class':'title_wrapper'})
    title=title.find('h1').getText()
    
    # Scraping out Genres from the Page URL
    genres=soup.find_all('div',{'class':'canwrap'})
    temp_genres=genres[-1].find_all('a')
    for elems in temp_genres:
        temp=elems.getText()
        temp=temp[1:]
        genre_final.append(temp)
    # Scraping out name of the director
    directors=soup.find_all('div',{'class':'credit_summary_item'})
    director=directors[0].find('a')
    director=director.getText()
    
    # Scraping out the cast of the movie
    cast=soup.find('table',{'class':'cast_list'})
    cast=cast.find_all('a')
    for i in range(len(cast)):
        temp=cast[i].getText()
        if(temp!=''):
            if(temp[-1]=='\n'):
                cast_final.append(temp[1:-1])
   # Scraping out few essential keywords of the movie
    temp_keywords=genres[-2].find_all('a')
    for elems in temp_keywords:
        temp=elems.getText()
        temp=temp[1:]
        keywords_final.append(temp)
        
    # Scraping out the language of the movie
    language=soup.find('div',{'class':'article','id':'titleDetails'})
    language=language.find_all('div',{'class':'txt-block'})
    var=0
    language_final='N/A'
    while(var<4):
        lang=language[var].find('h4').getText()
        if(lang=="Language:"):
            language=language[var].find('a').getText()
            language_final=language
            break
        else:
            var+=1
    
    #Scraping out rating of the movie
    rating=soup.find('div',{'class':'ratingValue'})
    rating=float(rating.find('span').getText())
    
    # Returning the values
    return title,genre_final,keywords_final[:-1],director,cast_final,language_final,rating