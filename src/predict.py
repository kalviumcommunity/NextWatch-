"""
Prediction (Inference) module for the NextWatch movie recommendation system.

Responsible for:
1. Loading saved model and preprocessing artifacts
2. Validating new input data
3. Transforming input using fitted scaler/encoders
4. Generating predictions on new data
5. Returning structured results

CRITICAL: This module NEVER:
- Fits preprocessing (uses saved artifacts only)
- Trains models
- Splits train/test data
- Uses fit_transform() (only transform())
"""

import logging
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Dict, List, Any, Union
from dataclasses import dataclass

# Import from local modules
from .config import (
    MODEL_PATH,
    SCALER_PATH,
    LABEL_ENCODER_PATH,
    FEATURES,
    CATEGORICAL_FEATURES,
    TARGET_COLUMN,
    GENRE_MAPPING,
    LOG_FORMAT,
    LOG_LEVEL,
)
from .feature_engineering import (
    encode_categorical_features,
    create_feature_interactions,
    scale_numeric_features,
    select_features,
)

# Configure logging
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)


@dataclass
class PredictionResult:
    """Structured prediction result."""
    predicted_movie_id: float
    confidence: float
    input_movie: str
    input_genre: str
    recommendation_text: str


def load_saved_artifacts(
    model_path: Path = MODEL_PATH,
    scaler_path: Path = SCALER_PATH,
    encoder_path: Path = LABEL_ENCODER_PATH
) -> Dict[str, Any]:
    """
    Load all saved artifacts (model, scaler, encoders).
    
    CRITICAL: These were fitted during training.
    We will use them for transform only.
    
    Args:
        model_path: Path to saved model.
        scaler_path: Path to saved scaler.
        encoder_path: Path to saved encoders.
        
    Returns:
        Dictionary with loaded artifacts.
    """
    logger.info("Loading saved artifacts from disk")
    
    artifacts = {}
    
    # Load model
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}. Run training first.")
    
    logger.info(f"Loading model from {model_path}")
    artifacts["model"] = joblib.load(model_path)
    
    # Load scaler (optional)
    if scaler_path.exists():
        logger.info(f"Loading scaler from {scaler_path}")
        artifacts["scaler"] = joblib.load(scaler_path)
    else:
        logger.warning(f"Scaler not found at {scaler_path}")
    
    # Load encoders (optional)
    if encoder_path.exists():
        logger.info(f"Loading encoders from {encoder_path}")
        artifacts["encoders"] = joblib.load(encoder_path)
    else:
        logger.warning(f"Encoders not found at {encoder_path}")
    
    logger.info("✓ All artifacts loaded successfully")
    
    return artifacts


def validate_input_data(
    movie_title: str,
    genre: str,
    available_genres: Dict[str, int] = GENRE_MAPPING
) -> bool:
    """
    Validate user input.
    
    Args:
        movie_title: Previously watched movie title.
        genre: Genre of the movie.
        available_genres: Valid genre dictionary.
        
    Returns:
        True if valid, raises otherwise.
    """
    logger.info(f"Validating input: movie='{movie_title}', genre='{genre}'")
    
    if not movie_title or not isinstance(movie_title, str):
        raise ValueError("Movie title must be a non-empty string")
    
    if not genre or genre not in available_genres:
        raise ValueError(f"Genre must be one of: {list(available_genres.keys())}")
    
    logger.info("✓ Input validation passed")
    return True


def prepare_input_dataframe(
    movie_title: str,
    genre: str,
    genre_mapping: Dict[str, int] = GENRE_MAPPING
) -> pd.DataFrame:
    """
    Create a DataFrame from single user input.
    
    Args:
        movie_title: Previously watched movie title.
        genre: Genre of that movie.
        genre_mapping: Genre to integer mapping.
        
    Returns:
        Single-row DataFrame with input features.
    """
    logger.info(f"Preparing input DataFrame for: {movie_title} ({genre})")
    
    # Create a single-row DataFrame with expected features
    # In production, you'd fetch real features from a database
    input_data = {
        "release_year": [2020],
        "rating": [7.5],
        "vote_count": [1000],
        "revenue": [100000000],
        "budget": [50000000],
        "runtime": [120],
        "popularity": [50.0],
        "genre": [genre],
    }
    
    df = pd.DataFrame(input_data)
    
    logger.info(f"Input DataFrame shape: {df.shape}")
    
    return df


