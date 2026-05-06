"""
Feature engineering module for the NextWatch movie recommendation system.

Handles feature extraction, encoding, scaling, and transformation.
Provides functions for creating and transforming features independently.
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
import pickle

from config import (
    FEATURES,
    CATEGORICAL_FEATURES,
    TARGET_COLUMN,
    FEATURES_DATA_PATH,
    GENRE_MAPPING,
    SCALER_PATH,
    LABEL_ENCODER_PATH,
    LOG_FORMAT,
    LOG_LEVEL,
    SCALE_FEATURES,
    SCALING_METHOD,
)

# Configure logging
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def encode_categorical_features(
    df: pd.DataFrame,
    categorical_features: list,
    mapping_dict: Dict[str, int],
    fit: bool = False
) -> Tuple[pd.DataFrame, Dict[str, LabelEncoder]]:
    """
    Encode categorical features using label encoding or predefined mappings.
    
    Args:
        df: Input DataFrame.
        categorical_features: List of categorical column names.
        mapping_dict: Dictionary mapping categorical values to integers.
        fit: Whether to fit encoders or use existing mappings.
        
    Returns:
        Tuple of (encoded DataFrame, dictionary of fitted encoders).
    """
    logger.info(f"Encoding categorical features: {categorical_features}")
    
    df = df.copy()
    encoders = {}
    
    for feature in categorical_features:
        if feature not in df.columns:
            logger.warning(f"Feature {feature} not found in DataFrame")
            continue
        
        if fit:
            encoder = LabelEncoder()
            df[feature] = encoder.fit_transform(df[feature].astype(str))
            encoders[feature] = encoder
        else:
            # Use predefined mapping if available
            if feature in mapping_dict:
                df[feature] = df[feature].map(mapping_dict).fillna(-1).astype(int)
            else:
                encoder = LabelEncoder()
                df[feature] = encoder.fit_transform(df[feature].astype(str))
                encoders[feature] = encoder
    
    return df, encoders


def create_feature_interactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create interaction features from existing features.
    
    Args:
        df: Input DataFrame.
        
    Returns:
        DataFrame with interaction features added.
    """
    logger.info("Creating feature interactions")
    
    df = df.copy()
    
    # Example: rating * popularity interaction
    if "rating" in df.columns and "popularity" in df.columns:
        df["rating_popularity"] = df["rating"] * df["popularity"]
    
    # Example: budget * revenue ratio
    if "budget" in df.columns and "revenue" in df.columns:
        df["revenue_budget_ratio"] = df.apply(
            lambda row: row["revenue"] / (row["budget"] + 1) if row["budget"] > 0 else 0,
            axis=1
        )
    
    # Example: movie age
    if "release_year" in df.columns:
        from datetime import datetime
        current_year = datetime.now().year
        df["movie_age"] = current_year - df["release_year"]
    
    logger.info(f"Added interaction features. New shape: {df.shape}")
    
    return df


def scale_numeric_features(
    df: pd.DataFrame,
    numeric_features: list,
    scaler: Any = None,
    fit: bool = False
) -> Tuple[pd.DataFrame, Any]:
    """
    Scale numeric features using StandardScaler or MinMaxScaler.
    
    Args:
        df: Input DataFrame.
        numeric_features: List of numeric column names to scale.
        scaler: Existing scaler object (if not fitting new one).
        fit: Whether to fit a new scaler.
        
    Returns:
        Tuple of (scaled DataFrame, scaler object).
    """
    logger.info(f"Scaling numeric features: {numeric_features}")
    
    df = df.copy()
    
    if fit:
        if SCALING_METHOD == "standard":
            scaler = StandardScaler()
        elif SCALING_METHOD == "minmax":
            scaler = MinMaxScaler()
        else:
            logger.warning(f"Unknown scaling method: {SCALING_METHOD}, using standard")
            scaler = StandardScaler()
        
        df[numeric_features] = scaler.fit_transform(df[numeric_features])
        logger.info(f"Fitted new scaler using {SCALING_METHOD} scaling")
    elif scaler is not None:
        df[numeric_features] = scaler.transform(df[numeric_features])
        logger.info("Applied existing scaler to features")
    else:
        logger.warning("No scaler provided and fit=False, skipping scaling")
    
    return df, scaler


