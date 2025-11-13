# 🎬 TMDB Movie Revenue Prediction Model - Déploiement

Modèle de machine learning pour prédire les revenus des films basé sur les données TMDB 5000.

## 📊 Performance du Modèle

- **Modèle**: RandomForest (200 arbres)
- **R² Score**: 0.6377 (explique 63.77% de la variance)
- **RMSE**: $72,016,328.80
- **Features**: Budget, Popularité, Durée, Note, Nombre de votes

## 🚀 Déploiement Rapide

### Option 1: Utilisation en Python

```bash
# 1. Entraîner et tester le modèle
python deploy_model.py

# Output:
# ✅ Modèle entraîné avec succès!
# ✨ Revenue Prédit: $150,000,000.00
```

### Option 2: Serveur API Flask (Web Service)

```bash
# 1. Installer Flask
pip install flask

# 2. Démarrer le serveur
python api_server.py

# ✅ API disponible sur http://localhost:5000
```

### Option 3: Interface Web Interactive

```bash
# Après avoir démarré le serveur API
# Ouvrir dans le navigateur:
# file:///.../index.html

# OU servir avec Python:
python -m http.server 8000
# Puis aller à http://localhost:8000
```

## 📡 API Endpoints

### 1. Health Check
```bash
GET http://localhost:5000/health
```

**Réponse:**
```json
{
  "status": "ok",
  "model": "TMDB Revenue Predictor",
  "version": "1.0"
}
```

### 2. Prédiction Simple
```bash
POST http://localhost:5000/predict
Content-Type: application/json

{
  "budget": 100000000,
  "popularity": 50,
  "runtime": 120,
  "vote_average": 7.5,
  "vote_count": 10000
}
```

**Réponse:**
```json
{
  "input": {
    "budget": 100000000,
    "popularity": 50,
    "runtime": 120,
    "vote_average": 7.5,
    "vote_count": 10000
  },
  "predicted_revenue": 150234567.89,
  "predicted_revenue_formatted": "$150,234,567.89"
}
```

### 3. Prédiction par Batch
```bash
POST http://localhost:5000/predict_batch
Content-Type: application/json

{
  "films": [
    {
      "budget": 100000000,
      "popularity": 50,
      "runtime": 120,
      "vote_average": 7.5,
      "vote_count": 10000
    },
    {
      "budget": 50000000,
      "popularity": 30,
      "runtime": 100,
      "vote_average": 6.8,
      "vote_count": 5000
    }
  ]
}
```

### 4. Importance des Features
```bash
GET http://localhost:5000/feature_importance
```

**Réponse:**
```json
{
  "features": [
    {"name": "budget", "importance": 0.65, "percentage": 65.0},
    {"name": "popularity", "importance": 0.20, "percentage": 20.0},
    {"name": "vote_count", "importance": 0.10, "percentage": 10.0},
    {"name": "vote_average", "importance": 0.04, "percentage": 4.0},
    {"name": "runtime", "importance": 0.01, "percentage": 1.0}
  ]
}
```

### 5. Infos du Modèle
```bash
GET http://localhost:5000/info
```

**Réponse:**
```json
{
  "model_type": "RandomForestRegressor",
  "n_estimators": 200,
  "max_depth": 15,
  "features": ["budget", "popularity", "runtime", "vote_average", "vote_count"],
  "r2_score": 0.6377,
  "rmse_original": 72016328.80
}
```

## 💻 Utilisation en Python

### Exemple 1: Prédiction Simple

```python
from deploy_model import TMDBRevenuePredictor

# Charger le modèle
predictor = TMDBRevenuePredictor()
predictor.load()

# Prédire
revenue = predictor.predict(
    budget=100_000_000,
    popularity=50,
    runtime=120,
    vote_average=7.5,
    vote_count=10_000
)

print(f"Revenue Prédit: ${revenue:,.2f}")
# Revenue Prédit: $150,234,567.89
```

### Exemple 2: Prédiction par Batch

```python
import pandas as pd
from deploy_model import TMDBRevenuePredictor

# Préparer les données
df = pd.DataFrame({
    'budget': [100_000_000, 50_000_000],
    'popularity': [50, 30],
    'runtime': [120, 100],
    'vote_average': [7.5, 6.8],
    'vote_count': [10_000, 5_000]
})

# Prédire
predictor = TMDBRevenuePredictor()
predictor.load()
revenues = predictor.predict_batch(df)

print(revenues)
```

### Exemple 3: Feature Importance

```python
predictor = TMDBRevenuePredictor()
predictor.load()

for feature, importance in predictor.get_feature_importance():
    print(f"{feature}: {importance*100:.1f}%")
```

## 📋 Structure des Fichiers

```
final2/
├── TMDB_Phase2_Presentation_Restored.ipynb  # Notebook complet avec analyses
├── deploy_model.py                          # Classe de déploiement du modèle
├── api_server.py                            # Serveur API Flask
├── index.html                               # Interface web interactive
├── README.md                                # Ce fichier
├── tmdb_5000_movies.csv                     # Données sources
├── revenue_model.pkl                        # Modèle sauvegardé
└── scaler.pkl                               # Scaler sauvegardé
```

## 📦 Dépendances

```
pandas>=1.3
numpy>=1.20
scikit-learn>=0.24
flask>=2.0 (pour API)
matplotlib>=3.4 (pour visualisations)
seaborn>=0.11 (pour visualisations)
```

### Installation

```bash
pip install pandas numpy scikit-learn flask matplotlib seaborn
```

## 🎯 Cas d'Usage

### 1. **Évaluation de Projets Cinématographiques**
Prédire le ROI potentiel avant d'investir

### 2. **Benchmarking**
Comparer votre film avec les projections du marché

### 3. **Stratégie de Marketing**
Optimiser le budget marketing basé sur les revenus estimés

### 4. **Analyse Comparative**
Tester différents scénarios (budget, popularité, etc.)

## ⚠️ Limitations

- Le modèle se base sur les données historiques TMDB (2014-2020)
- Les films récents ou très spécialisés peuvent avoir des prédictions moins précises
- Les facteurs externes (pandémie, trends) ne sont pas pris en compte
- Les revenus internationaux varient beaucoup selon le pays/culture

## 🔄 Améliorations Possibles

- [ ] Ajouter des données plus récentes
- [ ] Intégrer des features de genres/pays
- [ ] Ensemble de modèles (ensemble learning)
- [ ] API GraphQL
- [ ] Dashboard Streamlit
- [ ] Dockerization
- [ ] CI/CD Pipeline

## 📄 Licence

À usage éducatif et professionnel.

## 👨‍💻 Support

Pour toute question ou problème:
1. Vérifier que les données CSV sont dans le bon répertoire
2. S'assurer que les dépendances sont installées
3. Consulter les logs d'erreur
4. Réentraîner le modèle si nécessaire

---

**Créé avec ❤️ pour la prédiction de revenus TMDB**
