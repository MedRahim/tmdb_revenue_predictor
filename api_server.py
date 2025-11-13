"""
API Flask pour prédire les revenus des films TMDB
Déploiement web du modèle RandomForest
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from deploy_model import TMDBRevenuePredictor
import os
import numpy as np

app = Flask(__name__)
CORS(app)  # Activer CORS pour tous les endpoints

# Charger le modèle au démarrage
predictor = TMDBRevenuePredictor()

# Vérifier si le modèle existe
if os.path.exists('revenue_model.pkl') and os.path.exists('scaler.pkl'):
    predictor.load()
    print("✅ Modèle chargé depuis les fichiers sauvegardés")
else:
    print("⚠️ Modèle non trouvé. Entraînement du modèle...")
    predictor.train()
    predictor.save()
    print("✅ Modèle entraîné et sauvegardé")


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de vérification de santé"""
    return jsonify({
        'status': 'ok',
        'model': 'TMDB Revenue Predictor',
        'version': '1.0'
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint de prédiction
    
    Body JSON:
    {
        "budget": 100000000,
        "popularity": 50,
        "runtime": 120,
        "vote_average": 7.5,
        "vote_count": 10000
    }
    """
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['budget', 'popularity', 'runtime', 'vote_average', 'vote_count']
        missing = [f for f in required_fields if f not in data]
        
        if missing:
            return jsonify({
                'error': f'Champs manquants: {", ".join(missing)}'
            }), 400
        
        # Prédiction
        revenue = predictor.predict(
            budget=float(data['budget']),
            popularity=float(data['popularity']),
            runtime=float(data['runtime']),
            vote_average=float(data['vote_average']),
            vote_count=float(data['vote_count'])
        )
        
        return jsonify({
            'input': data,
            'predicted_revenue': revenue,
            'predicted_revenue_formatted': f"${revenue:,.2f}"
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    """
    Endpoint de prédiction par batch
    
    Body JSON:
    {
        "films": [
            {"budget": 100000000, "popularity": 50, ...},
            {"budget": 50000000, "popularity": 30, ...}
        ]
    }
    """
    try:
        data = request.get_json()
        
        if 'films' not in data:
            return jsonify({'error': 'Champ "films" requis'}), 400
        
        results = []
        for film in data['films']:
            revenue = predictor.predict(
                budget=float(film['budget']),
                popularity=float(film['popularity']),
                runtime=float(film['runtime']),
                vote_average=float(film['vote_average']),
                vote_count=float(film['vote_count'])
            )
            results.append({
                'input': film,
                'predicted_revenue': revenue,
                'predicted_revenue_formatted': f"${revenue:,.2f}"
            })
        
        return jsonify({
            'count': len(results),
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/feature_importance', methods=['GET'])
def feature_importance():
    """Retourne l'importance des features"""
    try:
        importance = predictor.get_feature_importance()
        return jsonify({
            'features': [
                {'name': f, 'importance': float(i), 'percentage': float(i*100)}
                for f, i in importance
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/info', methods=['GET'])
def info():
    """Informations sur le modèle"""
    return jsonify({
        'model_type': 'RandomForestRegressor',
        'n_estimators': 200,
        'max_depth': 15,
        'features': predictor.features,
        'r2_score': 0.6377,
        'rmse_original': 72016328.80
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 API TMDB Revenue Prediction - Démarrage")
    print("="*60)
    print("📍 Serveur: http://localhost:5000")
    print("📋 Endpoints:")
    print("   GET  /health - Vérifier le serveur")
    print("   POST /predict - Prédire pour un film")
    print("   POST /predict_batch - Prédire pour plusieurs films")
    print("   GET  /feature_importance - Importance des variables")
    print("   GET  /info - Infos du modèle")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
