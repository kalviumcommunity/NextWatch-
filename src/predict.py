"""
Prediction module for the NextWatch movie recommendation system.

Handles making predictions on new data and providing recommendations.
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass

from config import (
    MODEL_PATH,
    SCALER_PATH,
    TARGET_COLUMN,
    CATEGORICAL_FEATURES,
    GENRE_MAPPING,
    REVERSE_GENRE_MAPPING,
    LOG_FORMAT,
    LOG_LEVEL,
)

# Configure logging
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)


@dataclass
class PredictionResult:
    """Data class for storing prediction results."""
    predicted_movie_id: float
    confidence: float
    input_movie: str
    input_genre: str
    recommendation_text: str


def validate_input_data(
    movie_title: str,
    genre: str,
    available_genres: Dict[str, int] = GENRE_MAPPING
) -> bool:
    """
    Validate user input for prediction.
    
    Args:
        movie_title: Title of the previously watched movie.
        genre: Genre of the movie.
        available_genres: Dictionary of available genres.
        
    Returns:
        True if input is valid, False otherwise.
    """
    logger.info(f"Validating input: movie='{movie_title}', genre='{genre}'")
    
    if not movie_title or not isinstance(movie_title, str):
        logger.error("Invalid movie title")
        return False
    
    if genre not in available_genres:
        logger.error(f"Genre '{genre}' not found in available genres")
        return False
    
    logger.info("Input validation passed")
    return True


def encode_input_for_prediction(
    movie_features: Dict[str, Any],
    feature_columns: List[str]
) -> np.ndarray:
    """
    Encode and prepare input features for prediction.
    
    Args:
        movie_features: Dictionary with movie features.
        feature_columns: List of expected feature columns in order.
        
    Returns:
        NumPy array ready for model prediction.
    """
    logger.info("Encoding input features for prediction")
    
    # Create array in correct feature order
    features = []
    for col in feature_columns:
        if col in movie_features:
            features.append(movie_features[col])
        else:
            logger.warning(f"Feature '{col}' not provided, using 0")
            features.append(0)
    
    X = np.array(features).reshape(1, -1)
    logger.info(f"Input features shape: {X.shape}")
    
    return X


def prepare_user_input_features(
    movie_title: str,
    genre: str,
    genre_mapping: Dict[str, int] = GENRE_MAPPING,
) -> Dict[str, Any]:
    """
    Prepare user input into feature format for prediction.
    
    Args:
        movie_title: Title of the previously watched movie.
        genre: Genre of the movie.
        genre_mapping: Mapping of genres to numeric codes.
        
    Returns:
        Dictionary with movie features.
    """
    logger.info(f"Preparing features for: {movie_title} ({genre})")
    
    # Encode genre
    genre_encoded = genre_mapping.get(genre, 0)
    
    # Create feature dictionary with basic features
    # In a real scenario, you might look up movie details from a database
    features = {
        "genre": genre_encoded,
        "rating": 7.5,  # Default value
        "popularity": 50.0,  # Default value
        "vote_count": 1000,  # Default value
        "release_year": 2020,  # Default value
        "runtime": 120,  # Default value
        "revenue": 100000000,  # Default value
        "budget": 50000000,  # Default value
    }
    
    logger.info(f"Features prepared: {features}")
    
    return features


def make_prediction(
    model: Any,
    X: np.ndarray,
    movie_title: str = "Unknown",
    genre: str = "Unknown"
) -> PredictionResult:
    """
    Make a prediction using the trained model.
    
    Args:
        model: Trained model object.
        X: Feature matrix for prediction.
        movie_title: Title of input movie (for reference).
        genre: Genre of input movie (for reference).
        
    Returns:
        PredictionResult object with recommendation.
    """
    logger.info("Making prediction")
    
    # Get prediction
    prediction = model.predict(X)[0]
    
    # Get confidence (distance to nearest neighbors if KNN)
    try:
        distances, indices = model.kneighbors(X)
        confidence = 1.0 / (1.0 + np.mean(distances[0]))  # Convert distance to confidence
    except:
        # For other models, use a default confidence
        confidence = 0.8
        logger.warning("Could not calculate confidence from model")
    
    # Create recommendation text
    recommendation_text = (
        f"Based on your viewing of '{movie_title}' ({genre}), "
        f"we recommend movie ID: {int(prediction)}"
    )
    
    result = PredictionResult(
        predicted_movie_id=float(prediction),
        confidence=float(confidence),
        input_movie=movie_title,
        input_genre=genre,
        recommendation_text=recommendation_text
    )
    
    logger.info(f"Prediction made: {result.recommendation_text}")
    
    return result


def predict_for_user(
    model: Any,
    movie_title: str,
    genre: str,
    feature_columns: List[str] = None
) -> PredictionResult:
    """
    Complete prediction pipeline for a user input.
    
    Args:
        model: Trained model object.
        movie_title: Title of previously watched movie.
        genre: Genre of the movie.
        feature_columns: List of expected feature columns.
        
    Returns:
        PredictionResult with recommendation.
    """
    logger.info(f"Starting prediction for user: movie='{movie_title}', genre='{genre}'")
    
    # Validate input
    if not validate_input_data(movie_title, genre):
        raise ValueError(f"Invalid input: movie_title='{movie_title}', genre='{genre}'")
    
    # Prepare features
    movie_features = prepare_user_input_features(movie_title, genre)
    
    # If feature_columns not provided, use default feature order
    if feature_columns is None:
        feature_columns = list(movie_features.keys())
    
    # Encode for prediction
    X = encode_input_for_prediction(movie_features, feature_columns)
    
    # Make prediction
    result = make_prediction(model, X, movie_title, genre)
    
    logger.info("Prediction pipeline completed")
    
    return result


def batch_predict(
    model: Any,
    input_data: List[Dict[str, str]],
    feature_columns: List[str] = None
) -> List[PredictionResult]:
    """
    Make predictions for multiple user inputs.
    
    Args:
        model: Trained model object.
        input_data: List of dictionaries with 'movie_title' and 'genre'.
        feature_columns: List of expected feature columns.
        
    Returns:
        List of PredictionResult objects.
    """
    logger.info(f"Starting batch prediction for {len(input_data)} inputs")
    
    results = []
    for i, item in enumerate(input_data):
        try:
            result = predict_for_user(
                model,
                item.get("movie_title", "Unknown"),
                item.get("genre", "Unknown"),
                feature_columns
            )
            results.append(result)
            logger.info(f"Batch prediction {i+1}/{len(input_data)} completed")
        except Exception as e:
            logger.error(f"Error in batch prediction {i+1}: {str(e)}")
    
    logger.info(f"Batch prediction completed: {len(results)}/{len(input_data)} successful")
    
    return results


def format_prediction_output(result: PredictionResult) -> Dict[str, Any]:
    """
    Format prediction result for API response or display.
    
    Args:
        result: PredictionResult object.
        
    Returns:
        Dictionary with formatted output.
    """
    return {
        "status": "success",
        "input": {
            "movie": result.input_movie,
            "genre": result.input_genre,
        },
        "recommendation": {
            "movie_id": int(result.predicted_movie_id),
            "confidence": round(result.confidence, 4),
        },
        "message": result.recommendation_text,
    }


if __name__ == "__main__":
    # This is only for testing/standalone execution
    print("Prediction module loaded successfully")
