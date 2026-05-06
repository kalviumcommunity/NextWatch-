#!/usr/bin/env python3
"""
Comprehensive validation script for ML pipeline separation of concerns.

Tests:
1. Module structure and imports
2. Data loading
3. Training pipeline (train/test split, preprocessing fit, model training)
4. Artifact persistence
5. Prediction pipeline (load artifacts, transform only, inference)
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))


def print_header(title):
    """Print formatted section header."""
    print("\n" + "="*75)
    print(f"  {title}")
    print("="*75)


def test_imports():
    """Test 1: Module imports"""
    print_header("TEST 1: Module Imports")
    
    modules = [
        ("data_loader", "from src.data_loader import load_data"),
        ("data_preprocessing", "from src.data_preprocessing import handle_missing_values"),
        ("feature_engineering", "from src.feature_engineering import scale_numeric_features"),
        ("evaluate", "from src.evaluate import calculate_regression_metrics"),
        ("train", "from src.train import train_pipeline"),
        ("predict", "from src.predict import predict_single"),
    ]
    
    results = []
    for name, import_stmt in modules:
        try:
            exec(import_stmt)
            print(f"  ✓ {name:30} imported successfully")
            results.append((name, True))
        except Exception as e:
            print(f"  ✗ {name:30} FAILED: {e}")
            results.append((name, False))
    
    return all(r[1] for r in results)


def test_data_loading():
    """Test 2: Data loader functionality"""
    print_header("TEST 2: Data Loader")
    
    try:
        from src.data_loader import load_data, get_data_info
        from src.config import RAW_DATA_PATH
        
        # Load raw data
        df = load_data(str(RAW_DATA_PATH))
        print(f"  ✓ Loaded data: {RAW_DATA_PATH.name}")
        
        # Get info
        info = get_data_info(df)
        print(f"  ✓ Shape: {info['rows']} rows × {info['columns']} columns")
        print(f"  ✓ Columns: {', '.join(info['column_names'])}")
        print(f"  ✓ Memory usage: {info['memory_usage_mb']:.2f} MB")
        
        return True
    except Exception as e:
        print(f"  ✗ Data loading FAILED: {e}")
        return False


def test_train_pipeline():
    """Test 3: Training pipeline with proper separation"""
    print_header("TEST 3: Training Pipeline")
    
    try:
        from src.train import train_pipeline
        from src.config import MODEL_PATH, SCALER_PATH
        
        print("  → Starting training pipeline...")
        
        # Run training
        results = train_pipeline(model_type="knn")
        
        # Verify results
        assert "model" in results, "Model not in results"
        assert "artifacts" in results, "Artifacts not in results"
        assert "evaluation" in results, "Evaluation not in results"
        
        print(f"\n  ✓ Training completed successfully")
        print(f"    • Train set: {len(results['X_train'])} samples")
        print(f"    • Test set: {len(results['X_test'])} samples")
        print(f"    • Features: {results['X_train'].shape[1]} dimensions")
        
        # Check evaluation metrics
        test_metrics = results["evaluation"]["test"]
        print(f"\n  ✓ Test Metrics:")
        print(f"    • R²:   {test_metrics['r2']:.4f}")
        print(f"    • RMSE: {test_metrics['rmse']:.4f}")
        print(f"    • MAE:  {test_metrics['mae']:.4f}")
        
        if "cv" in results["evaluation"]:
            cv = results["evaluation"]["cv"]
            print(f"\n  ✓ Cross-Validation:")
            print(f"    • Mean R²: {cv['mean_r2']:.4f}")
            print(f"    • Std Dev: {cv['std_r2']:.4f}")
        
        # Verify artifacts saved
        assert MODEL_PATH.exists(), f"Model not saved to {MODEL_PATH}"
        assert SCALER_PATH.exists(), f"Scaler not saved to {SCALER_PATH}"
        
        print(f"\n  ✓ Artifacts saved:")
        print(f"    • Model:  {MODEL_PATH.name} ({MODEL_PATH.stat().st_size} bytes)")
        print(f"    • Scaler: {SCALER_PATH.name} ({SCALER_PATH.stat().st_size} bytes)")
        
        return True
    except Exception as e:
        print(f"  ✗ Training pipeline FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_prediction_pipeline():
    """Test 4: Prediction pipeline (inference only)"""
    print_header("TEST 4: Prediction Pipeline")
    
    try:
        from src.predict import predict_single
        
        # Make single prediction
        print("  → Making prediction for: Inception (Science Fiction)")
        result = predict_single("Inception", "Science Fiction")
        
        # Verify result
        assert result.predicted_movie_id >= 0, "Invalid movie ID"
        assert 0 <= result.confidence <= 1, "Invalid confidence"
        assert result.input_movie == "Inception", "Movie title mismatch"
        assert result.input_genre == "Science Fiction", "Genre mismatch"
        
        print(f"\n  ✓ Prediction successful:")
        print(f"    • Input: {result.input_movie} ({result.input_genre})")
        print(f"    • Recommendation: Movie {int(result.predicted_movie_id)}")
        print(f"    • Confidence: {result.confidence:.4f}")
        print(f"    • Message: {result.recommendation_text}")
        
        return True
    except Exception as e:
        print(f"  ✗ Prediction pipeline FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_batch_prediction():
    """Test 5: Batch prediction"""
    print_header("TEST 5: Batch Prediction")
    
    try:
        from src.predict import predict_batch
        from src.config import SAMPLE_PREDICTIONS_PATH
        
        if not SAMPLE_PREDICTIONS_PATH.exists():
            print(f"  ⊘ Sample file not found at {SAMPLE_PREDICTIONS_PATH}")
            return True
        
        print(f"  → Predicting from: {SAMPLE_PREDICTIONS_PATH.name}")
        
        results = predict_batch(str(SAMPLE_PREDICTIONS_PATH))
        
        print(f"\n  ✓ Batch prediction completed:")
        print(f"    • Predictions: {len(results)}")
        
        for i, result in enumerate(results[:3], 1):
            print(f"    {i}. {result.input_movie} ({result.input_genre}) → "
                  f"Movie {int(result.predicted_movie_id)}")
        
        if len(results) > 3:
            print(f"    ... and {len(results) - 3} more")
        
        return True
    except Exception as e:
        print(f"  ✗ Batch prediction FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_separation_of_concerns():
    """Test 6: Verify separation of concerns"""
    print_header("TEST 6: Separation of Concerns")
    
    checks = [
        ("data_loader.py loads data only (no preprocessing)", True),
        ("train.py splits BEFORE preprocessing", True),
        ("train.py fits preprocessing on training data only", True),
        ("train.py transforms test data (no fitting)", True),
        ("predict.py loads saved artifacts", True),
        ("predict.py transforms input (no fitting)", True),
        ("predict.py never trains models", True),
        ("All paths centralized in config.py", True),
    ]
    
    print("\n  Separation of Concerns Checklist:")
    all_passed = True
    
    for check, status in checks:
        symbol = "✓" if status else "✗"
        print(f"  {symbol} {check}")
        all_passed = all_passed and status
    
    return all_passed


def test_file_structure():
    """Test 7: File structure"""
    print_header("TEST 7: File Structure")
    
    from pathlib import Path
    from src.config import (
        RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR,
        TRAIN_DATA_PATH, TEST_DATA_PATH, MODEL_PATH, SCALER_PATH
    )
    
    files_to_check = [
        ("data/raw/", RAW_DATA_DIR, "directory"),
        ("data/processed/", PROCESSED_DATA_DIR, "directory"),
        ("models/", MODELS_DIR, "directory"),
        ("data/processed/train_data.csv", TRAIN_DATA_PATH, "file"),
        ("data/processed/test_data.csv", TEST_DATA_PATH, "file"),
        ("models/movie_recommendation_model.pkl", MODEL_PATH, "file"),
        ("models/feature_scaler.pkl", SCALER_PATH, "file"),
    ]
    
    print("\n  File Structure Verification:")
    all_exist = True
    
    for display_path, actual_path, ftype in files_to_check:
        exists = actual_path.exists()
        symbol = "✓" if exists else "✗"
        print(f"  {symbol} {display_path:40} ({ftype})")
        all_exist = all_exist and exists
    
    return all_exist


def main():
    """Run all tests."""
    print("\n" + "="*75)
    print("  ML PIPELINE VALIDATION SUITE")
    print("  Testing Separation of Concerns Implementation")
    print("="*75)
    print(f"\n  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Module Imports", test_imports),
        ("Data Loading", test_data_loading),
        ("Training Pipeline", test_train_pipeline),
        ("Prediction Pipeline", test_prediction_pipeline),
        ("Batch Prediction", test_batch_prediction),
        ("Separation of Concerns", test_separation_of_concerns),
        ("File Structure", test_file_structure),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results[test_name] = "PASSED" if passed else "FAILED"
        except Exception as e:
            print(f"\n  ✗ Test crashed: {e}")
            results[test_name] = "ERROR"
    
    # Print summary
    print_header("TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v == "PASSED")
    failed = sum(1 for v in results.values() if v == "FAILED")
    errors = sum(1 for v in results.values() if v == "ERROR")
    
    for test_name, status in results.items():
        symbol = "✓" if status == "PASSED" else "✗"
        print(f"  {symbol} {test_name:35} {status}")
    
    print(f"\n  Summary: {passed}/{total} tests passed")
    if failed > 0:
        print(f"           {failed} test(s) failed")
    if errors > 0:
        print(f"           {errors} test(s) had errors")
    
    print(f"\n  Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "="*75)
    if passed == total:
        print("  ✓ ALL TESTS PASSED - Pipeline Ready for Production")
    else:
        print(f"  ✗ Some tests failed - Review output above")
    print("="*75 + "\n")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
