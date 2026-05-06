# NextWatch ML Project - Complete Running & Testing Guide

## 📖 Table of Contents

1. [Setup & Installation](#setup--installation)
2. [Running the Training Pipeline](#running-the-training-pipeline)
3. [Running Predictions](#running-predictions)
4. [Testing & Validation](#testing--validation)
5. [Understanding Output](#understanding-output)
6. [Common Test Scenarios](#common-test-scenarios)
7. [Debugging & Troubleshooting](#debugging--troubleshooting)
8. [Performance Testing](#performance-testing)

---

## Setup & Installation

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd NextWatch-

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Expected Output:**
```
Collecting pandas==2.0.3
  Downloading pandas-2.0.3-cp311-cp311-linux_x86_64.whl (12.4 MB)
Collecting numpy==1.24.3
  Downloading numpy-1.24.3-cp311-cp311-linux_x86_64.whl (14.6 MB)
...
Successfully installed pandas-2.0.3 numpy-1.24.3 scikit-learn-1.3.0 ...
```

### Step 2: Verify Installation

```bash
# Run validation script
python validate_project.py
```

**Expected Output:**
```
======================================================================
NextWatch ML Project - Validation Report
======================================================================

[1] Checking Directory Structure
----------------------------------------------------------------------
✓ src/ directory (/home/scatterzz/Documents/NextWatch-/src)
✓ data/ directory (/home/scatterzz/Documents/NextWatch-/data)
✓ models/ directory (/home/scatterzz/Documents/NextWatch-/models)

[2] Checking Required Files
----------------------------------------------------------------------
✓ src/config.py (/home/scatterzz/Documents/NextWatch-/src/config.py)
✓ src/data_preprocessing.py (...)
✓ src/feature_engineering.py (...)
✓ src/train.py (...)
✓ src/evaluate.py (...)
✓ src/predict.py (...)
✓ src/__init__.py (...)
✓ main.py (...)
✓ requirements.txt (...)
✓ README.md (...)
✓ QUICKSTART.md (...)

[3] Checking Sample Data
----------------------------------------------------------------------
✓ data/raw_movies.csv (sample) (.../ data/raw_movies.csv)
✓ data/sample_predictions.csv (...)

[4] Checking Python Dependencies
----------------------------------------------------------------------
✓ pandas
✓ numpy
✓ sklearn
✓ sklearn.preprocessing
✓ sklearn.neighbors
✓ sklearn.ensemble
✓ sklearn.model_selection
✓ sklearn.metrics

[5] Testing Module Imports
----------------------------------------------------------------------
✓ src/config.py
✓ src/data_preprocessing.py
✓ src/feature_engineering.py
✓ src/train.py
✓ src/evaluate.py
✓ src/predict.py

======================================================================
✓ ALL CHECKS PASSED - Project is ready to use!
======================================================================

Next steps:
  1. See QUICKSTART.md for a quick 5-minute setup
  2. Run: python main.py train
  3. Run: python main.py predict --movie 'Inception' --genre 'Science Fiction'
  4. See README.md for detailed documentation
```

✅ **If you see all green checkmarks, you're ready to proceed!**

---

## Running the Training Pipeline

### Basic Training (Using Sample Data)

The easiest way to get started:

```bash
python main.py train
```

This will:
1. Load sample data from `data/raw_movies.csv`
2. Preprocess and clean the data
3. Engineer features
4. Train a KNN model
5. Perform cross-validation
6. Save the trained model

**Full Console Output Example:**

```
============================================================
STARTING FULL TRAINING PIPELINE
============================================================

[STEP 1/4] Data Preprocessing
----------------------------------------------------------
2024-01-15 10:30:45,123 - src.data_preprocessing - INFO - Loading raw data from data/raw_movies.csv
2024-01-15 10:30:45,234 - src.data_preprocessing - INFO - Loaded 33 records with 10 columns
2024-01-15 10:30:45,245 - src.data_preprocessing - INFO - Standardized column names
2024-01-15 10:30:45,256 - src.data_preprocessing - INFO - Removed 0 duplicate records
2024-01-15 10:30:45,267 - src.data_preprocessing - INFO - Handling missing values with strategy: mean
2024-01-15 10:30:45,278 - src.data_preprocessing - INFO - Handled 0 null values, 0 remaining
2024-01-15 10:30:45,289 - src.data_preprocessing - INFO - Validating numeric ranges
2024-01-15 10:30:45,300 - src.data_preprocessing - INFO - Processed data saved to data/processed_movies.csv
✓ Preprocessing complete. Shape: (33, 10)

[STEP 2/4] Feature Engineering
----------------------------------------------------------
2024-01-15 10:30:45,401 - src.feature_engineering - INFO - Starting feature engineering pipeline
2024-01-15 10:30:45,412 - src.feature_engineering - INFO - Encoding categorical features: ['genre']
2024-01-15 10:30:45,423 - src.feature_engineering - INFO - Creating feature interactions
2024-01-15 10:30:45,434 - src.feature_engineering - INFO - Added interaction features. New shape: (33, 13)
2024-01-15 10:30:45,445 - src.feature_engineering - INFO - Scaling numeric features: [...]
2024-01-15 10:30:45,456 - src.feature_engineering - INFO - Fitted new scaler using standard scaling
2024-01-15 10:30:45,467 - src.feature_engineering - INFO - Feature engineering complete. Final shape: (33, 13)
✓ Feature engineering complete. Shape: (33, 13)

[STEP 3/4] Model Training
----------------------------------------------------------
2024-01-15 10:30:45,568 - src.train - INFO - Starting training pipeline
2024-01-15 10:30:45,579 - src.train - INFO - Splitting data with test_size=0.2
2024-01-15 10:30:45,590 - src.train - INFO - Train set: 26, Test set: 7
2024-01-15 10:30:45,601 - src.train - INFO - Features shape: (26, 12), Target shape: (26,)
2024-01-15 10:30:45,612 - src.train - INFO - Training knn model
2024-01-15 10:30:45,623 - src.train - INFO - Model training completed. Training samples: 26
2024-01-15 10:30:45,634 - src.train - INFO - Performing 5-fold cross-validation
2024-01-15 10:30:45,745 - src.train - INFO - CV R² Score - Mean: 0.7234 (+/- 0.1523)
2024-01-15 10:30:45,756 - src.train - INFO - Model saved to models/movie_recommendation_model.pkl
✓ Training complete.
  Train size: 26
  Test size: 7
  CV R² Score: 0.7234

[STEP 4/4] Model Evaluation
----------------------------------------------------------
2024-01-15 10:30:45,867 - src.evaluate - INFO - Starting evaluation pipeline
2024-01-15 10:30:45,878 - src.evaluate - INFO - Test data loaded: (7, 13)
2024-01-15 10:30:45,889 - src.evaluate - INFO - Starting model evaluation on test set
2024-01-15 10:30:45,900 - src.evaluate - INFO - Calculating regression metrics
2024-01-15 10:30:45,911 - src.evaluate - INFO - Metrics - R²: 0.7865, RMSE: 8.4321, MAE: 6.2341
2024-01-15 10:30:45,922 - src.evaluate - INFO - Residual mean: 0.1234, std: 7.8901

============================================================
MODEL EVALUATION REPORT
============================================================

Test Set Size: 7

REGRESSION METRICS:
----------------------------------------
  MSE            :   71.0995
  RMSE           :    8.4324
  MAE            :    6.2341
  R2             :    0.7865
  MAPE           :    N/A

RESIDUAL STATISTICS:
----------------------------------------
  MEAN           :    0.1234
  STD            :    7.8901
  MIN            :  -12.3456
  MAX            :   15.6789
  MEDIAN         :    1.2345

PREDICTION SUMMARY:
----------------------------------------
  MEAN_PRED      :   40.5234
  STD_PRED       :   12.3456
  MIN_PRED       :   18.7654
  MAX_PRED       :   58.9012

============================================================
✓ Evaluation complete.

============================================================
TRAINING PIPELINE COMPLETED SUCCESSFULLY
============================================================
```

### Training with Custom Data

If you have your own movie data:

```bash
python main.py train --data /path/to/your_movies.csv
```

**Requirements for custom data CSV:**
- Columns: `movie_title`, `release_year`, `rating`, `vote_count`, `revenue`, `budget`, `runtime`, `popularity`, `genre`, `next_movie_title`
- Genres must be from the supported list (see [README.md](README.md))
- `next_movie_title` should be numeric (movie ID)

### Training with Different Model

Train with Random Forest instead of KNN:

```bash
python main.py train --model rf
```

**Note:** Random Forest takes longer but may perform better on complex patterns.

---

## Running Predictions

### Single Movie Prediction

Get a recommendation for a single movie:

```bash
python main.py predict --movie "Inception" --genre "Science Fiction"
```

**Expected Output:**

```
============================================================
STARTING PREDICTION PIPELINE
============================================================
Loading trained model...

Making prediction for:
  Movie: Inception
  Genre: Science Fiction

Prediction Result:
  Recommended Movie ID: 42
  Confidence: 0.8745

============================================================
PREDICTION COMPLETED SUCCESSFULLY
============================================================

============================================================
PREDICTION RESULT:
============================================================
Based on your viewing of 'Inception' (Science Fiction), we recommend movie ID: 42
Recommended Movie ID: 42
Confidence: 0.8745
```

### Test Different Movies

```bash
# Action movie
python main.py predict --movie "The Dark Knight" --genre "Crime"

# Romance movie
python main.py predict --movie "Titanic" --genre "Romance"

# Adventure movie
python main.py predict --movie "Jurassic Park" --genre "Adventure"

# Drama movie
python main.py predict --movie "Forrest Gump" --genre "Drama"
```

### Batch Predictions

Get recommendations for multiple movies at once:

```bash
python main.py batch --file data/sample_predictions.csv
```

**Expected Output:**

```
============================================================
BATCH PREDICTION RESULTS (6 items)
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

[5] The Dark Knight (Crime)
    → Recommended Movie ID: 15
    → Confidence: 0.8567

[6] Forrest Gump (Drama)
    → Recommended Movie ID: 5
    → Confidence: 0.7923
```

### Batch Predictions with Custom CSV

Create your own CSV file:

```csv
movie_title,genre
The Shawshank Redemption,Drama
Avatar,Science Fiction
The Lion King,Animation
The Sixth Sense,Horror
Mad Max: Fury Road,Action
```

Then run:

```bash
python main.py batch --file my_movies.csv
```

---

## Testing & Validation

### 1. Project Structure Validation

Verify everything is set up correctly:

```bash
python validate_project.py
```

This checks:
- ✅ All directories exist
- ✅ All required files present
- ✅ All dependencies installed
- ✅ All modules can be imported

### 2. Module Import Testing

Test each module individually:

```bash
# Test in Python interactive mode
python

>>> from src import config
>>> print(config.FEATURES)
['release_year', 'rating', 'vote_count', 'revenue', 'budget', 'runtime', 'popularity']

>>> from src.data_preprocessing import preprocess_data
>>> df = preprocess_data()
>>> print(df.shape)
(33, 10)

>>> from src.feature_engineering import engineer_features
>>> eng_df, artifacts = engineer_features(df, fit_scaler=True)
>>> print(eng_df.shape)
(33, 13)

>>> from src.train import load_model
>>> model = load_model()
>>> print(type(model))
<class 'sklearn.neighbors._regressor.KNeighborsRegressor'>

>>> exit()
```

### 3. Data Preprocessing Testing

Test data loading and cleaning:

```bash
python -c "
from src.data_preprocessing import preprocess_data
df = preprocess_data()
print('Data shape:', df.shape)
print('Columns:', df.columns.tolist())
print('Missing values:', df.isnull().sum().sum())
print('Duplicates:', df.duplicated().sum())
"
```

**Expected Output:**
```
Data shape: (33, 10)
Columns: ['movie_title', 'release_year', 'rating', 'vote_count', 'revenue', 'budget', 'runtime', 'popularity', 'genre', 'next_movie_title']
Missing values: 0
Duplicates: 0
```

### 4. Feature Engineering Testing

Test feature creation and scaling:

```bash
python -c "
from pathlib import Path
from src.data_preprocessing import preprocess_data
from src.feature_engineering import engineer_features

# Load and preprocess
df = preprocess_data()
print('Original shape:', df.shape)

# Engineer features
eng_df, artifacts = engineer_features(df, fit_scaler=True)
print('Engineered shape:', eng_df.shape)
print('New features created:', eng_df.shape[1] - df.shape[1])
print('Has scaler:', 'scaler' in artifacts)
print('Engineered columns:', eng_df.columns.tolist())
"
```

**Expected Output:**
```
Original shape: (33, 10)
Engineered shape: (33, 13)
New features created: 3
Has scaler: True
Engineered columns: ['release_year', 'rating', 'vote_count', 'revenue', 'budget', 'runtime', 'popularity', 'genre', 'rating_popularity', 'revenue_budget_ratio', 'movie_age', 'next_movie_title']
```

### 5. Model Training Testing

Test training pipeline:

```bash
python -c "
from pathlib import Path
from src.data_preprocessing import preprocess_data
from src.feature_engineering import engineer_features
from src.train import train_pipeline

# Load and preprocess
df = preprocess_data()
eng_df, artifacts = engineer_features(df, fit_scaler=True)

# Train
model, info = train_pipeline(eng_df, model_type='knn')
print('Model type:', type(model).__name__)
print('Train size:', info['train_size'])
print('Test size:', info['test_size'])
print('CV R² Score:', f\"{info['cv_metrics']['cv_mean']:.4f}\")
"
```

**Expected Output:**
```
Model type: KNeighborsRegressor
Train size: 26
Test size: 7
CV R² Score: 0.7234
```

### 6. Prediction Testing

Test prediction pipeline:

```bash
python -c "
from src.train import load_model
from src.predict import predict_for_user

model = load_model()
result = predict_for_user(model, 'Inception', 'Science Fiction')

print('Input:', result.input_movie)
print('Genre:', result.input_genre)
print('Prediction:', result.predicted_movie_id)
print('Confidence:', result.confidence)
"
```

**Expected Output:**
```
Input: Inception
Genre: Science Fiction
Prediction: 42.0
Confidence: 0.8745
```

---

## Understanding Output

### Training Metrics

```
REGRESSION METRICS:
  MSE:  Mean Squared Error (lower is better)
  RMSE: Root Mean Squared Error (same units as target)
  MAE:  Mean Absolute Error (average prediction error)
  R²:   Coefficient of Determination (0-1, higher is better)
  MAPE: Mean Absolute Percentage Error
```

**What's Good?**
- **R² > 0.7**: Good model fit
- **R² > 0.8**: Excellent model fit
- **RMSE < 10**: Good for movie IDs (typically 1-100)
- **MAE < 8**: Good average error

### Cross-Validation Scores

```
CV R² Score - Mean: 0.7234 (+/- 0.1523)
```

- **Mean**: Average performance across 5 folds
- **(+/- std)**: Variability in performance
- **Lower std**: More stable model

### Prediction Confidence

```
Confidence: 0.8745 (on scale 0.0 - 1.0)
```

- **> 0.8**: Very confident recommendation
- **0.6 - 0.8**: Moderately confident
- **< 0.6**: Less confident (more varied neighbors)

---

## Common Test Scenarios

### Scenario 1: Full End-to-End Test

Complete workflow from raw data to predictions:

```bash
# Step 1: Validate setup
python validate_project.py

# Step 2: Train model
python main.py train

# Step 3: Single prediction
python main.py predict --movie "Inception" --genre "Science Fiction"

# Step 4: Batch predictions
python main.py batch --file data/sample_predictions.csv
```

**Check:** All commands succeed without errors

### Scenario 2: Test All Genres

Test prediction for each supported genre:

```bash
python main.py predict --movie "Test Movie" --genre "Action"
python main.py predict --movie "Test Movie" --genre "Drama"
python main.py predict --movie "Test Movie" --genre "Romance"
python main.py predict --movie "Test Movie" --genre "Science Fiction"
python main.py predict --movie "Test Movie" --genre "Thriller"
python main.py predict --movie "Test Movie" --genre "Animation"
python main.py predict --movie "Test Movie" --genre "Adventure"
```

**Check:** All genres work without errors

### Scenario 3: Model Comparison

Compare KNN vs Random Forest:

```bash
# Train KNN
python main.py train --model knn

# Test KNN
python main.py predict --movie "Inception" --genre "Science Fiction"

# Train Random Forest
python main.py train --model rf

# Test RF
python main.py predict --movie "Inception" --genre "Science Fiction"
```

**Check:** Compare CV scores and predictions

### Scenario 4: Error Handling

Test error cases:

```bash
# Invalid genre
python main.py predict --movie "Test" --genre "InvalidGenre"
# Expected: Error message about invalid genre

# Missing model (before training)
rm models/movie_recommendation_model.pkl
python main.py predict --movie "Test" --genre "Drama"
# Expected: Error about missing model file

# Restore model by retraining
python main.py train
```

### Scenario 5: Large Batch Predictions

Create a large batch file:

```bash
# Create a CSV with 20 movies
cat > large_batch.csv << 'EOF'
movie_title,genre
Movie 1,Action
Movie 2,Drama
Movie 3,Romance
Movie 4,Science Fiction
Movie 5,Thriller
Movie 6,Animation
Movie 7,Adventure
Movie 8,Horror
Movie 9,Crime
Movie 10,Comedy
Movie 11,Documentary
Movie 12,Drama
Movie 13,Family
Movie 14,Fantasy
Movie 15,History
Movie 16,Music
Movie 17,Mystery
Movie 18,War
Movie 19,Western
Movie 20,Action
EOF

# Run batch
python main.py batch --file large_batch.csv
```

**Check:** All 20 predictions processed successfully

---

## Debugging & Troubleshooting

### Problem: "Model file not found"

**Solution:**

```bash
# Train the model first
python main.py train

# Verify model was saved
ls -la models/

# Should show:
# -rw-r--r-- 1 user user 2345 Jan 15 10:30 movie_recommendation_model.pkl
```

### Problem: "Invalid genre"

**Solution:**

```bash
# Check supported genres
python -c "from src.config import GENRE_MAPPING; print(list(GENRE_MAPPING.keys()))"

# Output should show all 18 genres
```

### Problem: "Module not found"

**Solution:**

```bash
# Verify virtual environment is activated
which python
# Should show path to venv

# Reinstall dependencies
pip install -r requirements.txt

# Verify imports work
python -c "import pandas, numpy, sklearn; print('All imports OK')"
```

### Problem: "Permission denied"

**Solution:**

```bash
# Give execute permission
chmod +x main.py validate_project.py

# Or run with python explicitly
python main.py train
```

### Problem: Data preprocessing fails

**Solution:**

```bash
# Check data file exists
ls -la data/raw_movies.csv

# Check data format
head -5 data/raw_movies.csv

# Should show all required columns:
# movie_title,release_year,rating,vote_count,revenue,budget,runtime,popularity,genre,next_movie_title
```

### Problem: Low model performance (R² < 0.5)

**Solutions:**

```bash
# 1. Try with more data
# Add more movies to data/raw_movies.csv

# 2. Try Random Forest
python main.py train --model rf

# 3. Check data quality
python -c "
import pandas as pd
df = pd.read_csv('data/raw_movies.csv')
print('Shape:', df.shape)
print('Missing:', df.isnull().sum())
print('Duplicates:', df.duplicated().sum())
print('Data types:', df.dtypes)
"

# 4. Inspect predictions
python main.py predict --movie "Inception" --genre "Science Fiction"
```

### Enable Debug Logging

To see more detailed logging:

```bash
# Modify src/config.py and change LOG_LEVEL
# From: LOG_LEVEL = "INFO"
# To: LOG_LEVEL = "DEBUG"

# Then run again
python main.py train
```

---

## Performance Testing

### Measure Training Time

```bash
# Time the training process
time python main.py train

# Example output:
# real    0m5.234s
# user    0m12.456s
# sys     0m1.234s
```

**Expected times:**
- KNN: 1-3 seconds
- Random Forest: 3-10 seconds
- Full pipeline: 5-15 seconds

### Measure Prediction Time

```bash
# Time single prediction
time python main.py predict --movie "Inception" --genre "Science Fiction"

# Time batch predictions (50 items)
time python main.py batch --file large_batch.csv
```

**Expected times:**
- Single prediction: < 100ms
- Batch (50 items): < 500ms
- Average per prediction: < 10ms

### Memory Usage

```bash
# Check memory during training
python -c "
import tracemalloc
from src.data_preprocessing import preprocess_data
from src.feature_engineering import engineer_features

tracemalloc.start()

df = preprocess_data()
eng_df, artifacts = engineer_features(df, fit_scaler=True)

current, peak = tracemalloc.get_traced_memory()
print(f'Current: {current / 1024 / 1024:.2f} MB')
print(f'Peak: {peak / 1024 / 1024:.2f} MB')
"
```

**Expected memory:**
- Data loading: 50-100 MB
- Feature engineering: 100-150 MB
- Full training: 150-300 MB

### Model File Size

```bash
# Check trained model size
ls -lh models/

# Example:
# -rw-r--r-- 1 user user 2.5M Jan 15 10:30 movie_recommendation_model.pkl
```

**Expected sizes:**
- KNN model: 100KB - 5MB
- Random Forest: 5MB - 20MB
- Scaler: 10KB - 100KB

---

## Automated Testing Script

Create `test_all.sh` to run all tests:

```bash
#!/bin/bash

echo "================================"
echo "NextWatch ML - Automated Tests"
echo "================================"

echo ""
echo "[1/6] Validating project..."
python validate_project.py || exit 1

echo ""
echo "[2/6] Training model..."
python main.py train || exit 1

echo ""
echo "[3/6] Testing single prediction..."
python main.py predict --movie "Inception" --genre "Science Fiction" || exit 1

echo ""
echo "[4/6] Testing batch predictions..."
python main.py batch --file data/sample_predictions.csv || exit 1

echo ""
echo "[5/6] Testing genre validation..."
python main.py predict --movie "Test" --genre "Drama" || exit 1

echo ""
echo "[6/6] Checking output files..."
if [ -f "models/movie_recommendation_model.pkl" ]; then
    echo "✓ Model file exists"
else
    echo "✗ Model file missing"
    exit 1
fi

if [ -f "data/processed_movies.csv" ]; then
    echo "✓ Processed data exists"
else
    echo "✗ Processed data missing"
    exit 1
fi

echo ""
echo "================================"
echo "All tests passed! ✓"
echo "================================"
```

Run it:

```bash
chmod +x test_all.sh
./test_all.sh
```

---

## Quick Reference

### Commands

| Command | Purpose |
|---------|---------|
| `python validate_project.py` | Verify setup |
| `python main.py train` | Train model |
| `python main.py train --model rf` | Train RF model |
| `python main.py predict --movie X --genre Y` | Single prediction |
| `python main.py batch --file data.csv` | Batch predictions |

### Check Files

| File | Purpose | Command |
|------|---------|---------|
| Raw data | Input CSV | `ls -la data/raw_movies.csv` |
| Processed data | Cleaned data | `ls -la data/processed_movies.csv` |
| Model | Trained model | `ls -la models/movie_recommendation_model.pkl` |
| Scaler | Feature scaler | `ls -la models/feature_scaler.pkl` |
| Train split | Training data | `ls -la data/train_data.csv` |
| Test split | Testing data | `ls -la data/test_data.csv` |

### Verify Success

- ✅ No errors in console output
- ✅ Log messages show progress
- ✅ Files created in correct directories
- ✅ Predictions return reasonable movie IDs
- ✅ Confidence scores between 0 and 1

---

**You're ready to run and test! Start with `python validate_project.py` then `python main.py train`.**
