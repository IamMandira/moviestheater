
from urllib import request
import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import pandas as pd
import numpy as np
import requests


def get_movie_id(selected_movie_name):
  res_movie_id=movies_list[movies_list['title'] == selected_movie_name]['movie_id'].iloc[0]
  return res_movie_id
def get_genre_movies(selected_genre):
  selected_genre=selected_genre.lower()
  ids=[]
  ids=genre_movies[genre_movies['genres'].str.contains(selected_genre)]['movie_id'].head(10).tolist()
  return ids
def get_actor_movie_list(selected_actor):
  selected_actor=selected_actor.lower()
  ids=genre_movies[genre_movies['cast'].str.contains(selected_actor)]['movie_id'].tolist()
  return ids
def get_genre_recommendation(selected_genre_list):
  genre_movie_ids=[]
  for i in selected_genre_list:
    i=i.lower()
    movie_ids=genre_movies[genre_movies['genres'].str.contains(i)]['movie_id'].tolist()
    movie_id_set=set(movie_ids)
    genre_movie_ids.append(movie_id_set)
  output_Set=genre_movie_ids[0]
  for i in genre_movie_ids:
    output_Set = output_Set.intersection(i)
  output_list=list(output_Set)
  output_list=output_list[0:12]
  return output_list
def recommend(movie):
  movie_index=movies_list[movies_list['title']==movie].index[0]
  distances=similarity[movie_index]
  movies_list2=sorted(list(enumerate(distances)),reverse=True,key= lambda x:x[1])[1:11]
  recommended_movies=[]
  recommended_ids=[]
  for i in movies_list2:
    recommended_movies.append(movies_list.iloc[i[0]].title)
    recommended_ids.append(movies_list.iloc[i[0]]['movie_id'])
  return recommended_movies,recommended_ids
def show_movie_details(movie_id):
  st.subheader(movies_list[movies_list['movie_id'] ==movie_id ]['title'].iloc[0])
  try:
      url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2619e2000028eeff6dad695d2f621c85&language=en-US"
      response=requests.get(url)
      re=response.json()
      col1,col2=st.columns([1,2])
      with col1:
        st.image("https://image.tmdb.org/t/p/w185/"+re['poster_path'],caption=re['title'])
      with col2:
        st.text(f" Overview: {re['overview']}")
        st.write(f" Release date: {re['release_date']}")
        actor_list=cast_list[cast_list['movie_id'] ==movie_id]['cast'].tolist()
        st.write("Top cast:",actor_list[0][0]," , ",actor_list[0][1]," , ",actor_list[0][2])
        director=cast_list[cast_list['movie_id'] ==movie_id ]['crew'].tolist()
        st.write("Director:"+director[0][0])
        st.write(f" Vote_average: {re['vote_average']}")
  except:
      st.info("Movie details unavailable")
  st.write(" ")
  st.write(" ")
def show_movie_brief(movie_id):
  try:
        url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2619e2000028eeff6dad695d2f621c85&language=en-US"
        response=requests.get(url)
        re=response.json()
        st.image("https://image.tmdb.org/t/p/w185/"+re['poster_path'],caption=re['title'])
  except:
        st.write(movies_list[movies_list['movie_id'] ==movie_id]['title'].iloc[0])
        st.info("Movie details unavailable")
      






movies_list=pickle.load(open('movies.pkl','rb'))
movies_name_list=movies_list['title'].values
similarity=pickle.load(open('similarity.pkl','rb'))
popular_movies=pickle.load(open('movies_popular.pkl','rb'))
genre_movies=pickle.load(open('movies_scored_df.pkl','rb'))
genre_list=pickle.load(open('genre_list.pkl','rb'))
cast_list=pickle.load(open('cast.pkl','rb'))
actor_list=pickle.load(open('actor_list.pkl','rb'))


with st.sidebar:
 selected=option_menu(menu_title="MOVIESTHEATER",
    options=["Home","Search by title","Search by actor","Search by genres","Categories"],
    icons=["house","search","person","tag","star"],
    menu_icon="film",
    default_index=0,
    orientation="vertical"
    )

if selected=="Home":
  st.subheader("POPULAR MOVIES")
  popular_movies_ids=popular_movies['movie_id'].values
  index=0
  cols=st.columns(5)
  cols2=st.columns(5)
  cols3=st.columns(5)
  cols4=st.columns(5)
  for i in cols:
    with i:
      show_movie_brief(popular_movies_ids[index])
      index+=1
  for i in cols2:
    with i:
      show_movie_brief(popular_movies_ids[index])
      index+=1
  for i in cols3:
    with i:
      show_movie_brief(popular_movies_ids[index])
      index+=1
  for i in cols4:
    with i:
      show_movie_brief(popular_movies_ids[index])
      index+=1   
if selected=="Search by actor":
    selected_actor= st.selectbox(
          'type or select the name of the actor to get recommendation',
          actor_list)
    third_button_clicked=st.button('Search',key="3")
    if(third_button_clicked):
      ids=get_actor_movie_list(selected_actor)
      for i in ids:
        show_movie_details(i)
if selected=="Search by genres":
    selected_genres=st.multiselect(
     'Select the genres of the movie to get recommendation',
     genre_list)
    second_button_clicked=st.button('Search',key="2")
    if second_button_clicked:
      #showing movies containing all selected genre
      if len(selected_genres)==0:
        st.write("Please select at least one genre")
      else:
        allgenre_ids=get_genre_recommendation(selected_genres)
        if (len(allgenre_ids))==0:
          st.write("Sorry..We don't have anything matching your search..Please try for some other combination of genres")
        else:
          counter=0
          st.subheader("Recommended for you")
          for i in allgenre_ids:
            show_movie_details(i)  

  
if selected=="Search by title":
    selected_movie_name = st.selectbox(
        'type or select the movie name to get recommendation',
        movies_name_list)
    first_button_clicked=st.button('Search',key="1")
    if(first_button_clicked):
      selected_movie_id=get_movie_id(selected_movie_name)
      show_movie_details(selected_movie_id)

      #showing content based recommended movies
      st.subheader('RECOMMENDED MOVIES')
      recommendations_movies,recommendations_ids=recommend(selected_movie_name)
      for i in recommendations_ids:
          show_movie_details(i)
  
  
if selected=="Categories":
  selected_categories=st.multiselect(
        'Choose your favourite genres',
        genre_list)
  fourth_button_clicked=st.button('RECOMMEND',key="4")
  if(fourth_button_clicked):
    for i in selected_categories:
      st.write(' Popular in ', i)
      genre_ids=get_genre_movies(i)
      cols=st.columns(5)
      cols2=st.columns(5)
      index=0
      for i in cols:
        with i:
          show_movie_brief(genre_ids[index])
          index+=1
      for i in cols2:
        with i:
          show_movie_brief(genre_ids[index])
          index+=1



    
  




  
  
      

  


      

  
  
      