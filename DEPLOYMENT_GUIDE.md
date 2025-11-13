# 🚀 Guide de Déploiement sur GitHub & Streamlit Cloud

## Étape 1: Créer un dépôt GitHub

1. Allez sur [GitHub.com](https://github.com)
2. Cliquez sur **"+"** > **"New repository"**
3. **Nom du repo**: `tmdb-revenue-predictor`
4. **Description**: "Machine Learning app to predict movie revenues"
5. Selectionnez **Public** (pour Streamlit Cloud gratuit)
6. **NE cochez PAS** "Initialize with README" (on en a déjà un)
7. Cliquez **"Create repository"**

## Étape 2: Connecter votre Git local à GitHub

Après avoir créé le repo, GitHub vous donnera des commandes. Exécutez:

```powershell
cd "c:\Users\MedRa\OneDrive\Bureau\2éme ingénierie\ML\Prediction"

# Ajouter GitHub comme "remote"
git remote add origin https://github.com/[VOTRE_USERNAME]/tmdb-revenue-predictor.git

# Renommer la branche principale
git branch -M main

# Pousser le code
git push -u origin main
```

**Remplacez `[VOTRE_USERNAME]` par votre nom d'utilisateur GitHub!**

## Étape 3: Déployer sur Streamlit Cloud (Gratuit)

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez-vous avec votre compte GitHub
3. Cliquez **"New app"**
4. Sélectionnez:
   - **Repository**: `tmdb-revenue-predictor`
   - **Branch**: `main`
   - **Main file path**: `app_streamlit.py`
5. Cliquez **"Deploy"**

✨ Votre app sera disponible sur: `https://[votre-username]-tmdb-revenue-predictor.streamlit.app`

## Étape 4: Mettre à jour votre code

Chaque fois que vous modifiez le code localement:

```powershell
# Étape 1: Faire des changements
# ... modifiez vos fichiers ...

# Étape 2: Ajouter les changements
git add .

# Étape 3: Créer un commit
git commit -m "Description du changement"

# Étape 4: Pousser vers GitHub
git push
```

**Streamlit Cloud redéploiera automatiquement!** 🚀

## Troubleshooting

### Le déploiement échoue?

1. **Vérifiez requirements.txt** - assurez-vous que toutes les dépendances sont listées
2. **Vérifiez le nom du fichier** - doit être `app_streamlit.py`
3. **Regardez les logs** - Streamlit Cloud affiche les erreurs

### L'app s'arrête après un moment?

C'est normal sur le plan gratuit de Streamlit Cloud. Attendez quelques secondes et rechargez.

## Options de déploiement alternatives

### Heroku (Payant)
```bash
heroku login
heroku create [votre-app-name]
git push heroku main
```

### AWS / Google Cloud (Payant mais plus flexible)
- Utilisez Docker: `docker build -t app . && docker run -p 8501:8501 app`
- Déployez sur Cloud Run, EC2, etc.

### Railway.app (Simple)
1. Connectez votre repo GitHub
2. Railway détecte automatiquement `requirements.txt` et `app_streamlit.py`
3. Deploy en 1 clic

## 📊 Vérifier le statut du déploiement

- **Streamlit Cloud**: Cliquez sur "Manage app" pour voir les logs
- **GitHub Actions**: Vérifiez l'onglet "Actions" pour les tests CI/CD

## 🎯 Checklist finale

- [ ] Dépôt GitHub créé
- [ ] Code poussé sur `main`
- [ ] Streamlit Cloud connecté
- [ ] App en ligne et fonctionnelle
- [ ] README.md correct
- [ ] Fichier `.gitignore` en place
- [ ] `requirements.txt` à jour

## 💡 Tips

- Utilisez des branches pour les features: `git checkout -b feature/nouvelle-feature`
- Faites des pull requests pour réviser le code
- Activez les GitHub Actions pour l'intégration continue
- Utilisez des badges dans le README: `[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://[votre-app].streamlit.app)`

---

**C'est tout!** Votre app ML est maintenant en ligne et accessible 24/7! 🎉
