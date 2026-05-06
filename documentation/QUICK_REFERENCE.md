# NextWatch ML - Quick Reference Card

## 🚀 Installation (Copy & Paste)

```bash
cd NextWatch-
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## ✅ Validation (Run First)

```bash
python validate_project.py
# Should show: ✓ ALL CHECKS PASSED
```

---

## 🎓 Training

### Basic Training
```bash
python main.py train
```
**What it does:** Preprocesses data → Engineers features → Trains KNN model → Evaluates

### Training with Random Forest
```bash
python main.py train --model rf
```

### Training with Custom Data
```bash
python main.py train --data /path/to/your_movies.csv
```

**Expected Output Contains:**
- ✓ Preprocessing complete. Shape: (33, 10)
- ✓ Feature engineering complete. Shape: (33, 13)
- ✓ Training complete.
- ✓ CV R² Score: 0.7234 (+/- 0.1523)

---

## 🎬 Making Predictions

### Single Prediction
```bash
python main.py predict --movie "Inception" --genre "Science Fiction"
```

**Output:**
```
Recommended Movie ID: 42
Confidence: 0.8745
```

### Test All Genres
```bash
python main.py predict --movie "Test" --genre "Action"
python main.py predict --movie "Test" --genre "Drama"
python main.py predict --movie "Test" --genre "Romance"
python main.py predict --movie "Test" --genre "Science Fiction"
```

### Batch Predictions
```bash
python main.py batch --file data/sample_predictions.csv
```

---

## 📊 Understanding Metrics

| Metric | Range | Good | Explanation |
|--------|-------|------|-------------|
| **R²** | 0-1 | >0.7 | How well model explains data |
| **RMSE** | 0-∞ | <10 | Average prediction error |
| **MAE** | 0-∞ | <8 | Absolute error size |
| **Confidence** | 0-1 | >0.8 | How sure about prediction |

---

## 📁 File Locations

| What | Where | Created By |
|-----|-------|-----------|
| Raw data | `data/raw_movies.csv` | User |
| Processed data | `data/processed_movies.csv` | Training |
| Features | `data/features.csv` | Training |
| Train split | `data/train_data.csv` | Training |
| Test split | `data/test_data.csv` | Training |
| Trained model | `models/movie_recommendation_model.pkl` | Training |
| Feature scaler | `models/feature_scaler.pkl` | Training |

---

## 🧪 Testing Checklist

- [ ] `python validate_project.py` - All green ✓
- [ ] `python main.py train` - Completes without errors
- [ ] Check `models/movie_recommendation_model.pkl` exists - File size > 0
- [ ] `python main.py predict --movie "Inception" --genre "Science Fiction"` - Returns movie ID
- [ ] `python main.py batch --file data/sample_predictions.csv` - Predicts 6 movies
- [ ] Console shows no ERROR messages - All INFO/WARNING only

---

## 🔧 Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| "Module not found" | `pip install -r requirements.txt` |
| "Model file not found" | `python main.py train` |
| "Invalid genre" | Check supported genres (18 total) |
| "Permission denied" | `chmod +x main.py` |
| "Data file not found" | Create/copy `data/raw_movies.csv` |

---

## 📋 Supported Genres

Action, Adventure, Animation, Comedy, Crime, Documentary, Drama, Family, Fantasy, History, Horror, Music, Mystery, Romance, Science Fiction, Thriller, War, Western

---

## ⚡ Quick Commands

```bash
# One-liner test everything
python validate_project.py && python main.py train && python main.py predict --movie "Inception" --genre "Science Fiction"

# Time the training
time python main.py train

# Check what's been created
ls -la models/
ls -la data/*.csv

# View sample data
head data/raw_movies.csv

# Show all module functions
python -c "from src import train; help(train.train_pipeline)"
```

---

## 📚 Documentation Quick Links

- **Fast Start:** [QUICKSTART.md](QUICKSTART.md) - 5 min read
- **How to Run:** [RUN_AND_TEST_GUIDE.md](RUN_AND_TEST_GUIDE.md) - This!
- **Full Docs:** [README.md](README.md) - 30 min read
- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- **API Ref:** [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md) - Function details
- **Navigation:** [INDEX.md](INDEX.md) - Find anything

---

## ✨ Expected Results

### After Training
```
✓ CV R² Score > 0.6  (0.7 is good, >0.8 is excellent)
✓ Test RMSE < 15     (lower is better)
✓ Model file exists  (2-20 MB)
✓ Data files saved   (processed_movies.csv, train_data.csv, test_data.csv)
```

### After Prediction
```
✓ Recommended Movie ID returned (integer, 0-100 range)
✓ Confidence score returned     (0.0-1.0 range)
✓ No errors in console         (only INFO/WARNING messages)
```

---

## 🎯 Typical Session

```bash
# 1. Setup (5 min)
cd NextWatch-
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Verify (30 sec)
python validate_project.py

# 3. Train (5-10 sec)
python main.py train

# 4. Test (5 sec)
python main.py predict --movie "Inception" --genre "Science Fiction"
python main.py batch --file data/sample_predictions.csv

# Total: ~15-20 minutes for complete setup and testing
```

---

## 🆘 Quick Help

```bash
# Show available commands
python main.py --help

# Show train command options
python main.py train --help

# Show predict command options
python main.py predict --help

# Show batch command options
python main.py batch --help
```

---

## 📞 Common Questions

**Q: Is the model trained?**
A: Check: `ls -la models/movie_recommendation_model.pkl`

**Q: How good is the model?**
A: Check CV R² Score in training output. >0.7 is good, >0.8 is excellent.

**Q: Why is prediction low?**
A: Could need more training data or better features. Try `--model rf`.

**Q: Can I use my own data?**
A: Yes! File must have columns: `movie_title`, `release_year`, `rating`, `vote_count`, `revenue`, `budget`, `runtime`, `popularity`, `genre`, `next_movie_title`

**Q: How do I add new genres?**
A: Edit `src/config.py` → Add to `GENRE_MAPPING` → Retrain

**Q: Can I see the code?**
A: Check `src/` directory. Each file has detailed docstrings.

---

**Ready to start? Run:** `python validate_project.py` **then** `python main.py train`
