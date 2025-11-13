"""
Script مبسط لجلب بيانات الأفلام من TMDB وتحسين الـ model
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
    """جلب بيانات فيلم واحد"""
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            movie = response.json()
            
            # التحقق من وجود budget و revenue
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
    """البحث عن أفلام حسب السنة"""
    movies = []
    
    print(f"📅 جاري البحث عن أفلام سنة {year}...")
    
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
                        # احصل على البيانات الكاملة
                        full_movie = get_movie_data(movie_summary['id'])
                        if full_movie:
                            movies.append(full_movie)
                            print(f"   ✓ {full_movie['title']} ({year})", end="\r")
                        time.sleep(0.1)
        except Exception as e:
            print(f"   ❌ خطأ في الصفحة {page}: {e}")
        
        time.sleep(0.5)
    
    return movies

def main():
    print("="*70)
    print("🎬 TMDB Data Enhancement Script")
    print("="*70)
    
    # جلب أفلام من سنوات مختلفة
    all_movies = []
    
    for year in [2023, 2022, 2021, 2020]:
        movies = search_movies_by_year(year, pages=1)
        all_movies.extend(movies)
        print(f"✅ وجدنا {len(movies)} فيلم من {year}\n")
    
    print(f"\n📊 المجموع: {len(all_movies)} فيلم جديد")
    
    # تحويل لـ DataFrame
    new_df = pd.DataFrame(all_movies)
    
    print(f"\n📁 دمج البيانات...")
    
    # قراءة البيانات القديمة
    try:
        old_df = pd.read_csv('tmdb_5000_movies.csv')
        print(f"   القديمة: {len(old_df)} فيلم")
        
        # دمج
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['id'] if 'id' in combined_df.columns else None, keep='first')
        
        print(f"   الجديدة: {len(new_df)} فيلم")
        print(f"   المدمجة: {len(combined_df)} فيلم")
        
    except:
        combined_df = new_df
        print(f"   استعمال البيانات الجديدة فقط: {len(new_df)} فيلم")
    
    # حفظ
    output_file = 'tmdb_combined.csv'
    combined_df.to_csv(output_file, index=False)
    print(f"\n✅ تم حفظ البيانات في: {output_file}")
    
    # إحصائيات
    print(f"\n📊 الإحصائيات:")
    print(f"   الأعمدة: {list(combined_df.columns)}")
    print(f"   عدد الأفلام: {len(combined_df)}")
    if 'revenue' in combined_df.columns and 'budget' in combined_df.columns:
        print(f"   متوسط الـ revenue: ${combined_df['revenue'].mean():,.0f}")
        print(f"   متوسط الـ budget: ${combined_df['budget'].mean():,.0f}")
    
    print("\n" + "="*70)
    print("✅ انتهى! الآن تقدر تستعمل tmdb_combined.csv للتدريب")
    print("="*70)

if __name__ == "__main__":
    main()
