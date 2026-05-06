#!/usr/bin/env python3
"""
Validation script to verify the NextWatch project structure and setup.

Run this script to ensure all files and dependencies are properly installed.
"""

import sys
from pathlib import Path
import importlib.util

def check_directory(path, name):
    """Check if a directory exists."""
    if path.exists() and path.is_dir():
        print(f"✓ {name:40s} ({path})")
        return True
    else:
        print(f"✗ {name:40s} (MISSING)")
        return False

def check_file(path, name):
    """Check if a file exists."""
    if path.exists() and path.is_file():
        print(f"✓ {name:40s} ({path})")
        return True
    else:
        print(f"✗ {name:40s} (MISSING)")
        return False

def check_import(module_name):
    """Check if a Python module can be imported."""
    spec = importlib.util.find_spec(module_name)
    if spec is not None:
        print(f"✓ {module_name:40s}")
        return True
    else:
        print(f"✗ {module_name:40s} (NOT INSTALLED)")
        return False

def main():
    """Run all validation checks."""
    print("=" * 70)
    print("NextWatch ML Project - Validation Report")
    print("=" * 70)
    
    project_root = Path(__file__).parent
    all_checks_passed = True
    
    # Check directory structure
    print("\n[1] Checking Directory Structure")
    print("-" * 70)
    
    checks = [
        (project_root / "src", "src/ directory"),
        (project_root / "data", "data/ directory"),
        (project_root / "models", "models/ directory"),
    ]
    
    for path, name in checks:
        if not check_directory(path, name):
            all_checks_passed = False
    
    # Check required files
    print("\n[2] Checking Required Files")
    print("-" * 70)
    
    file_checks = [
        (project_root / "src" / "config.py", "src/config.py"),
        (project_root / "src" / "data_preprocessing.py", "src/data_preprocessing.py"),
        (project_root / "src" / "feature_engineering.py", "src/feature_engineering.py"),
        (project_root / "src" / "train.py", "src/train.py"),
        (project_root / "src" / "evaluate.py", "src/evaluate.py"),
        (project_root / "src" / "predict.py", "src/predict.py"),
        (project_root / "src" / "__init__.py", "src/__init__.py"),
        (project_root / "main.py", "main.py"),
        (project_root / "requirements.txt", "requirements.txt"),
        (project_root / "README.md", "README.md"),
        (project_root / "QUICKSTART.md", "QUICKSTART.md"),
    ]
    
    for path, name in file_checks:
        if not check_file(path, name):
            all_checks_passed = False
    
    # Check sample data
    print("\n[3] Checking Sample Data")
    print("-" * 70)
    
    data_checks = [
        (project_root / "data" / "raw_movies.csv", "data/raw_movies.csv (sample)"),
        (project_root / "data" / "sample_predictions.csv", "data/sample_predictions.csv"),
    ]
    
    for path, name in data_checks:
        if not check_file(path, name):
            all_checks_passed = False
    
    # Check Python dependencies
    print("\n[4] Checking Python Dependencies")
    print("-" * 70)
    
    dependencies = [
        "pandas",
        "numpy",
        "sklearn",
        "sklearn.preprocessing",
        "sklearn.neighbors",
        "sklearn.ensemble",
        "sklearn.model_selection",
        "sklearn.metrics",
    ]
    
    for dep in dependencies:
        if not check_import(dep):
            all_checks_passed = False
    
    # Test imports from src modules
    print("\n[5] Testing Module Imports")
    print("-" * 70)
    
    sys.path.insert(0, str(project_root / "src"))
    
    modules = [
        "config",
        "data_preprocessing",
        "feature_engineering",
        "train",
        "evaluate",
        "predict",
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {f'src/{module}.py':40s}")
        except Exception as e:
            print(f"✗ {f'src/{module}.py':40s} (ERROR: {str(e)[:30]}...)")
            all_checks_passed = False
    
    # Summary
    print("\n" + "=" * 70)
    if all_checks_passed:
        print("✓ ALL CHECKS PASSED - Project is ready to use!")
        print("=" * 70)
        print("\nNext steps:")
        print("  1. See QUICKSTART.md for a quick 5-minute setup")
        print("  2. Run: python main.py train")
        print("  3. Run: python main.py predict --movie 'Inception' --genre 'Science Fiction'")
        print("  4. See README.md for detailed documentation")
        return 0
    else:
        print("✗ SOME CHECKS FAILED - Please verify your setup")
        print("=" * 70)
        print("\nCommon issues:")
        print("  - Missing directories: Create data/ and models/ directories")
        print("  - Missing files: Check that all src/ modules are present")
        print("  - Missing dependencies: Run 'pip install -r requirements.txt'")
        return 1

if __name__ == "__main__":
    sys.exit(main())
