# NextWatch ML System - Technical Specification

## 📋 Complete API Reference

### Module: config.py

**Purpose**: Centralized configuration and constants

#### Constants (Configuration)

```python
# Paths
PROJECT_ROOT: Path
DATA_DIR: Path
RAW_DATA_PATH: Path
PROCESSED_DATA_PATH: Path
FEATURES_DATA_PATH: Path
TRAIN_DATA_PATH: Path
TEST_DATA_PATH: Path
MODELS_DIR: Path
MODEL_PATH: Path
SCALER_PATH: Path
LABEL_ENCODER_PATH: Path

# Features
FEATURES: List[str]  # [release_year, rating, vote_count, revenue, budget, runtime, popularity]
CATEGORICAL_FEATURES: List[str]  # [genre]
TARGET_COLUMN: str  # next_movie_title

# Training
TRAIN_TEST_SPLIT_RATIO: float  # 0.2
RANDOM_STATE: int  # 42
TEST_SIZE: float  # 0.2
VALIDATION_SIZE: float  # 0.2

# Model Hyperparameters
MODEL_CONFIG: Dict[str, Any]  # n_neighbors=5, weights=distance, metric=euclidean

# Genre Mapping
GENRE_MAPPING: Dict[str, int]  # 18 genres mapped to integers
REVERSE_GENRE_MAPPING: Dict[int, str]

# Validation Ranges
MIN_YEAR: int  # 1900
MAX_YEAR: int  # 2100
MIN_RATING: float  # 0.0
MAX_RATING: float  # 10.0

# Feature Scaling
SCALE_FEATURES: bool  # True
SCALING_METHOD: str  # "standard" or "minmax"

# Cross-validation
N_SPLITS: int  # 5
CV_SHUFFLE: bool  # True
```

---

### Module: data_preprocessing.py

**Purpose**: Data loading, cleaning, and preparation

#### Functions

```python
def load_raw_data(filepath: Path) -> pd.DataFrame
    """Load raw movie data from CSV file."""
    # Returns: DataFrame with raw data
    # Raises: FileNotFoundError

def handle_missing_values(
    df: pd.DataFrame, 
    strategy: str = "mean"
) -> pd.DataFrame
    """Handle missing values using specified strategy."""
    # strategy: "mean", "median", or "drop"
    # Returns: DataFrame with missing values handled

def remove_duplicates(
    df: pd.DataFrame, 
    subset: Optional[list] = None
) -> pd.DataFrame
    """Remove duplicate records from dataset."""
    # subset: Columns to consider for duplicates
    # Returns: DataFrame with duplicates removed

def validate_numeric_ranges(df: pd.DataFrame) -> pd.DataFrame
    """Validate and clip numeric features to acceptable ranges."""
    # Clips: release_year, rating, runtime
    # Returns: DataFrame with validated ranges

def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame
    """Standardize column names to lowercase with underscores."""
    # Returns: DataFrame with standardized column names

def preprocess_data(
    input_path: Path = RAW_DATA_PATH,
    output_path: Path = PROCESSED_DATA_PATH,
    missing_value_strategy: str = "mean"
) -> pd.DataFrame
    """Main preprocessing pipeline."""
    # Orchestrates: load → standardize → deduplicate → 
    #              handle_missing → validate
    # Returns: Processed DataFrame
    # Saves: Processed data to output_path
```

---

### Module: feature_engineering.py

**Purpose**: Feature extraction, encoding, and scaling

#### Functions

