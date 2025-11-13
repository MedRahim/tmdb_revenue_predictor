APP_NAME = "TMDB Revenue Predictor"
VERSION = "1.0.0"
AUTHOR = "MedRa"
DESCRIPTION = "Machine Learning app to predict movie revenues using RandomForest"
MODEL_VERSION = "1.0"

# Model Info
MODEL_TYPE = "RandomForestRegressor"
N_ESTIMATORS = 200
MAX_DEPTH = 15
R2_SCORE = 0.6377
RMSE_ORIGINAL = 72016328.80

# Features
FEATURES = ['budget', 'popularity', 'runtime', 'vote_average', 'vote_count']
