import streamlit as st
import pickle
import requests

# Load movie data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDb API key
API_KEY = "Replace with your actual TMDb API key"  # Replace with your actual TMDb API key

st.title("Movie Recommender system  🎬")

# Movie dropdown
selected_movie_name = st.selectbox(
    "How would you like to communicate",
    movies['title'].values
)


# Function to fetch poster using TMDb
import time

def fetch_poster(movieid, retries=3):
    print(f"Fetching poster for movie ID: {movieid}")
    for attempt in range(retries):
        try:
            response = requests.get(f"https://api.themoviedb.org/3/movie/{movieid}?api_key={API_KEY}&language=en-US")
            data = response.json()
            poster_url = "https://image.tmdb.org/t/p/w500" + data['poster_path']
            print(f"Poster URL: {poster_url}")
            return poster_url
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(1)  # Wait before retrying
    print(f"Failed to fetch poster for movie ID {movieid} after {retries} attempts")
    return "sorry image.jpeg"


# Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# Button to recommend
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    for i in range(len(names)):
        with [col1, col2, col3, col4, col5][i]:
            st.text(names[i])
            st.image(posters[i])