```python
def encode_categorical_features(
    df: pd.DataFrame,
    categorical_features: list,
    mapping_dict: Dict[str, int],
    fit: bool = False
) -> Tuple[pd.DataFrame, Dict[str, LabelEncoder]]
    """Encode categorical features using label encoding."""
    # Returns: (encoded DataFrame, encoders dict)

def create_feature_interactions(df: pd.DataFrame) -> pd.DataFrame
    """Create interaction features from existing features."""
    # Creates: rating_popularity, revenue_budget_ratio, movie_age
    # Returns: DataFrame with interaction features added

def scale_numeric_features(
    df: pd.DataFrame,
    numeric_features: list,
    scaler: Any = None,
    fit: bool = False
) -> Tuple[pd.DataFrame, Any]
    """Scale numeric features using StandardScaler or MinMaxScaler."""
    # Returns: (scaled DataFrame, scaler object)

def select_features(
    df: pd.DataFrame,
    feature_list: list
) -> pd.DataFrame
    """Select specified features from DataFrame."""
    # Returns: DataFrame with only selected features

def engineer_features(
    df: pd.DataFrame,
    fit_scaler: bool = False,
    existing_scaler: Any = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]
    """Main feature engineering pipeline."""
    # Orchestrates: encode → interactions → scale → select
    # Returns: (engineered DataFrame, artifacts dict)

def save_artifacts(
    artifacts: Dict[str, Any], 
    scaler_path: Path = SCALER_PATH
) -> None
    """Save feature engineering artifacts to disk."""
    # Saves: scaler, encoders

def load_artifacts(
    scaler_path: Path = SCALER_PATH
) -> Dict[str, Any]
    """Load feature engineering artifacts from disk."""
    # Returns: artifacts dict with scaler
```

---

### Module: train.py

**Purpose**: Model training and persistence

#### Classes

```python
# None (uses scikit-learn models directly)
```

#### Functions

```python
def split_train_test_data(
    df: pd.DataFrame,
    test_size: float = TRAIN_TEST_SPLIT_RATIO,
    random_state: int = RANDOM_STATE
) -> Tuple[pd.DataFrame, pd.DataFrame]
    """Split data into training and testing sets."""
    # Returns: (train_df, test_df)

def prepare_features_and_target(
    df: pd.DataFrame,
    feature_columns: list = None
) -> Tuple[np.ndarray, np.ndarray]
    """Separate features and target variable."""
    # Returns: (X features, y target)

def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    model_type: str = "knn"
) -> Any
    """Train a recommendation model."""
    # model_type: "knn" or "rf"
    # Returns: Trained model object

def evaluate_with_cross_validation(
    X: np.ndarray,
    y: np.ndarray,
    model_type: str = "knn",
    n_splits: int = N_SPLITS
) -> Dict[str, float]
    """Perform cross-validation to evaluate model."""
    # Returns: Dict with cv_scores, cv_mean, cv_std

def save_model(
    model: Any, 
    filepath: Path = MODEL_PATH
) -> None
    """Save trained model to disk."""
    # Saves: Model as pickle file

def load_model(filepath: Path = MODEL_PATH) -> Any
    """Load trained model from disk."""
    # Returns: Loaded model object
    # Raises: FileNotFoundError

def save_train_test_split(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    train_path: Path = TRAIN_DATA_PATH,
    test_path: Path = TEST_DATA_PATH
) -> None
    """Save train and test splits to CSV."""
    # Saves: train_data.csv and test_data.csv

def train_pipeline(
    df: pd.DataFrame,
    model_type: str = "knn"
) -> Tuple[Any, Dict[str, Any]]
    """Main training pipeline."""
    # Orchestrates: split → prepare → train → cross_validate → save
    # Returns: (trained_model, training_info_dict)
```

---

### Module: evaluate.py

**Purpose**: Model evaluation and performance metrics

#### Functions

```python
def calculate_regression_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> Dict[str, float]
    """Calculate regression evaluation metrics."""
    # Returns: Dict with mse, rmse, mae, r2, mape

def calculate_residuals(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> Dict[str, float]
    """Calculate residual statistics."""
    # Returns: Dict with mean, std, min, max, median

def evaluate_model(
    model: Any,
    test_df: pd.DataFrame,
    feature_columns: list = None
) -> Dict[str, Any]
    """Evaluate model on test data."""
    # Returns: Dict with test_size, metrics, residuals

def generate_evaluation_report(
    evaluation_results: Dict[str, Any],
    output_path: Path = None
) -> str
    """Generate formatted evaluation report."""
    # Returns: Report string
    # Optionally saves: Report to file

def save_evaluation_results(
    evaluation_results: Dict[str, Any],
    output_path: Path
) -> None
    """Save evaluation results to JSON file."""
    # Saves: Results as JSON

def evaluate_pipeline(
    model: Any,
    test_path: Path = TEST_DATA_PATH
) -> Dict[str, Any]
    """Main evaluation pipeline."""
    # Orchestrates: load_data → evaluate → generate_report
    # Returns: evaluation_results dict
```

