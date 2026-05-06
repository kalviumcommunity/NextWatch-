"""
Training module for the NextWatch movie recommendation system.

Handles model training, cross-validation, and model persistence.
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Any, Dict
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
import pickle

from config import (
    TRAIN_DATA_PATH,
    TEST_DATA_PATH,
    MODEL_PATH,
    FEATURES,
    CATEGORICAL_FEATURES,
    TARGET_COLUMN,
    TRAIN_TEST_SPLIT_RATIO,
    RANDOM_STATE,
    MODEL_CONFIG,
    N_SPLITS,
    LOG_FORMAT,
    LOG_LEVEL,
)

# Configure logging
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def split_train_test_data(
    df: pd.DataFrame,
    test_size: float = TRAIN_TEST_SPLIT_RATIO,
    random_state: int = RANDOM_STATE
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into training and testing sets.
    
    Args:
        df: Input DataFrame with features and target.
        test_size: Proportion of data for testing.
        random_state: Random seed for reproducibility.
        
    Returns:
        Tuple of (train_df, test_df).
    """
    logger.info(f"Splitting data with test_size={test_size}")
    
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in DataFrame")
    
    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state
    )
    
    logger.info(f"Train set: {len(train_df)}, Test set: {len(test_df)}")
    
    return train_df, test_df


def prepare_features_and_target(
    df: pd.DataFrame,
    feature_columns: list = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Separate features and target variable.
    
    Args:
        df: Input DataFrame.
        feature_columns: List of feature column names. If None, uses all except target.
        
    Returns:
        Tuple of (X, y) where X is features and y is target.
    """
    if feature_columns is None:
        feature_columns = [c for c in df.columns if c != TARGET_COLUMN]
    
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in DataFrame")
    
    X = df[feature_columns].values
    y = df[TARGET_COLUMN].values
    
    logger.info(f"Features shape: {X.shape}, Target shape: {y.shape}")
    
    return X, y


def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    model_type: str = "knn"
) -> Any:
    """
    Train a recommendation model.
    
    Args:
        X_train: Training feature matrix.
        y_train: Training target vector.
        model_type: Type of model to train ("knn", "rf").
        
    Returns:
        Trained model object.
    """
    logger.info(f"Training {model_type} model")
    
    if model_type == "knn":
        model = KNeighborsRegressor(**MODEL_CONFIG)
    elif model_type == "rf":
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=RANDOM_STATE,
            n_jobs=-1
        )
    else:
        logger.warning(f"Unknown model type: {model_type}, using KNN")
        model = KNeighborsRegressor(**MODEL_CONFIG)
    
    model.fit(X_train, y_train)
    logger.info(f"Model training completed. Training samples: {len(X_train)}")
    
    return model


def evaluate_with_cross_validation(
    X: np.ndarray,
    y: np.ndarray,
    model_type: str = "knn",
    n_splits: int = N_SPLITS
) -> Dict[str, float]:
    """
    Perform cross-validation to evaluate model performance.
    
    Args:
        X: Feature matrix.
        y: Target vector.
        model_type: Type of model to train.
        n_splits: Number of cross-validation splits.
        
    Returns:
        Dictionary with cross-validation metrics.
    """
    logger.info(f"Performing {n_splits}-fold cross-validation")
    
    if model_type == "knn":
        model = KNeighborsRegressor(**MODEL_CONFIG)
    elif model_type == "rf":
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=RANDOM_STATE,
            n_jobs=-1
        )
    else:
        model = KNeighborsRegressor(**MODEL_CONFIG)
    
    # Use R² score for regression
    scores = cross_val_score(
        model,
        X,
        y,
        cv=n_splits,
        scoring="r2",
        n_jobs=-1
    )
    
    metrics = {
        "cv_scores": scores,
        "cv_mean": scores.mean(),
        "cv_std": scores.std(),
    }
    
    logger.info(f"CV R² Score - Mean: {metrics['cv_mean']:.4f} (+/- {metrics['cv_std']:.4f})")
    
    return metrics


def save_model(model: Any, filepath: Path = MODEL_PATH) -> None:
    """
    Save trained model to disk.
    
    Args:
        model: Trained model object.
        filepath: Path to save the model.
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, "wb") as f:
        pickle.dump(model, f)
    
    logger.info(f"Model saved to {filepath}")


def load_model(filepath: Path = MODEL_PATH) -> Any:
    """
    Load trained model from disk.
    
    Args:
        filepath: Path to the saved model.
        
    Returns:
        Loaded model object.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Model file not found: {filepath}")
    
    with open(filepath, "rb") as f:
        model = pickle.load(f)
    
    logger.info(f"Model loaded from {filepath}")
    
    return model


def save_train_test_split(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    train_path: Path = TRAIN_DATA_PATH,
    test_path: Path = TEST_DATA_PATH
) -> None:
    """
    Save train and test splits to CSV for reproducibility.
    
    Args:
        train_df: Training DataFrame.
        test_df: Testing DataFrame.
        train_path: Path to save training data.
        test_path: Path to save testing data.
    """
    train_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.parent.mkdir(parents=True, exist_ok=True)
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    logger.info(f"Train/test split saved: {train_path}, {test_path}")


def train_pipeline(
    df: pd.DataFrame,
    model_type: str = "knn"
) -> Tuple[Any, Dict[str, Any]]:
    """
    Main training pipeline that orchestrates all training steps.
    
    Args:
        df: Engineered features DataFrame.
        model_type: Type of model to train ("knn", "rf").
        
    Returns:
        Tuple of (trained_model, training_info_dict).
    """
    logger.info("Starting training pipeline")
    
    # Split data
    train_df, test_df = split_train_test_data(df)
    save_train_test_split(train_df, test_df)
    
    # Prepare features and target
    feature_columns = [c for c in df.columns if c != TARGET_COLUMN]
    X_train, y_train = prepare_features_and_target(train_df, feature_columns)
    
    # Train model
    model = train_model(X_train, y_train, model_type=model_type)
    
    # Cross-validation
    X, y = prepare_features_and_target(df, feature_columns)
    cv_metrics = evaluate_with_cross_validation(X, y, model_type=model_type)
    
    # Save model
    save_model(model)
    
    training_info = {
        "model_type": model_type,
        "feature_columns": feature_columns,
        "train_size": len(train_df),
        "test_size": len(test_df),
        "cv_metrics": cv_metrics,
    }
    
    logger.info("Training pipeline completed successfully")
    
    return model, training_info


if __name__ == "__main__":
    # This is only for testing/standalone execution
    print("Training module loaded successfully")
