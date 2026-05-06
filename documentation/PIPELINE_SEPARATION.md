# ML Pipeline Separation of Concerns

## Overview

This document explains the professional separation of concerns in the NextWatch ML pipeline, demonstrating proper engineering practices for machine learning systems.

---

## Architecture

### Module Responsibilities

#### 1. **data_loader.py** - Data Loading ONLY
**Purpose**: Load raw data from files  
**Responsibility**: 
- Load CSV files
- Basic file validation
- Return clean DataFrame

**Does NOT do**:
- Preprocessing ❌
- Feature engineering ❌
- Model training ❌
- Inference ❌

**Key Functions**:
```python
load_data(filepath)           # Load raw CSV → DataFrame
validate_columns(df, cols)    # Verify required columns exist
get_data_info(df)            # Get shape, dtypes, memory usage
```

---

#### 2. **data_preprocessing.py** - Data Cleaning
**Purpose**: Handle missing values, duplicates, validation

**Responsibility**:
- Handle missing values (mean/median/drop strategies)
- Remove duplicates
- Validate numeric ranges
- Data quality checks

**Does NOT do**:
- Feature engineering ❌
- Scaling/normalization ❌
- Model training ❌

**Key Functions**:
```python
handle_missing_values(df, strategy)
remove_duplicates(df)
validate_numeric_ranges(df)
```

---

#### 3. **feature_engineering.py** - Feature Creation & Transformation
**Purpose**: Create features, encode categories, scale values

**Responsibility**:
- Encode categorical variables
- Create interaction features
- Scale numeric features
- Select final features

**Does NOT do**:
- Model training ❌
- Inference without artifacts ❌

**Key Functions**:
```python
encode_categorical_features(df, fit=True/False)  # Fit OR transform
create_feature_interactions(df)
scale_numeric_features(df, fit=True/False)       # Fit OR transform
select_features(df, feature_list)
```

---

#### 4. **train.py** - Model Training Pipeline
**Purpose**: Training workflow orchestration

**Critical Pattern**:
```
RAW DATA
    ↓
[SPLIT into train/test BEFORE preprocessing]
    ↓
Training Data              Test Data
    ↓                          ↓
[Preprocess + FIT]        [Preprocess + TRANSFORM]
encoders/scaler created    uses saved encoders/scaler
    ↓                          ↓
[Train Model]             [Evaluate on Test Set]
    ↓                          ↓
[Save All Artifacts]      Metrics Calculated
```

**Responsibility**:
1. Load raw data via `data_loader`
2. Split into train/test **BEFORE preprocessing**
3. Preprocess training data (fit encoders/scaler)
4. Preprocess test data (transform with training artifacts)
5. Train model on training data only
6. Evaluate on test set
7. Save model + artifacts

**Key Functions**:
```python
split_train_test(df)                      # BEFORE preprocessing
preprocess_training_data(df)              # FIT artifacts
preprocess_test_data(df, artifacts)       # TRANSFORM with artifacts
train_model(X_train, y_train)
evaluate_model(model, X_test, y_test)
save_model_and_artifacts(model, artifacts)
train_pipeline()                          # Orchestration
```

---

#### 5. **predict.py** - Inference/Prediction Pipeline
**Purpose**: Make predictions on new data

**Critical Pattern**:
```
NEW INPUT DATA
    ↓
[Load Saved Artifacts]
model, scaler, encoders (trained during training)
    ↓
[Transform Input]
Uses ONLY saved scaler/encoders
NO FITTING
    ↓
[Make Prediction]
Returns movie recommendation
```

**Responsibility**:
1. Load saved model + artifacts
2. Validate input
3. Transform input with saved artifacts (NO fitting)
4. Extract features in correct order
5. Make prediction
6. Return structured result

**Critical**: NEVER fits preprocessing
- Uses `encoder.transform()` NOT `encoder.fit_transform()`
- Uses `scaler.transform()` NOT `scaler.fit_transform()`
- No train/test split ❌
- No preprocessing fitting ❌

**Key Functions**:
```python
load_saved_artifacts()                        # Load saved models/scalers
validate_input_data(title, genre)
prepare_input_dataframe(title, genre)
transform_input_with_artifacts(df, artifacts) # TRANSFORM ONLY
extract_features_for_model(df)
make_prediction(model, X)
predict_single(movie_title, genre)            # Single prediction
predict_batch(input_data)                     # Multiple predictions
```

