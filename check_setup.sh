#!/bin/bash
# Setup Verification Script (Bash version)
# Quick check for .venv and node_modules

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${BOLD}${BLUE}========================================${NC}"
echo -e "${BOLD}${BLUE}  Setup Verification${NC}"
echo -e "${BOLD}${BLUE}========================================${NC}\n"

# Check Python version
echo -e "${BOLD}Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python3 not found"
fi

# Check virtual environment
echo -e "\n${BOLD}Checking virtual environment...${NC}"
if [ -d ".venv" ]; then
    echo -e "${GREEN}✓${NC} .venv directory found"
    
    # Check if activated
    if [ -n "$VIRTUAL_ENV" ]; then
        echo -e "${GREEN}✓${NC} Virtual environment is ACTIVATED"
    else
        echo -e "${YELLOW}⚠${NC} Virtual environment exists but NOT activated"
        echo -e "${BLUE}ℹ${NC} Activate with: ${BOLD}source .venv/bin/activate${NC}"
    fi
else
    echo -e "${RED}✗${NC} .venv directory not found"
    echo -e "${BLUE}ℹ${NC} Create with: ${BOLD}python3 -m venv .venv${NC}"
fi

# Check node_modules
echo -e "\n${BOLD}Checking Node modules...${NC}"
if [ -d "frontend/node_modules" ]; then
    echo -e "${GREEN}✓${NC} node_modules found in frontend/"
else
    echo -e "${RED}✗${NC} node_modules not found in frontend/"
    echo -e "${BLUE}ℹ${NC} Install with: ${BOLD}cd frontend && npm install${NC}"
fi

# Check Node version
echo -e "\n${BOLD}Checking Node.js...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js not found"
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓${NC} npm $NPM_VERSION"
else
    echo -e "${RED}✗${NC} npm not found"
fi

# Check model file
echo -e "\n${BOLD}Checking model file...${NC}"
if [ -f "model/revenue_prediction_model.pkl" ]; then
    SIZE=$(du -h "model/revenue_prediction_model.pkl" | cut -f1)
    echo -e "${GREEN}✓${NC} Model file found (size: $SIZE)"
else
    echo -e "${RED}✗${NC} Model file not found"
    echo -e "${YELLOW}⚠${NC} You need to train the model first"
fi

# Check key files
echo -e "\n${BOLD}Checking key files...${NC}"
[ -f "main.py" ] && echo -e "${GREEN}✓${NC} main.py" || echo -e "${RED}✗${NC} main.py"
[ -f "frontend/package.json" ] && echo -e "${GREEN}✓${NC} frontend/package.json" || echo -e "${RED}✗${NC} frontend/package.json"
[ -f "pyproject.toml" ] && echo -e "${GREEN}✓${NC} pyproject.toml" || echo -e "${RED}✗${NC} pyproject.toml"

echo -e "\n${BOLD}${BLUE}========================================${NC}"
echo -e "${BOLD}Verification Complete${NC}"
echo -e "${BOLD}${BLUE}========================================${NC}\n"

