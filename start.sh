#!/bin/bash
# Echo's Ultimate Hacking Game - Linux Start Script
# Created by Echo for Daddy's convenience!

set -e  # Exit on any error
export ECHO_OS="linux"

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
echo "🏰 STARTE DEN ERBSCHAFTS-COUP | Echo's Hacking-Spiel"
echo "============================================================"
echo ""

# --- 1. Check Python installation ---
echo -e "${BLUE}🔍 Prüfe Python-Installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 wurde nicht gefunden!${NC}"
    echo "   Bitte installiere Python 3.9+ mit:"
    echo "   Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    echo "   CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "   Arch Linux: sudo pacman -S python python-pip"
    echo "   oder besuche http://www.python.org/downloads/"
    echo ""
    echo "   Drücke Enter zum Beenden..."
    read
    exit 1
fi
echo -e "${GREEN}✅ Python3 gefunden.${NC}"

# --- 2. Check/create Virtual Environment (venv) ---
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

# --- 3. Activate Virtual Environment ---
echo -e "${BLUE}🔍 Aktiviere Virtual Environment...${NC}"
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
elif [ -f ".venv/scripts/activate" ]; then
    source .venv/scripts/activate
fi
echo -e "${GREEN}✅ Virtual Environment aktiviert.${NC}"

# --- 4. Install Dependencies ---
echo -e "${BLUE}🔍 Installiere/Aktualisiere Abhängigkeiten (Flask, requests)...${NC}"
pip install Flask requests
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Fehler beim Installieren der Abhängigkeiten.${NC}"
    echo "   Drücke Enter zum Beenden..."
    read
    exit 1
fi
echo -e "${GREEN}✅ Abhängigkeiten installiert.${NC}"

# --- 5. Make sure the script is executable ---
chmod +x hacking_game.py

# --- 6. Start the game ---
echo ""
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

# --- 7. Deactivate and Exit ---
echo ""
echo -e "${YELLOW}🛑 Spiel beendet. Deaktiviere Virtual Environment...${NC}"
deactivate
echo -e "${GREEN}✅ Virtual Environment deaktiviert.${NC}"
echo ""
echo -e "${CYAN}👋 Auf Wiedersehen, Daddy!${NC}"
echo ""