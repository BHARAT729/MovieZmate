import pandas as pd
import pickle
import requests

# Load data
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

# Function to fetch posters
def fetch_posters(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NzFlNjZkODBlNzVlMDY1NWQxZWNjYTE3OWYyYjc1YSIsInN1YiI6IjY0YmQwNmI5ZTlkYTY5MDBlY2VhNjJmMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9oIez0y-WbwchQvc-avTyxaRA2Av8H9DrdGdWmOHoEk",
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return "https://image.tmdb.org/t/p/original" + data["poster_path"]


# Function to recommend movies with descriptions and ratings (placeholders for now)
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]

    recommended_movies = []
    recommend_movie_posters = []
    recommend_movie_descriptions = []
    recommend_movie_ratings = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommend_movie_posters.append(fetch_posters(movie_id))

        # Placeholders for descriptions and ratings until you implement the API calls
        recommend_movie_descriptions.append("Description is not available at this moment.")
        recommend_movie_ratings.append("Rating is not available at this moment.")

    return (
        recommended_movies,
        recommend_movie_posters,
        recommend_movie_descriptions,
        recommend_movie_ratings,
    )


similarity = pickle.load(open("similarity.pkl", "rb"))

# Simulate the Streamlit UI for demonstration purposes (assuming you have Streamlit installed)
selected_movie_name = "The Shawshank Redemption"  # Example movie selection

names, posters, descriptions, ratings = recommend(selected_movie_name)

print("Recommended Movies:")
for i in range(len(names)):
    print(f"{i+1}. {names[i]} - Poster: {posters[i]} - Description: {descriptions[i]} - Rating: {ratings[i]}")
