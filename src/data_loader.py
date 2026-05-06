"""
Data loader module for the NextWatch movie recommendation system.

Responsible ONLY for:
- Loading raw data from file (CSV)
- Basic file validation
- Returning a clean DataFrame
- Handling file-related errors

Does NOT perform:
- Preprocessing
- Feature engineering
- Model training or inference
"""

import logging
import pandas as pd
from pathlib import Path
from typing import Optional

from .config import LOG_FORMAT, LOG_LEVEL

# Configure logging
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load raw data from CSV file.
    
    Args:
        filepath: Path to the CSV file (string or Path object).
        
    Returns:
        DataFrame containing the raw data.
        
    Raises:
        FileNotFoundError: If file doesn't exist.
        ValueError: If file is empty or malformed.
        pd.errors.ParserError: If CSV is invalid.
    """
    filepath = Path(filepath)
    
    # Validate file exists
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    # Validate file is not empty
    if filepath.stat().st_size == 0:
        raise ValueError(f"Data file is empty: {filepath}")
    
    try:
        logger.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)
        
        if df.empty:
            raise ValueError(f"CSV file is empty: {filepath}")
        
        logger.info(f"✓ Loaded {len(df)} records, {len(df.columns)} columns")
        return df
        
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Invalid CSV file {filepath}: {e}")
    except Exception as e:
        raise RuntimeError(f"Error loading data from {filepath}: {e}")


def validate_columns(df: pd.DataFrame, required_columns: Optional[list] = None) -> bool:
    """
    Validate that DataFrame has expected columns.
    
    Args:
        df: Input DataFrame.
        required_columns: List of required column names. If None, just checks non-empty.
        
    Returns:
        True if validation passes.
        
    Raises:
        ValueError: If columns are missing or invalid.
    """
    if df.empty:
        raise ValueError("DataFrame is empty")
    
    if required_columns:
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
    
    logger.info(f"✓ Column validation passed")
    return True


def get_data_shape(df: pd.DataFrame) -> tuple:
    """
    Get shape of the DataFrame.
    
    Args:
        df: Input DataFrame.
        
    Returns:
        Tuple of (rows, columns).
    """
    return df.shape


def get_data_info(df: pd.DataFrame) -> dict:
    """
    Get basic information about the DataFrame.
    
    Args:
        df: Input DataFrame.
        
    Returns:
        Dictionary with shape, columns, and dtypes.
    """
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
        "null_counts": df.isnull().sum().to_dict()
    }
