'''
MovieMatch - Movie Recommendation System
A web application that recommends movies based on user preferences using machine learning
'''

import pickle
import requests
from flask import Flask, request, jsonify, render_template, send_from_directory, redirect
import os
import random
import pandas as pd

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load the movie list and similarity matrix
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    try:
        # Log the movie ID being requested
        print(f"Fetching poster for movie ID: {movie_id}")
        
        # Check if movie_id is valid
        if not movie_id or pd.isna(movie_id):
            print(f"Invalid movie ID: {movie_id}")
            return f"https://via.placeholder.com/500x750/222222/e50914?text=No+Poster"
        
        # Convert to integer if necessary
        try:
            movie_id = int(movie_id)
        except (ValueError, TypeError):
            print(f"Could not convert movie ID to integer: {movie_id}")
            return f"https://via.placeholder.com/500x750/222222/e50914?text=Invalid+ID"
        
        # Make API request
        api_key = "8265bd1679663a7ea12ac168da84d2e8"
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        print(f"Requesting URL: {url}")
        response = requests.get(url, timeout=5)
        
        # Check response status
        if response.status_code != 200:
            print(f"API error: Status {response.status_code} for movie ID {movie_id}")
            return f"https://via.placeholder.com/500x750/222222/e50914?text=API+Error+{response.status_code}"
            
        data = response.json()
        
        # Check if poster path exists
        if 'poster_path' in data and data['poster_path']:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500" + poster_path
            print(f"Found poster: {full_path}")
            return full_path
        else:
            print(f"No poster found for movie ID {movie_id}")
            return f"https://via.placeholder.com/500x750/222222/e50914?text=No+Poster"
    except requests.exceptions.Timeout:
        print(f"Timeout error fetching poster for movie ID {movie_id}")
        return f"https://via.placeholder.com/500x750/222222/e50914?text=Timeout"
    except requests.exceptions.ConnectionError:
        print(f"Connection error fetching poster for movie ID {movie_id}")
        return f"https://via.placeholder.com/500x750/222222/e50914?text=Connection+Error"
    except Exception as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return f"https://via.placeholder.com/500x750/222222/e50914?text=Error"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_movies', methods=['GET'])
def get_movies():
    movie_list = movies['title'].values.tolist()
    return jsonify(movie_list)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    movie = data['movie']
    recommended_movie_names, recommended_movie_posters = recommend(movie)
    
    recommendations = []
    for i in range(len(recommended_movie_names)):
        recommendations.append({
            'title': recommended_movie_names[i],
            'poster': recommended_movie_posters[i]
        })
    
    return jsonify(recommendations)

@app.route('/api/placeholder/<int:id>')
def placeholder_image(id):
    # Use a more reliable placeholder image service
    return redirect(f"https://via.placeholder.com/500x750/222222/e50914?text=MovieMatch")

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    app.run(debug=True)