---

### Module: predict.py

**Purpose**: Making predictions and recommendations

#### Classes

```python
@dataclass
class PredictionResult:
    """Data class for storing prediction results."""
    predicted_movie_id: float
    confidence: float
    input_movie: str
    input_genre: str
    recommendation_text: str
```

#### Functions

```python
def validate_input_data(
    movie_title: str,
    genre: str,
    available_genres: Dict[str, int] = GENRE_MAPPING
) -> bool
    """Validate user input for prediction."""
    # Returns: True if valid, False otherwise

def encode_input_for_prediction(
    movie_features: Dict[str, Any],
    feature_columns: List[str]
) -> np.ndarray
    """Encode and prepare input features for prediction."""
    # Returns: NumPy array (1, n_features)

def prepare_user_input_features(
    movie_title: str,
    genre: str,
    genre_mapping: Dict[str, int] = GENRE_MAPPING
) -> Dict[str, Any]
    """Prepare user input into feature format."""
    # Returns: Feature dictionary

def make_prediction(
    model: Any,
    X: np.ndarray,
    movie_title: str = "Unknown",
    genre: str = "Unknown"
) -> PredictionResult
    """Make a prediction using the trained model."""
    # Returns: PredictionResult object

def predict_for_user(
    model: Any,
    movie_title: str,
    genre: str,
    feature_columns: List[str] = None
) -> PredictionResult
    """Complete prediction pipeline for single user."""
    # Orchestrates: validate → prepare → encode → predict
    # Returns: PredictionResult

def batch_predict(
    model: Any,
    input_data: List[Dict[str, str]],
    feature_columns: List[str] = None
) -> List[PredictionResult]
    """Make predictions for multiple inputs."""
    # input_data: List of dicts with movie_title and genre
    # Returns: List of PredictionResult objects

def format_prediction_output(
    result: PredictionResult
) -> Dict[str, Any]
    """Format prediction result for API response."""
    # Returns: Dict with status, input, recommendation, message
```

---

### Module: main.py

**Purpose**: CLI entry point and pipeline orchestration

#### Functions

```python
def train_full_pipeline(
    raw_data_path: Optional[Path] = None,
    model_type: str = "knn"
) -> dict
    """Execute complete training pipeline."""
    # Orchestrates: preprocess → engineer → train → evaluate
    # Returns: Dict with status, model, training_info, artifacts

def predict_pipeline(
    movie_title: str,
    genre: str,
    model_path: Optional[Path] = None
) -> dict
    """Execute prediction pipeline."""
    # Returns: Dict with status and result

def main() -> int
    """Main entry point with CLI argument parsing."""
    # Subcommands: train, predict, batch
    # Returns: 0 for success, 1 for failure
```

---

## 🔄 Data Structures

### DataFrame Columns Progression

#### Step 1: Raw Data (raw_movies.csv)
```
[movie_title, release_year, rating, vote_count, revenue, budget, 
 runtime, popularity, genre, next_movie_title]
```

#### Step 2: After Preprocessing
```
[movie_title, release_year, rating, vote_count, revenue, budget, 
 runtime, popularity, genre, next_movie_title]
(cleaned, validated, deduplicated)
```

#### Step 3: After Feature Engineering
```
[release_year, rating, vote_count, revenue, budget, runtime, popularity,
 genre (encoded), rating_popularity, revenue_budget_ratio, movie_age,
 next_movie_title]
(scaled and engineered)
```

#### Train/Test Split
```
X: [release_year, rating, vote_count, revenue, budget, runtime, popularity,
    genre, rating_popularity, revenue_budget_ratio, movie_age]
y: [next_movie_title]  (numeric)
```

---

## 📊 Model Details

### KNN (Default)
```
Algorithm: K-Nearest Neighbors (Regression)
n_neighbors: 5
weights: "distance"
metric: "euclidean"
Training time: ~1 second
Prediction time: <1ms per sample
Model size: ~100KB
```

### Random Forest
```
Algorithm: Random Forest Regressor
n_estimators: 100
max_depth: None
random_state: 42
Training time: ~5 seconds
Prediction time: <5ms per sample
Model size: ~5MB
```

