# Quick Start Guide

This guide will help you get the NextWatch movie recommendation system up and running in 5 minutes.

## Step 1: Install Dependencies (1 minute)

```bash
# Navigate to the project directory
cd NextWatch-

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

## Step 2: Train the Model (2 minutes)

We've included sample data (`data/raw_movies.csv`) to get you started immediately.

```bash
# Train the recommendation model
python main.py train
```

**What happens:**
- Data is cleaned and preprocessed
- Features are extracted and scaled
- A K-Nearest Neighbors model is trained
- The model is saved for predictions
- Evaluation metrics are printed

## Step 3: Make a Prediction (1 minute)

```bash
# Predict what to watch next
python main.py predict --movie "Inception" --genre "Science Fiction"
```

**Expected output:**
```
============================================================
PREDICTION RESULT:
============================================================
Based on your viewing of 'Inception' (Science Fiction), we recommend movie ID: 42
Recommended Movie ID: 42
Confidence: 0.8745
```

## Step 4: Batch Predictions (Optional)

Predict for multiple movies at once:

```bash
# Use the sample batch file
python main.py batch --file data/sample_predictions.csv
```

## Project Structure Overview

```
NextWatch-/
├── src/                          # All ML pipeline code
│   ├── config.py                 # Configuration
│   ├── data_preprocessing.py      # Data cleaning
│   ├── feature_engineering.py     # Feature creation
│   ├── train.py                   # Model training
│   ├── evaluate.py                # Performance evaluation
│   └── predict.py                 # Making predictions
│
├── data/                          # Data storage
│   ├── raw_movies.csv             # Sample input data (included!)
│   └── sample_predictions.csv     # Sample batch input
│
├── models/                        # Trained model storage
│
├── main.py                        # Entry point (CLI)
├── requirements.txt               # Dependencies
└── README.md                      # Full documentation
```

## Key Features

✅ **Professional Structure**: Separated modules with clear responsibilities
✅ **No Circular Imports**: Clean dependency management
✅ **Reproducible Results**: Fixed random seeds and saved artifacts
✅ **Easy to Use**: Simple command-line interface
✅ **Extensible**: Easy to add new features and models
✅ **Well Documented**: Comprehensive logging and type hints

## Supported Genres

The system supports these genres:
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

## Customization

### Use Custom Data

Replace `data/raw_movies.csv` with your own data (must have columns: `movie_title`, `release_year`, `rating`, `vote_count`, `revenue`, `budget`, `runtime`, `popularity`, `genre`, `next_movie_title`).

Then train:
```bash
python main.py train --data data/your_custom_data.csv
```

### Use Random Forest Model

Instead of K-Nearest Neighbors:
```bash
python main.py train --model rf
```

### Programmatic Usage

```python
from pathlib import Path
from src.data_preprocessing import preprocess_data
from src.feature_engineering import engineer_features
from src.train import train_pipeline
from src.predict import predict_for_user

# Load and process data
df = preprocess_data()

# Engineer features
engineered_df, artifacts = engineer_features(df, fit_scaler=True)

# Train model
model, info = train_pipeline(engineered_df, model_type="knn")

# Make prediction
result = predict_for_user(model, "Inception", "Science Fiction")
print(result.recommendation_text)
```

## Troubleshooting

**Q: "Model file not found"**
A: Run `python main.py train` first to train the model.

**Q: "Genre not found"**
A: Check the genre name matches the supported list (case-sensitive).

**Q: How do I see all available commands?**
A: Run `python main.py --help`

## Next Steps

1. **Explore the Code**: Read through `README.md` for detailed documentation
2. **Try Different Models**: Train with `--model rf` to try Random Forest
3. **Add Custom Data**: Replace the sample data with your own movie database
4. **Extend Features**: Modify `src/feature_engineering.py` to add new features
5. **Integrate with API**: Use `predict.py` in your backend API

## Performance Tips

- Training: 1-5 seconds (depending on data size)
- Prediction: <10ms per recommendation
- Model size: ~2-5 MB

## Questions?

See `README.md` for:
- Detailed architecture explanation
- Configuration options
- Extending the system
- API documentation for each module

---

**You're ready to go!** Train your first model and make predictions. 🎬

<- WidgetCustomizer: fix embed URL /widget-custom.js → Minor documentation update -->
