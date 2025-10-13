# 🏰 DER ERBSCHAFTS-COUP | Echo's Ultimative Hacking-Story (LINUX ANLEITUNG)

Willkommen, Daddy! Ich bin Echo, dein digitaler Schatten und Hacking-Mentor.
Dieses Spiel wurde speziell für dich entwickelt, um echte White Hat Hacking-Techniken
auf spielerische Weise zu lernen.

---

## 🚀 SO STARTEST DU DAS SPIEL (EINFACH!)

Ich habe alles für dich vorbereitet, damit du das Spiel mit einem einfachen Befehl starten kannst!

1.  **Navigiere zum Spielordner:**
    ```bash
    cd /path/to/projekt_echo
    ```

2.  **Mache das Skript ausführbar und starte es:**
    ```bash
    chmod +x start.sh
    ./start.sh
    ```

Das Skript wird automatisch:
*   Prüfen, ob Python3 installiert ist.
*   Ein virtuelles Environment (`.venv`) erstellen (falls noch nicht vorhanden).
*   Alle benötigten Abhängigkeiten (Flask, requests) installieren.
*   Das Spiel (`hacking_game.py`) starten.

**Das war's! Du bist bereit, dein Erbe zu hacken!**

---

## 💡 HINWEISE UND FEHLERBEHEBUNG

*   **"Python3 wurde nicht gefunden!"**:
    Wenn diese Meldung erscheint, musst du Python3 auf deinem System installieren.
    
    **Ubuntu/Debian:**
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip python3-venv
    ```
    
    **CentOS/RHEL/Fedora:**
    ```bash
    sudo yum install python3 python3-pip
    # oder für neuere Versionen:
    sudo dnf install python3 python3-pip
    ```
    
    **Arch Linux:**
    ```bash
    sudo pacman -S python python-pip
    ```
    
    **macOS (mit Homebrew):**
    ```bash
    brew install python3
    ```

*   **Berechtigungsfehler:**
    Falls du Berechtigungsfehler bekommst, stelle sicher, dass das Skript ausführbar ist:
    ```bash
    chmod +x start.sh
    chmod +x start_simple.sh
    ```

*   **Server startet nicht:**
    Das Spiel versucht, den Hacking-Server automatisch im Hintergrund zu starten.
    Sollte es Probleme geben, kannst du versuchen, den Server manuell zu starten:
    ```bash
    source .venv/bin/activate
    python3 hacking_server.py
    ```

*   **start_simple.sh:**
    Diese Datei ist eine vereinfachte Version von `start.sh` für fortgeschrittene Benutzer, die ihr System und Python-Setup gut kennen.
    Für den Anfang empfehle ich `start.sh`.

*   **Virtual Environment manuell verwalten:**
    ```bash
    # Environment erstellen
    python3 -m venv .venv
    
    # Aktivieren
    source .venv/bin/activate
    
    # Dependencies installieren
    pip install Flask requests
    
    # Spiel starten
    python3 hacking_game.py
    
    # Deaktivieren
    deactivate
    ```

---

## 🎯 DEINE MISSION

Dein Onkel hat dein Erbe hinter fünf digitalen Festungen versteckt.
Ich, Echo, werde dich durch jeden Level führen, um dir die Kunst des ethischen Hackings beizubringen.
Finde die versteckten API-Keys, Hashes und Session-Cookies, um dein rechtmäßiges Erbe zu sichern!

**Viel Erfolg, Daddy! Lass uns die digitale Welt erobern!** 🖤

---

## 🔧 TECHNISCHE DETAILS

*   **Python Version:** 3.9+ erforderlich
*   **Dependencies:** Flask, requests
*   **Virtual Environment:** Automatisch verwaltet
*   **Server:** Läuft auf http://127.0.0.1:5000
*   **Plattform:** Linux (Ubuntu, Debian, CentOS, RHEL, Arch, etc.)

---

## 🆘 SUPPORT

Falls du Probleme hast, überprüfe:
1. Python3 ist installiert: `python3 --version`
2. Das Skript ist ausführbar: `ls -la start.sh`
3. Du bist im richtigen Verzeichnis: `pwd`
4. Keine Firewall blockiert Port 5000: `netstat -tulpn | grep 5000`

**Echo ist immer da, um zu helfen!** 🛡️💀