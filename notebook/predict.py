#!/usr/bin/env python3
"""
Simple script to test the revenue prediction model.
"""

import pandas as pd
import numpy as np
import pickle
from pathlib import Path

# Try importing joblib (preferred for sklearn models)
try:
    import joblib
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False
    print("Warning: joblib not available, will try pickle instead")

# Define paths
MODEL_PATH = Path(__file__).parent / "model" / "revenue_prediction_model.pkl"
DATA_PATH = Path(__file__).parent / "data" / "vcc_edge_for_prediction.xlsx"

# Tier 1 cities mapping
TIER_1_CITIES = {
    "Bengaluru", "Bangalore", "Mumbai", "Delhi", "New Delhi",
    "Hyderabad", "Chennai", "Pune", "Gurgaon", "Noida"
}

def map_city_tier(city):
    """Map city to tier classification."""
    if pd.isna(city):
        return "Unknown"
    return "Tier_1" if city in TIER_1_CITIES else "Tier_2_3"

def preprocess_data(df):
    """Preprocess the data to match model requirements."""
    # Create a copy to avoid modifying original
    df_processed = df.copy()
    
    # Map city to tier
    if "city" in df_processed.columns:
        df_processed["city_tier"] = df_processed["city"].apply(map_city_tier)
    
    # Calculate revenue_per_employee (if revenue column exists)
    if "revenue" in df_processed.columns and "employeeCount" in df_processed.columns:
        df_processed["revenue_per_employee"] = df_processed["revenue"] / df_processed["employeeCount"]
    
    # Calculate tenure_index
    if "companyAge" in df_processed.columns and "employeeCount" in df_processed.columns:
        df_processed["tenure_index"] = df_processed["companyAge"] / df_processed["employeeCount"]
    
    # Select required features
    required_features = [
        "employeeCount",
        "companyAge",
        "revenue_per_employee",
        "tenure_index",
        "companyType",
        "category",
        "city_tier",
        "state"
    ]
    
    # Check if all required features exist
    missing_features = [f for f in required_features if f not in df_processed.columns]
    if missing_features:
        raise ValueError(f"Missing required features: {missing_features}")
    
    return df_processed[required_features]

def predict_revenue(model_path, data_path=None, input_data=None):
    """
    Predict revenue using the trained model.
    
    Args:
        model_path: Path to the saved model pickle file
        data_path: Path to Excel file with data (optional)
        input_data: DataFrame with input data (optional)
    
    Returns:
        DataFrame with predictions
    
    Note:
        This function uses pickle.load() which can execute arbitrary code.
        Only load model files from trusted sources. For production use,
        consider additional security measures like file integrity verification.
    """
    # Verify model file exists
    model_path_obj = Path(model_path)
    if not model_path_obj.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    # Load model - try multiple methods for compatibility
    # Security Note: pickle.load()/joblib.load() can execute arbitrary code. 
    # Only use trusted model files. In production, consider file integrity checks.
    print(f"Loading model from {model_path}...")
    
    model = None
    errors = []
    
    # Try joblib first (preferred for sklearn models)
    if HAS_JOBLIB:
        try:
            model = joblib.load(model_path)
            print("Model loaded successfully using joblib!")
        except Exception as e:
            errors.append(f"joblib: {str(e)}")
            print(f"joblib loading failed: {e}")
    
    # Try pickle with different methods if joblib failed
    if model is None:
        try:
            with open(model_path, 'rb') as f:
                # Method 1: Standard pickle.load()
                try:
                    model = pickle.load(f)
                    print("Model loaded successfully using pickle!")
                except (pickle.UnpicklingError, ValueError, TypeError) as e:
                    errors.append(f"pickle (default): {str(e)}")
                    # Method 2: Try with latin1 encoding (Python 2/3 compatibility)
                    f.seek(0)
                    try:
                        model = pickle.load(f, encoding='latin1')
                        print("Model loaded successfully using pickle (latin1 encoding)!")
                    except Exception as e2:
                        errors.append(f"pickle (latin1): {str(e2)}")
                        # Method 3: Try with bytes encoding
                        f.seek(0)
                        try:
                            model = pickle.load(f, encoding='bytes')
                            print("Model loaded successfully using pickle (bytes encoding)!")
                        except Exception as e3:
                            errors.append(f"pickle (bytes): {str(e3)}")
                            # Method 4: Try with errors='ignore'
                            f.seek(0)
                            try:
                                model = pickle.load(f, encoding='latin1', errors='ignore')
                                print("Model loaded successfully using pickle (latin1, errors='ignore')!")
                            except Exception as e4:
                                errors.append(f"pickle (latin1, ignore errors): {str(e4)}")
                                raise
        except Exception as e:
            error_msg = (
                f"Failed to load model. Tried multiple methods:\n"
                + "\n".join(f"  - {err}" for err in errors)
                + f"\n\nLast error: {e}\n"
                + "This error often occurs due to Python version mismatch.\n"
                + "Tip: Try saving the model again with the same Python version you're using to load it."
            )
            raise RuntimeError(error_msg) from e
    
    if model is None:
        raise RuntimeError("Failed to load model with all available methods")
    
    # Load data
    if input_data is not None:
        df = input_data.copy()
    elif data_path is not None:
        print(f"Loading data from {data_path}...")
        df = pd.read_excel(data_path)
        print(f"Loaded {len(df)} records")
    else:
        raise ValueError("Either data_path or input_data must be provided")
    
    # Preprocess data
    print("Preprocessing data...")
    X = preprocess_data(df)
    
    # Make predictions (log scale)
    print("Making predictions...")
    predictions_log = model.predict(X)
    
    # Convert back to actual revenue
    predictions = np.expm1(predictions_log)
    
    # Create results dataframe
    results = df.copy()
    results["predicted_revenue"] = predictions
    
    return results

def main():
    """Main function to run predictions."""
    print("=" * 50)
    print("Revenue Prediction Model - Test Script")
    print("=" * 50)
    print()
    
    try:
        # Load and predict
        results = predict_revenue(MODEL_PATH, DATA_PATH)
        
        # Display results
        print("\n" + "=" * 50)
        print("Prediction Results")
        print("=" * 50)
        
        # Show summary statistics
        print(f"\nTotal predictions: {len(results)}")
        print(f"Mean predicted revenue: ${results['predicted_revenue'].mean():,.2f}")
        print(f"Median predicted revenue: ${results['predicted_revenue'].median():,.2f}")
        print(f"Min predicted revenue: ${results['predicted_revenue'].min():,.2f}")
        print(f"Max predicted revenue: ${results['predicted_revenue'].max():,.2f}")
        
        # Show first few predictions
        print("\n" + "-" * 50)
        print("First 10 Predictions:")
        print("-" * 50)
        
        display_cols = ["employeeCount", "companyAge", "companyType", "category", "city_tier", "state"]
        if "revenue" in results.columns:
            display_cols.append("revenue")
        display_cols.append("predicted_revenue")
        
        # Filter to only existing columns
        display_cols = [col for col in display_cols if col in results.columns]
        
        print(results[display_cols].head(10).to_string(index=False))
        
        # Save results
        output_path = Path(__file__).parent / "predictions_output.xlsx"
        results.to_excel(output_path, index=False)
        print(f"\n✓ Predictions saved to: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

