# NextWatch ML System Architecture

## 🏗️ System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         NextWatch ML System                              │
│                    Movie Recommendation Engine                           │
└─────────────────────────────────────────────────────────────────────────┘

                          ┌──────────────────┐
                          │    main.py       │
                          │   CLI Interface  │
                          │  (argparse)      │
                          └────────┬─────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
            ┌───────▼────┐  ┌──────▼─────┐  ┌────▼──────┐
            │   train    │  │  predict   │  │  batch    │
            │  command   │  │  command   │  │  command  │
            └───────┬────┘  └──────┬─────┘  └────┬──────┘
                    │              │             │
                    └──────────────┼─────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
        ┌───────▼────────┐  ┌──────▼─────┐  ┌───────▼──────┐
        │ Training       │  │ Prediction │  │  Evaluation  │
        │ Pipeline       │  │ Pipeline   │  │  Pipeline    │
        └───────┬────────┘  └──────┬─────┘  └───────┬──────┘
                │                  │               │
                │                  │               │
        ┌───────▼───────────────┐  │      ┌────────▼────────┐
        │ 1. Preprocessing      │  │      │ evaluate.py     │
        │ - load_raw_data()     │  │      │ - calculate     │
        │ - handle_missing()    │  │      │   metrics()     │
        │ - remove_duplicates() │  │      │ - generate      │
        │ - validate_ranges()   │  │      │   report()      │
        │ - standardize_names() │  │      └────────┬────────┘
        │ data_preprocessing.py │  │               │
        └───────┬───────────────┘  │      ┌────────▼────────┐
                │                  │      │ Metrics Output  │
        ┌───────▼────────────────┐ │      │ - RMSE          │
        │ 2. Feature Engineering │ │      │ - MAE           │
        │ - encode_categorical() │ │      │ - R²            │
        │ - create_interactions()│ │      │ - Residuals     │
        │ - scale_numeric()      │ │      └─────────────────┘
        │ feature_engineering.py │ │
        └───────┬────────────────┘ │
                │                  │
        ┌───────▼─────────────────┐│
        │ 3. Model Training       ││
        │ - split_train_test()    ││
        │ - train_model()         ││
        │ - cross_validate()      ││
        │ train.py                ││
        │                         ││
        │ Models:                 ││
        │ • KNN (default)         ││
        │ • Random Forest         ││
        └───────┬─────────────────┘│
                │                  │
        ┌───────▼──────────────┐   │
        │ Model Artifacts      │   │
        │ - model.pkl          │   │
        │ - scaler.pkl         │   │
        │ - train_data.csv     │   │
        │ - test_data.csv      │   │
        └──────────────────────┘   │
                                   │
                         ┌─────────▼──────┐
                         │ predict.py     │
                         │ - validate()   │
                         │ - encode()     │
                         │ - predict()    │
                         └────────┬───────┘
                                  │
                    ┌─────────────┴──────────────┐
                    │                            │
            ┌───────▼────────┐         ┌────────▼──────┐
            │ Single         │         │ Batch         │
            │ Prediction     │         │ Predictions   │
            │ Result:        │         │ Results:      │
            │ - Movie ID     │         │ - CSV output  │
            │ - Confidence   │         │ - Multiple    │
            │ - Message      │         │   results     │
            └────────────────┘         └───────────────┘
```

## 📊 Data Flow Diagram

```
┌─────────────────┐
│  Raw Data CSV   │
│  (raw_movies)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│   data_preprocessing.py          │
│ ┌─────────────────────────────┐  │
│ │ Clean & Validate            │  │
│ │ - Remove duplicates         │  │
│ │ - Handle missing values     │  │
│ │ - Validate ranges           │  │
│ └─────────────────────────────┘  │
└────────┬────────────────────────┘
         │
         ▼
┌────────────────────────────┐
│  Processed Data CSV        │
│  (processed_movies)        │
└────────┬───────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  feature_engineering.py           │
│ ┌────────────────────────────────┐│
│ │ Transform Features              ││
│ │ - Encode categories (genre)     ││
│ │ - Create interactions           ││
│ │ - Scale numeric features        ││
│ └────────────────────────────────┘│
└────────┬───────────────────────────┘
         │
         ├──────────────────────────┐
         │                          │
         ▼                          ▼
    ┌─────────────┐         ┌──────────────┐
    │ Features    │         │ Scaler       │
    │ CSV         │         │ (pkl)        │
    └──────┬──────┘         └──────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  train.py                         │
