# Virtual Environment Quick Start

## ⚡ Activate Environment (Run First)

```bash
cd NextWatch-
source venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
cd NextWatch-
venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
cd NextWatch-
venv\Scripts\activate.bat
```

**Success indicator:** You'll see `(venv)` at the start of your prompt

---

## 🚀 Quick Commands (While Activated)

```bash
# Validate everything is working
python validate_project.py

# Train the ML model
python main.py train

# Make a prediction
python main.py predict --movie "Inception" --genre "Science Fiction"

# Batch predictions
python main.py batch --file data/sample_predictions.csv
```

---

## 📦 What's Installed

```
pandas==3.0.2          numpy==2.4.4           scikit-learn==1.8.0
matplotlib==3.10.9     seaborn==0.13.2        joblib==1.5.3
scipy==1.17.1          + 12 supporting packages
```

All versions are pinned for reproducibility.

---

## 🔄 Deactivate Environment (When Done)

```bash
deactivate
```

The `(venv)` prefix disappears from your prompt.

---

## 📖 Documentation

- **Quick Start:** This file
- **Full Setup:** [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)
- **Completion Summary:** [SETUP_COMPLETION_SUMMARY.md](SETUP_COMPLETION_SUMMARY.md)
- **Main Guide:** [README.md](README.md) (see "Environment Setup" section)
- **All Docs:** [INDEX.md](INDEX.md)

---

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| `(venv)` not in prompt | Run activation command for your OS |
| `ModuleNotFoundError` | Activate venv: `source venv/bin/activate` |
| `permission denied` | Try: `chmod +x venv/bin/activate` |
| Windows PowerShell error | Try Command Prompt instead |

---

## ✅ Environment Status

- **Python:** 3.14.4
- **Virtual Environment:** 447 MB at `./venv/`
- **Packages:** 19 (all with pinned versions)
- **Ready:** ✓ Yes, fully functional

---

**Ready to go! Activate and start using the ML project.**

<- WidgetCustomizer: fix embed URL /widget-custom.js → Minor documentation update -->
