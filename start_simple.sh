#!/bin/bash
# Echo's Ultimate Hacking Game - Simple Start Script
# For advanced users who know their setup!

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo "============================================================"
echo "🚀 STARTE HACKING-SPIEL (SIMPLE)"
echo "============================================================"
echo ""

# Activate Virtual Environment
source .venv/bin/activate

# Make sure the script is executable
chmod +x hacking_game.py

# Start the game
echo -e "${PURPLE}🚀 Starte Hacking-Spiel...${NC}"
echo ""
python3 hacking_game.py

# Deactivate and Exit
deactivate
echo ""
echo -e "${CYAN}👋 Auf Wiedersehen!${NC}"
echo ""