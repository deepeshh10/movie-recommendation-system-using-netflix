import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

print("Loading data...")
movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')

print("Movies shape:", movies.shape)
print("Credits shape:", credits.shape)
print("\nMovies columns:", movies.columns.tolist())
print("Credits columns:", credits.columns.tolist())

# Rename movie_id to id in credits for merging
credits = credits.rename(columns={'movie_id': 'id'})

# Merge credits with movies
print("\nMerging datasets...")
movies = movies.merge(credits, on='id')

print("Merged shape:", movies.shape)
print("Merged columns:", movies.columns.tolist())

# Create tags for movies
print("\nProcessing movie features...")
# Fill NaN values with empty strings
movies['overview'] = movies['overview'].fillna('')
movies['genres'] = movies['genres'].fillna('')
movies['keywords'] = movies['keywords'].fillna('')

movies['tags'] = movies['overview'] + ' ' + movies['genres'] + ' ' + movies['keywords']

# Select relevant columns - make sure to keep the TMDB id for API calls
new_df = movies[['id', 'title_x', 'tags']]
new_df = new_df.rename(columns={'title_x': 'title'})

# Check for duplicate titles and print them
duplicate_titles = new_df['title'].duplicated()
if duplicate_titles.any():
    print("\nWarning: Found duplicate movie titles:")
    print(new_df[new_df['title'].duplicated(keep=False)]['title'].unique())

# Create feature vectors
print("\nCreating feature vectors...")
cv = CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(new_df['tags']).toarray()

# Calculate similarity matrix
print("\nCalculating similarity matrix...")
similarity = cosine_similarity(vector)
print(f"Similarity matrix shape: {similarity.shape}")

# Create artifacts directory if it doesn't exist
os.makedirs('artifacts', exist_ok=True)

# Save the processed data and similarity matrix
print("\nSaving model files...")
pickle.dump(new_df, open('artifacts/movie_list.pkl', 'wb'))
pickle.dump(similarity, open('artifacts/similarity.pkl', 'wb'))

print("Done! Model files have been generated successfully.") 