# Quick Setup Guide

## 🚀 Getting Started

This guide will help you set up and run the Revenue Prediction Application.

## Prerequisites

- **Python 3.10+** (Python 3.13 recommended)
- **Node.js 16+** and npm
- **Git** (optional, for version control)

## Step-by-Step Setup

### 1. Extract the Zip File

```bash
unzip revenue-prediction-app.zip
cd revenue-prediction-app
```

### 2. Verify Your Setup

Run the setup verification script to check if everything is ready:

```bash
python3 check_setup.py
```

This will check:
- ✅ Python version
- ✅ Project structure
- ✅ Required files
- ✅ Dependencies

### 3. Set Up Python Backend

#### 3.1 Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### 3.2 Install Python Dependencies

```bash
pip install -e .
```

Or if using `uv`:
```bash
uv pip install -e .
```

This will install:
- FastAPI
- Uvicorn
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Joblib
- And other required packages

### 4. Set Up Frontend

#### 4.1 Navigate to Frontend Directory

```bash
cd frontend
```

#### 4.2 Install Node Dependencies

```bash
npm install
```

This will install:
- React
- Vite
- Tailwind CSS
- Recharts
- Lucide React
- And other required packages

### 5. Run the Application

#### 5.1 Start the Backend Server

Open a terminal and run:

```bash
# Make sure you're in the project root and venv is activated
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

#### 5.2 Start the Frontend Server

Open another terminal and run:

```bash
cd frontend
npm run dev
```

The frontend will be available at: `http://localhost:3000`

## ✅ Verification

After setup, run the verification script again:

```bash
python3 check_setup.py
```

All checks should pass! ✓

## 🎯 Using the Application

1. **Single Prediction**: 
   - Go to "Predict Revenue" tab
   - Fill in company details
   - Click "Predict Revenue"
   - View the predicted revenue

2. **Bulk Prediction**:
   - Go to "Bulk Analysis" tab
   - Upload an Excel file (.xlsx)
   - View results and download predictions

3. **Analytics**:
   - Go to "Analytics" tab
   - View data visualizations

## 📁 Project Structure

```
revenue-prediction-app/
├── main.py                 # FastAPI backend
├── check_setup.py         # Setup verification script
├── pyproject.toml         # Python dependencies
├── README.md              # Full documentation
├── SETUP_GUIDE.md         # This file
├── frontend/              # React frontend
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   └── ...
│   └── package.json       # Node dependencies
├── model/                 # Trained model
│   └── revenue_prediction_model.pkl
├── data/                  # Data files
│   └── vcc_edge_for_prediction.xlsx
└── notebook/              # Training notebook
    └── final_xgboost.ipynb
```

## 🐛 Troubleshooting

### Issue: Python packages not installing

**Solution:**
```bash
# Make sure venv is activated
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Upgrade pip first
pip install --upgrade pip

# Then install dependencies
pip install -e .
```

### Issue: Node modules not installing

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue: Model file not found

**Solution:**
- The model file should be in `model/revenue_prediction_model.pkl`
- If missing, check the zip file extraction
- The model is required for predictions

### Issue: Port already in use

**Solution:**
- Backend: Change port in `main.py` or use `--port` flag
- Frontend: Change port in `frontend/vite.config.js`

### Issue: CORS errors

**Solution:**
- Make sure backend is running on port 8000
- Check `frontend/src/App.jsx` - API_BASE_URL should be `http://localhost:8000`
- For production, update CORS settings in `main.py`

## 📞 Support

If you encounter any issues:

1. Run `python3 check_setup.py` to diagnose problems
2. Check the README.md for detailed documentation
3. Verify all prerequisites are installed
4. Check that ports 8000 and 3000 are available

## 🎉 You're All Set!

Once everything is set up:
- Backend API: http://localhost:8000
- Frontend UI: http://localhost:3000
- API Docs: http://localhost:8000/docs

Happy predicting! 🚀

