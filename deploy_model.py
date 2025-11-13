"""
TMDB Movie Revenue Prediction Model - Production Deployment
Modèle RandomForest entraîné pour prédire les revenus des films
"""

import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import json
import warnings
warnings.filterwarnings('ignore')


class TMDBRevenuePredictor:
    """Classe pour charger, entraîner et utiliser le modèle de prédiction des revenus TMDB"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.features = ['budget', 'popularity', 'runtime', 'vote_average', 'vote_count']
        self.is_trained = False
        
    def train(self, csv_path='tmdb_5000_movies.csv'):
        """Entraîne le modèle RandomForest sur les données TMDB"""
        print("🔄 Chargement et préparation des données...")
        
        # Charger les données
        movies_df = pd.read_csv(csv_path)
        
        # Nettoyage
        columns_to_drop = ['homepage', 'tagline', 'overview', 'status', 'spoken_languages', 
                          'production_countries', 'production_companies']
        movies_df = movies_df.drop(columns=[c for c in columns_to_drop if c in movies_df.columns])
        movies_df = movies_df.dropna(subset=['revenue', 'budget'])
        
        # Préparation
        movies_cleaned = movies_df.copy()
        movies_cleaned.loc[:, 'runtime'] = movies_cleaned['runtime'].fillna(movies_cleaned['runtime'].median())
        
        # Filtrer outliers (99ème percentile)
        budget_threshold = np.percentile(movies_cleaned['budget'], 99)
        revenue_threshold = np.percentile(movies_cleaned['revenue'], 99)
        mask = (movies_cleaned['budget'] <= budget_threshold) & (movies_cleaned['revenue'] <= revenue_threshold)
        movies_cleaned = movies_cleaned.loc[mask].copy()
        
        # Transformation log
        movies_cleaned.loc[:, 'budget'] = np.log1p(movies_cleaned['budget'])
        movies_cleaned.loc[:, 'revenue'] = np.log1p(movies_cleaned['revenue'])
        
        # Standardisation
        numeric_features = ['popularity', 'runtime', 'vote_average', 'vote_count']
        self.scaler = StandardScaler()
        movies_cleaned.loc[:, numeric_features] = self.scaler.fit_transform(movies_cleaned[numeric_features])
        
        # Préparation X, y
        X = movies_cleaned[self.features]
        y = movies_cleaned['revenue']
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Entraînement
        print("🤖 Entraînement du RandomForest...")
        self.model = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        # Évaluation
        y_pred = self.model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        # Métriques sur échelle originale
        y_test_orig = np.expm1(y_test)
        y_pred_orig = np.expm1(y_pred)
        rmse_orig = np.sqrt(mean_squared_error(y_test_orig, y_pred_orig))
        r2_orig = r2_score(y_test_orig, y_pred_orig)
        
        self.is_trained = True
        
        print(f"\n✅ Modèle entraîné avec succès!")
        print(f"   R² (log-scale):     {r2:.4f}")
        print(f"   RMSE (log-scale):   {rmse:.4f}")
        print(f"   R² (original):      {r2_orig:.4f}")
        print(f"   RMSE (original):    ${rmse_orig:,.2f}")
        
        return self
    
    def save(self, model_path='revenue_model.pkl', scaler_path='scaler.pkl'):
        """Sauvegarde le modèle et le scaler"""
        if not self.is_trained:
            raise ValueError("Le modèle doit être entraîné avant de le sauvegarder")
        
        pickle.dump(self.model, open(model_path, 'wb'))
        pickle.dump(self.scaler, open(scaler_path, 'wb'))
        
        print(f"✅ Modèle sauvegardé: {model_path}")
        print(f"✅ Scaler sauvegardé: {scaler_path}")
        
    def load(self, model_path='revenue_model.pkl', scaler_path='scaler.pkl'):
        """Charge un modèle pré-entraîné"""
        self.model = pickle.load(open(model_path, 'rb'))
        self.scaler = pickle.load(open(scaler_path, 'rb'))
        self.is_trained = True
        
        print("[OK] Model loaded: " + model_path)
        print("[OK] Scaler loaded: " + scaler_path)
        
        return self
    
    def predict(self, budget, popularity, runtime, vote_average, vote_count):
        """
        Prédit le revenue d'un film
        
        Paramètres:
        - budget: Budget du film en dollars
        - popularity: Score de popularité TMDB (0-100)
        - runtime: Durée du film en minutes
        - vote_average: Note moyenne (0-10)
        - vote_count: Nombre de votes
        
        Returns:
        - revenue: Revenu prédit en dollars
        """
        if not self.is_trained:
            raise ValueError("Modèle non entraîné. Utilisez train() ou load() d'abord.")
        
        # Transformation log du budget
        budget_log = np.log1p(budget)
        
        # Standardisation
        numeric_values = np.array([[popularity, runtime, vote_average, vote_count]])
        numeric_scaled = self.scaler.transform(numeric_values)[0]
        
        # Préparation des features
        X = np.array([[budget_log, numeric_scaled[0], numeric_scaled[1], 
                       numeric_scaled[2], numeric_scaled[3]]])
        
        # Prédiction (log-scale)
        revenue_log = self.model.predict(X)[0]
        
        # Conversion en échelle originale
        revenue = np.expm1(revenue_log)
        
        return max(0, revenue)  # Éviter les revenus négatifs
    
    def predict_batch(self, df):
        """Prédit les revenues pour un DataFrame de films"""
        results = []
        
        for idx, row in df.iterrows():
            revenue = self.predict(
                budget=row['budget'],
                popularity=row['popularity'],
                runtime=row['runtime'],
                vote_average=row['vote_average'],
                vote_count=row['vote_count']
            )
            results.append(revenue)
        
        return pd.Series(results, index=df.index)
    
    def get_feature_importance(self):
        """Retourne l'importance des features"""
        if not self.is_trained:
            raise ValueError("Modèle non entraîné")
        
        importance_dict = {
            feature: importance 
            for feature, importance in zip(self.features, self.model.feature_importances_)
        }
        
        return sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)


