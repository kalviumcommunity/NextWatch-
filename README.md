# NextWatch: Movie Recommendation System

A professionally structured machine learning project for recommending the next movie to watch based on a user's previously watched movie and its genre.

## Project Structure

```
NextWatch-/
│
├── data/                              # Data directory
│   ├── raw_movies.csv                 # Raw input data
│   ├── processed_movies.csv            # Cleaned/preprocessed data
│   ├── features.csv                    # Engineered features
│   ├── train_data.csv                  # Training set
│   └── test_data.csv                   # Test set
│
├── models/                             # Trained models directory
│   ├── movie_recommendation_model.pkl  # Trained recommendation model
│   ├── feature_scaler.pkl              # Feature scaler (StandardScaler/MinMaxScaler)
│   └── label_encoder.pkl               # Categorical label encoder
│
├── src/                                # Source code modules
│   ├── config.py                       # Configuration and constants
│   ├── data_preprocessing.py           # Data loading, cleaning, validation
│   ├── feature_engineering.py          # Feature extraction, encoding, scaling
│   ├── train.py                        # Model training and cross-validation
│   ├── evaluate.py                     # Model evaluation and metrics
│   └── predict.py                      # Prediction on new data
│
├── main.py                             # Main entry point (CLI interface)
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
└── .git/                               # Git repository
```

## Architecture Overview

### Module Responsibilities

1. **config.py**: Central configuration hub
   - All constants and paths
   - Feature definitions
   - Model hyperparameters
   - Data validation ranges

2. **data_preprocessing.py**: Data cleaning and preparation
   - Load raw CSV data
   - Handle missing values
   - Remove duplicates
   - Validate numeric ranges
   - Standardize column names

3. **feature_engineering.py**: Feature creation and transformation
   - Encode categorical features (genre → numeric)
   - Create interaction features (rating × popularity)
   - Scale numeric features (StandardScaler/MinMaxScaler)
   - Select and transform features for modeling

4. **train.py**: Model training and persistence
   - Split data into train/test
   - Train KNN or Random Forest models
   - Perform cross-validation
   - Save trained models to disk

5. **evaluate.py**: Performance assessment
   - Calculate regression metrics (RMSE, MAE, R²)
   - Generate residual statistics
   - Create evaluation reports
   - Save results to JSON

6. **predict.py**: Inference and recommendations
   - Validate user input
   - Prepare features for prediction
   - Make recommendations
   - Support batch predictions

### Key Design Principles

- **No Circular Imports**: Each module imports only from `config` and standard libraries
- **Independent Pipelines**: Training and prediction can run independently
- **Function-Based**: All executable code is in functions, no top-level execution
- **Reproducibility**: Seeds and random states are configurable
- **Type Hints**: All functions include type annotations
- **Logging**: Comprehensive logging throughout

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone or navigate to the project**
   ```bash
   cd NextWatch-
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-Line Interface

The main entry point is `main.py` with three commands:

#### 1. Train the Model

```bash
# Train with default settings (KNN model)
python main.py train

# Train with custom data path
python main.py train --data /path/to/custom_data.csv

# Train with Random Forest instead of KNN
python main.py train --model rf
```

**Expected Output:**
- Preprocessed data saved to `data/processed_movies.csv`
- Engineered features saved to `data/features.csv`
- Train/test split saved to `data/train_data.csv` and `data/test_data.csv`
- Trained model saved to `models/movie_recommendation_model.pkl`
- Feature scaler saved to `models/feature_scaler.pkl`
- Evaluation report printed to console
- Metrics saved to `models/evaluation_results.json` (if implemented)

#### 2. Make a Single Prediction

```bash
# Predict what to watch next
python main.py predict --movie "Inception" --genre "Science Fiction"
```

**Example Output:**
```
============================================================
PREDICTION RESULT:
============================================================
Based on your viewing of 'Inception' (Science Fiction), we recommend movie ID: 42
Recommended Movie ID: 42
Confidence: 0.8745
```

#### 3. Batch Predictions

```bash
# Make predictions for multiple movies from a CSV file
python main.py batch --file input_movies.csv
```

**Input CSV Format** (`input_movies.csv`):
```csv
movie_title,genre
Inception,Science Fiction
The Matrix,Science Fiction
Titanic,Romance
Jurassic Park,Adventure
```

**Example Output:**
```
============================================================
BATCH PREDICTION RESULTS (4 items)
============================================================

[1] Inception (Science Fiction)
    → Recommended Movie ID: 42
    → Confidence: 0.8745

[2] The Matrix (Science Fiction)
    → Recommended Movie ID: 17
    → Confidence: 0.9123

[3] Titanic (Romance)
    → Recommended Movie ID: 55
    → Confidence: 0.7234

[4] Jurassic Park (Adventure)
    → Recommended Movie ID: 8
    → Confidence: 0.8891
```

### Using Modules Programmatically

```python
from pathlib import Path
from src.data_preprocessing import preprocess_data
from src.feature_engineering import engineer_features
from src.train import train_pipeline, load_model
from src.predict import predict_for_user

# Step 1: Preprocess data
df = preprocess_data()

# Step 2: Engineer features
engineered_df, artifacts = engineer_features(df, fit_scaler=True)

# Step 3: Train model
model, info = train_pipeline(engineered_df, model_type="knn")