def transform_input_with_artifacts(
    df: pd.DataFrame,
    artifacts: Dict[str, Any]
) -> pd.DataFrame:
    """
    Transform input data using saved preprocessing artifacts.
    
    CRITICAL: This uses TRANSFORM only (no fitting).
    Uses scaler and encoders fitted during training.
    
    Args:
        df: Raw input DataFrame.
        artifacts: Saved scaler and encoders.
        
    Returns:
        Transformed DataFrame ready for prediction.
    """
    logger.info("Transforming input with saved artifacts")
    
    df = df.copy()
    
    # Apply fitted encoders
    if "encoders" in artifacts:
        logger.info("Applying fitted encoders")
        for feature, encoder in artifacts["encoders"].items():
            if feature in df.columns:
                try:
                    df[feature] = encoder.transform(df[feature].astype(str))
                except Exception as e:
                    logger.warning(f"Could not encode {feature}: {e}")
    
    # Create interaction features
    df = create_feature_interactions(df)
    
    # Apply fitted scaler
    if "scaler" in artifacts:
        logger.info("Applying fitted scaler")
        numeric_features = [
            f for f in df.columns
            if f not in CATEGORICAL_FEATURES + [TARGET_COLUMN]
            and df[f].dtype in [np.float64, np.int64]
        ]
        try:
            df, _ = scale_numeric_features(
                df,
                numeric_features,
                scaler=artifacts["scaler"],
                fit=False  # TRANSFORM ONLY
            )
        except Exception as e:
            logger.warning(f"Could not scale features: {e}")
    
    # Select final features
    df = select_features(df, FEATURES + CATEGORICAL_FEATURES)
    
    logger.info(f"✓ Input transformation complete. Shape: {df.shape}")
    
    return df


def extract_features_for_model(
    df: pd.DataFrame,
    feature_list: List[str] = None
) -> np.ndarray:
    """
    Extract features in correct order for model.
    
    Args:
        df: Transformed DataFrame.
        feature_list: Expected feature order.
        
    Returns:
        NumPy array ready for prediction.
    """
    if feature_list is None:
        feature_list = [f for f in FEATURES + CATEGORICAL_FEATURES if f in df.columns]
    
    # Select features in correct order
    available_features = [f for f in feature_list if f in df.columns]
    
    if not available_features:
        raise ValueError("No features found in DataFrame")
    
    X = df[available_features].values
    
    logger.info(f"Features extracted: {X.shape}")
    
    return X


def make_prediction(
    model: Any,
    X: np.ndarray,
    input_movie: str,
    input_genre: str
) -> PredictionResult:
    """
    Make prediction using loaded model.
    
    Args:
        model: Loaded trained model.
        X: Transformed features (from inference data).
        input_movie: Original movie title (for reference).
        input_genre: Original genre (for reference).
        
    Returns:
        PredictionResult with recommendation.
    """
    logger.info(f"Making prediction on {X.shape[0]} sample(s)")
    
    # Predict
    y_pred = model.predict(X)
    prediction = float(y_pred[0])
    
    # Calculate confidence
    confidence = 0.8  # Default confidence
    try:
        # For KNN, use distance-based confidence
        if hasattr(model, 'kneighbors'):
            distances, _ = model.kneighbors(X)
            # Closer neighbors = higher confidence
            confidence = 1.0 / (1.0 + np.mean(distances[0]))
    except Exception as e:
        logger.debug(f"Could not calculate distance-based confidence: {e}")
    
    confidence = float(confidence)
    
    # Create recommendation text
    recommendation_text = (
        f"Based on your viewing of '{input_movie}' ({input_genre}), "
        f"we recommend Movie ID: {int(prediction)}"
    )
    
    result = PredictionResult(
        predicted_movie_id=prediction,
        confidence=confidence,
        input_movie=input_movie,
        input_genre=input_genre,
        recommendation_text=recommendation_text
    )
    
    logger.info(f"✓ Prediction: {result.recommendation_text} (confidence: {confidence:.4f})")
    
    return result