---

## Critical Patterns

### Pattern 1: FIT vs TRANSFORM

**Training Phase** (train.py):
```python
# FIT on training data only
scaler = StandardScaler()
scaler.fit(X_train)                  # ← FITTING happens here

X_train_scaled = scaler.transform(X_train)  # Transform training
X_test_scaled = scaler.transform(X_test)    # Transform test (uses fitted scaler)
```

**Inference Phase** (predict.py):
```python
# Load already-fitted scaler
scaler = joblib.load("scaler.pkl")   # ← Loaded, not fitted

X_new_scaled = scaler.transform(X_new)  # ← TRANSFORM ONLY, no fitting
```

---

### Pattern 2: Train/Test Split BEFORE Preprocessing

**WRONG** ❌:
```python
df = load_data()
df = preprocess(df)           # Fits scaler on ALL data
train, test = split(df)       # DATA LEAKAGE!
model.fit(train)
```

**CORRECT** ✅:
```python
df = load_data()
train, test = split(df)        # Split FIRST

# Fit preprocessing on training data only
train = preprocess(train)      # Scaler fitted on 80% of data
test = preprocess(test)        # Scaler transforms on 20% (no fitting)

model.fit(train)
```

---

### Pattern 3: Artifacts Saved During Training

**training.py** saves:
```
models/
├── movie_recommendation_model.pkl       # Trained model
├── scaler.pkl                           # Fitted StandardScaler
├── label_encoders.pkl                   # Fitted LabelEncoders
├── evaluation_report.json               # Test metrics
└── preprocessing_metadata.json          # Feature info
```

**predict.py** loads and uses:
```python
model = joblib.load("movie_recommendation_model.pkl")
scaler = joblib.load("scaler.pkl")
encoders = joblib.load("label_encoders.pkl")

# Never re-fit these - only transform new data
```

---

## Workflow Examples

### Example 1: Training

```bash
# Run complete training pipeline
python -m src.train

# Or with specific model
python -m src.train knn  # or 'rf' for Random Forest
```

**What happens**:
1. ✅ Loads raw data (data/raw/raw_movies.csv)
2. ✅ Splits 80/20 train/test
3. ✅ Preprocesses training set (fits scaler/encoders)
4. ✅ Preprocesses test set (transforms with training artifacts)
5. ✅ Trains KNN or RF model on training set
6. ✅ Evaluates on test set
7. ✅ Saves all artifacts to models/

---

### Example 2: Single Prediction

```bash
# Make single prediction
python -m src.predict --movie "Inception" --genre "Science Fiction"
```

**What happens**:
1. ✅ Loads saved model & artifacts
2. ✅ Validates input (genre exists)
3. ✅ Creates input features
4. ✅ Transforms with saved scaler/encoders (NO fitting)
5. ✅ Makes prediction
6. ✅ Returns result with confidence

---

### Example 3: Batch Prediction

```python
from src.predict import predict_batch

# CSV with columns: movie_title, genre
results = predict_batch("data/sample_predictions.csv")

for result in results:
    print(f"{result.input_movie} → Movie {result.predicted_movie_id}")
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ RAW DATA                                                    │
│ (data/raw/raw_movies.csv)                                  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ├──────── data_loader.load_data()
                  │
┌─────────────────▼───────────────────────────────────────────┐
│ TRAINING                              PREDICTION (INFERENCE)│
└──────────┬──────────────────────────────┬───────────────────┘
           │                              │
    [STEP 1: Split]                  [STEP 1: Load Artifacts]
    train (80%)                       model.pkl
    test (20%)                        scaler.pkl
           │                          encoders.pkl
           │                              │
    ┌──────┴──────────────┐              │
    │                     │              │
[train_data]         [test_data]    [Input Data]
    │                     │              │
    │              (NO preprocessing)    │
    │                     │              │
    ├─ FIT PREPROCESSING  ├─ TRANSFORM   ├─ VALIDATE
    │  (scalers)          │  (transform) │
    │  (encoders)         │              ├─ TRANSFORM
    │                     │              │  (no fitting)
    ├─ TRAIN MODEL        ├─ EVALUATE    │
    │                     │              ├─ PREDICT
    └─────────┬───────────┴──────────┬───┴───────┘
              │                      │
         [Model.pkl]            [Result]
         [Scaler.pkl]           {movie_id, confidence}
         [Encoders.pkl]
         [Metrics.json]
```