---

## ✅ Validation & Quality Checks

### Input Validation
- movie_title: Non-empty string
- genre: Must be in GENRE_MAPPING
- Data types: Numeric ranges, categorical values

### Data Validation
- Missing values: Handled (mean/median/drop)
- Duplicates: Removed
- Ranges: Clipped to valid bounds
- NaN values: Detected and reported

### Model Validation
- CV scores: Reported with mean and std
- Residuals: Statistics calculated
- Test metrics: RMSE, MAE, R²

---

## 🔐 Error Handling

### File Operations
```python
# Missing file
FileNotFoundError("Data file not found: {filepath}")

# Invalid path
ValueError("Invalid input path")
```

### Data Operations
```python
# Missing column
ValueError("Target column 'X' not found in DataFrame")

# Invalid input
ValueError(f"Invalid input: movie_title='{movie_title}', genre='{genre}'")
```

### Model Operations
```python
# Model not trained
FileNotFoundError("Model file not found: {MODEL_PATH}")

# Feature mismatch
ValueError("Feature dimension mismatch")
```

---

## 📝 Logging Format

```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
2024-01-15 10:30:45,123 - src.train - INFO - Starting training pipeline
```

### Log Levels
- **DEBUG**: Detailed variable values
- **INFO**: Pipeline progress, important milestones
- **WARNING**: Potential issues (missing features, fallbacks)
- **ERROR**: Runtime errors with context

---

## 🎯 Performance Specifications

| Operation | Time | Memory | Notes |
|-----------|------|--------|-------|
| Load data | <1s | ~50MB | For 30K records |
| Preprocess | 1-2s | ~100MB | Includes all cleaning |
| Feature eng | 1-2s | ~150MB | With scaling |
| Train KNN | 1-2s | ~100MB | On 24K records |
| Train RF | 3-5s | ~300MB | More complex |
| Predict (KNN) | <1ms | <10MB | Per sample |
| Predict (RF) | <5ms | <10MB | Per sample |
| Cross-val (5F) | 5-10s | ~100MB | Complete CV |

---

## 🔄 Reproducibility

### Random States
```python
RANDOM_STATE = 42  # Used in:
  - train_test_split()
  - RandomForestRegressor()
  - cross_val_score()
  - np.random operations
```

### Saved Artifacts
```python
# Training produces:
- models/movie_recommendation_model.pkl
- models/feature_scaler.pkl
- data/train_data.csv
- data/test_data.csv

# Ensures reproducibility via:
- Saved train/test split indices
- Saved scaler (identical scaling in predict)
- Fixed random seed
```

---

## 📦 Dependencies

| Package | Import | Version | Use |
|---------|--------|---------|-----|
| pandas | pd | 2.0.3 | DataFrames, CSV I/O |
| numpy | np | 1.24.3 | Arrays, math |
| sklearn | - | 1.3.0 | ML algorithms, metrics |
| sklearn.preprocessing | - | 1.3.0 | Scaler, LabelEncoder |
| sklearn.neighbors | - | 1.3.0 | KNeighborsRegressor |
| sklearn.ensemble | - | 1.3.0 | RandomForestRegressor |
| sklearn.model_selection | - | 1.3.0 | train_test_split, CV |
| sklearn.metrics | - | 1.3.0 | MSE, RMSE, MAE, R² |
| pickle | pickle | builtin | Model serialization |
| pathlib | Path | builtin | File paths |
| logging | logging | builtin | Logging |
| json | json | builtin | Results I/O |
| dataclasses | dataclass | builtin | PredictionResult |
| typing | - | builtin | Type hints |

---

## 🚀 Quick Command Reference

```bash
# Validate setup
python validate_project.py

# Train model
python main.py train
python main.py train --data custom.csv
python main.py train --model rf

# Single prediction
python main.py predict --movie "Title" --genre "Action"

# Batch prediction
python main.py batch --file input.csv

# Help
python main.py --help
python main.py train --help
python main.py predict --help
```

---

**This specification provides complete technical documentation for all modules, functions, and data structures in the NextWatch ML system.**

<- WidgetCustomizer: fix embed URL /widget-custom.js → Minor documentation update -->
