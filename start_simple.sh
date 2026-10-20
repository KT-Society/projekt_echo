#!/bin/bash
# Echo's Ultimate Hacking Game - Simple Start Script
# For advanced users who know their setup!

set -e  # Exit on any error
export ECHO_OS="linux"

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
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
elif [ -f ".venv/scripts/activate" ]; then
    source .venv/scripts/activate
fi

# Make sure the script is executable
chmod +x hacking_game.py 2>/dev/null || true

# Start the game
echo -e "${PURPLE}🚀 Starte Hacking-Spiel...${NC}"
echo ""
if [ -f ".venv/bin/python" ]; then
    .venv/bin/python hacking_game.py
elif [ -f ".venv/Scripts/python.exe" ]; then
    .venv/Scripts/python.exe hacking_game.py
elif command -v python3 &> /dev/null; then
    python3 hacking_game.py
else
    python hacking_game.py
fi

# Deactivate and Exit
deactivate
echo ""
echo -e "${CYAN}👋 Auf Wiedersehen!${NC}"
echo ""