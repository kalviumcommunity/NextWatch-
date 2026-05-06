"""
Configuration module for the NextWatch movie recommendation system.

This module contains all configuration constants, paths, and hyperparameters
used throughout the project.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw_movies.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed_movies.csv"
FEATURES_DATA_PATH = DATA_DIR / "features.csv"
TRAIN_DATA_PATH = DATA_DIR / "train_data.csv"
TEST_DATA_PATH = DATA_DIR / "test_data.csv"

# Model paths
MODELS_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODELS_DIR / "movie_recommendation_model.pkl"
SCALER_PATH = MODELS_DIR / "feature_scaler.pkl"
LABEL_ENCODER_PATH = MODELS_DIR / "label_encoder.pkl"

# Feature configuration
FEATURES = [
    "release_year",
    "rating",
    "vote_count",
    "revenue",
    "budget",
    "runtime",
    "popularity"
]

CATEGORICAL_FEATURES = ["genre"]
TARGET_COLUMN = "next_movie_title"

# Training configuration
TRAIN_TEST_SPLIT_RATIO = 0.2
RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.2

# Model hyperparameters
MODEL_CONFIG = {
    "n_neighbors": 5,
    "weights": "distance",
    "metric": "euclidean",
    "algorithm": "auto"
}

# Genre mapping (extend as needed)
GENRE_MAPPING = {
    "Action": 0,
    "Adventure": 1,
    "Animation": 2,
    "Comedy": 3,
    "Crime": 4,
    "Documentary": 5,
    "Drama": 6,
    "Family": 7,
    "Fantasy": 8,
    "History": 9,
    "Horror": 10,
    "Music": 11,
    "Mystery": 12,
    "Romance": 13,
    "Science Fiction": 14,
    "Thriller": 15,
    "War": 16,
    "Western": 17,
}

# Reverse genre mapping for predictions
REVERSE_GENRE_MAPPING = {v: k for k, v in GENRE_MAPPING.items()}

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"

# Data validation
MIN_YEAR = 1900
MAX_YEAR = 2100
MIN_RATING = 0.0
MAX_RATING = 10.0
MIN_RUNTIME = 1
MAX_RUNTIME = 500

# Feature scaling
SCALE_FEATURES = True
SCALING_METHOD = "standard"  # Options: "standard", "minmax"

# Cross-validation
N_SPLITS = 5
CV_SHUFFLE = True