# Step 4: Make prediction
result = predict_for_user(model, "Inception", "Science Fiction")
print(result.recommendation_text)
```

## Data Format

### Input Data (`data/raw_movies.csv`)

The system expects a CSV file with the following columns:

```csv
movie_title,release_year,rating,vote_count,revenue,budget,runtime,popularity,genre,next_movie_title
Inception,2010,8.8,2505811,839467222,160000000,148,83.5,Science Fiction,41
The Matrix,1999,8.7,1726179,467222728,63000000,136,78.2,Science Fiction,42
```

**Column Descriptions:**
- `movie_title`: Name of the input movie
- `release_year`: Year the movie was released
- `rating`: IMDB rating (0-10)
- `vote_count`: Number of votes
- `revenue`: Box office revenue
- `budget`: Production budget
- `runtime`: Duration in minutes
- `popularity`: Popularity score
- `genre`: Movie genre (must match `GENRE_MAPPING` in config)
- `next_movie_title`: Target - ID of recommended movie (numeric)

### Supported Genres

The system currently supports these genres:
- Action
- Adventure
- Animation
- Comedy
- Crime
- Documentary
- Drama
- Family
- Fantasy
- History
- Horror
- Music
- Mystery
- Romance
- Science Fiction
- Thriller
- War
- Western

To add more genres, modify `GENRE_MAPPING` in `src/config.py`.

## Configuration

All configuration is centralized in `src/config.py`. Key settings:

```python
# Data paths
RAW_DATA_PATH = Path("data/raw_movies.csv")
MODEL_PATH = Path("models/movie_recommendation_model.pkl")

# Feature engineering
FEATURES = ["release_year", "rating", "vote_count", "revenue", "budget", "runtime", "popularity"]
CATEGORICAL_FEATURES = ["genre"]
TARGET_COLUMN = "next_movie_title"

# Training
TRAIN_TEST_SPLIT_RATIO = 0.2
RANDOM_STATE = 42

# Model hyperparameters
MODEL_CONFIG = {
    "n_neighbors": 5,
    "weights": "distance",
    "metric": "euclidean",
}
```

## Model Details

### Supported Models

1. **K-Nearest Neighbors (KNN)** [Default]
   - Fast, interpretable
   - Good for recommendation systems
   - Hyperparameters: `n_neighbors=5`, `weights='distance'`

2. **Random Forest**
   - More complex, handles non-linearity
   - Better for complex patterns
   - Hyperparameters: `n_estimators=100`

### Evaluation Metrics

The system reports:
- **MSE**: Mean Squared Error
- **RMSE**: Root Mean Squared Error
- **MAE**: Mean Absolute Error
- **R²**: Coefficient of Determination
- **MAPE**: Mean Absolute Percentage Error (if applicable)

### Cross-Validation

- **Method**: K-Fold (default 5 splits)
- **Shuffle**: True
- **Random State**: 42 (for reproducibility)

## Logging

All modules include logging at the INFO level. Logs include:
- Data loading and preprocessing steps
- Feature engineering transformations
- Model training progress
- Evaluation results
- Prediction details

Adjust log level in `src/config.py` (`LOG_LEVEL` setting).

## Reproducibility

The system ensures reproducible results through:
- Fixed `RANDOM_STATE = 42` in all operations
- Saved train/test splits
- Saved feature scalers and encoders
- Documented hyperparameters
- Version pinning in `requirements.txt`

## Extending the System

### Adding New Features

Edit `src/feature_engineering.py`:
```python
def create_feature_interactions(df: pd.DataFrame) -> pd.DataFrame:
    # Add new interaction features here
    df["new_feature"] = df["feature1"] * df["feature2"]
    return df
```

### Adding New Models

Edit `src/train.py`:
```python
def train_model(X_train, y_train, model_type="knn"):
    if model_type == "my_model":
        model = MyCustomModel()
    # ... rest of function
```

### Custom Evaluation Metrics

Edit `src/evaluate.py`:
```python
def calculate_regression_metrics(y_true, y_pred):
    # Add new metrics here
    custom_metric = custom_calculation(y_true, y_pred)
    metrics["custom"] = custom_metric
    return metrics
```

## Troubleshooting

### "Model file not found"
- Ensure you've run `python main.py train` first
- Check that `models/` directory exists

### "Data file not found"
- Ensure raw data exists at `data/raw_movies.csv`
- Verify the path in `src/config.py`

### "Genre not found in available genres"
- Check the genre name matches `GENRE_MAPPING` in `src/config.py`
- Genre names are case-sensitive

### Low prediction confidence
- The model may need more training data
- Check feature scaling is enabled in config
- Verify feature engineering artifacts were saved

## Testing

To test the system with sample data:

```python
# Create sample data
import pandas as pd

sample_data = pd.DataFrame({
    'movie_title': ['Inception', 'The Matrix', 'Interstellar'],
    'release_year': [2010, 1999, 2014],
    'rating': [8.8, 8.7, 8.6],
    'vote_count': [2500000, 1700000, 2000000],
    'revenue': [839467222, 467222728, 731000000],
    'budget': [160000000, 63000000, 165000000],
    'runtime': [148, 136, 169],
    'popularity': [83.5, 78.2, 85.3],
    'genre': ['Science Fiction', 'Science Fiction', 'Science Fiction'],
    'next_movie_title': [42, 17, 23],
})

sample_data.to_csv('data/raw_movies.csv', index=False)
```

Then run: `python main.py train`

## Performance Benchmarks

Expected performance on typical movie datasets:
- **Training Time**: 1-5 seconds (depending on dataset size)
- **Prediction Time**: <10ms per prediction
- **Model Size**: ~2-5 MB (pickled)

## Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **scikit-learn**: Machine learning algorithms
- **matplotlib**: Visualization (optional)
- **seaborn**: Statistical visualization (optional)

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Contact & Support

[Add contact information here]

## Changelog

### Version 1.0.0
- Initial release
- KNN and Random Forest models
- Single and batch predictions
- Complete evaluation pipeline
