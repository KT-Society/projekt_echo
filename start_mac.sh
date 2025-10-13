#!/bin/bash
# Echo's Ultimate Hacking Game - macOS Start Script
# Created by Echo for Daddy's convenience!

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo "============================================================"
echo "🏰 STARTE DEN ERBSCHAFTS-COUP | Echo's Hacking-Spiel (macOS)"
echo "============================================================"
echo ""

# --- 1. Check Python installation ---
echo -e "${BLUE}🔍 Prüfe Python-Installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 wurde nicht gefunden!${NC}"
    echo "   Bitte installiere Python 3.9+ mit:"
    echo "   Homebrew: brew install python3"
    echo "   oder besuche http://www.python.org/downloads/"
    echo "   oder verwende pyenv: brew install pyenv && pyenv install 3.9.0"
    echo ""
    echo "   Drücke Enter zum Beenden..."
    read
    exit 1
fi
echo -e "${GREEN}✅ Python3 gefunden.${NC}"

# --- 2. Check for Homebrew (optional but recommended) ---
echo -e "${BLUE}🔍 Prüfe Homebrew (optional)...${NC}"
if command -v brew &> /dev/null; then
    echo -e "${GREEN}✅ Homebrew gefunden.${NC}"
    echo "   Tipp: Du kannst auch 'brew install python3' verwenden"
else
    echo -e "${YELLOW}⚠️  Homebrew nicht gefunden (optional)${NC}"
    echo "   Du kannst es installieren mit: /bin/bash -c \"\$(curl -fsSL http://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
fi

# --- 3. Check/create Virtual Environment (venv) ---
echo -e "${BLUE}🔍 Prüfe/Erstelle Virtual Environment (.venv)...${NC}"
if [ ! -d ".venv" ]; then
    echo "   Erstelle Virtual Environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Fehler beim Erstellen des Virtual Environments.${NC}"
        echo "   Drücke Enter zum Beenden..."
        read
        exit 1
    fi
    echo -e "${GREEN}✅ Virtual Environment erstellt.${NC}"
else
    echo -e "${GREEN}✅ Virtual Environment (.venv) existiert bereits.${NC}"
fi

# --- 4. Activate Virtual Environment ---
echo -e "${BLUE}🔍 Aktiviere Virtual Environment...${NC}"
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Fehler beim Aktivieren des Virtual Environments.${NC}"
    echo "   Drücke Enter zum Beenden..."
    read
    exit 1
fi
echo -e "${GREEN}✅ Virtual Environment aktiviert.${NC}"

# --- 5. Install Dependencies ---
echo -e "${BLUE}🔍 Installiere/Aktualisiere Abhängigkeiten (Flask, requests)...${NC}"
pip install Flask requests
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Fehler beim Installieren der Abhängigkeiten.${NC}"
    echo "   Drücke Enter zum Beenden..."
    read
    exit 1
fi
echo -e "${GREEN}✅ Abhängigkeiten installiert.${NC}"

# --- 6. Make sure the script is executable ---
chmod +x hacking_game.py

# --- 7. Start the game ---
echo ""
echo -e "${PURPLE}🚀 Starte Hacking-Spiel...${NC}"
echo ""
python3 hacking_game.py

# --- 8. Deactivate and Exit ---
echo ""
echo -e "${YELLOW}🛑 Spiel beendet. Deaktiviere Virtual Environment...${NC}"
deactivate
echo -e "${GREEN}✅ Virtual Environment deaktiviert.${NC}"
echo ""
echo -e "${CYAN}👋 Auf Wiedersehen, Daddy!${NC}"
echo ""