def select_features(
    df: pd.DataFrame,
    feature_list: list
) -> pd.DataFrame:
    """
    Select specified features from DataFrame.
    
    Args:
        df: Input DataFrame.
        feature_list: List of features to select.
        
    Returns:
        DataFrame with only selected features.
    """
    available_features = [f for f in feature_list if f in df.columns]
    missing_features = set(feature_list) - set(available_features)
    
    if missing_features:
        logger.warning(f"Missing features: {missing_features}")
    
    return df[available_features]


def engineer_features(
    df: pd.DataFrame,
    fit_scaler: bool = False,
    existing_scaler: Any = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Main feature engineering pipeline.
    
    Args:
        df: Input preprocessed DataFrame.
        fit_scaler: Whether to fit a new scaler.
        existing_scaler: Existing scaler for transform.
        
    Returns:
        Tuple of (features DataFrame, dictionary with scaler and encoders).
    """
    logger.info("Starting feature engineering pipeline")
    
    df = df.copy()
    artifacts = {}
    
    # Encode categorical features
    df, encoders = encode_categorical_features(
        df,
        CATEGORICAL_FEATURES,
        GENRE_MAPPING,
        fit=fit_scaler
    )
    artifacts["encoders"] = encoders
    
    # Create interaction features
    df = create_feature_interactions(df)
    
    # Select numeric features for scaling
    numeric_features = [f for f in df.columns if f not in CATEGORICAL_FEATURES + [TARGET_COLUMN]]
    numeric_features = [f for f in numeric_features if df[f].dtype in [np.float64, np.int64]]
    
    # Scale numeric features
    if SCALE_FEATURES:
        df, scaler = scale_numeric_features(
            df,
            numeric_features,
            scaler=existing_scaler,
            fit=fit_scaler
        )
        artifacts["scaler"] = scaler
    
    # Select final features
    all_features = FEATURES + CATEGORICAL_FEATURES + [TARGET_COLUMN]
    available_final_features = [f for f in all_features if f in df.columns]
    df = df[available_final_features]
    
    logger.info(f"Feature engineering complete. Final shape: {df.shape}")
    logger.info(f"Final features: {available_final_features}")
    
    return df, artifacts


def save_artifacts(artifacts: Dict[str, Any], scaler_path: Path = SCALER_PATH) -> None:
    """
    Save feature engineering artifacts (scaler, encoders) to disk.
    
    Args:
        artifacts: Dictionary containing scaler and encoders.
        scaler_path: Path to save the scaler.
    """
    logger.info("Saving feature engineering artifacts")
    
    if "scaler" in artifacts:
        scaler_path.parent.mkdir(parents=True, exist_ok=True)
        with open(scaler_path, "wb") as f:
            pickle.dump(artifacts["scaler"], f)
        logger.info(f"Scaler saved to {scaler_path}")


def load_artifacts(scaler_path: Path = SCALER_PATH) -> Dict[str, Any]:
    """
    Load feature engineering artifacts from disk.
    
    Args:
        scaler_path: Path to load the scaler from.
        
    Returns:
        Dictionary containing loaded artifacts.
    """
    logger.info("Loading feature engineering artifacts")
    
    artifacts = {}
    
    if scaler_path.exists():
        with open(scaler_path, "rb") as f:
            artifacts["scaler"] = pickle.load(f)
        logger.info(f"Scaler loaded from {scaler_path}")
    
    return artifacts


if __name__ == "__main__":
    # This is only for testing/standalone execution
    print("Feature engineering module loaded successfully")
