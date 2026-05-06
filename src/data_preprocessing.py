"""
Data preprocessing module for the NextWatch movie recommendation system.

Handles data loading, cleaning, validation, and preparation for feature engineering.
Avoids circular imports and provides functions for reproducible data processing.
"""

import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional

from config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    MIN_YEAR,
    MAX_YEAR,
    MIN_RATING,
    MAX_RATING,
    MIN_RUNTIME,
    MAX_RUNTIME,
    LOG_FORMAT,
    LOG_LEVEL,
)

# Configure logging
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def load_raw_data(filepath: Path) -> pd.DataFrame:
    """
    Load raw movie data from CSV file.
    
    Args:
        filepath: Path to the CSV file.
        
    Returns:
        DataFrame containing raw movie data.
        
    Raises:
        FileNotFoundError: If the file doesn't exist.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    logger.info(f"Loading raw data from {filepath}")
    df = pd.read_csv(filepath)
    logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")
    
    return df


def handle_missing_values(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """
    Handle missing values in the dataset.
    
    Args:
        df: Input DataFrame.
        strategy: Strategy for handling missing values ("mean", "median", "drop").
        
    Returns:
        DataFrame with missing values handled.
    """
    logger.info(f"Handling missing values with strategy: {strategy}")
    
    initial_nulls = df.isnull().sum().sum()
    
    if strategy == "drop":
        df = df.dropna()
    elif strategy == "mean":
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == "median":
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    else:
        logger.warning(f"Unknown strategy: {strategy}, using 'drop'")
        df = df.dropna()
    
    final_nulls = df.isnull().sum().sum()
    logger.info(f"Handled {initial_nulls} null values, {final_nulls} remaining")
    
    return df


def remove_duplicates(df: pd.DataFrame, subset: Optional[list] = None) -> pd.DataFrame:
    """
    Remove duplicate records from the dataset.
    
    Args:
        df: Input DataFrame.
        subset: Columns to consider for identifying duplicates.
        
    Returns:
        DataFrame with duplicates removed.
    """
    initial_rows = len(df)
    df = df.drop_duplicates(subset=subset)
    final_rows = len(df)
    
    logger.info(f"Removed {initial_rows - final_rows} duplicate records")
    
    return df


def validate_numeric_ranges(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and clip numeric features to acceptable ranges.
    
    Args:
        df: Input DataFrame.
        
    Returns:
        DataFrame with validated numeric ranges.
    """
    logger.info("Validating numeric ranges")
    
    # Validate release_year
    if "release_year" in df.columns:
        df["release_year"] = df["release_year"].clip(MIN_YEAR, MAX_YEAR)
    
    # Validate rating
    if "rating" in df.columns:
        df["rating"] = df["rating"].clip(MIN_RATING, MAX_RATING)
    
    # Validate runtime
    if "runtime" in df.columns:
        df["runtime"] = df["runtime"].clip(MIN_RUNTIME, MAX_RUNTIME)
    
    return df


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to lowercase with underscores.
    
    Args:
        df: Input DataFrame.
        
    Returns:
        DataFrame with standardized column names.
    """
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("-", "_")
    logger.info("Standardized column names")
    
    return df


def preprocess_data(
    input_path: Path = RAW_DATA_PATH,
    output_path: Path = PROCESSED_DATA_PATH,
    missing_value_strategy: str = "mean",
) -> pd.DataFrame:
    """
    Main preprocessing pipeline that orchestrates all cleaning and validation steps.
    
    Args:
        input_path: Path to raw data file.
        output_path: Path to save processed data.
        missing_value_strategy: Strategy for handling missing values.
        
    Returns:
        Processed DataFrame.
    """
    logger.info("Starting data preprocessing pipeline")
    
    # Load data
    df = load_raw_data(input_path)
    
    # Standardize column names
    df = standardize_column_names(df)
    
    # Remove duplicates
    df = remove_duplicates(df)
    
    # Handle missing values
    df = handle_missing_values(df, strategy=missing_value_strategy)
    
    # Validate numeric ranges
    df = validate_numeric_ranges(df)
    
    # Save processed data
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Processed data saved to {output_path}")
    
    return df


if __name__ == "__main__":
    # This is only for testing/standalone execution
    # Normal execution should use the function via imports
    processed_df = preprocess_data()
    print(f"Data shape: {processed_df.shape}")
    print(f"Columns: {processed_df.columns.tolist()}")
