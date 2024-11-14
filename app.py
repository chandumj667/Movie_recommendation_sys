import streamlit as st
st.title("movie recommendation system")
import pickle
import pandas as pd
import requests

def poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7af877499b8ca0aaed20794724a41338&language=en-US", timeout=15)
    response.raise_for_status()
    data = response.json()
    # return ("https://image.tmdb.org/t/p/original/" + data['poster_path'])
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/original/" + poster_path
    else:
        # Provide a default image if 'poster_path' is None
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances =  similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies=[]
    recommended_movies_poster =[]
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(poster(movie_id))
    return recommended_movies, recommended_movies_poster


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'],
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    c1, c2, c3, c4, c5 =  st.columns(5)
    with c1:
        st.text(names[0])
        st.image(posters[0])
    
    with c2:
        st.text(names[1])
        st.image(posters[1])
    
    with c3:
        st.text(names[2])
        st.image(posters[2])
    
    with c4:
        st.text(names[3])
        st.image(posters[3])
    
    with c5:
        st.text(names[4])
        st.image(posters[4])
    
    # for i in recommendations:
    #     st.write(i)

st.write("You selected:", selected_movie_name)