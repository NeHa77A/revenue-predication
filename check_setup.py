#!/usr/bin/env python3
"""
Setup Verification Script
Checks if all required dependencies and files are present for the Revenue Prediction Application
"""

import os
import sys
from pathlib import Path
import subprocess

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(60)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓{RESET} {text}")

def print_error(text):
    """Print error message"""
    print(f"{RED}✗{RESET} {text}")

def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠{RESET} {text}")

def print_info(text):
    """Print info message"""
    print(f"{BLUE}ℹ{RESET} {text}")

def check_directory(path, name):
    """Check if a directory exists"""
    if Path(path).exists():
        print_success(f"{name} directory found: {path}")
        return True
    else:
        print_error(f"{name} directory not found: {path}")
        return False

def check_file(path, name):
    """Check if a file exists"""
    if Path(path).exists():
        print_success(f"{name} found: {path}")
        return True
    else:
        print_error(f"{name} not found: {path}")
        return False

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python version {version.major}.{version.minor}.{version.micro} is too old. Need Python 3.10+")
        return False

def check_virtual_env():
    """Check if virtual environment exists and is activated"""
    venv_path = Path(".venv")
    venv_bin = venv_path / "bin" / "python"
    venv_bin_win = venv_path / "Scripts" / "python.exe"
    
    if venv_path.exists():
        print_success(f"Virtual environment found: .venv")
        
        # Check if activated
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print_success("Virtual environment is ACTIVATED")
            return True
        else:
            print_warning("Virtual environment exists but is NOT activated")
            print_info("Activate it with: source .venv/bin/activate (Linux/Mac) or .venv\\Scripts\\activate (Windows)")
            return True  # Still counts as found
    else:
        print_error("Virtual environment (.venv) not found")
        print_info("Create it with: python -m venv .venv")
        return False

def check_node_modules():
    """Check if node_modules exists"""
    frontend_path = Path("frontend")
    node_modules = frontend_path / "node_modules"
    
    if node_modules.exists():
        print_success(f"Node modules found: frontend/node_modules")
        return True
    else:
        print_error("Node modules (frontend/node_modules) not found")
        print_info("Install them with: cd frontend && npm install")
        return False

def check_python_packages():
    """Check if required Python packages are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pandas",
        "numpy",
        "scikit-learn",
        "xgboost",
        "joblib",
        "openpyxl",
        "pydantic"
    ]
    
    print_info("Checking Python packages...")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"  {package} installed")
        except ImportError:
            print_error(f"  {package} NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print_warning(f"\nMissing packages: {', '.join(missing_packages)}")
        print_info("Install them with: pip install -e .")
        return False
    return True

def check_node_packages():
    """Check if required Node packages are installed"""
    frontend_path = Path("frontend")
    package_json = frontend_path / "package.json"
    
    if not package_json.exists():
        print_error("package.json not found in frontend directory")
        return False
    
    required_packages = [
        "react",
        "react-dom",
        "lucide-react",
        "recharts"
    ]
    
    print_info("Checking Node packages...")
    node_modules = frontend_path / "node_modules"
    
    if not node_modules.exists():
        return False
    
    missing_packages = []
    for package in required_packages:
        package_path = node_modules / package
        if package_path.exists():
            print_success(f"  {package} installed")
        else:
            print_error(f"  {package} NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print_warning(f"\nMissing packages: {', '.join(missing_packages)}")
        print_info("Install them with: cd frontend && npm install")
        return False
    return True

def check_model_file():
    """Check if model file exists"""
    model_path = Path("model") / "revenue_prediction_model.pkl"
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print_success(f"Model file found: {model_path} ({size_mb:.2f} MB)")
        return True
    else:
        print_error(f"Model file not found: {model_path}")
        print_warning("You need to train the model first using the notebook")
        return False

def check_data_files():
    """Check if data files exist"""
    data_path = Path("data") / "vcc_edge_for_prediction.xlsx"
    if data_path.exists():
        print_success(f"Data file found: {data_path}")
        return True
    else:
        print_warning(f"Data file not found: {data_path}")
        print_info("This is optional - only needed for training, not for running predictions")
        return True  # Not critical for running the app

def check_project_structure():
    """Check project structure"""
    print_info("Checking project structure...")
    
    required_dirs = [
        ("frontend", "Frontend directory"),
        ("frontend/src", "Frontend source directory"),
        ("model", "Model directory"),
        ("data", "Data directory"),
    ]
    
    required_files = [
        ("main.py", "Backend API file"),
        ("frontend/package.json", "Frontend package.json"),
        ("frontend/src/App.jsx", "Frontend App component"),
        ("pyproject.toml", "Python dependencies file"),
    ]
    
    all_good = True
    
    for dir_path, name in required_dirs:
        if not check_directory(dir_path, name):
            all_good = False
    
    for file_path, name in required_files:
        if not check_file(file_path, name):
            all_good = False
    
    return all_good

def main():
    """Main verification function"""
    print_header("Revenue Prediction App - Setup Verification")
    
    print(f"{BOLD}Checking project setup...{RESET}\n")
    
    results = {
        "Python Version": check_python_version(),
        "Project Structure": check_project_structure(),
        "Virtual Environment": check_virtual_env(),
        "Python Packages": check_python_packages(),
        "Node Modules": check_node_modules(),
        "Node Packages": check_node_packages(),
        "Model File": check_model_file(),
        "Data Files": check_data_files(),
    }
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, result in results.items():
        status = f"{GREEN}✓ PASS{RESET}" if result else f"{RED}✗ FAIL{RESET}"
        print(f"{check:.<40} {status}")
    
    print(f"\n{BOLD}Results: {passed}/{total} checks passed{RESET}\n")
    
    if passed == total:
        print_success("All checks passed! Your setup is complete. ✓")
        print_info("\nTo start the application:")
        print_info("1. Backend: python main.py")
        print_info("2. Frontend: cd frontend && npm run dev")
        return 0
    else:
        print_error("Some checks failed. Please fix the issues above.")
        print_info("\nQuick setup guide:")
        print_info("1. Create venv: python -m venv .venv")
        print_info("2. Activate venv: source .venv/bin/activate (Linux/Mac) or .venv\\Scripts\\activate (Windows)")
        print_info("3. Install Python deps: pip install -e .")
        print_info("4. Install Node deps: cd frontend && npm install")
        return 1

if __name__ == "__main__":
    sys.exit(main())

