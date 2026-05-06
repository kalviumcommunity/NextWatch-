"""
Evaluation module for the NextWatch movie recommendation system.

Handles model evaluation, performance metrics, and result reporting.
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Any
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error
)
import json

from .config import (
    TEST_DATA_PATH,
    TARGET_COLUMN,
    LOG_FORMAT,
    LOG_LEVEL,
)

# Configure logging
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def calculate_regression_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> Dict[str, float]:
    """
    Calculate regression evaluation metrics.
    
    Args:
        y_true: True target values.
        y_pred: Predicted target values.
        
    Returns:
        Dictionary with various regression metrics.
    """
    logger.info("Calculating regression metrics")
    
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    # MAPE can cause division errors, so we handle it carefully
    try:
        mape = mean_absolute_percentage_error(y_true, y_pred)
    except:
        mape = None
        logger.warning("Could not calculate MAPE (may contain zero values)")
    
    metrics = {
        "mse": float(mse),
        "rmse": float(rmse),
        "mae": float(mae),
        "r2": float(r2),
        "mape": float(mape) if mape is not None else None,
    }
    
    logger.info(f"Metrics - R²: {metrics['r2']:.4f}, RMSE: {metrics['rmse']:.4f}, MAE: {metrics['mae']:.4f}")
    
    return metrics


def calculate_residuals(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> Dict[str, float]:
    """
    Calculate residual statistics.
    
    Args:
        y_true: True target values.
        y_pred: Predicted target values.
        
    Returns:
        Dictionary with residual statistics.
    """
    residuals = y_true - y_pred
    
    residual_stats = {
        "mean": float(np.mean(residuals)),
        "std": float(np.std(residuals)),
        "min": float(np.min(residuals)),
        "max": float(np.max(residuals)),
        "median": float(np.median(residuals)),
    }
    
    logger.info(f"Residual mean: {residual_stats['mean']:.4f}, std: {residual_stats['std']:.4f}")
    
    return residual_stats


def evaluate_model(
    model: Any,
    test_df: pd.DataFrame,
    feature_columns: list = None
) -> Dict[str, Any]:
    """
    Evaluate model on test data.
    
    Args:
        model: Trained model object.
        test_df: Test DataFrame with features and target.
        feature_columns: List of feature column names.
        
    Returns:
        Dictionary with evaluation results.
    """
    logger.info("Starting model evaluation on test set")
    
    if feature_columns is None:
        feature_columns = [c for c in test_df.columns if c != TARGET_COLUMN]
    
    # Prepare test data
    X_test = test_df[feature_columns].values
    y_test = test_df[TARGET_COLUMN].values
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = calculate_regression_metrics(y_test, y_pred)
    residuals = calculate_residuals(y_test, y_pred)
    
    evaluation_results = {
        "test_size": len(test_df),
        "metrics": metrics,
        "residuals": residuals,
        "predictions_summary": {
            "mean_pred": float(np.mean(y_pred)),
            "std_pred": float(np.std(y_pred)),
            "min_pred": float(np.min(y_pred)),
            "max_pred": float(np.max(y_pred)),
        }
    }
    
    logger.info("Model evaluation completed")
    
    return evaluation_results


def generate_evaluation_report(
    evaluation_results: Dict[str, Any],
    output_path: Path = None
) -> str:
    """
    Generate a formatted evaluation report.
    
    Args:
        evaluation_results: Dictionary with evaluation metrics.
        output_path: Optional path to save the report.
        
    Returns:
        Formatted report string.
    """
    logger.info("Generating evaluation report")
    
    report = "=" * 60 + "\n"
    report += "MODEL EVALUATION REPORT\n"
    report += "=" * 60 + "\n\n"
    
    report += f"Test Set Size: {evaluation_results['test_size']}\n\n"
    
    report += "REGRESSION METRICS:\n"
    report += "-" * 40 + "\n"
    for metric, value in evaluation_results["metrics"].items():
        if value is not None:
            report += f"  {metric.upper():15s}: {value:10.4f}\n"
        else:
            report += f"  {metric.upper():15s}: N/A\n"
    
    report += "\nRESIDUAL STATISTICS:\n"
    report += "-" * 40 + "\n"
    for stat, value in evaluation_results["residuals"].items():
        report += f"  {stat.upper():15s}: {value:10.4f}\n"
    
    report += "\nPREDICTION SUMMARY:\n"
    report += "-" * 40 + "\n"
    for stat, value in evaluation_results["predictions_summary"].items():
        report += f"  {stat.upper():15s}: {value:10.4f}\n"
    
    report += "\n" + "=" * 60 + "\n"
    
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(report)
        logger.info(f"Report saved to {output_path}")
    
    return report


def save_evaluation_results(
    evaluation_results: Dict[str, Any],
    output_path: Path
) -> None:
    """
    Save evaluation results to JSON file.
    
    Args:
        evaluation_results: Dictionary with evaluation results.
        output_path: Path to save results.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(evaluation_results, f, indent=2)
    
    logger.info(f"Evaluation results saved to {output_path}")


def evaluate_pipeline(
    model: Any,
    test_path: Path = TEST_DATA_PATH
) -> Dict[str, Any]:
    """
    Main evaluation pipeline.
    
    Args:
        model: Trained model object.
        test_path: Path to test data.
        
    Returns:
        Dictionary with evaluation results.
    """
    logger.info("Starting evaluation pipeline")
    
    # Load test data
    if not test_path.exists():
        raise FileNotFoundError(f"Test data file not found: {test_path}")
    
    test_df = pd.read_csv(test_path)
    logger.info(f"Test data loaded: {test_df.shape}")
    
    # Evaluate model
    feature_columns = [c for c in test_df.columns if c != TARGET_COLUMN]
    evaluation_results = evaluate_model(model, test_df, feature_columns)
    
    # Generate report
    report = generate_evaluation_report(evaluation_results)
    print(report)
    
    logger.info("Evaluation pipeline completed")
    
    return evaluation_results


if __name__ == "__main__":
    # This is only for testing/standalone execution
    print("Evaluation module loaded successfully")
