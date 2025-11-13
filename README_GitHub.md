# 🎬 TMDB Revenue Predictor

Un système de prédiction des revenus des films basé sur le machine learning, utilisant les données TMDB. L'application utilise un modèle **RandomForest** entraîné sur des données réelles de films.

## 🚀 Déploiement

### Streamlit Cloud (Recommandé - Gratuit)

1. **Créez un compte** sur [Streamlit Cloud](https://streamlit.io/cloud)
2. **Connectez votre repo GitHub**
3. **Déploiez** en 1 clic !

L'application sera disponible sur: `https://[votre-nom]-tmdb-revenue-predictor.streamlit.app`

### Local

```bash
# 1. Clonez le repo
git clone https://github.com/[votre-user]/tmdb-revenue-predictor.git
cd tmdb-revenue-predictor

# 2. Créez un environnement virtuel
python -m venv venv
.\venv\Scripts\activate

# 3. Installez les dépendances
pip install -r requirements.txt

# 4. Lancez l'app
streamlit run app_streamlit.py
```

## 📊 Features

- **Prédiction en temps réel** des revenus de films
- **Calcul du ROI** (Retour sur Investissement)
- **Interface moderne** avec Streamlit
- **Modèle ML performant** (R² Score: 0.6377)
- **Design responsive** sur tous les appareils

## 🎯 Paramètres d'entrée

| Paramètre | Range | Description |
|-----------|-------|-------------|
| Budget | $1M+ | Budget du film en dollars |
| Popularité | 0-100 | Score de popularité TMDB |
| Durée | 60-300 min | Durée du film en minutes |
| Note Moyenne | 0-10 | Note moyenne IMDB/TMDB |
| Nombre de Votes | 0+ | Nombre total de votes |

## 📈 Modèle ML

- **Type**: RandomForestRegressor
- **Estimators**: 200 arbres
- **Max Depth**: 15
- **R² Score**: 0.6377
- **RMSE**: $72,016,329

## 🔧 Technologies

- **Backend**: Python, scikit-learn
- **Frontend**: Streamlit
- **Data**: TMDB 5000 Movies Dataset
- **Deployment**: Streamlit Cloud / Docker

## 📁 Structure du projet

```
.
├── app_streamlit.py           # Application principale
├── deploy_model.py            # Classe du modèle ML
├── api_server.py              # API Flask (optionnel)
├── index.html                 # Interface HTML (optionnel)
├── requirements.txt           # Dépendances Python
├── Dockerfile                 # Pour déploiement Docker
├── .streamlit/
│   └── config.toml           # Configuration Streamlit
├── .gitignore
└── README.md                  # Ce fichier
```

## 🐳 Déploiement avec Docker

```bash
# Construire l'image
docker build -t tmdb-predictor .

# Lancer le conteneur
docker run -p 8501:8501 tmdb-predictor
```

L'app sera disponible sur `http://localhost:8501`

## 📝 Utilisation

1. Entrez les paramètres du film
2. Cliquez sur "Prédire le Revenue"
3. Consultez la prédiction et le ROI

## 🛠️ Développement

### Entraîner un nouveau modèle

```python
from deploy_model import TMDBRevenuePredictor

predictor = TMDBRevenuePredictor()
predictor.train()
predictor.save()
```

### Utiliser l'API Flask

```bash
python api_server.py
# L'API sera sur http://localhost:5000
```

## 📊 Exemples de prédictions

| Budget | Popularité | Durée | Note | Votes | Revenue Prédit |
|--------|-----------|-------|------|-------|-----------------|
| $100M | 75 | 120 | 7.5 | 50000 | ~$300M |
| $50M | 50 | 110 | 7.0 | 10000 | ~$150M |
| $200M | 80 | 150 | 8.0 | 100000 | ~$600M |

## 🤝 Contribution

Les contributions sont bienvenues ! N'hésitez pas à:
- Ouvrir une issue pour signaler un bug
- Soumettre une PR pour une amélioration
- Suggérer des nouvelles features

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## 👨‍💻 Auteur

TMDB Revenue Predictor - Machine Learning Project

## 📞 Support

Pour toute question, contactez-moi ou ouvrez une issue sur GitHub.

---

**Lien de déploiement**: [À remplir après déploiement]

**Dataset source**: [TMDB 5000 Movies Dataset](https://www.kaggle.com/tmdb/tmdb-movie-metadata)
