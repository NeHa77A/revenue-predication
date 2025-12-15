"""
FastAPI backend for Revenue Prediction Model
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from contextlib import asynccontextmanager
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import io

# Configuration
MAX_FILE_SIZE_MB = 50  # Maximum file size for bulk uploads (in MB)
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Model path - adjust based on where backend/main.py is located
MODEL_PATH = Path(__file__).parent / "model" / "revenue_prediction_model.pkl"
# Fallback: try current directory structure
if not MODEL_PATH.exists():
    MODEL_PATH = Path("model") / "revenue_prediction_model.pkl"

# Tier 1 cities mapping
TIER_1_CITIES = {
    "Bengaluru", "Bangalore", "Mumbai", "Delhi", "New Delhi",
    "Hyderabad", "Chennai", "Pune", "Gurgaon", "Noida"
}

# Model variable
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    global model
    try:
        print(f"Loading model from {MODEL_PATH}...")
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise RuntimeError(f"Failed to load model: {e}")
    
    yield
    
    # Shutdown (if needed, add cleanup code here)
    print("Shutting down...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Revenue Prediction API",
    description="API for predicting company revenue using XGBoost model",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware to allow frontend requests
# TODO: In production, replace ["*"] with specific frontend URLs:
# allow_origins=["http://localhost:3000", "https://your-production-domain.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only - restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def map_city_tier(city: Optional[str]) -> str:
    """Map city to tier classification."""
    if not city or pd.isna(city):
        return "Tier_2_3"
    return "Tier_1" if city in TIER_1_CITIES else "Tier_2_3"

def calculate_derived_features(employee_count: float, company_age: float, revenue: Optional[float] = None) -> tuple:
    """Calculate derived features: revenue_per_employee and tenure_index."""
    revenue_per_employee = revenue / employee_count if revenue is not None and employee_count > 0 else 1.0
    tenure_index = company_age / employee_count if employee_count > 0 else 0
    return revenue_per_employee, tenure_index

def preprocess_single_input(data: dict) -> pd.DataFrame:
    """Preprocess a single input for prediction."""
    # Extract values
    employee_count = float(data.get("employeeCount", 1))
    company_age = float(data.get("companyAge", 0))
    company_type = data.get("companyType", "Private Company")
    category = data.get("category", "")
    city = data.get("city", "")
    state = data.get("state", "")
    
    # Calculate derived features using shared function
    revenue = data.get("revenue")
    revenue_per_employee, tenure_index = calculate_derived_features(
        employee_count, company_age, float(revenue) if revenue is not None else None
    )
    
    city_tier = map_city_tier(city)
    
    # Create DataFrame
    df = pd.DataFrame([{
        "employeeCount": employee_count,
        "companyAge": company_age,
        "revenue_per_employee": revenue_per_employee,
        "tenure_index": tenure_index,
        "companyType": company_type,
        "category": category,
        "city_tier": city_tier,
        "state": state
    }])
    
    return df

def preprocess_bulk_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess bulk data for prediction."""
    df_processed = df.copy()
    
    # Normalize column names (case-insensitive, handle spaces)
    df_processed.columns = df_processed.columns.str.strip().str.lower().str.replace(' ', '')
    
    # Map city to tier
    if "city" in df_processed.columns:
        df_processed["city_tier"] = df_processed["city"].apply(map_city_tier)
    else:
        df_processed["city_tier"] = "Tier_2_3"
    
    # Calculate derived features using shared function
    if "employeecount" in df_processed.columns and "companyage" in df_processed.columns:
        # Calculate revenue_per_employee
        if "revenue" in df_processed.columns:
            df_processed["revenue_per_employee"] = df_processed["revenue"] / df_processed["employeecount"]
        else:
            df_processed["revenue_per_employee"] = 1.0
        
        # Calculate tenure_index
        df_processed["tenure_index"] = df_processed["companyage"] / df_processed["employeecount"]
    else:
        df_processed["revenue_per_employee"] = 1.0
        df_processed["tenure_index"] = 0
    
    # Map column names to expected format
    column_mapping = {
        "employeecount": "employeeCount",
        "companyage": "companyAge",
        "companytype": "companyType",
    }
    
    for old_name, new_name in column_mapping.items():
        if old_name in df_processed.columns:
            df_processed[new_name] = df_processed[old_name]
    
    # Ensure required columns exist
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
    
    # Fill missing columns with defaults
    if "companyType" not in df_processed.columns:
        df_processed["companyType"] = "Private Company"
    if "category" not in df_processed.columns:
        df_processed["category"] = ""
    if "state" not in df_processed.columns:
        df_processed["state"] = ""
    
    return df_processed[required_features]

# Pydantic models for request/response
class PredictionRequest(BaseModel):
    employeeCount: float = Field(..., gt=0, description="Number of employees")
    companyAge: float = Field(..., ge=0, description="Company age in years")
    companyType: str = Field(..., description="Company type (e.g., 'Private Company', 'Public Company')")
    category: Optional[str] = Field(None, description="Industry category")
    city: Optional[str] = Field(None, description="City name")
    state: str = Field(..., description="State name")
    revenue: Optional[float] = Field(None, ge=0, description="Current revenue (optional, for revenue_per_employee calculation)")

class PredictionResponse(BaseModel):
    predicted_revenue: float
    input_data: dict

class BulkPredictionResponse(BaseModel):
    predictions: List[dict]
    statistics: dict

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Revenue Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "/api/predict": "POST - Single prediction",
            "/api/predict/bulk": "POST - Bulk prediction from Excel file",
            "/health": "GET - Health check",
            "/docs": "GET - Interactive API documentation (Swagger UI)"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/api/predict", response_model=PredictionResponse)
async def predict_single(request: PredictionRequest):
    """Predict revenue for a single company"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Preprocess input
        input_df = preprocess_single_input(request.dict())
        
        # Make prediction (log scale)
        prediction_log = model.predict(input_df)[0]
        
        # Convert back to actual revenue
        predicted_revenue = float(np.expm1(prediction_log))
        
        return PredictionResponse(
            predicted_revenue=predicted_revenue,
            input_data=request.dict()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.post("/api/predict/bulk", response_model=BulkPredictionResponse)
async def predict_bulk(file: UploadFile = File(...)):
    """Predict revenue for multiple companies from Excel file"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File must be Excel format (.xlsx or .xls)")
    
    try:
        # Read Excel file with size validation
        contents = await file.read()
        
        # Validate file size
        if len(contents) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=400, 
                detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE_MB}MB"
            )
        df = pd.read_excel(io.BytesIO(contents))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Excel file is empty")
        
        # Preprocess data
        processed_df = preprocess_bulk_data(df)
        
        # Make predictions (log scale)
        predictions_log = model.predict(processed_df)
        
        # Convert back to actual revenue
        predictions = np.expm1(predictions_log)
        
        # Combine original data with predictions
        results = df.copy()
        results["predicted_revenue"] = predictions
        
        # Calculate statistics
        stats = {
            "count": len(predictions),
            "mean": float(np.mean(predictions)),
            "median": float(np.median(predictions)),
            "min": float(np.min(predictions)),
            "max": float(np.max(predictions)),
            "std": float(np.std(predictions))
        }
        
        # Convert to list of dicts for JSON response
        predictions_list = results.to_dict(orient='records')
        
        return BulkPredictionResponse(
            predictions=predictions_list,
            statistics=stats
        )
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Excel file is empty or corrupted")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

