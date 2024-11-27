from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__, static_folder="frontend")

# Load the dataset
data = pd.read_csv('movies_data_cleaned.csv')

# Precompute similarity matrix
# Combine genres into a single string for each movie if not already done
genre_columns = [col for col in data.columns if col not in ['title', 'release_year', 'rating', 'description', 'poster_url']]
data['combined_genres'] = data[genre_columns].apply(lambda row: ' '.join(row[row == 1].index), axis=1)

# Combine genres and description into one metadata column
data['combined_metadata'] = data['combined_genres'] + ' ' + data['description'].fillna('')

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = vectorizer.fit_transform(data['combined_metadata'])
cosine_sim = cosine_similarity(tfidf_matrix)

# Serve the frontend files
@app.route('/')
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/<path:path>')
def serve_static_file(path):
    return send_from_directory(app.static_folder, path)

# Recommendation endpoint
@app.route('/recommend', methods=['GET'])
def recommend_movies():
    title = request.args.get('title')
    if title not in data['title'].values:
        return jsonify({'error': 'Movie not found'})

    # Find the movie index
    idx = data[data['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get top 5 recommendations
    recommendations = [data.iloc[i[0]]['title'] for i in sim_scores[1:6]]
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


@app.route('/movie-details', methods=['GET'])
def movie_details():
    title = request.args.get('title')
    movie = data[data['title'] == title].iloc[0]
    return jsonify({
        'title': movie['title'],
        'description': movie['description'],
        'poster_url': movie['poster_url']
    })





@app.route('/suggest', methods=['GET'])
def suggest_movies():
    query = request.args.get('query', '').lower()

    if not query:
        return jsonify([])

    # Filter movies containing the query
    suggestions = data[data['title'].str.lower().str.contains(query, na=False)]['title'].head(10).tolist()
    return jsonify(suggestions)
