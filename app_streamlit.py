"""
Application Streamlit pour prédire les revenus des films TMDB
Interface web moderne avec Streamlit
"""

import streamlit as st
import pandas as pd
from deploy_model import TMDBRevenuePredictor
import os

# Configuration de la page
st.set_page_config(
    page_title="TMDB Revenue Predictor",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Styles personnalisés
st.markdown("""
    <style>
    .main {
        padding-top: 0rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Titre et description
st.markdown("# 🎬 TMDB Revenue Predictor")
st.markdown("### Prédisez les revenus d'un film avec IA")
st.divider()

# Charger le modèle
@st.cache_resource
def load_model():
    predictor = TMDBRevenuePredictor()
    if os.path.exists('revenue_model.pkl') and os.path.exists('scaler.pkl'):
        predictor.load()
        return predictor, True
    else:
        st.warning("⚠️ Modèle non trouvé. Entraînement du modèle...")
        predictor.train()
        predictor.save()
        return predictor, False

try:
    predictor, model_loaded = load_model()
    if model_loaded:
        st.success("✅ Modèle chargé avec succès")
except Exception as e:
    st.error(f"❌ Erreur lors du chargement du modèle: {e}")
    st.stop()

# Créer deux colonnes pour le layout
col1, col2 = st.columns(2)

with col1:
    budget = st.number_input(
        "💰 Budget ($)",
        min_value=1_000_000,
        value=50_000_000,
        step=1_000_000,
        help="Budget minimum: $1M | Recommandé: $50M-200M"
    )
    
    runtime = st.number_input(
        "⏱️ Durée (minutes)",
        min_value=60,
        max_value=300,
        value=120,
        step=5,
        help="Durée du film en minutes"
    )
    
    vote_count = st.number_input(
        "📊 Nombre de Votes",
        min_value=0,
        value=10_000,
        step=1_000,
        help="Nombre total de votes"
    )

with col2:
    popularity = st.number_input(
        "⭐ Popularité (0-100)",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        help="Score de popularité TMDB"
    )
    
    vote_average = st.number_input(
        "🎯 Note Moyenne (0-10)",
        min_value=0.0,
        max_value=10.0,
        value=7.5,
        step=0.1,
        help="Note moyenne IMDB/TMDB"
    )

st.divider()

# Bouton de prédiction
if st.button("🚀 Prédire le Revenue", use_container_width=True, type="primary"):
    try:
        with st.spinner('Calcul en cours...'):
            revenue = predictor.predict(
                budget=budget,
                popularity=popularity,
                runtime=runtime,
                vote_average=vote_average,
                vote_count=vote_count
            )
        
        # Afficher le résultat
        st.success("✅ Prédiction réussie!")
        
        # Afficher le revenue prédit en grande taille
        col1, col2 = st.columns([1, 1])
        with col1:
            st.metric("💵 Revenue Prédit", f"${revenue:,.0f}")
        
        with col2:
            # Calculer le retour sur investissement (ROI)
            if budget > 0:
                roi = ((revenue - budget) / budget) * 100
                st.metric("📈 ROI", f"{roi:.1f}%")
        
        st.divider()
        
        # Afficher les paramètres utilisés
        st.markdown("### 📋 Paramètres utilisés:")
        params_df = pd.DataFrame({
            'Paramètre': ['Budget', 'Popularité', 'Durée', 'Note Moyenne', 'Nombre de Votes'],
            'Valeur': [
                f"${budget:,}",
                f"{popularity}/100",
                f"{runtime} min",
                f"{vote_average}/10",
                f"{vote_count:,}"
            ]
        })
        st.dataframe(params_df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la prédiction: {e}")

st.divider()

# Sidebar avec informations
with st.sidebar:
    st.markdown("### 📊 Informations du Modèle")
    st.markdown("""
    - **Type**: RandomForestRegressor
    - **Estimators**: 200
    - **Max Depth**: 15
    - **R² Score**: 0.6377
    - **RMSE**: $72,016,329
    
    ### 🎯 Features utilisées
    - Budget
    - Popularité
    - Durée
    - Note Moyenne
    - Nombre de Votes
    """)
    
    st.markdown("---")
    st.markdown("""
    ### 💡 Conseils
    - Budget minimum supporté: $1M
    - Les films blockbuster: $100M+
    - Pour de meilleurs résultats, utilisez des valeurs réalistes
    """)
