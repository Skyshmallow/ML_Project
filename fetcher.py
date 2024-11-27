import requests
import pandas as pd

# Replace with your actual API key
API_KEY = '401aa692d6aa27c92e0fc0adedd58769'
BASE_URL = 'https://api.themoviedb.org/3'

def fetch_movies(page=1):
    """
    Fetch popular movies from TMDb API.
    :param page: Page number for pagination
    :return: List of movie details
    """
    url = f"{BASE_URL}/movie/popular"
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'page': page
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

def extract_movie_data(movie):
    """
    Extract required attributes from a movie dictionary.
    :param movie: Movie details from TMDb API
    :return: Dictionary with required fields
    """
    return {
        'title': movie.get('title'),
        'release_year': movie.get('release_date', '').split('-')[0],
        'rating': movie.get('vote_average'),
        'genres': movie.get('genre_ids'),  # We'll map these later
        'description': movie.get('overview'),
        'poster_url': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None
    }

def get_genre_mapping():
    """
    Fetch genre mapping from TMDb API.
    :return: Dictionary mapping genre IDs to genre names
    """
    url = f"{BASE_URL}/genre/movie/list"
    params = {'api_key': API_KEY, 'language': 'en-US'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        return {genre['id']: genre['name'] for genre in genres}
    else:
        print(f"Error fetching genres: {response.status_code}")
        return {}

# Main Script
if __name__ == '__main__':
    genre_mapping = get_genre_mapping()
    all_movies = []
    
    # Fetch multiple pages of movies (adjust the range for more data)
    for page in range(1, 251):  # Fetch 5 pages
        movies = fetch_movies(page)
        for movie in movies:
            data = extract_movie_data(movie)
            # Map genre IDs to names
            if data['genres']:
                data['genres'] = ', '.join([genre_mapping.get(genre_id, 'Unknown') for genre_id in data['genres']])
            all_movies.append(data)
    
    # Save to CSV
    df = pd.DataFrame(all_movies)
    df.to_csv('movies_data.csv', index=False)
    print("Data saved to movies_data.csv")
