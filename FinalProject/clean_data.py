#import streamlit as st
#import boto3
import pandas as pd
#import mysql.connector
#from mysql.connector import Error
from io import StringIO
import ast
from pathlib import Path

# AWS S3 Configuration

MOVIE_FILE = "datasets/movies_full/movies_metadata.csv"
CREDITS_FILE = "datasets/movies_full/credits.csv"
TV_SHOW_FILE = "datasets/tv_full.csv"
ALBUM_FILE = "datasets/spotify_full/top_10000_1950-now.csv"


# Function to extract names from the cast list
def extract_cast_names(cast_str):
    try:
        cast_list = ast.literal_eval(cast_str)  # Convert string to Python list
        return [person['name'] for person in cast_list]
    except (ValueError, KeyError):
        return []

# Function to extract crew names
def extract_crew_names(crew_str):
    try:
        crew_list = ast.literal_eval(crew_str)
        return [person['name'] for person in crew_list]
    except (ValueError, KeyError):
        return []

# Function to extract director's name
def extract_director_name(crew_str):
    try:
        crew_list = ast.literal_eval(crew_str)  # Safely parse the string into a list
        for person in crew_list:
            if person.get('job') == 'Director':  # Use .get to avoid KeyError
                return person.get('name', None)  # Return None if 'name' is missing
        return None  # Return None if no director is found
    except (ValueError, SyntaxError):  # Catch errors in literal_eval
        return None

def create_spotify_ids(dataframe, column_name):
    dataframe['id'] = pd.factorize(dataframe[column_name])[0] + 1  # Generate unique integer IDs
    return dataframe


def main():
    
    
    movie_data = pd.read_csv(MOVIE_FILE)
    credits_data = pd.read_csv(CREDITS_FILE)

    tv_show_data = pd.read_csv(TV_SHOW_FILE)

    spotify_data = pd.read_csv(ALBUM_FILE)
    
    cleaned_credits = pd.DataFrame()
    # Apply the functions to the DataFrame
    cleaned_credits['cast'] = credits_data['cast'].apply(extract_cast_names)
    cleaned_credits['crew'] = credits_data['crew'].apply(extract_crew_names)
    cleaned_credits['directors'] = credits_data['crew'].apply(extract_director_name)
    cleaned_credits['id'] = credits_data['id']
        
    cleaned_credits = cleaned_credits[['cast', 'crew', 'directors', 'id']]

    movie_data['id'] = movie_data['id'].astype(str)
    cleaned_credits['id'] = cleaned_credits['id'].astype(str)
    
    movie_merged = pd.merge(movie_data, cleaned_credits, on="id", how="outer")
    movie_final = movie_merged[['title', 'overview', 'cast', 'directors', 'crew', 'release_date', 'runtime', 'id']]
    tv_final = tv_show_data[['name', 'number_of_seasons', 'number_of_episodes', 'overview', 'first_air_date', 'last_air_date', 'created_by', 'id']]
    spotify_final = spotify_data[['Track Name', 'Artist Name(s)', 'Album Name', 'Album Artist Name(s)', 'Album Release Date', 'Track Number', 'Artist Genres']]
    spotify_final = create_spotify_ids(spotify_final, 'Album Name')
    
    movie_final.to_csv('movie_final.csv', index=False)
    tv_final.to_csv('tv_final.csv', index=False)
    spotify_final.to_csv('spotify_final.csv', index=False)
    print("Cleaned data generated!")

    

if __name__ == "__main__":
    main()
