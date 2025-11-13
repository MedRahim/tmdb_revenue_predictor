"""
Script to fetch movie data from TMDB API and improve the ML model
"""

import requests
import pandas as pd
import time
import os

# Fix encoding for Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'

API_KEY = "1b166d942d59f6489f876d314c1430bd"
BASE_URL = "https://api.themoviedb.org/3"

def get_movie_data(movie_id):
    """Fetch complete data for a single movie"""
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            movie = response.json()
            
            # Check if budget and revenue exist
            if movie.get('budget', 0) > 0 and movie.get('revenue', 0) > 0:
                return {
                    'id': movie.get('id'),
                    'title': movie.get('title'),
                    'budget': movie.get('budget', 0),
                    'revenue': movie.get('revenue', 0),
                    'popularity': movie.get('popularity', 0),
                    'runtime': movie.get('runtime', 0),
                    'vote_average': movie.get('vote_average', 0),
                    'vote_count': movie.get('vote_count', 0),
                    'release_date': movie.get('release_date', ''),
                }
    except:
        pass
    
    return None

def search_movies_by_year(year, pages=2):
    """Search for movies by release year"""
    movies = []
    
    print(f"📅 Searching for movies from year {year}...")
    
    for page in range(1, pages + 1):
        url = f"{BASE_URL}/discover/movie"
        params = {
            "api_key": API_KEY,
            "primary_release_year": year,
            "page": page,
            "sort_by": "revenue.desc"
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    for movie_summary in data['results']:
                        # Get full movie details
                        full_movie = get_movie_data(movie_summary['id'])
                        if full_movie:
                            movies.append(full_movie)
                            print(f"   ✓ {full_movie['title']} ({year})", end="\r")
                        time.sleep(0.1)
        except Exception as e:
            print(f"   ❌ Error on page {page}: {e}")
        
        time.sleep(0.5)
    
    return movies

def main():
    print("="*70)
    print("🎬 TMDB Data Enhancement Script")
    print("="*70)
    
    # Fetch movies from different years
    all_movies = []
    
    for year in [2023, 2022, 2021, 2020]:
        movies = search_movies_by_year(year, pages=1)
        all_movies.extend(movies)
        print(f"✅ Found {len(movies)} movies from {year}\n")
    
    print(f"\n📊 Total: {len(all_movies)} new movies")
    
    # Convert to DataFrame
    new_df = pd.DataFrame(all_movies)
    
    print(f"\n📁 Merging data...")
    
    # Read old data
    try:
        old_df = pd.read_csv('tmdb_5000_movies.csv')
        print(f"   Old data: {len(old_df)} movies")
        
        # Merge
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['id'] if 'id' in combined_df.columns else None, keep='first')
        
        print(f"   New data: {len(new_df)} movies")
        print(f"   Combined: {len(combined_df)} movies")
        
    except:
        combined_df = new_df
        print(f"   Using new data only: {len(new_df)} movies")
    
    # Save
    output_file = 'tmdb_combined.csv'
    combined_df.to_csv(output_file, index=False)
    print(f"\n✅ Data saved to: {output_file}")
    
    # Statistics
    print(f"\n📊 Statistics:")
    print(f"   Columns: {list(combined_df.columns)}")
    print(f"   Number of movies: {len(combined_df)}")
    if 'revenue' in combined_df.columns and 'budget' in combined_df.columns:
        print(f"   Average revenue: ${combined_df['revenue'].mean():,.0f}")
        print(f"   Average budget: ${combined_df['budget'].mean():,.0f}")
    
    print("\n" + "="*70)
    print("✅ Done! Now you can use tmdb_combined.csv for training")
    print("="*70)

if __name__ == "__main__":
    main()
