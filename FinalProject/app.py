import streamlit as st
import boto3
import pandas as pd
import mysql.connector
from mysql.connector import Error
from io import StringIO
import ast

# AWS S3 Configuration
S3_BUCKET = "movies-ds4300-final"
MOVIE_FILE = "movie_final.csv"
TV_SHOW_FILE = "tv_final.csv"
ALBUM_FILE = "spotify_final.csv"

# MySQL RDS Configuration
DB_CONFIG = {
    "host": "mysql-gawler-final.crk4sk6g2c1k.us-east-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Miami9663!",
    "database": "mysql-gawler-final"
}



def main():
    st.title("Betterboxd")

    # Load data from S3
    st.sidebar.header("Recent Reviews")
    #search_query = st.sidebar.text_input("Search", "")
    #print(search_query)
    
    with st.spinner("Loading data..."):
        #movie_data = load_data_from_s3(S3_BUCKET, MOVIE_FILE)
        #tv_show_data = load_data_from_s3(S3_BUCKET, TV_SHOW_FILE)
        #album_data = load_data_from_s3(S3_BUCKET, ALBUM_FILE)
        movie_data = pd.read_csv(MOVIE_FILE)
        tv_show_data = pd.read_csv(TV_SHOW_FILE)
        spotify_data = pd.read_csv(ALBUM_FILE)

    # Search and Display Results
    def search_data(dataframe, query):
        if query:
            return dataframe[dataframe.apply(lambda row: query.lower() in row.to_string().lower(), axis=1)]
        return dataframe

    # Define tabs
    tab1, tab2, tab3 = st.tabs(
        ["🎥 Movie Reviews", "📺 TV Show Reviews", "🎵 Album Reviews"]
    )

    # Tab 1: Movie Reviews
    with tab1:
        st.markdown("### Select a Movie")
        movie_search = st.text_input("Search Movies")
        filtered_movies = search_data(movie_data, movie_search)
        print(filtered_movies)
        st.dataframe(filtered_movies if not filtered_movies.empty else movie_data.head())
        #selected_movie_id = st.selectbox("Movies", filtered_movies["movieId"], format_func=lambda mid: filtered_movies.loc[filtered_movies["movieId"] == mid, "movieId"].values[0])
        #selected_movie_row = filtered_movies[filtered_movies["movieId"] == selected_movie_id]
        #if not selected_movie_row.empty:
        #    st.write("Selected Movie Details:")
        #    st.dataframe(selected_movie_row)
        #movie_review = st.text_area("Write your review:")
        # if st.button("Submit Movie Review"):
        #     if save_review_to_rds("Movie", selected_movie, movie_review):
        #         st.success(f"Review for '{selected_movie}' saved successfully!")

    # Tab 2: TV Show Reviews
    with tab2:
        st.markdown("### Select a TV Show")
        tv_search = st.text_input("Search TV Shows")
        filtered_tv_shows = search_data(tv_show_data, tv_search)
        print(filtered_tv_shows)
        st.dataframe(filtered_tv_shows if not filtered_tv_shows.empty else tv_show_data.head())
        # selected_tv_show = st.selectbox("TV Shows", filtered_tv_shows["title"] if not filtered_tv_shows.empty else ["No matches found"])
        # tv_show_review = st.text_area("Write your review:")
        # if st.button("Submit TV Show Review"):
        #     if save_review_to_rds("TV Show", selected_tv_show, tv_show_review):
        #         st.success(f"Review for '{selected_tv_show}' saved successfully!")

    # Tab 3: Album Reviews
    with tab3:
        st.markdown("### Select an Album")
        spotify_search = st.text_input("Search Songs")
        filtered_albums = search_data(spotify_data, spotify_search)
        print(filtered_albums)
        st.dataframe(filtered_albums if not filtered_albums.empty else spotify_data.head())

        
        # selected_album = st.selectbox("Albums", filtered_albums["title"] if not filtered_albums.empty else ["No matches found"])
        # album_review = st.text_area("Write your review:")
        # if st.button("Submit Album Review"):
        #     if save_review_to_rds("Album", selected_album, album_review):
        #         st.success(f"Review for '{selected_album}' saved successfully!")

if __name__ == "__main__":
    main()
