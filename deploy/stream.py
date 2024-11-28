import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Load the data
movies_data = pd.read_csv("movies_data.csv")

# Set page configuration
st.set_page_config(
    page_title="Movies Explorer",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title
st.title("🎥 Movies Explorer")

# Sidebar filters
st.sidebar.header("Filter Movies")
selected_genre = st.sidebar.multiselect(
    "Genres", options=sorted(set(
        genre.strip() for sublist in movies_data['genres'].str.split(',') for genre in sublist
    ))
)
selected_year = st.sidebar.slider(
    "Release Year", min_value=int(movies_data['release_year'].min()), max_value=int(movies_data['release_year'].max()), value=(int(movies_data['release_year'].min()), int(movies_data['release_year'].max()))
)
selected_rating = st.sidebar.slider(
    "Rating", min_value=0.0, max_value=10.0, value=(0.0, 10.0), step=0.1
)

# Apply filters
filtered_movies = movies_data[
    (movies_data['release_year'] >= selected_year[0]) &
    (movies_data['release_year'] <= selected_year[1]) &
    (movies_data['rating'] >= selected_rating[0]) &
    (movies_data['rating'] <= selected_rating[1])
]

if selected_genre:
    filtered_movies = filtered_movies[filtered_movies['genres'].apply(lambda x: any(genre.strip() in x for genre in selected_genre))]

# Display movies
st.header("Movies")

if filtered_movies.empty:
    st.write("No movies found with the selected filters.")
else:
    for _, row in filtered_movies.iterrows():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            response = requests.get(row['poster_url'])
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                st.image(img, use_column_width=True)

        with col2:
            st.subheader(row['title'])
            st.write(f"**Release Year:** {row['release_year']}")
            st.write(f"**Rating:** {row['rating']}")
            st.write(f"**Genres:** {row['genres']}")
            st.write(row['description'])

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ by Streamlit")
