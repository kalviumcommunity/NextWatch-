"""
Main entry point for the NextWatch movie recommendation system.

Orchestrates the complete ML pipeline: data preprocessing, feature engineering,
model training, evaluation, and prediction.
"""

import sys
import logging
import argparse
from pathlib import Path
from typing import Optional

# Add src directory to path for imports
SRC_DIR = Path(__file__).parent / "src"
sys.path.insert(0, str(SRC_DIR))

import config
from src.data_preprocessing import preprocess_data
from src.feature_engineering import engineer_features, load_artifacts
from src.train import train_pipeline, load_model
from src.evaluate import evaluate_pipeline
from src.predict import predict_for_user, batch_predict, format_prediction_output

# Configure logging
logging.basicConfig(
    format=config.LOG_FORMAT,
    level=config.LOG_LEVEL
)
logger = logging.getLogger(__name__)


def train_full_pipeline(
    raw_data_path: Optional[Path] = None,
    model_type: str = "knn"
) -> dict:
    """
    Execute the complete training pipeline.
    
    Args:
        raw_data_path: Path to raw data CSV. If None, uses default path.
        model_type: Type of model to train ("knn", "rf").
        
    Returns:
        Dictionary with training results.
    """
    logger.info("=" * 60)
    logger.info("STARTING FULL TRAINING PIPELINE")
    logger.info("=" * 60)
    
    if raw_data_path is None:
        raw_data_path = config.RAW_DATA_PATH
    
    try:
        # Step 1: Data Preprocessing
        logger.info("\n[STEP 1/4] Data Preprocessing")
        logger.info("-" * 60)
        processed_df = preprocess_data(input_path=raw_data_path)
        logger.info(f"✓ Preprocessing complete. Shape: {processed_df.shape}\n")
        
        # Step 2: Feature Engineering
        logger.info("[STEP 2/4] Feature Engineering")
        logger.info("-" * 60)
        engineered_df, artifacts = engineer_features(
            processed_df,
            fit_scaler=True
        )
        logger.info(f"✓ Feature engineering complete. Shape: {engineered_df.shape}\n")
        
        # Step 3: Model Training
        logger.info("[STEP 3/4] Model Training")
        logger.info("-" * 60)
        model, training_info = train_pipeline(engineered_df, model_type=model_type)
        logger.info(f"✓ Training complete.\n")
        logger.info(f"  Train size: {training_info['train_size']}")
        logger.info(f"  Test size: {training_info['test_size']}")
        logger.info(f"  CV R² Score: {training_info['cv_metrics']['cv_mean']:.4f}\n")
        
        # Step 4: Model Evaluation
        logger.info("[STEP 4/4] Model Evaluation")
        logger.info("-" * 60)
        evaluation_results = evaluate_pipeline(model, config.TEST_DATA_PATH)
        logger.info(f"✓ Evaluation complete.\n")
        
        logger.info("=" * 60)
        logger.info("TRAINING PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        
        return {
            "status": "success",
            "model": model,
            "training_info": training_info,
            "evaluation_results": evaluation_results,
            "artifacts": artifacts,
        }
        
    except Exception as e:
        logger.error(f"Error in training pipeline: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": str(e),
        }


def predict_pipeline(
    movie_title: str,
    genre: str,
    model_path: Optional[Path] = None
) -> dict:
    """
    Execute prediction pipeline for a single user input.
    
    Args:
        movie_title: Title of previously watched movie.
        genre: Genre of the movie.
        model_path: Path to saved model. If None, uses default.
        
    Returns:
        Dictionary with prediction result.
    """
    logger.info("=" * 60)
    logger.info("STARTING PREDICTION PIPELINE")
    logger.info("=" * 60)
    
    if model_path is None:
        model_path = config.MODEL_PATH
    
    try:
        # Load model
        logger.info("Loading trained model...")
        model = load_model(model_path)
        
        # Get feature columns from training data
        import pandas as pd
        train_df = pd.read_csv(config.TRAIN_DATA_PATH)
        feature_columns = [c for c in train_df.columns if c != config.TARGET_COLUMN]
        
        # Make prediction
        logger.info(f"\nMaking prediction for:")
        logger.info(f"  Movie: {movie_title}")
        logger.info(f"  Genre: {genre}")
        
        result = predict_for_user(
            model,
            movie_title,
            genre,
            feature_columns=feature_columns
        )
        
        # Format output
        output = format_prediction_output(result)
        
        logger.info(f"\nPrediction Result:")
        logger.info(f"  Recommended Movie ID: {output['recommendation']['movie_id']}")
        logger.info(f"  Confidence: {output['recommendation']['confidence']}")
        
        logger.info("=" * 60)
        logger.info("PREDICTION COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        
        return {
            "status": "success",
            "result": output,
        }
        
    except Exception as e:
        logger.error(f"Error in prediction pipeline: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error_message": str(e),
        }


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="NextWatch Movie Recommendation System"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Train command
    train_parser = subparsers.add_parser("train", help="Train the model")
    train_parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="Path to raw data CSV file"
    )
    train_parser.add_argument(
        "--model",
        type=str,
        choices=["knn", "rf"],
        default="knn",
        help="Model type to train"
    )
    
    # Predict command
    predict_parser = subparsers.add_parser("predict", help="Make a prediction")
    predict_parser.add_argument(
        "--movie",
        type=str,
        required=True,
        help="Title of previously watched movie"
    )
    predict_parser.add_argument(
        "--genre",
        type=str,
        required=True,
        help="Genre of the movie"
    )
    predict_parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Path to trained model"
    )
    
    # Batch predict command
    batch_parser = subparsers.add_parser("batch", help="Make batch predictions")
    batch_parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="CSV file with columns: movie_title, genre"
    )
    batch_parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Path to trained model"
    )
    
    args = parser.parse_args()
    
    if args.command == "train":
        result = train_full_pipeline(
            raw_data_path=Path(args.data) if args.data else None,
            model_type=args.model
        )
        return 0 if result["status"] == "success" else 1
    
    elif args.command == "predict":
        result = predict_pipeline(
            movie_title=args.movie,
            genre=args.genre,
            model_path=Path(args.model) if args.model else None
        )
        if result["status"] == "success":
            print("\n" + "=" * 60)
            print("PREDICTION RESULT:")
            print("=" * 60)
            print(result["result"]["message"])
            print(f"Recommended Movie ID: {result['result']['recommendation']['movie_id']}")
            print(f"Confidence: {result['result']['recommendation']['confidence']}")
            return 0
        else:
            print(f"Error: {result['error_message']}")
            return 1
    
    elif args.command == "batch":
        import pandas as pd
        model_path = Path(args.model) if args.model else config.MODEL_PATH
        model = load_model(model_path)
        
        # Load input data
        input_df = pd.read_csv(args.file)
        input_data = input_df.to_dict("records")
        
        # Get feature columns
        train_df = pd.read_csv(config.TRAIN_DATA_PATH)
        feature_columns = [c for c in train_df.columns if c != config.TARGET_COLUMN]
        
        # Make predictions
        results = batch_predict(model, input_data, feature_columns)
        
        # Print results
        print("\n" + "=" * 60)
        print(f"BATCH PREDICTION RESULTS ({len(results)} items)")
        print("=" * 60)
        for i, result in enumerate(results, 1):
            print(f"\n[{i}] {result.input_movie} ({result.input_genre})")
            print(f"    → Recommended Movie ID: {int(result.predicted_movie_id)}")
            print(f"    → Confidence: {result.confidence:.4f}")
        
        return 0
    
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
