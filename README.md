# Revenue Prediction Application

A modern, full-stack web application for predicting company revenue using an XGBoost machine learning model. Built with FastAPI backend and React frontend, featuring a beautiful, responsive UI with dark mode support.

## 🚀 Features

- **Single Company Prediction**: Predict revenue for individual companies with detailed input forms
- **Bulk Prediction**: Upload Excel files (.xlsx) to predict revenue for multiple companies at once
- **Analytics Dashboard**: Interactive data visualizations including scatter plots, pie charts, and bar charts
- **Modern UI**: Beautiful, responsive design with dark mode support
- **Real-time Validation**: Form validation with helpful error messages
- **Prediction History**: Track recent predictions for quick reference
- **Export Functionality**: Download bulk predictions as Excel files
- **RESTful API**: Well-documented FastAPI backend with automatic Swagger documentation

## 📋 Prerequisites

- **Python 3.10+** (Python 3.13 recommended)
- **Node.js 16+** and npm
- **Virtual environment** (venv or similar)

## 📁 Project Structure

```
revenue-prediction-app/
├── main.py                      # FastAPI backend server
├── pyproject.toml              # Python dependencies
├── check_setup.py              # Setup verification script
├── check_setup.sh              # Setup verification shell script
├── create_zip.py               # Utility to create distribution zip
├── create_zip.sh               # Shell script for zip creation
├── README.md                   # This file
├── SETUP_GUIDE.md              # Detailed setup instructions
│
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── main.jsx           # React entry point
│   │   └── index.css          # Global styles
│   ├── package.json           # Node.js dependencies
│   ├── vite.config.js         # Vite configuration
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   └── postcss.config.js      # PostCSS configuration
│
├── model/                      # Trained ML model
│   └── revenue_prediction_model.pkl
│
├── data/                       # Data files
│   └── vcc_edge_for_prediction.xlsx
│
└── notebook/                   # Jupyter notebooks
    ├── final_xgboost.ipynb    # Model training notebook
    └── predict.py             # Prediction utilities
```

## 🛠️ Setup Instructions

### 1. Clone or Extract the Project

```bash
cd revenue-prediction-app
```

### 2. Verify Your Setup

Run the setup verification script:

```bash
python3 check_setup.py
```

This checks:
- ✅ Python version
- ✅ Project structure
- ✅ Required files
- ✅ Dependencies

### 3. Backend Setup

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
pip install --upgrade pip
pip install -e .
```

Or if using `uv`:
```bash
uv pip install -e .
```

This installs:
- FastAPI
- Uvicorn
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Joblib
- OpenPyXL
- And other required packages

#### 3.3 Start the Backend Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Server**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

### 4. Frontend Setup

#### 4.1 Navigate to Frontend Directory

```bash
cd frontend
```

#### 4.2 Install Node Dependencies

```bash
npm install
```

Or using yarn:
```bash
yarn install
```

This installs:
- React 18
- Vite
- Tailwind CSS
- Recharts (for data visualization)
- Lucide React (icons)
- And other required packages

#### 4.3 Start the Frontend Development Server

```bash
npm run dev
```

Or:
```bash
yarn dev
```

The frontend will be available at: `http://localhost:3000`

## 🎯 Usage

### Single Prediction

1. Navigate to the "Predict Revenue" tab
2. Fill in the company details:
   - **Employee Count**: Total number of full-time employees (required)
   - **Company Age**: Years since incorporation (required)
   - **Company Type**: Private Company, Public Company, Partnership, or LLP (required)
   - **Industry Category**: Optional category selection
   - **City**: City name (optional, affects tier classification)
   - **State**: State name (required)
3. Click "Predict Revenue"
4. View the predicted revenue and related metrics
5. Check the "Recent Predictions" sidebar for history

### Bulk Prediction

1. Navigate to the "Bulk Analysis" tab
2. Drag and drop an Excel file (.xlsx) or click "Browse Files"
3. The file should contain columns:
   - `EmployeeCount` or `Employee Count`
   - `CompanyAge` or `Company Age`
   - `CompanyType` or `Company Type` (optional)
   - `Category` (optional)
   - `City` (optional)
   - `State` (optional)
4. Wait for processing to complete
5. View summary statistics and prediction preview
6. Click "Export Excel" to download results

### Analytics Dashboard

1. Navigate to the "Analytics" tab
2. View interactive visualizations:
   - Revenue vs Employee Count scatter plot
   - Distribution by Company Type pie chart
   - Average Revenue by City Tier bar chart

## 📡 API Endpoints

### Root
- **GET** `/`
  - Returns API information and available endpoints

### Health Check
- **GET** `/health`
  - **Response:**
    ```json
    {
      "status": "healthy",
      "model_loaded": true
    }
    ```

### Single Prediction
- **POST** `/api/predict`
  - **Request Body:**
    ```json
    {
      "employeeCount": 250,
      "companyAge": 12,
      "companyType": "Private Company",
      "category": "Managed Services",
      "city": "Bengaluru",
      "state": "Karnataka",
      "revenue": 5000000
    }
    ```
  - **Response:**
    ```json
    {
      "predicted_revenue": 3187700.50,
      "input_data": {
        "employeeCount": 250,
        "companyAge": 12,
        "companyType": "Private Company",
        "category": "Managed Services",
        "city": "Bengaluru",
        "state": "Karnataka"
      }
    }
    ```