---

## File Organization

```
NextWatch-/
│
├── data/
│   ├── raw/
│   │   ├── raw_movies.csv                 ← Input (from data_loader)
│   │   └── sample_predictions.csv         ← Input for predict_batch()
│   │
│   └── processed/
│       ├── train_data.csv                 ← Output of train.py
│       └── test_data.csv                  ← Output of train.py
│
├── models/
│   ├── movie_recommendation_model.pkl     ← Trained model
│   ├── scaler.pkl                         ← Fitted scaler
│   ├── label_encoders.pkl                 ← Fitted encoders
│   ├── evaluation_report.json             ← Test metrics
│   └── preprocessing_metadata.json        ← Feature config
│
├── src/
│   ├── __init__.py
│   ├── config.py                          ← All constants
│   ├── data_loader.py                     ← Load data
│   ├── data_preprocessing.py              ← Clean data
│   ├── feature_engineering.py             ← Create features
│   ├── train.py                           ← Training pipeline
│   ├── predict.py                         ← Inference pipeline
│   └── evaluate.py                        ← Metrics
│
├── requirements.txt
├── README.md
└── PIPELINE_SEPARATION.md                 ← This file
```

---

## Why This Design?

### 1. **Prevents Data Leakage** ✅
- Train/test split happens BEFORE preprocessing
- Scaler fitted only on training data
- Test set statistics don't influence model

### 2. **Reproducibility** ✅
- Saved artifacts = consistent predictions
- Same scaler used for all future predictions
- No randomness in inference

### 3. **Production Readiness** ✅
- Separate training and inference codepaths
- Inference module independent of training
- Easy deployment (just copy model files)

### 4. **Maintainability** ✅
- Clear responsibilities per module
- Easy to test each component
- Easy to replace models/algorithms

### 5. **Scalability** ✅
- Can serve predictions without training code
- Can train new models without affecting inference
- Easy to parallelize batch predictions

---

## Testing Your Pipeline

### Test 1: Training Pipeline
```bash
cd /home/scatterzz/Documents/NextWatch-
source venv/bin/activate
python -m src.train
```

Expected output:
- ✅ Model saved to models/movie_recommendation_model.pkl
- ✅ Scaler saved to models/scaler.pkl
- ✅ Metrics printed to console

### Test 2: Single Prediction
```bash
python -m src.predict --movie "Inception" --genre "Science Fiction"
```

Expected output:
- ✅ Loads saved artifacts
- ✅ Makes prediction
- ✅ Returns movie_id with confidence

### Test 3: Batch Prediction
```python
from src.predict import predict_batch
results = predict_batch("data/raw/sample_predictions.csv")
print(f"Predicted {len(results)} movies")
```

---

## Key Takeaways

| Aspect | Training | Inference |
|--------|----------|-----------|
| Data | Raw data from files | Single/batch new inputs |
| Preprocessing | FIT encoders/scaler | TRANSFORM with saved artifacts |
| Model | Train from scratch | Load saved model |
| Output | Save model + artifacts | Prediction + confidence |
| Fitting | YES - fits preprocessing | NO - never fits |
| Train/Test | YES - split before prep | NO - only inference |

---

## Command Reference

### Training
```bash
python -m src.train              # Train with default KNN
python -m src.train knn          # Explicit KNN
python -m src.train rf           # Train with Random Forest
```

### Single Prediction
```bash
python -m src.predict --movie "MovieTitle" --genre "GenreName"
```

### Batch Prediction
```python
from src.predict import predict_batch
results = predict_batch("path/to/file.csv")
```

### Load Artifacts Manually
```python
import joblib
from src.config import MODEL_PATH, SCALER_PATH, LABEL_ENCODER_PATH

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
encoders = joblib.load(LABEL_ENCODER_PATH)
```

---

## Summary

This pipeline demonstrates **professional ML engineering**:
- ✅ Clear separation of concerns
- ✅ No data leakage (train/test split first)
- ✅ Proper fit vs transform usage
- ✅ Reproducible predictions
- ✅ Production-ready architecture
- ✅ Independent training and inference
- ✅ Easy to test and maintain
