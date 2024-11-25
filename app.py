import streamlit as st
import pickle
import requests
movies=pickle.load(open("similarity.pkl", 'rb'))
similarity=pickle.load(open("movies_list.pkl", 'rb'))
movies_list=movies['title'].values
st.header("Movie Recommender System")
select_value=st.selectbox("Select Movie From Dropdown",movies_list)

def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance=sorted(list(enumerate(similarity[index])),reverse=True ,key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]
    for i in distance[1:6]:
         movies_id=movies.iloc[i[0]].id
         recommend_movie.append(movies.iloc[i[0]].title)
         recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie
    
def fetch_poster(movies_id):
    url="https://api.themoviedb.org/34/movie/550?api_key=115ca7422af5c87a6675cfe25e9da01f"
    data=requests.get(url)
    data=data.json()
    poster_path=data('poster_path')
    full_path ="https://image.tmdb.org/t/p/w500"+poster_path
    return full_path

if st.button("Recommend"):
    movie_name,movie_poster=recommend(select_value)
    col1,col2,col3,col4,col5=st.columns
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1]) 
        st.image(movie_poster[1])   
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])   
        st.image(movie_poster[4])         