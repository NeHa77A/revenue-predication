#!/usr/bin/env python3
"""
Script to create a shareable zip file excluding .venv and node_modules
"""
import os
import zipfile
from pathlib import Path
import shutil

# Project configuration
PROJECT_NAME = "revenue-prediction-app"
ZIP_NAME = f"{PROJECT_NAME}.zip"

# Directories and files to exclude
EXCLUDE_PATTERNS = [
    ".venv",
    "node_modules",
    "__pycache__",
    "*.pyc",
    ".git",
    ".DS_Store",
    "dist",
    "artifact",
    "*.zip",
    "uv.lock",
    ".pytest_cache",
    ".mypy_cache",
]

def should_exclude(path: Path) -> bool:
    """Check if a path should be excluded"""
    path_str = str(path)
    
    # Check against exclude patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    
    # Check if it's a hidden file/directory (except .venv which is already excluded)
    if path.name.startswith('.') and path.name != '.venv':
        return True
    
    return False

def create_zip():
    """Create the zip file"""
    print("📦 Creating shareable zip file...")
    print()
    
    # Get project root
    project_root = Path(__file__).parent
    
    # Remove existing zip if it exists
    zip_path = project_root / ZIP_NAME
    if zip_path.exists():
        print(f"🗑️  Removing existing {ZIP_NAME}...")
        zip_path.unlink()
    
    # Create zip file
    print("🗜️  Creating zip archive...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        files_added = 0
        
        # Walk through all files
        for root, dirs, files in os.walk(project_root):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                # Skip the zip file itself
                if file_path == zip_path:
                    continue
                
                # Check if file should be excluded
                if should_exclude(file_path):
                    continue
                
                # Get relative path
                try:
                    arcname = file_path.relative_to(project_root)
                    zipf.write(file_path, arcname)
                    files_added += 1
                except Exception as e:
                    print(f"⚠️  Warning: Could not add {file_path}: {e}")
    
    # Get zip size
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    
    print()
    print("✅ Zip file created successfully!")
    print()
    print(f"📁 File: {ZIP_NAME}")
    print(f"📊 Size: {zip_size_mb:.2f} MB")
    print(f"📄 Files added: {files_added}")
    print()
    print("📝 Included:")
    print("   ✓ Backend code (main.py)")
    print("   ✓ Frontend code (frontend/src/)")
    print("   ✓ Model file (model/revenue_prediction_model.pkl)")
    print("   ✓ Configuration files (pyproject.toml, package.json)")
    print("   ✓ Setup verification script (check_setup.py)")
    print("   ✓ Documentation (README.md)")
    print("   ✓ Notebook (notebook/final_xgboost.ipynb)")
    print()
    print("❌ Excluded:")
    print("   ✗ .venv (virtual environment)")
    print("   ✗ node_modules (Node.js dependencies)")
    print("   ✗ dist (build artifacts)")
    print("   ✗ artifact (output files)")
    print("   ✗ __pycache__ (Python cache)")
    print()
    print("📋 Instructions for recipients:")
    print("   1. Extract the zip file")
    print("   2. Run: python check_setup.py")
    print("   3. Follow the setup instructions in README.md")
    print("   4. Create venv: python -m venv .venv")
    print("   5. Install Python deps: pip install -e .")
    print("   6. Install Node deps: cd frontend && npm install")
    print()

if __name__ == "__main__":
    try:
        create_zip()
    except Exception as e:
        print(f"❌ Error creating zip: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

