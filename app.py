import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Download pkl files from Google Drive
def download_file_from_drive(drive_url, output_filename):
    file_id = drive_url.split("/d/")[1].split("/")[0]
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    gdown.download(download_url, output_filename, quiet=False)

# Paths to save the downloaded files
movies_dict_path = "movies_dict.pkl"
movies_path = "movies.pkl"
similarity_path = "similarity.pkl"

# Download the files if not already downloaded
if not os.path.exists(movies_dict_path):
    download_file_from_drive("https://drive.google.com/file/d/1rHVsr9PGql3I7HMBmLa-YCy3tnMhyswG/view?usp=drivesdk", movies_dict_path)

if not os.path.exists(movies_path):
    download_file_from_drive("https://drive.google.com/file/d/1tRumsN4fdqmZmoIOdpQQo3Qtkt64PXCS/view?usp=drivesdk", movies_path)

if not os.path.exists(similarity_path):
    download_file_from_drive("https://drive.google.com/file/d/1WtWvlREFnJYCQs_uKsxQqLHD26GyR4uX/view?usp=drivesdk", similarity_path)

# Load movie data and similarity matrix
movies_dict = pickle.load(open(movies_dict_path, "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open(similarity_path, "rb"))

# TMDB API Headers
API_HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NzFlNjZkODBlNzVlMDY1NWQxZWNjYTE3OWYyYjc1YSIsInN1YiI6IjY0YmQwNmI5ZTlkYTY5MDBlY2VhNjJmMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9oIez0y-WbwchQvc-avTyxaRA2Av8H9DrdGdWmOHoEk",
}

# Fetch movie posters
def fetch_posters(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(url, headers=API_HEADERS)
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data.get("poster_path", "")

# Recommend movie
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

# Fetch movie details
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(url, headers=API_HEADERS)
    data = response.json()
    overview = data.get("overview", "No overview available.")
    genres = [genre["name"] for genre in data.get("genres", [])]
    release_date = data.get("release_date", "N/A")
    return f"**Overview:** {overview}\n**Genres:** {', '.join(genres)}\n**Release Date:** {release_date}"

# Fetch cast information
def get_cast(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    response = requests.get(url, headers=API_HEADERS)
    data = response.json()
    cast_list = data.get("cast", [])
    main_cast = cast_list[:5]  # Fetch only top 5 cast members
    cast_details = [
        f"{member['name']} as {member['character']}" for member in main_cast
    ]
    return cast_details if cast_details else ["No cast information available."]

# Fetch ratings
def get_ratings(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(url, headers=API_HEADERS)
    data = response.json()
    ratings = {
        "TMDB Average Rating": data.get("vote_average", "N/A"),
        "TMDB Vote Count": data.get("vote_count", "N/A")
    }
    return ratings

# Fetch trailer
def get_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"
    response = requests.get(url, headers=API_HEADERS)
    data = response.json()
    if "results" in data and len(data["results"]) > 0:
        for video in data["results"]:
            if video["type"] == "Trailer" and video["site"] == "YouTube":
                return f"https://www.youtube.com/watch?v={video['key']}"
    return None

# Add background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://i.imgur.com/YmqAzL1.png');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit UI
st.title("MovieZmate (Movies Recommendation System)")

selected_movie_name = st.selectbox(
    "Select A Movie From Below List", movies["title"].values
)

if st.button("Find Movies For Me"):
    names, posters, movie_ids = recommend(selected_movie_name)

    for i, (name, poster, movie_id) in enumerate(zip(names, posters, movie_ids)):
        with st.container():
            st.image(poster)
            st.text(name)
            st.write(get_movie_details(movie_id))
            
            # Display ratings
            ratings = get_ratings(movie_id)
            if ratings:
                st.write("**Ratings:**")
                for source, rating in ratings.items():
                    st.write(f"- {source}: {rating}")

            # Display cast information
            cast = get_cast(movie_id)
            st.write("**Main Cast:**")
            for member in cast:
                st.write(f"- {member}")

            # Display trailer link with YouTube logo and "Watch Trailer" button
            trailer_url = get_trailer(movie_id)
            if trailer_url:
                youtube_logo_url = "https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png"
                
                # Display the "Watch Trailer on YouTube" button and the logo
                st.markdown(
                    f'<a href="{trailer_url}" target="_blank">'
                    f'<button style="background-color: red; color: white; padding: 10px 20px; border-radius: 5px; display: flex; align-items: center; justify-content: center;">'
                    f'<img src="{youtube_logo_url}" alt="YouTube" style="width: 30px; height: 30px; margin-right: 10px;">'
                    f'Watch Trailer on YouTube</button></a>',
                    unsafe_allow_html=True,
                )