def main():
    """Fonction principale pour démontrer l'utilisation"""
    
    print("="*60)
    print("TMDB MOVIE REVENUE PREDICTION MODEL")
    print("="*60)
    
    # Créer et entraîner le modèle
    predictor = TMDBRevenuePredictor()
    predictor.train()
    
    # Sauvegarder
    predictor.save()
    
    # Afficher l'importance des features
    print("\n📊 Importance des Features:")
    print("-" * 40)
    for feature, importance in predictor.get_feature_importance():
        print(f"  {feature:15s}: {importance:.4f} ({importance*100:.1f}%)")
    
    # Exemples de prédictions
    print("\n" + "="*60)
    print("EXEMPLES DE PRÉDICTIONS")
    print("="*60)
    
    examples = [
        {
            'nom': 'Film à Budget Modéré',
            'budget': 50_000_000,
            'popularity': 30,
            'runtime': 120,
            'vote_average': 7.0,
            'vote_count': 5000
        },
        {
            'nom': 'Film Blockbuster',
            'budget': 200_000_000,
            'popularity': 80,
            'runtime': 150,
            'vote_average': 8.5,
            'vote_count': 50000
        },
        {
            'nom': 'Film Indépendant',
            'budget': 5_000_000,
            'popularity': 10,
            'runtime': 90,
            'vote_average': 6.5,
            'vote_count': 500
        }
    ]
    
    for example in examples:
        nom = example.pop('nom')
        revenue = predictor.predict(**example)
        print(f"\n{nom}:")
        print(f"  Budget: ${example['budget']:,.0f}")
        print(f"  Popularity: {example['popularity']}/100")
        print(f"  Runtime: {example['runtime']} min")
        print(f"  Vote Average: {example['vote_average']}/10")
        print(f"  Vote Count: {example['vote_count']}")
        print(f"  ✨ Revenue Prédit: ${revenue:,.2f}")
    
    print("\n" + "="*60)
    print("✅ Modèle déployé et prêt à l'emploi!")
    print("="*60)


if __name__ == "__main__":
    main()
