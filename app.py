import streamlit as st
import pickle
import pandas as pd
import os
import urllib.request

import requests
def download_file(url, filename):
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)
MOVIES_URL = "https://github.com/soni132/movie-recommender-system/releases/download/v2.0/movies_dict.pkl"
SIMILARITY_URL = "https://github.com/soni132/movie-recommender-system/releases/download/v2.0/similarity.pkl"

download_file(MOVIES_URL, "movies_dict.pkl")
download_file(SIMILARITY_URL, "similarity.pkl")


API_KEY = "c5c4aafc"

@st.cache_data
def fetch_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    data = requests.get(url).json()

    if data.get("Response") == "True":
        return data.get("Poster")
    return None




movies_dict=pickle.load(open('movies_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters





st.title("Movie Recommender System")

selected_movie_name=st.selectbox(
    'Which movies do you like?',
    (movies["title"].values)
)
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            if poster and poster != "N/A":
                st.image(poster)
            st.write(name)


