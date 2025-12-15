#!/bin/bash
# Script to create a shareable zip file excluding .venv and node_modules

PROJECT_NAME="revenue-prediction-app"
ZIP_NAME="${PROJECT_NAME}.zip"
TEMP_DIR=$(mktemp -d)

echo "📦 Creating shareable zip file..."
echo ""

# Copy project files to temp directory
echo "📋 Copying project files..."
rsync -av --exclude='.venv' \
          --exclude='node_modules' \
          --exclude='*.zip' \
          --exclude='.git' \
          --exclude='__pycache__' \
          --exclude='*.pyc' \
          --exclude='.DS_Store' \
          --exclude='dist' \
          --exclude='artifact' \
          --exclude='uv.lock' \
          . "$TEMP_DIR/$PROJECT_NAME/"

# Create zip file
echo "🗜️  Creating zip archive..."
cd "$TEMP_DIR"
zip -r "$ZIP_NAME" "$PROJECT_NAME" > /dev/null

# Move zip to original directory
mv "$ZIP_NAME" "$OLDPWD/"

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Zip file created: $ZIP_NAME"
echo ""
echo "📝 Included files:"
echo "   - Backend code (main.py)"
echo "   - Frontend code (frontend/src/)"
echo "   - Model file (model/revenue_prediction_model.pkl)"
echo "   - Configuration files (pyproject.toml, package.json)"
echo "   - Setup verification script (check_setup.py)"
echo "   - Documentation (README.md)"
echo ""
echo "❌ Excluded:"
echo "   - .venv (virtual environment)"
echo "   - node_modules (Node.js dependencies)"
echo "   - dist (build artifacts)"
echo "   - artifact (output files)"
echo ""
echo "📋 To use this zip:"
echo "   1. Extract the zip file"
echo "   2. Run: python check_setup.py"
echo "   3. Follow the setup instructions"

