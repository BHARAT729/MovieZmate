import streamlit as st
import pickle
import pandas as pd
import requests

# Load the movie data and similarity matrix
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Function to fetch movie posters
def fetch_posters(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NzFlNjZkODBlNzVlMDY1NWQxZWNjYTE3OWYyYjc1YSIsInN1YiI6IjY0YmQwNmI5ZTlkYTY5MDBlY2VhNjJmMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9oIez0y-WbwchQvc-avTyxaRA2Av8H9DrdGdWmOHoEk",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data.get("poster_path", "")

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommend_movie_posters = []
    recommend_movie_ids = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommend_movie_posters.append(fetch_posters(movie_id))
        recommend_movie_ids.append(movie_id)
    return recommended_movies, recommend_movie_posters, recommend_movie_ids

# Function to fetch movie details
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NzFlNjZkODBlNzVlMDY1NWQxZWNjYTE3OWYyYjc1YSIsInN1YiI6IjY0YmQwNmI5ZTlkYTY5MDBlY2VhNjJmMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9oIez0y-WbwchQvc-avTyxaRA2Av8H9DrdGdWmOHoEk",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    overview = data.get("overview", "No overview available.")
    genres = [genre["name"] for genre in data.get("genres", [])]
    release_date = data.get("release_date", "N/A")
    return f"**Overview:** {overview}\n**Genres:** {', '.join(genres)}\n**Release Date:** {release_date}"

# Function to fetch ratings from TMDB
def get_ratings(movie_id):
    url =
