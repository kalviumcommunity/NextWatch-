"""
Training module for the NextWatch movie recommendation system.

Responsible for:
1. Loading raw data
2. Splitting into train/test sets BEFORE preprocessing
3. Preprocessing fitted ONLY on training data
4. Training the model on training data
5. Evaluating on test set
6. Saving all artifacts (model, scaler, encoders)

Critical Pattern:
- Preprocessing is FITTED on X_train
- Preprocessing is TRANSFORMED on X_test
- Model is TRAINED only on X_train
"""

import logging
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Dict, Tuple, Any
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
import json

# Import from local modules
from .config import (
    TRAIN_DATA_PATH,
    TEST_DATA_PATH,
    MODEL_PATH,
    SCALER_PATH,
    LABEL_ENCODER_PATH,
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
from .data_loader import load_data, validate_columns
from .data_preprocessing import (
    handle_missing_values,
    remove_duplicates,
    validate_numeric_ranges,
)
from .feature_engineering import (
    encode_categorical_features,
    create_feature_interactions,
    scale_numeric_features,
    select_features,
)
from .evaluate import calculate_regression_metrics, calculate_residuals

# Configure logging
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def split_train_test(
    df: pd.DataFrame,
    target_col: str = TARGET_COLUMN,
    test_size: float = TRAIN_TEST_SPLIT_RATIO,
    random_state: int = RANDOM_STATE
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into training and test sets.
    
    CRITICAL: This happens BEFORE preprocessing fitting.
    Preprocessing will be fitted only on training data.
    
    Args:
        df: Complete dataset with features and target.
        target_col: Name of target column.
        test_size: Fraction of data for test set.
        random_state: Random seed for reproducibility.
        
    Returns:
        Tuple of (train_df, test_df).
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found")
    
    logger.info(f"Splitting data: test_size={test_size}, random_state={random_state}")
    
    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state
    )
    
    # Save splits for reference
    TRAIN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(TRAIN_DATA_PATH, index=False)
    test_df.to_csv(TEST_DATA_PATH, index=False)
    
    logger.info(f"✓ Train: {len(train_df)} records, Test: {len(test_df)} records")
    logger.info(f"  Saved: {TRAIN_DATA_PATH}")
    logger.info(f"  Saved: {TEST_DATA_PATH}")
    
    return train_df, test_df


def preprocess_training_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Preprocess training data and fit preprocessing artifacts.
    
    CRITICAL: This creates the scaler and encoders that will be
    applied to test/inference data.
    
    Args:
        df: Raw training data.
        
    Returns:
        Tuple of (processed_df, artifacts).
    """
    logger.info("Preprocessing TRAINING data (fitting artifacts)")
    
    df = df.copy()
    artifacts = {}
    
    # Step 1: Handle missing values
    df = handle_missing_values(df, strategy="mean")
    
    # Step 2: Remove duplicates
    df = remove_duplicates(df)
    
    # Step 3: Validate numeric ranges
    df = validate_numeric_ranges(df)
    
    # Step 4: Feature engineering and scaling (FIT on training data)
    # Use GENRE_MAPPING for consistent encoding across train/test
    from .config import GENRE_MAPPING
    df, encoders = encode_categorical_features(
        df, CATEGORICAL_FEATURES, GENRE_MAPPING, fit=False
    )
    artifacts["encoders"] = encoders
    
    df = create_feature_interactions(df)
    
    # Identify numeric features for scaling
    numeric_features = [
        f for f in df.columns
        if f not in CATEGORICAL_FEATURES + [TARGET_COLUMN]
        and df[f].dtype in [np.float64, np.int64]
    ]
    
    df, scaler = scale_numeric_features(
        df, numeric_features, fit=True
    )
    artifacts["scaler"] = scaler
    artifacts["numeric_features"] = numeric_features
    
    # Step 5: Select final features
    df = select_features(df, FEATURES + CATEGORICAL_FEATURES + [TARGET_COLUMN])
    
    logger.info(f"✓ Training preprocessing complete. Shape: {df.shape}")
    
    return df, artifacts


def preprocess_test_data(
    df: pd.DataFrame,
    artifacts: Dict[str, Any]
) -> pd.DataFrame:
    """
    Preprocess test data using artifacts fitted on training data.
    
    CRITICAL: This uses TRANSFORM only (no fitting).
    Uses the same scaler and encoders from training.
    
    Args:
        df: Raw test data.
        artifacts: Preprocessing artifacts from training.
        
    Returns:
        Processed test DataFrame.
    """
    logger.info("Preprocessing TEST data (transforming with training artifacts)")
    
    df = df.copy()
    
    # Apply same preprocessing steps (no fitting)
    df = handle_missing_values(df, strategy="mean")
    df = remove_duplicates(df)
    df = validate_numeric_ranges(df)
    
    # Apply genre mapping (consistent with training)
    from .config import GENRE_MAPPING
    if "genre" in df.columns:
        df["genre"] = df["genre"].map(GENRE_MAPPING).fillna(-1).astype(int)
    
    df = create_feature_interactions(df)
    
    if "scaler" in artifacts and "numeric_features" in artifacts:
        df, _ = scale_numeric_features(
            df,
            artifacts["numeric_features"],
            scaler=artifacts["scaler"],
            fit=False
        )
    
    df = select_features(df, FEATURES + CATEGORICAL_FEATURES + [TARGET_COLUMN])
    
    logger.info(f"✓ Test preprocessing complete. Shape: {df.shape}")
    
    return df


def prepare_features_and_target(
    df: pd.DataFrame,
    target_col: str = TARGET_COLUMN
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Separate features and target.
    
    Args:
        df: Processed DataFrame.
        target_col: Target column name.
        
    Returns:
        Tuple of (X, y) as numpy arrays.
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found")
    
    X = df.drop(columns=[target_col]).values
    y = df[target_col].values
    
    logger.info(f"✓ Features prepared: X.shape={X.shape}, y.shape={y.shape}")
    
    return X, y


def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    model_type: str = "knn"
) -> Any:
    """
    Train the model.
    
    Args:
        X_train: Training features.
        y_train: Training target.
        model_type: Type of model ("knn" or "rf").
        
    Returns:
        Trained model object.
    """
    logger.info(f"Training {model_type.upper()} model on {len(X_train)} samples")
    
    if model_type == "knn":
        model = KNeighborsRegressor(**MODEL_CONFIG)
    elif model_type == "rf":
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=RANDOM_STATE
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    model.fit(X_train, y_train)
    logger.info(f"✓ Model trained successfully")
    
    return model


def evaluate_model(
    model: Any,
    X_test: np.ndarray,
    y_test: np.ndarray,
    X_train: np.ndarray = None,
    y_train: np.ndarray = None
) -> Dict[str, Any]:
    """
    Evaluate model on test set and optionally provide cross-validation.
    
    Args:
        model: Trained model.
        X_test: Test features.
        y_test: Test target.
        X_train: Optional training features for cross-validation.
        y_train: Optional training target for cross-validation.
        
    Returns:
        Dictionary with evaluation results.
    """
    logger.info("Evaluating model on test set")
    
    results = {}
    
    # Test set predictions
    y_pred_test = model.predict(X_test)
    test_metrics = calculate_regression_metrics(y_test, y_pred_test)
    results["test"] = test_metrics
    
    residuals = calculate_residuals(y_test, y_pred_test)
    results["residuals"] = residuals
    
    logger.info(f"✓ Test R²: {test_metrics['r2']:.4f}, RMSE: {test_metrics['rmse']:.4f}")
    
    # Optional: Cross-validation on training data
    if X_train is not None and y_train is not None:
        logger.info(f"Running {N_SPLITS}-fold cross-validation on training data")
        cv_scores = cross_val_score(
            model, X_train, y_train, cv=N_SPLITS, scoring="r2"
        )
        results["cv"] = {
            "mean_r2": float(cv_scores.mean()),
            "std_r2": float(cv_scores.std()),
            "all_scores": cv_scores.tolist()
        }
        logger.info(f"✓ CV Mean R²: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    return results


def save_model_and_artifacts(
    model: Any,
    artifacts: Dict[str, Any],
    evaluation_results: Dict[str, Any],
    model_path: Path = MODEL_PATH,
    artifacts_dir: Path = None
) -> None:
    """
    Save trained model and preprocessing artifacts to disk.
    
    Args:
        model: Trained model object.
        artifacts: Dictionary with scaler, encoders, etc.
        evaluation_results: Evaluation metrics dictionary.
        model_path: Path to save model.
        artifacts_dir: Directory to save artifacts (defaults to models/).
    """
    if artifacts_dir is None:
        artifacts_dir = model_path.parent
    
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    # Save model
    logger.info(f"Saving model to {model_path}")
    joblib.dump(model, model_path)
    
    # Save scaler
    if "scaler" in artifacts:
        logger.info(f"Saving scaler to {SCALER_PATH}")
        joblib.dump(artifacts["scaler"], SCALER_PATH)
    
    # Save encoders
    if "encoders" in artifacts:
        logger.info(f"Saving encoders to {LABEL_ENCODER_PATH}")
        joblib.dump(artifacts["encoders"], LABEL_ENCODER_PATH)
    
    # Save evaluation results
    eval_report_path = artifacts_dir / "evaluation_report.json"
    logger.info(f"Saving evaluation report to {eval_report_path}")
    with open(eval_report_path, "w") as f:
        # Convert numpy values to Python native types for JSON serialization
        def convert_to_serializable(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, (np.integer, np.floating)):
                return obj.item()
            elif isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_serializable(item) for item in obj]
            return obj
        
        json.dump(convert_to_serializable(evaluation_results), f, indent=2)
    
    # Save preprocessing metadata
    metadata_path = artifacts_dir / "preprocessing_metadata.json"
    logger.info(f"Saving metadata to {metadata_path}")
    metadata = {
        "numeric_features": artifacts.get("numeric_features", []),
        "categorical_features": CATEGORICAL_FEATURES,
        "feature_list": FEATURES + CATEGORICAL_FEATURES,
        "random_state": RANDOM_STATE,
    }
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    
    logger.info("✓ All artifacts saved successfully")


def train_pipeline(
    input_path: Path = None,
    model_type: str = "knn"
) -> Dict[str, Any]:
    """
    Complete training pipeline.
    
    Steps:
    1. Load raw data
    2. Split into train/test
    3. Preprocess training data (fit scaler/encoders)
    4. Preprocess test data (transform with fitted artifacts)
    5. Train model on training data
    6. Evaluate on test data
    7. Save all artifacts
    
    Args:
        input_path: Path to raw data CSV (defaults to RAW_DATA_PATH).
        model_type: Model type ("knn" or "rf").
        
    Returns:
        Dictionary with results.
    """
    if input_path is None:
        from .config import RAW_DATA_PATH
        input_path = RAW_DATA_PATH
    
    logger.info("="*70)
    logger.info("STARTING TRAINING PIPELINE")
    logger.info("="*70)
    
    # Step 1: Load raw data
    logger.info("\n[STEP 1] Loading raw data")
    df_raw = load_data(str(input_path))
    validate_columns(df_raw)
    
    # Step 2: Split into train/test BEFORE preprocessing
    logger.info("\n[STEP 2] Splitting train/test (BEFORE preprocessing)")
    train_df, test_df = split_train_test(df_raw)
    
    # Step 3: Preprocess training data and fit artifacts
    logger.info("\n[STEP 3] Preprocessing training data (FITTING artifacts)")
    train_processed, artifacts = preprocess_training_data(train_df)
    
    # Step 4: Preprocess test data with training artifacts
    logger.info("\n[STEP 4] Preprocessing test data (TRANSFORMING with artifacts)")
    test_processed = preprocess_test_data(test_df, artifacts)
    
    # Step 5: Prepare features and targets
    logger.info("\n[STEP 5] Preparing features and targets")
    X_train, y_train = prepare_features_and_target(train_processed)
    X_test, y_test = prepare_features_and_target(test_processed)
    
    # Step 6: Train model
    logger.info("\n[STEP 6] Training model")
    model = train_model(X_train, y_train, model_type=model_type)
    
    # Step 7: Evaluate model
    logger.info("\n[STEP 7] Evaluating model")
    evaluation = evaluate_model(model, X_test, y_test, X_train, y_train)
    
    # Step 8: Save all artifacts
    logger.info("\n[STEP 8] Saving artifacts")
    save_model_and_artifacts(model, artifacts, evaluation)
    
    logger.info("\n" + "="*70)
    logger.info("✓ TRAINING PIPELINE COMPLETE")
    logger.info("="*70)
    
    return {
        "model": model,
        "artifacts": artifacts,
        "evaluation": evaluation,
        "X_train": X_train,
        "y_train": y_train,
        "X_test": X_test,
        "y_test": y_test,
    }


if __name__ == "__main__":
    """
    Run training pipeline as standalone script.
    
    Usage:
        python -m src.train
    """
    import sys
    
    model_type = "knn" if len(sys.argv) < 2 else sys.argv[1]
    results = train_pipeline(model_type=model_type)
    
    logger.info("\nFinal Results:")
    logger.info(f"  Test R²:     {results['evaluation']['test']['r2']:.4f}")
    logger.info(f"  Test RMSE:   {results['evaluation']['test']['rmse']:.4f}")
    logger.info(f"  Test MAE:    {results['evaluation']['test']['mae']:.4f}")
    if "cv" in results["evaluation"]:
        logger.info(f"  CV Mean R²:  {results['evaluation']['cv']['mean_r2']:.4f}")
