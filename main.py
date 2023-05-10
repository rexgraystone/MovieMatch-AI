import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
import pickle

def convert(text):
    list_ = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            list_.append(i['name'])
        counter+=1
    return list_

def fetch_director(text):
    list_ = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            list_.append(i['name'])
    return list_

def collapse(L):
    list_ = []
    for i in L:
        list_.append(i.replace(" ",""))
    return list_

movies = pd.read_csv('Dataset/tmdb_5000_movies.csv')
credits = pd.read_csv('Dataset/tmdb_5000_credits.csv')
movies = movies.merge(credits, on='title')
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.dropna(inplace=True)

temp = ['genres', 'keywords', 'cast']
for column in temp:
    movies[column] = movies[column].apply(convert)
    
movies['cast'] = movies['cast'].apply(lambda x: x[0:3])
movies['crew'] = movies['crew'].apply(fetch_director)

temp_ = ['genres', 'keywords', 'cast', 'crew']
for column in temp_:
    movies[column] = movies[column].apply(collapse)

movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
new = movies.drop(columns=['overview','genres','keywords','cast','crew'])
new['tags'] = new['tags'].apply(lambda x: " ".join(x))

cv = CountVectorizer(max_features=4806, stop_words='english')
vector = cv.fit_transform(new['tags']).toarray()
similarity = cosine_similarity(vector)

def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    for i in distance[1:6]:
        print(new.iloc[i[0]].title)
        
movie = str(input("Enter a movie name: "))
recommend(movie)

pickle.dump(new, open('movie_list.pkl','wb'))
pickle.dump(similarity, open('similarity.pkl','wb'))