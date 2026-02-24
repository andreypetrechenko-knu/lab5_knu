#!/usr/bin/env bash
set -e

REPO_URL="https://github.com/andreypetrechenko-knu/lab5_knu"
PROJECT_DIR="lab5-aws"
VENV_DIR=".venv"

echo "[INFO] Installing system dependencies..."
sudo apt update -y
sudo apt install -y git python3 python3-venv python3-pip

if [ -d "$PROJECT_DIR" ]; then
    echo "[INFO] Removing old project directory..."
    rm -rf "$PROJECT_DIR"
fi

echo "[INFO] Cloning repository..."
git clone "$REPO_URL" "$PROJECT_DIR"

cd "$PROJECT_DIR"

echo "[INFO] Creating virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "[INFO] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "[OK] Installation completed successfully!"
echo ""
echo "To activate environment:"
echo "source $PROJECT_DIR/$VENV_DIR/bin/activate"
echo ""
echo "Then run scripts, for example:"
echo "python ec2_create.py"