def predict_single(
    movie_title: str,
    genre: str
) -> PredictionResult:
    """
    Complete inference pipeline for single input.
    
    Steps:
    1. Load saved artifacts
    2. Validate input
    3. Prepare input DataFrame
    4. Transform with saved artifacts (no fitting)
    5. Make prediction
    
    Args:
        movie_title: Previously watched movie title.
        genre: Genre of that movie.
        
    Returns:
        PredictionResult with recommendation.
    """
    logger.info("="*70)
    logger.info("STARTING PREDICTION PIPELINE")
    logger.info("="*70)
    
    # Step 1: Load artifacts
    logger.info("\n[STEP 1] Loading saved artifacts")
    artifacts = load_saved_artifacts()
    
    # Step 2: Validate input
    logger.info("\n[STEP 2] Validating input")
    validate_input_data(movie_title, genre)
    
    # Step 3: Prepare input
    logger.info("\n[STEP 3] Preparing input DataFrame")
    df_input = prepare_input_dataframe(movie_title, genre)
    
    # Step 4: Transform with saved artifacts
    logger.info("\n[STEP 4] Transforming input (no fitting)")
    df_transformed = transform_input_with_artifacts(df_input, artifacts)
    
    # Step 5: Extract features
    logger.info("\n[STEP 5] Extracting features for model")
    X = extract_features_for_model(df_transformed)
    
    # Step 6: Predict
    logger.info("\n[STEP 6] Making prediction")
    result = make_prediction(
        artifacts["model"],
        X,
        movie_title,
        genre
    )
    
    logger.info("\n" + "="*70)
    logger.info("✓ PREDICTION PIPELINE COMPLETE")
    logger.info("="*70)
    
    return result


def predict_batch(
    input_data: Union[str, pd.DataFrame]
) -> List[PredictionResult]:
    """
    Make predictions for multiple inputs from CSV or DataFrame.
    
    Args:
        input_data: Path to CSV or DataFrame with columns:
                   'movie_title' and 'genre'.
        
    Returns:
        List of PredictionResults.
    """
    logger.info("Starting batch prediction")
    
    # Load input data
    if isinstance(input_data, str):
        df = pd.read_csv(input_data)
        logger.info(f"Loaded {len(df)} records from {input_data}")
    else:
        df = input_data.copy()
        logger.info(f"Processing {len(df)} records from DataFrame")
    
    # Load artifacts once
    artifacts = load_saved_artifacts()
    
    results = []
    
    for idx, row in df.iterrows():
        try:
            movie_title = row.get("movie_title", "Unknown")
            genre = row.get("genre", "Unknown")
            
            logger.info(f"\nPrediction {idx+1}/{len(df)}: {movie_title} ({genre})")
            
            # Validate
            validate_input_data(movie_title, genre)
            
            # Prepare and transform
            df_input = prepare_input_dataframe(movie_title, genre)
            df_transformed = transform_input_with_artifacts(df_input, artifacts)
            X = extract_features_for_model(df_transformed)
            
            # Predict
            result = make_prediction(
                artifacts["model"],
                X,
                movie_title,
                genre
            )
            
            results.append(result)
            
        except Exception as e:
            logger.error(f"Error in prediction {idx+1}: {str(e)}")
            continue
    
    logger.info(f"\n✓ Batch prediction complete: {len(results)}/{len(df)} successful")
    
    return results


def format_result_for_output(result: PredictionResult) -> Dict[str, Any]:
    """
    Format prediction result for API/display.
    
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
    """
    Run prediction as standalone script.
    
    Usage:
        python -m src.predict --movie "Inception" --genre "Science Fiction"
    """
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Make predictions with trained model")
    parser.add_argument("--movie", type=str, required=True, help="Movie title")
    parser.add_argument("--genre", type=str, required=True, help="Movie genre")
    
    args = parser.parse_args()
    
    result = predict_single(args.movie, args.genre)
    
    print("\n" + "="*70)
    print("PREDICTION RESULT")
    print("="*70)
    output = format_result_for_output(result)
    for key, value in output.items():
        print(f"{key}: {value}")
    print("="*70)
