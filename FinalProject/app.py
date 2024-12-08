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
    "host": "mysql-gawler-test.crk4sk6g2c1k.us-east-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Miami9663",
    "database": "mysql-gawler-final"
}

s3 = boto3.client('s3')

def save_to_rds(item_type, item_id, item_title, review_text, review_score):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Insert review into database
        query = """
        INSERT INTO reviews (item_type, item_id, item_title, review_text, review_score)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (item_type, item_id, item_title, review_text, review_score))
        connection.commit()
        st.success("Review saved successfully!")
    except Error as e:
        st.error(f"Error saving review: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    st.title("Betterboxd")

    # Load data from S3
    st.sidebar.header("Recent Reviews")
    #search_query = st.sidebar.text_input("Search", "")
    #print(search_query)
    
    with st.spinner("Loading data..."):
        # movie_obj = s3.get_object(Bucket=S3_BUCKET, Key=MOVIE_FILE)
        # movie_data = pd.read_csv(movie_obj['Body'])
        # tv_show_obj = s3.get_object(Bucket=S3_BUCKET, Key=TV_SHOW_FILE)
        # tv_show_data = pd.read_csv(tv_show_obj['Body'])
        # spotify_obj = s3.get_object(S3_BUCKET, ALBUM_FILE)
        # spotify_data = pd.read_csv(spotify_obj['Body'])
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

        selected_movie = st.selectbox("Select a Movie", filtered_movies["title"] if not filtered_movies.empty else movie_data["title"])

        if selected_movie:
            # Get details of the selected movie
            movie_details = movie_data[movie_data["title"] == selected_movie].iloc[0]
            st.markdown(f"### {movie_details['title']}")
            st.markdown(f"**Overview:** {movie_details.get('overview', 'N/A')}")
            st.markdown(f"**Director:** {movie_details.get('directors', 'N/A')}")
            st.markdown(f"**Release Date:** {movie_details.get('release_date', 'N/A')}")
            st.markdown(f"**Runtime:** {movie_details.get('runtime', 'N/A')} minutes")
            st.markdown(f"**Cast:** {movie_details.get('cast', 'N/A')}")
            st.markdown(f"**Crew:** {movie_details.get('crew', 'N/A')}")

            movie_review_text = st.text_area("Write your movie review:")
            movie_review_score = st.slider("Rate the movie (1-10)", 1, 10)

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

        selected_tv_show = st.selectbox("Select a TV Show", filtered_tv_shows["name"] if not filtered_tv_shows.empty else tv_show_data["name"])

        if selected_tv_show:
            # Get details of the selected movie
            tv_show_details = tv_show_data[tv_show_data["name"] == selected_tv_show].iloc[0]
            st.markdown(f"### {tv_show_details['name']}")
            st.markdown(f"**Overview:** {tv_show_details.get('overview', 'N/A')}")
            st.markdown(f"**Created By:** {tv_show_details.get('created_by', 'N/A')}")
            st.markdown(f"**First Air Date:** {tv_show_details.get('first_air_date', 'N/A')}")
            st.markdown(f"**Number of Seasons:** {tv_show_details.get('number_of_seasons', 'N/A')}")
            st.markdown(f"**Number of Episodes:** {tv_show_details.get('number_of_episodes', 'N/A')}")
            

            tv_show_review_text = st.text_area("Write your TV review:")
            tv_show_review_score = st.slider("Rate the show (1-10)", 1, 10)
        # selected_tv_show = st.selectbox("TV Shows", filtered_tv_shows["title"] if not filtered_tv_shows.empty else ["No matches found"])
        # tv_show_review = st.text_area("Write your review:")
        # if st.button("Submit TV Show Review"):
        #     if save_review_to_rds("TV Show", selected_tv_show, tv_show_review):
        #         st.success(f"Review for '{selected_tv_show}' saved successfully!")

    # Tab 3: Album Reviews
    with tab3:
        st.markdown("### Select an Album")
        spotify_search = st.text_input("Search Albums")
        filtered_albums = search_data(spotify_data, spotify_search)
        print(filtered_albums)
        st.dataframe(filtered_albums if not filtered_albums.empty else spotify_data.head())

        selected_album = st.selectbox("Select an Album", filtered_albums["Album Name"] if not filtered_albums.empty else spotify_data["Album Name"])

        if selected_album:
            # Get details of the selected movie
            album_details = spotify_data[spotify_data["Album Name"] == selected_album].iloc[0]
            st.markdown(f"### {album_details['Album Name']}")
            st.markdown(f"**Album Artist:** {album_details.get('Album Artist Name(s)', 'N/A')}")
            st.markdown(f"**Album Release Date:** {album_details.get('Album Release Date', 'N/A')}")
            st.markdown(f"**Artist Genres:** {album_details.get('Artist Genres', 'N/A')}")
            

            album_review_text = st.text_area("Write your album review:")
            album_review_score = st.slider("Rate the album (1-10)", 1, 10)

        
        # selected_album = st.selectbox("Albums", filtered_albums["title"] if not filtered_albums.empty else ["No matches found"])
        # album_review = st.text_area("Write your review:")
        # if st.button("Submit Album Review"):
        #     if save_review_to_rds("Album", selected_album, album_review):
        #         st.success(f"Review for '{selected_album}' saved successfully!")

if __name__ == "__main__":
    main()