│ ┌────────────────────────────────┐│
│ │ Train & Evaluate                ││
│ │ - Split: 80% train, 20% test    ││
│ │ - Train model (KNN/RF)          ││
│ │ - Cross-validation (5-fold)     ││
│ │ - Save model                    ││
│ └────────────────────────────────┘│
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────┐
│ Trained Model (pkl)    │
│ + Train/Test splits    │
└────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  evaluate.py                      │
│ ┌────────────────────────────────┐│
│ │ Calculate Metrics               ││
│ │ - RMSE, MAE, R²                 ││
│ │ - Residual analysis             ││
│ │ - Generate report               ││
│ └────────────────────────────────┘│
└────────┬───────────────────────────┘
         │
         ▼
   Evaluation Report
```

## 🔄 Prediction Flow

```
User Input
    │
    ├─ movie_title: "Inception"
    ├─ genre: "Science Fiction"
    │
    ▼
┌──────────────────────────────────────┐
│  predict.py - predict_for_user()     │
│                                      │
│ ┌──────────────────────────────────┐ │
│ │ 1. Validate Input                │ │
│ │    ✓ movie_title exists          │ │
│ │    ✓ genre in GENRE_MAPPING      │ │
│ └──────────────────────────────────┘ │
│                                      │
│ ┌──────────────────────────────────┐ │
│ │ 2. Prepare Features              │ │
│ │    feature_dict = {              │ │
│ │      "genre": 14,                │ │
│ │      "rating": 7.5,              │ │
│ │      ...                         │ │
│ │    }                             │ │
│ └──────────────────────────────────┘ │
│                                      │
│ ┌──────────────────────────────────┐ │
│ │ 3. Encode for Prediction         │ │
│ │    X = [14, 7.5, 50.0, ...]     │ │
│ │    Shape: (1, n_features)        │ │
│ └──────────────────────────────────┘ │
│                                      │
│ ┌──────────────────────────────────┐ │
│ │ 4. Load Model & Predict          │ │
│ │    model = load_model()          │ │
│ │    prediction = model.predict(X) │ │
│ │    confidence = calc_confidence()│ │
│ └──────────────────────────────────┘ │
└────────────┬─────────────────────────┘
             │
             ▼
    PredictionResult(
      predicted_movie_id: 42,
      confidence: 0.8745,
      input_movie: "Inception",
      input_genre: "Science Fiction",
      recommendation_text: "..."
    )
             │
             ▼
    ┌─────────────────────────┐
    │ Formatted Output (Dict) │
    │ {                       │
    │   "status": "success",  │
    │   "recommendation": {   │
    │     "movie_id": 42,     │
    │     "confidence": 0.8745│
    │   },                    │
    │   "message": "Based..." │
    │ }                       │
    └─────────────────────────┘
             │
             ▼
      Display to User
```

## 📦 Module Dependency Graph

```
┌──────────────┐
│  config.py   │  ← All modules import from here
└──────┬───────┘
       │
       ├─────────┬────────────┬──────────┬──────────┬──────────┐
       │         │            │          │          │          │
       ▼         ▼            ▼          ▼          ▼          ▼
   ┌────┐  ┌──────────┐  ┌──────┐  ┌───────┐  ┌────────┐  ┌───────┐
   │    │  │          │  │      │  │       │  │        │  │       │
   │NO  │  │  data_   │  │feature│  │train │  │evaluate│  │predict│
   │    │  │  preproc │  │enginering│    │  │        │  │       │
   │    │  │          │  │      │  │      │  │        │  │       │
   │CIRC│  └──────────┘  └──┬───┘  └──┬───┘  └────┬───┘  └───┬───┘
   │    │                    │        │          │           │
   │ULAR│         ┌──────────┼────────┼──────────┴──────────┘
   │    │         │          │        │
   │    │         │    ┌─────┴────────┴──────┐
   │IMP │         │    │                     │
   │ORT │         │    │ (Prediction uses    │
   │S   │         │    │  train.load_model) │
   │    │         │    │                     │
   └────┘         │    └─────────────────────┘
              ┌───▼────────────────────────────┐
              │        main.py                  │
              │ (Orchestrates all modules)     │
              └────────────────────────────────┘
```

## 🎯 Key Features

### No Circular Dependencies ✓
```
config ← all modules (no reverse imports)
```

### Independent Pipelines ✓
```
Training Pipeline:   preprocess → engineer → train → evaluate
Prediction Pipeline: load_model → engineer → predict
(Both can run independently)
```

### Modular & Extensible ✓
```
Adding a new model:   Modify train.py only
Adding new features:  Modify feature_engineering.py only
Adding metrics:       Modify evaluate.py only
New genre:            Modify config.py only
```

---

**This architecture ensures scalability, maintainability, and professional code organization.**

<- WidgetCustomizer: fix embed URL /widget-custom.js → Minor documentation update -->

<- WidgetCustomizer: fix embed URL /widget-custom.js → Individual file update -->