### Bulk Prediction
- **POST** `/api/predict/bulk`
  - **Content-Type**: `multipart/form-data`
  - **Body**: Excel file (.xlsx or .xls)
  - **Response:**
    ```json
    {
      "predictions": [
        {
          "EmployeeCount": 250,
          "CompanyAge": 12,
          "predicted_revenue": 3187700.50
        }
      ],
      "statistics": {
        "count": 100,
        "mean": 1392000.00,
        "median": 221000.00,
        "min": -40000.00,
        "max": 76720000.00,
        "std": 5234000.00
      }
    }
    ```

## 🤖 Model Details

### Model Type
- **Algorithm**: XGBoost Regressor
- **Target**: Annual Revenue (log-transformed)

### Features Used
1. **Employee Count**: Total number of employees
2. **Company Age**: Years since incorporation
3. **Revenue per Employee**: Calculated as `revenue / employeeCount` (defaults to 1.0 if revenue not provided)
4. **Tenure Index**: Calculated as `companyAge / employeeCount`
5. **Company Type**: Categorical (Private Company, Public Company, Partnership, LLP)
6. **Category**: Industry category (optional)
7. **City Tier**: Automatically mapped from city name
   - **Tier 1 Cities**: Bengaluru, Bangalore, Mumbai, Delhi, New Delhi, Hyderabad, Chennai, Pune, Gurgaon, Noida
   - **Tier 2/3 Cities**: All other cities
8. **State**: State name

### Preprocessing
- City names are automatically mapped to tier classification
- Revenue per employee is calculated from input data
- Tenure index is calculated as company age divided by employee count
- Model predictions are in log scale and converted back using `expm1` transformation

## 🎨 Frontend Features

### UI Components
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark Mode**: Toggle between light and dark themes
- **Collapsible Sidebar**: Expandable navigation sidebar
- **Toast Notifications**: Success and error notifications
- **Loading States**: Visual feedback during API calls
- **Form Validation**: Real-time input validation

### Technologies
- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Charting library for data visualization
- **Lucide React**: Beautiful icon library

## 🔧 Development

### Backend Development
- FastAPI with automatic API documentation
- Hot reload enabled with `--reload` flag
- Type hints and Pydantic models for validation
- CORS middleware configured for development

### Frontend Development
- React with Vite for fast HMR (Hot Module Replacement)
- Tailwind CSS for styling
- Recharts for data visualization
- Component-based architecture

### Running in Development Mode

**Terminal 1 - Backend:**
```bash
source .venv/bin/activate  # Activate venv
python main.py
# Or: uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 🚢 Production Deployment

### Build Frontend

```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

### Serve Backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Production Considerations

1. **CORS Configuration**: Update `allow_origins` in `main.py` to restrict access:
   ```python
   allow_origins=["https://your-production-domain.com"]
   ```

2. **Environment Variables**: Use environment variables for:
   - API keys
   - Database connections
   - Model paths
   - Port configurations

3. **Static Files**: Serve frontend build files through a web server (Nginx, Apache) or CDN

4. **Security**: 
   - Enable HTTPS
   - Add authentication/authorization
   - Rate limiting
   - Input sanitization

5. **Monitoring**: Add logging and monitoring tools

## 🐛 Troubleshooting

### Model Loading Errors
- **Issue**: `Model not loaded` error
- **Solution**: Ensure the model file exists at `model/revenue_prediction_model.pkl`
- **Check**: Verify the file path in `main.py` (line 21)

### CORS Errors
- **Issue**: Frontend cannot connect to backend
- **Solution**: 
  - Ensure backend is running on port 8000
  - Check `API_BASE_URL` in `frontend/src/App.jsx` (should be `http://localhost:8000`)
  - For production, update CORS settings in `main.py`

### Port Conflicts
- **Issue**: Port already in use
- **Solution**: 
  - Backend: Change port in `main.py` or use `--port` flag: `uvicorn main:app --port 8001`
  - Frontend: Change port in `frontend/vite.config.js`

### Python Packages Not Installing
- **Issue**: `pip install -e .` fails
- **Solution**:
  ```bash
  # Upgrade pip first
  pip install --upgrade pip
  
  # Make sure venv is activated
  source .venv/bin/activate  # Linux/Mac
  # or
  .venv\Scripts\activate     # Windows
  
  # Install dependencies
  pip install -e .
  ```

### Node Modules Issues
- **Issue**: Frontend dependencies not installing
- **Solution**:
  ```bash
  cd frontend
  rm -rf node_modules package-lock.json
  npm install
  ```

### Excel File Upload Errors
- **Issue**: Bulk prediction fails
- **Solution**:
  - Ensure file is `.xlsx` or `.xls` format
  - Check file size (max 50MB)
  - Verify required columns exist (case-insensitive matching)
  - Check browser console for detailed error messages

## 📊 Performance

- **Single Prediction**: < 100ms response time
- **Bulk Prediction**: ~1-2 seconds per 1000 records
- **Model Loading**: ~1-2 seconds on startup
- **File Size Limit**: 50MB for bulk uploads

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions:
1. Run `python3 check_setup.py` to diagnose setup problems
2. Check the `SETUP_GUIDE.md` for detailed setup instructions
3. Review API documentation at `http://localhost:8000/docs`
4. Check browser console and backend logs for error messages

## 🎉 Getting Started Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 16+ installed
- [ ] Virtual environment created and activated
- [ ] Python dependencies installed (`pip install -e .`)
- [ ] Node dependencies installed (`cd frontend && npm install`)
- [ ] Model file exists at `model/revenue_prediction_model.pkl`
- [ ] Backend running on `http://localhost:8000`
- [ ] Frontend running on `http://localhost:3000`
- [ ] All checks pass: `python3 check_setup.py`

---

**Happy Predicting! 🚀**
