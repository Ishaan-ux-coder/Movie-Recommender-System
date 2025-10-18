import streamlit as st
import pandas as pd
import requests
import pickle
from io import BytesIO

# Google Drive direct download link
PICKLE_URL = "https://drive.google.com/uc?export=download&id=1QWn7fmO_7dVDM6hRAkew72TNT6LbZuHB"

# Load movie data from Google Drive (cached for faster reloads)
@st.cache_data(show_spinner=True)
def load_movie_data():
    st.info("Downloading movie data... Please wait ⏳")
    response = requests.get(PICKLE_URL)
    response.raise_for_status()
    data = pickle.load(BytesIO(response.content))
    st.success("✅ Movie data loaded successfully!")
    return data  # Expecting (movies, cosine_sim)

# Load data
movies, cosine_sim = load_movie_data()

# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Streamlit UI
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

st.title("🎥 Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Recommend"):
    recommendations = get_recommendations(selected_movie)
    st.write("### Top 10 Recommended Movies for You 🎯")

    # 2x5 grid layout for movie posters
    for i in range(0, 10, 5):
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i + 5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)
                with col:
                    st.image(poster_url, width=130)
                    st.caption(movie_title)
